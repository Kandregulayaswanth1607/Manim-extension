"""manim_pics - Image processing and visual effects for Manim Community."""

from .assets import add_asset_dir, asset_dirs, fetch, resolve
from .builtin import REGISTRY, register
from .pic import Emoji, Pic, pic_row
from .scene import PicScene
from .widgets import SpeechBubble

from .core import ImageAsset, ImageMetadata
from .io import ImageSequence, load_gif, load_image
from .effects import (vignette, film_grain, bloom, chromatic_aberration, scanlines, color_grade, glitch, shake, glow_pulse)
from .transitions import fade_in, fade_out, slide_in, zoom_in, spin_in, wipe_in
from .animation import image_particles, particle_reveal, particle_dissolve, typewriter, word_reveal

from .processing import (
    resize, crop, rotate, flip, brightness, contrast, saturation, grayscale,
    gaussian_blur, sharpen, apply_mask, composite,
)


def load(path):
    """Load a raster image as ImageAsset or an animated GIF as ImageSequence."""
    return load_image(path)


__version__ = "0.3.0"

__all__ = [
    "Pic", "Emoji", "pic_row", "PicScene", "SpeechBubble",
    "add_asset_dir", "asset_dirs", "fetch", "resolve", "register",
    "ImageAsset", "ImageMetadata", "ImageSequence", "load", "load_image", "load_gif",
    "resize", "crop", "rotate", "flip", "brightness", "contrast",
    "saturation", "grayscale", "gaussian_blur", "sharpen",
    "apply_mask", "composite",
    "vignette", "film_grain", "bloom", "chromatic_aberration", "scanlines", "color_grade", "glitch",
    "shake", "glow_pulse", "fade_in", "fade_out", "slide_in", "zoom_in", "spin_in", "wipe_in",
    "image_particles", "particle_reveal", "particle_dissolve", "typewriter", "word_reveal",
]