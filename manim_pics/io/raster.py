from pathlib import Path

from ..core import ImageAsset


SUPPORTED_FORMATS = {
    "PNG",
    "JPEG",
    "WEBP",
    "BMP",
    "TIFF",
}


def load_raster(path: str | Path) -> ImageAsset:
    """
    Load a supported raster image into an ImageAsset.

    The actual image format is checked after decoding,
    rather than trusting the file extension.
    """
    path = Path(path)

    if not path.is_file():
        raise FileNotFoundError(f"Image not found: {path}")

    asset = ImageAsset.from_file(path)

    image_format = (asset.metadata.format or "").upper()

    if image_format not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported raster format: {image_format or 'unknown'}"
        )

    asset.record(f"Decoded raster format: {image_format}")
    return asset
