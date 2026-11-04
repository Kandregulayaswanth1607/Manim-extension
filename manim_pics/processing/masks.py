"""Alpha masks for ImageAsset."""
from dataclasses import replace
import numpy as np
from ..core import ImageAsset

def apply_mask(asset: ImageAsset, mask, invert=False) -> ImageAsset:
    """Multiply image alpha by a grayscale mask (0 transparent, 255 opaque).

    `mask` can be another ImageAsset or a 2D NumPy array. Dimensions must match.
    """
    if not isinstance(asset, ImageAsset):
        raise TypeError("asset must be an ImageAsset")
    if isinstance(mask, ImageAsset):
        values = mask.pixels[..., :3].astype(np.float32).mean(axis=2)
    else:
        values = np.asarray(mask)
        if values.ndim != 2:
            raise ValueError("mask must be a 2D array or ImageAsset")
        if not np.issubdtype(values.dtype, np.number) or not np.all(np.isfinite(values)):
            raise ValueError("mask values must be finite numbers")
        values = np.clip(values, 0, 255).astype(np.float32)
    if values.shape != (asset.height, asset.width):
        raise ValueError("mask dimensions must match the image")
    if not isinstance(invert, bool):
        raise TypeError("invert must be a boolean")
    alpha = values / 255.0
    if invert:
        alpha = 1.0 - alpha
    pixels = asset.pixels.copy()
    pixels[..., 3] = np.round(pixels[..., 3].astype(np.float32) * alpha).astype(np.uint8)
    metadata = replace(asset.metadata, extra=asset.metadata.extra.copy())
    result = ImageAsset(pixels, metadata, asset.history.copy())
    result.record("Applied inverted alpha mask" if invert else "Applied alpha mask")
    return result
