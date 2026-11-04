
import numpy as np
from dataclasses import replace
from PIL import Image, ImageFilter

from ..core import ImageAsset


def _validate_asset(asset):
    if not isinstance(asset, ImageAsset):
        raise TypeError("asset must be an ImageAsset")


def _build_result(asset, pixels, operation):
    result = ImageAsset(
        pixels=np.ascontiguousarray(pixels, dtype=np.uint8),
        metadata=replace(asset.metadata, extra=asset.metadata.extra.copy()),
        history=asset.history.copy(),
    )
    result.record(operation)
    return result


def gaussian_blur(asset, radius: float = 2.0):
    """Apply Gaussian blur while preserving alpha."""
    _validate_asset(asset)

    if isinstance(radius, bool) or not isinstance(radius, (int, float, np.number)):
        raise TypeError("radius must be a real number")
    if not np.isfinite(radius) or radius < 0:
        raise ValueError("Blur radius must be finite and non-negative.")

    image = Image.fromarray(asset.pixels[:, :, :3], mode="RGB")
    blurred = image.filter(ImageFilter.GaussianBlur(radius=radius))

    pixels = asset.pixels.copy()
    pixels[:, :, :3] = np.asarray(blurred)

    return _build_result(asset, pixels, f"Gaussian blur: {radius}")


def sharpen(asset, factor: float = 2.0):
    """Sharpen an image. Factor 1.0 means unchanged."""
    _validate_asset(asset)

    if isinstance(factor, bool) or not isinstance(factor, (int, float, np.number)):
        raise TypeError("factor must be a real number")
    if not np.isfinite(factor) or factor < 0:
        raise ValueError("Sharpen factor must be finite and non-negative.")

    image = Image.fromarray(asset.pixels[:, :, :3], mode="RGB")
    sharpened = ImageFilter.UnsharpMask(
        radius=2,
        percent=int(factor * 100),
        threshold=3,
    )
    result_image = image.filter(sharpened)

    pixels = asset.pixels.copy()
    pixels[:, :, :3] = np.asarray(result_image)

    return _build_result(asset, pixels, f"Sharpen: {factor}")
