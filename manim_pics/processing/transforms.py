from dataclasses import replace

import numpy as np
from PIL import Image

from ..core import ImageAsset


def resize(
    asset: ImageAsset,
    width: int,
    height: int,
) -> ImageAsset:
    """
    Resize an ImageAsset to the requested dimensions.

    Returns a new ImageAsset without modifying the original.
    """

    if not isinstance(asset, ImageAsset):
        raise TypeError("asset must be an ImageAsset")

    if not isinstance(width, int) or not isinstance(height, int):
        raise TypeError("Width and height must be integers.")

    if width <= 0 or height <= 0:
        raise ValueError("Width and height must be greater than zero.")

    image = asset.to_pillow()

    resized_image = image.resize(
        (width, height),
        Image.Resampling.LANCZOS,
    )

    pixels = np.asarray(resized_image)

    metadata = replace(
        asset.metadata,
        extra=asset.metadata.extra.copy(),
    )

    result = ImageAsset(
        pixels=pixels,
        metadata=metadata,
        history=asset.history.copy(),
    )

    result.record(
        f"Resized image from {asset.size} to {(width, height)}"
    )

    return result



def crop(
    asset: ImageAsset,
    x: int,
    y: int,
    width: int,
    height: int,
) -> ImageAsset:
    """Extract a rectangular region from an image."""

    if not isinstance(asset, ImageAsset):
        raise TypeError("asset must be an ImageAsset")

    values = (x, y, width, height)
    if any(not isinstance(v, int) or isinstance(v, bool) for v in values):
        raise TypeError("Crop coordinates and dimensions must be integers.")

    if x < 0 or y < 0 or width <= 0 or height <= 0:
        raise ValueError("Invalid crop coordinates or dimensions.")

    if x + width > asset.width or y + height > asset.height:
        raise ValueError("Crop region extends outside the image.")

    pixels = asset.pixels[y:y + height, x:x + width].copy()

    metadata = replace(asset.metadata, extra=asset.metadata.extra.copy())

    result = ImageAsset(
        pixels=pixels,
        metadata=metadata,
        history=asset.history.copy(),
    )
    result.record(f"Cropped image at ({x}, {y}) with size {(width, height)}")
    return result


def rotate(asset: ImageAsset, angle: float) -> ImageAsset:
    """Rotate an image counterclockwise, expanding to preserve the full image."""

    if not isinstance(asset, ImageAsset):
        raise TypeError("asset must be an ImageAsset")

    if isinstance(angle, bool) or not isinstance(angle, (int, float)):
        raise TypeError("angle must be a number.")

    if not np.isfinite(angle):
        raise ValueError("angle must be finite.")

    image = asset.to_pillow()
    rotated = image.rotate(
        angle,
        resample=Image.Resampling.BICUBIC,
        expand=True,
    )

    metadata = replace(asset.metadata, extra=asset.metadata.extra.copy())

    result = ImageAsset(
        pixels=np.asarray(rotated),
        metadata=metadata,
        history=asset.history.copy(),
    )
    result.record(f"Rotated image by {angle} degrees")
    return result


def flip(asset: ImageAsset, direction: str = "horizontal") -> ImageAsset:
    """Flip an image horizontally or vertically."""

    if not isinstance(asset, ImageAsset):
        raise TypeError("asset must be an ImageAsset")

    if direction not in ("horizontal", "vertical"):
        raise ValueError("direction must be 'horizontal' or 'vertical'.")

    if direction == "horizontal":
        pixels = np.flip(asset.pixels, axis=1).copy()
    else:
        pixels = np.flip(asset.pixels, axis=0).copy()

    metadata = replace(asset.metadata, extra=asset.metadata.extra.copy())

    result = ImageAsset(
        pixels=pixels,
        metadata=metadata,
        history=asset.history.copy(),
    )
    result.record(f"Flipped image: {direction}")
    return result
