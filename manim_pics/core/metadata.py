from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class ImageMetadata:
    """Descriptive information about a raster image."""

    source: Optional[str] = None
    format: Optional[str] = None
    width: int = 0
    height: int = 0
    mode: str = "RGBA"
    has_alpha: bool = True
    dpi: Optional[tuple[float, float]] = None
    extra: dict[str, Any] = field(default_factory=dict)
