"""Alpha compositing helpers."""
from dataclasses import replace
import numpy as np
from ..core import ImageAsset

def composite(background: ImageAsset, foreground: ImageAsset, x=0, y=0) -> ImageAsset:
    """Composite foreground over background at pixel offset (x, y).

    Parts of the foreground outside the background canvas are clipped.
    Coordinates are measured from the top-left corner.
    """
    if not isinstance(background, ImageAsset) or not isinstance(foreground, ImageAsset):
        raise TypeError("background and foreground must be ImageAsset objects")
    for name, value in (("x", x), ("y", y)):
        if isinstance(value, bool) or not isinstance(value, (int, np.integer)):
            raise TypeError(f"{name} must be an integer")
    out = background.pixels.astype(np.float32) / 255.0
    src = foreground.pixels.astype(np.float32) / 255.0
    bx0, by0 = max(0, x), max(0, y)
    bx1, by1 = min(background.width, x + foreground.width), min(background.height, y + foreground.height)
    if bx1 > bx0 and by1 > by0:
        sx0, sy0 = bx0 - x, by0 - y
        src_region = src[sy0:sy0 + by1 - by0, sx0:sx0 + bx1 - bx0]
        dst_region = out[by0:by1, bx0:bx1]
        sa = src_region[..., 3:4]
        da = dst_region[..., 3:4]
        oa = sa + da * (1.0 - sa)
        rgb = np.zeros_like(dst_region[..., :3])
        np.divide(src_region[..., :3] * sa + dst_region[..., :3] * da * (1.0 - sa), oa, out=rgb, where=oa > 0)
        dst_region[..., :3] = rgb
        dst_region[..., 3:4] = oa
    pixels = np.clip(np.round(out * 255), 0, 255).astype(np.uint8)
    metadata = replace(background.metadata, extra=background.metadata.extra.copy())
    result = ImageAsset(pixels, metadata, background.history.copy())
    result.record(f"Composited foreground at ({x}, {y})")
    return result
