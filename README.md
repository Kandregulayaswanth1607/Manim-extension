# manim-pics

**Image processing and visual helpers for Manim Community.**

`manim-pics` combines a Manim-friendly picture API with a Manim-independent RGBA image-processing core. Use it for educational videos, documentaries, explainers, fiction, and visual-effects workflows.

## Features

- Preserve the original `Pic`, `Emoji`, `pic_row`, `PicScene`, and `SpeechBubble` API.
- Load PNG, JPEG, WebP, BMP, TIFF, and animated GIF images.
- Work with immutable-by-convention `ImageAsset` operations: each processing operation returns a new asset.
- Chain resize, crop, rotate, flip, color adjustments, blur, sharpen, masks, and compositing.
- Preserve alpha transparency through color adjustments and filters.
- Convert processed assets into Manim `ImageMobject` objects.
- Resolve local assets, register custom vector built-ins, and fetch remote assets with caching.

## Installation

Python 3.10 or newer is required. Manim Community, Pillow, and NumPy are installed as dependencies.

```bash
python -m pip install .
```

For editable development installation:

```bash
python -m pip install -e ".[dev]"
```

## Quick start: Manim picture API

```python
from manim import *
import manim_pics as mp

class PictureDemo(mp.PicScene):
    def construct(self):
        photo = mp.Pic("photo", height=3, frame=True, label="A photograph")
        robot = mp.Pic("robot", height=1.5)
        self.play(FadeIn(mp.pic_row(photo, robot)))
        self.show_narrator()
        self.say("Pictures made easy!")
        self.wait(1)
```

Run with Manim from the directory containing your scene file:

```bash
manim -pql demo.py PictureDemo
```

## Image processing

```python
import manim_pics as mp

image = (
    mp.load("photo.png")
    .resize(1600, 900)
    .crop(100, 50, 1200, 800)
    .grayscale()
    .contrast(1.25)
    .gaussian_blur(0.4)
)
image.save("processed.png")
```

The functional API is also available:

```python
from manim_pics import load, grayscale, contrast

image = contrast(grayscale(load("photo.png")), 1.25)
```

All image assets use contiguous `uint8` RGBA pixels with shape `(height, width, 4)`. Processing operations leave their input unchanged.

### Available operations

| Operation | Description |
|---|---|
| `resize(width, height)` | Resize with Lanczos resampling |
| `crop(x, y, width, height)` | Extract a rectangular region |
| `rotate(angle)` | Rotate counterclockwise and expand canvas |
| `flip(direction)` | Horizontal or vertical flip |
| `brightness(factor)` | Adjust brightness; `1.0` is unchanged |
| `contrast(factor)` | Adjust contrast; `1.0` is unchanged |
| `saturation(factor)` | Adjust saturation; `1.0` is unchanged |
| `grayscale()` | Convert RGB to grayscale, retaining alpha |
| `gaussian_blur(radius)` | Gaussian blur, retaining alpha |
| `sharpen(factor)` | Unsharp-mask sharpening |
| `apply_mask(mask, invert=False)` | Multiply alpha by a grayscale mask |
| `composite(foreground, x=0, y=0)` | Composite foreground over the current image |

Masks can be a same-size `ImageAsset` or a 2D NumPy array with values from 0 to 255. Composite coordinates are pixel offsets from the top-left; out-of-canvas foreground pixels are clipped.

## Manim bridge

```python
asset = mp.load("photo.png").grayscale().contrast(1.2)
mobject = asset.to_mobject(scale_to=4)  # scale_to is target Manim height
self.add(mobject)
```

## Animated GIFs

```python
from manim_pics import load_gif

sequence = load_gif("animation.gif")
print(sequence.frame_count, sequence.size, sequence.total_duration)
sequence.frames[0].save("first-frame.png")
```

`load("animation.gif")` also returns an `ImageSequence`. Each frame is an `ImageAsset`; durations are stored in milliseconds. `ImageSequence.save_gif()` writes the sequence back to GIF.

## Picture assets and built-ins

`Pic("name")` searches the current working directory's `assets` folder and any folders registered with `add_asset_dir`. Your files take priority over built-ins. Supported picture files include PNG, JPEG, WebP, SVG, and GIF (Manim's SVG object support is used for SVG pictures).

```python
import manim_pics as mp
mp.add_asset_dir("./my_art")

photo = mp.Pic("portrait", height=3, circle=True, frame=True)
emoji = mp.Emoji("🦾", height=1)

# Register your own Manim vector factory.
def make_star():
    from manim import Star, YELLOW
    return Star(color=YELLOW, fill_opacity=1)

mp.register("star", make_star, height=1.5)
star = mp.Pic("star")
```

`Pic.from_url(url, name)` downloads and caches a remote picture. `Emoji` downloads Twemoji on first use and caches it locally. Emoji artwork is Twemoji, licensed CC-BY 4.0; credit Twemoji (jdecked/twemoji) when publishing. Always ensure you have rights to use remote images.

## Public API

Legacy helpers: `Pic`, `Emoji`, `pic_row`, `PicScene`, `SpeechBubble`, `add_asset_dir`, `asset_dirs`, `fetch`, `resolve`, `register`, and `REGISTRY`.

Image core: `ImageAsset`, `ImageMetadata`, `ImageSequence`, `load`, `load_image`, `load_gif`.

Processing functions are exported at package level and from `manim_pics.processing`.

## Development and tests

From the repository root, run:

```bash
python -m unittest discover -s tests -v
```

The Manim-dependent scene and rendering helpers should additionally be smoke-tested with a real Manim installation.

## Current limitations

- `ImageAsset` is a raster abstraction; SVG is rendered as a Manim vector object through `Pic`, not loaded into `ImageAsset`.
- GIF frames can be loaded, inspected, processed, and saved, but automatic timeline playback as a Manim animation is not included.
- Network downloads require an internet connection.
- This library does not generate images; it processes and presents assets supplied by the user or fetched from configured sources.

## Advanced motion graphics (v0.3.0)

The 0.3 series adds cinematic raster finishing, Manim transition constructors,
particle-based image reveals, and kinetic typography. Existing 0.2 APIs remain
available unchanged.

### Cinematic image finishing

```python
import manim_pics as mp

frame = mp.load('photo.png')
frame = mp.color_grade(frame, contrast=1.1, saturation=1.15)
frame = mp.bloom(frame, radius=14, intensity=0.55)
frame = mp.chromatic_aberration(frame, offset=2)
frame = mp.vignette(frame, strength=0.5)
frame = mp.film_grain(frame, amount=0.025, seed=12)
frame.save('cinematic.png')
```

Available pixel effects: `vignette`, `film_grain`, `bloom`,
`chromatic_aberration`, `scanlines`, `color_grade`, and `glitch`. These operate
on `ImageAsset`, preserve alpha, and return a new asset. Grain/glitch support
seeds for reproducible output.

### Transitions and motion

```python
from manim import *
import manim_pics as mp

class TransitionDemo(Scene):
    def construct(self):
        title = Text('A NEW CHAPTER')
        self.play(mp.slide_in(title, direction='left', distance=1.2))
        self.play(mp.glow_pulse(title, color=TEAL, duration=1.5))
        self.play(mp.shake(title, duration=0.3, amplitude=0.04))
        self.play(mp.fade_out(title))
```

Transition constructors: `fade_in`, `fade_out`, `slide_in`, `zoom_in`,
`spin_in`, and `wipe_in`. Motion helpers: `shake` and `glow_pulse`.
`wipe_in` uses Manim's `Create` for vector objects; raster objects use a fade
fallback, not a true pixel-mask wipe.

### Image-to-particle animation

```python
asset = mp.load('photo.png').resize(640, 420)
particles = mp.image_particles(asset, count=800, seed=10)
self.play(LaggedStart(*(FadeIn(p, scale=0.1) for p in particles), lag_ratio=0.001))
self.play(AnimationGroup(*(FadeOut(p, shift=2*UP) for p in particles), lag_ratio=0.001))
```

`image_particles` samples source colors and positions into Manim dots. Particle
count is approximate and large counts increase render time and memory. Helpers
`particle_reveal` and `particle_dissolve` are also available.

### Kinetic typography

`typewriter(text)` staggers character submobjects; `word_reveal(text)` staggers
whatever word/group submobjects the supplied Manim text object exposes. For
reliable character-level behavior, use Manim `Text` rather than `MarkupText`.

See `examples/advanced/cinematic_photo.py` for full scene examples.

### Rendering and performance notes

- Pixel effects run on CPU using Pillow/NumPy; they are best applied once per
  source image, not repeatedly inside per-frame updaters.
- Particle scenes create one Manim dot per sampled pixel. Start with 300–800
  particles and increase only after checking render time and RAM.
- Bloom is a soft highlight overlay, not physically simulated light.
- Motion blur, volumetric lighting, depth-aware 3D parallax, and GPU shaders are
  not implemented in this release. The package does not claim them as features.
