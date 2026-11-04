from pathlib import Path

from .raster import load_raster


RASTER_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".bmp",
    ".tif",
    ".tiff",
}


def load_image(path: str | Path):
    """
    Load an image by detecting its file extension.

    Currently supported: PNG, JPEG, WebP, BMP, TIFF and animated GIF. SVG is supported by Pic as a Manim vector object.
    """
    path = Path(path)

    if not path.is_file():
        raise FileNotFoundError(f"Image not found: {path}")

    extension = path.suffix.lower()

    if extension in RASTER_EXTENSIONS:
        return load_raster(path)

    if extension == ".gif":
        from .sequence import load_gif
        return load_gif(path)

    if extension == ".svg":
        raise NotImplementedError(
            "SVG loading is not implemented yet."
        )

    raise ValueError(f"Unsupported image extension: {extension}")
