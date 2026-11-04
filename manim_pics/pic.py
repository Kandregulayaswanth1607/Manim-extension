"""Pic: one object for PNG / JPG / SVG / built-in vector / emoji pictures."""
from __future__ import annotations

from pathlib import Path

from manim import *

from . import assets, builtin

# Twemoji (CC-BY 4.0, https://github.com/jdecked/twemoji). SVG first: stays sharp at any size.
_TWEMOJI = [
    "https://raw.githubusercontent.com/jdecked/twemoji/main/assets/svg/{code}.svg",
    "https://raw.githubusercontent.com/jdecked/twemoji/main/assets/72x72/{code}.png",
    "https://raw.githubusercontent.com/twitter/twemoji/master/assets/svg/{code}.svg",
]


def _placeholder(name: str):
    box = RoundedRectangle(width=2, height=2, corner_radius=0.2, color=GREY_B,
                           fill_color="#1b2030", fill_opacity=1, stroke_width=3)
    txt = Text(f"{name}\n(missing)", font_size=20, color=GREY_B).move_to(box)
    if txt.width > 1.8:
        txt.scale_to_fit_width(1.8)
    return VGroup(box, txt)


def _circle_crop(path: Path) -> Path:
    from PIL import Image, ImageDraw
    img = Image.open(path).convert("RGBA")
    s = min(img.size)
    left, top = (img.width - s) // 2, (img.height - s) // 2
    img = img.crop((left, top, left + s, top + s))
    mask = Image.new("L", (s, s), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, s - 1, s - 1), fill=255)
    img.putalpha(mask)
    out_dir = assets.asset_dirs()[0] / ".cache"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{path.stem}_circle.png"
    img.save(out)
    return out


class Pic(Group):
    """
    Pic("cat")                       # assets/cat.png|jpg|svg, else built-in vector "cat"
    Pic("photo.jpg", height=3)       # explicit file
    Pic("me", circle=True, frame=True, label="Me")
    Pic(some_mobject)                # wrap anything so it gets label/frame too

    Missing pictures never crash the render: you get a labelled placeholder
    (and a warning), so you can write the scene before the art exists.
    """

    def __init__(self, source, height=None, width=None, label=None, frame=False,
                 circle=False, label_size=22, label_color=WHITE, **kwargs):
        super().__init__(**kwargs)
        self.source = source
        self.is_placeholder = False
        size = {}
        body = self._load(source, circle, size)
        if height is not None:
            body.scale_to_fit_height(height)
        elif width is not None:
            body.scale_to_fit_width(width)
        elif "height" in size:
            body.scale_to_fit_height(size["height"])
        elif "width" in size:
            body.scale_to_fit_width(size["width"])
        else:
            body.scale_to_fit_height(2)
        body.move_to(ORIGIN)
        self.body = body
        self.add(body)
        if frame:
            self.frame_box = SurroundingRectangle(body, buff=0.12, color=GREY_B, corner_radius=0.12)
            self.add(self.frame_box)
        if label:
            self.caption = Text(label, font_size=label_size, color=label_color)
            self.caption.next_to(self, DOWN, buff=0.15)
            self.add(self.caption)

    def _load(self, source, circle, size):
        if isinstance(source, Mobject):
            return source
        path = assets.resolve(source)               # your files win over built-ins
        if path is not None:
            if path.suffix.lower() == ".svg":
                return SVGMobject(str(path))
            if circle:
                path = _circle_crop(path)
            return ImageMobject(str(path))
        if source in builtin.REGISTRY:
            factory, default = builtin.REGISTRY[source]
            size.update(default)
            return factory()
        logger.warning(f"manim_pics: picture '{source}' not found in {[str(d) for d in assets.asset_dirs()]}")
        self.is_placeholder = True
        return _placeholder(str(source))

    @classmethod
    def from_url(cls, url: str, name: str, **kwargs):
        """Download once into the assets folder, then behave like Pic(name)."""
        try:
            path = assets.fetch(url, name)
        except Exception as e:
            logger.warning(f"manim_pics: download failed for {url}: {e}")
            return cls(name, **kwargs)
        return cls(str(path), **kwargs)


class Emoji(Pic):
    """Emoji("🐱", height=1) -> Twemoji picture (downloaded once, cached in assets/emoji)."""

    def __init__(self, char: str, height=1.0, **kwargs):
        code = "-".join(f"{ord(c):x}" for c in char if ord(c) != 0xFE0F)
        path = assets.resolve(f"emoji/{code}")
        if path is None:
            for tmpl in _TWEMOJI:
                try:
                    path = assets.fetch(tmpl.format(code=code), code, subdir="emoji")
                    break
                except Exception:
                    continue
        if path is None:
            logger.warning(f"manim_pics: could not get emoji {char} (offline?)")
        super().__init__(str(path) if path else char, height=height, **kwargs)


def pic_row(*pics, buff=0.8, **kwargs):
    """Lay pictures out in a row (a Group, ready for FadeIn)."""
    return Group(*pics, **kwargs).arrange(RIGHT, buff=buff)
