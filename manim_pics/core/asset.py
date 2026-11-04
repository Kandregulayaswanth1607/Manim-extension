from __future__ import annotations

from pathlib import Path
from dataclasses import replace
from typing import Union

import numpy as np
from PIL import Image, UnidentifiedImageError

from .metadata import ImageMetadata


PathLike = Union[str, Path]


class ImageAsset:
    """
    Manim-independent raster image.

    Pixels are stored as a contiguous uint8 RGBA NumPy array
    with shape (height, width, 4).

    Processing methods should return new ImageAsset objects,
    leaving the source asset unchanged.
    """

    def __init__(
        self,
        pixels: np.ndarray,
        metadata: ImageMetadata | None = None,
        history: list[str] | None = None,
    ):
        array = np.asarray(pixels)

        if array.ndim != 3 or array.shape[2] != 4:
            raise ValueError(
                "Expected an RGBA array with shape (height, width, 4)."
            )

        if array.shape[0] == 0 or array.shape[1] == 0:
            raise ValueError("Image dimensions must be greater than zero.")

        if not np.issubdtype(array.dtype, np.number) or np.issubdtype(array.dtype, np.complexfloating):
            raise TypeError("Image pixels must use a real numeric dtype.")

        if np.issubdtype(array.dtype, np.floating):
            if not np.all(np.isfinite(array)):
                raise ValueError("Image pixels cannot contain NaN or infinity.")

        if array.dtype != np.uint8:
            array = np.clip(array, 0, 255).astype(np.uint8)

        self.pixels = np.ascontiguousarray(array)
        if metadata is None:
            self.metadata = ImageMetadata()
        else:
            if not isinstance(metadata, ImageMetadata):
                raise TypeError("metadata must be an ImageMetadata instance")
            self.metadata = replace(metadata, extra=metadata.extra.copy())
        self.history = list(history or [])

        self.metadata.width = self.width
        self.metadata.height = self.height
        self.metadata.mode = "RGBA"
        self.metadata.has_alpha = bool(
            np.any(self.pixels[:, :, 3] < 255)
        )

    @classmethod
    def from_file(cls, path: PathLike) -> "ImageAsset":
        """Load a raster image and convert it to RGBA."""

        path = Path(path)

        if not path.is_file():
            raise FileNotFoundError(f"Image not found: {path}")

        try:
            with Image.open(path) as image:
                image.load()

                metadata = ImageMetadata(
                    source=str(path.resolve()),
                    format=image.format,
                    dpi=image.info.get("dpi"),
                    extra={
                        key: value
                        for key, value in image.info.items()
                        if key not in {"dpi", "icc_profile", "exif"}
                        and isinstance(value, (str, int, float, bool))
                    },
                )

                pixels = np.asarray(image.convert("RGBA").copy())

        except (UnidentifiedImageError, OSError) as exc:
            raise ValueError(f"Unable to decode image: {path}") from exc

        return cls(
            pixels=pixels,
            metadata=metadata,
            history=[f"Loaded image from {path}"],
        )

    @property
    def width(self) -> int:
        return int(self.pixels.shape[1])

    @property
    def height(self) -> int:
        return int(self.pixels.shape[0])

    @property
    def size(self) -> tuple[int, int]:
        return self.width, self.height

    def copy(self) -> "ImageAsset":
        """Return an independent copy of the image."""

        metadata = ImageMetadata(
            source=self.metadata.source,
            format=self.metadata.format,
            width=self.metadata.width,
            height=self.metadata.height,
            mode=self.metadata.mode,
            has_alpha=self.metadata.has_alpha,
            dpi=self.metadata.dpi,
            extra=self.metadata.extra.copy(),
        )

        return ImageAsset(
            pixels=self.pixels.copy(),
            metadata=metadata,
            history=self.history.copy(),
        )

    def to_pillow(self) -> Image.Image:
        """Return a Pillow image containing a copy of the pixels."""
        return Image.fromarray(self.pixels.copy(), mode="RGBA")

    def to_mobject(self, scale_to=None):
        """Create a Manim ImageMobject from this asset.

        `scale_to` may be a positive number interpreted as target height.
        The returned Manim object is independent of this ImageAsset.
        """
        from manim import ImageMobject
        mob = ImageMobject(self.pixels.copy())
        if scale_to is not None:
            if isinstance(scale_to, bool) or not isinstance(scale_to, (int, float)) or scale_to <= 0:
                raise ValueError("scale_to must be a positive number")
            mob.set_height(float(scale_to))
        return mob

    def save(self, path: PathLike, **kwargs) -> None:
        """Save the image. JPEG output is flattened against a configurable background."""
        path = Path(path)
        image = self.to_pillow()
        fmt = (kwargs.get("format") or path.suffix.lstrip(".")).upper()
        if fmt in {"JPG", "JPEG"}:
            if kwargs.get("format", "").upper() == "JPG":
                kwargs["format"] = "JPEG"
            background = kwargs.pop("background", (255, 255, 255))
            base = Image.new("RGB", image.size, background)
            base.paste(image, mask=image.getchannel("A"))
            image = base
        image.save(path, **kwargs)

    # Chainable processing API. Local imports avoid circular dependencies.
    def resize(self, width, height):
        from ..processing import resize
        return resize(self, width, height)

    def crop(self, x, y, width, height):
        from ..processing import crop
        return crop(self, x, y, width, height)

    def rotate(self, angle):
        from ..processing import rotate
        return rotate(self, angle)

    def flip(self, direction="horizontal"):
        from ..processing import flip
        return flip(self, direction)

    def brightness(self, factor):
        from ..processing import brightness
        return brightness(self, factor)

    def contrast(self, factor):
        from ..processing import contrast
        return contrast(self, factor)

    def saturation(self, factor):
        from ..processing import saturation
        return saturation(self, factor)

    def grayscale(self):
        from ..processing import grayscale
        return grayscale(self)

    # Cinematic effects are chainable and preserve the source asset.
    def vignette(self, strength=0.65, softness=0.55):
        from ..effects import vignette
        return vignette(self, strength, softness)

    def film_grain(self, amount=0.08, seed=0, monochrome=True):
        from ..effects import film_grain
        return film_grain(self, amount, seed, monochrome)

    def bloom(self, radius=12, intensity=0.8, threshold=190):
        from ..effects import bloom
        return bloom(self, radius, intensity, threshold)

    def chromatic_aberration(self, offset=4):
        from ..effects import chromatic_aberration
        return chromatic_aberration(self, offset)

    def scanlines(self, spacing=3, opacity=0.22):
        from ..effects import scanlines
        return scanlines(self, spacing, opacity)

    def color_grade(self, contrast=1.08, saturation=1.12, brightness=1.0, tint=(1.0, 0.96, 0.88)):
        from ..effects import color_grade
        return color_grade(self, contrast, saturation, brightness, tint)

    def glitch(self, amount=0.12, slices=12, seed=0, rgb_shift=3):
        from ..effects import glitch
        return glitch(self, amount, slices, seed, rgb_shift)

    def gaussian_blur(self, radius=2.0):
        from ..processing import gaussian_blur
        return gaussian_blur(self, radius)

    def sharpen(self, factor=2.0):
        from ..processing import sharpen
        return sharpen(self, factor)

    def apply_mask(self, mask, invert=False):
        from ..processing import apply_mask
        return apply_mask(self, mask, invert=invert)

    def composite(self, foreground, x=0, y=0):
        from ..processing import composite
        return composite(self, foreground, x=x, y=y)

    def record(self, operation: str) -> None:
        """Append an operation to the processing history."""

        self.history.append(operation)

    def __repr__(self) -> str:
        return (
            f"ImageAsset(size={self.size}, mode='RGBA', "
            f"history_entries={len(self.history)})"
        )
