
import numpy as np
from dataclasses import replace
from PIL import Image, ImageEnhance, ImageOps

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


def brightness(asset, factor: float):
    """Adjust brightness. 1.0 means unchanged; 0.0 means black."""
    _validate_asset(asset)

    if isinstance(factor, bool) or not isinstance(factor, (int, float, np.number)):
        raise TypeError("factor must be a real number")
    if not np.isfinite(factor) or factor < 0:
        raise ValueError("Brightness factor must be finite and non-negative.")

    rgb = Image.fromarray(asset.pixels[:, :, :3], mode="RGB")
    adjusted = ImageEnhance.Brightness(rgb).enhance(factor)

    pixels = asset.pixels.copy()
    pixels[:, :, :3] = np.asarray(adjusted)

    return _build_result(asset, pixels, f"Brightness: {factor}")


def contrast(asset, factor: float):
    """Adjust contrast. 1.0 means unchanged."""
    _validate_asset(asset)

    if isinstance(factor, bool) or not isinstance(factor, (int, float, np.number)):
        raise TypeError("factor must be a real number")
    if not np.isfinite(factor) or factor < 0:
        raise ValueError("Contrast factor must be finite and non-negative.")

    rgb = Image.fromarray(asset.pixels[:, :, :3], mode="RGB")
    adjusted = ImageEnhance.Contrast(rgb).enhance(factor)

    pixels = asset.pixels.copy()
    pixels[:, :, :3] = np.asarray(adjusted)

    return _build_result(asset, pixels, f"Contrast: {factor}")


def saturation(asset, factor: float):
    """Adjust color saturation. 1.0 means unchanged; 0.0 means grayscale."""
    _validate_asset(asset)

    if isinstance(factor, bool) or not isinstance(factor, (int, float, np.number)):
        raise TypeError("factor must be a real number")
    if not np.isfinite(factor) or factor < 0:
        raise ValueError("Saturation factor must be finite and non-negative.")

    rgb = Image.fromarray(asset.pixels[:, :, :3], mode="RGB")
    adjusted = ImageEnhance.Color(rgb).enhance(factor)

    pixels = asset.pixels.copy()
    pixels[:, :, :3] = np.asarray(adjusted)

    return _build_result(asset, pixels, f"Saturation: {factor}")


def grayscale(asset):
    """Convert RGB pixels to grayscale while preserving alpha."""
    _validate_asset(asset)

    rgb = Image.fromarray(asset.pixels[:, :, :3], mode="RGB")
    gray = ImageOps.grayscale(rgb)
    gray_rgb = np.asarray(gray.convert("RGB"))

    pixels = asset.pixels.copy()
    pixels[:, :, :3] = gray_rgb

    return _build_result(asset, pixels, "Converted to grayscale")

