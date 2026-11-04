"""Animated raster image sequences (GIF)."""
from dataclasses import dataclass
from pathlib import Path
from PIL import Image, ImageSequence as PILImageSequence, UnidentifiedImageError
from ..core import ImageAsset, ImageMetadata
import numpy as np

@dataclass
class ImageSequence:
    """A sequence of raster frames with per-frame durations in milliseconds."""
    frames: list[ImageAsset]
    durations: list[int]
    loop: int = 0

    def __post_init__(self):
        if not self.frames:
            raise ValueError("An ImageSequence must contain at least one frame")
        if len(self.frames) != len(self.durations):
            raise ValueError("Each frame must have one duration")
        if any(not isinstance(frame, ImageAsset) for frame in self.frames):
            raise TypeError("All sequence frames must be ImageAsset objects")
        if any(frame.size != self.frames[0].size for frame in self.frames):
            raise ValueError("All sequence frames must have identical dimensions")
        if any(isinstance(value, bool) or not isinstance(value, int) or value < 0
               for value in self.durations):
            raise ValueError("Frame durations must be non-negative integers")

    @property
    def size(self):
        return self.frames[0].size

    @property
    def frame_count(self):
        return len(self.frames)

    @property
    def total_duration(self):
        return sum(self.durations)

    @property
    def durations_seconds(self):
        return [duration / 1000.0 for duration in self.durations]

    def to_mobjects(self, scale_to=None):
        """Convert every frame to a Manim ImageMobject."""
        return [frame.to_mobject(scale_to=scale_to) for frame in self.frames]

    def save_gif(self, path, **kwargs):
        images = [frame.to_pillow() for frame in self.frames]
        images[0].save(path, save_all=True, append_images=images[1:],
                        duration=self.durations, loop=self.loop,
                        disposal=2, **kwargs)

def load_gif(path: str | Path) -> ImageSequence:
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Image not found: {path}")
    try:
        with Image.open(path) as image:
            if image.format != "GIF":
                raise ValueError("File is not a GIF image")
            frames, durations = [], []
            loop = int(image.info.get("loop", 0))
            for frame in PILImageSequence.Iterator(image):
                frame.load()
                metadata = ImageMetadata(source=str(path), format="GIF")
                frames.append(ImageAsset(np.asarray(frame.convert("RGBA").copy()), metadata,
                                         [f"Loaded GIF frame from {path}"]))
                durations.append(max(0, int(frame.info.get("duration", image.info.get("duration", 100)))))
    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError(f"Unable to decode GIF: {path}") from exc
    return ImageSequence(frames, durations, loop)
