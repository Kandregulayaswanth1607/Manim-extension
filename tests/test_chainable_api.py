import unittest
import numpy as np
from manim_pics.core import ImageAsset

class TestChainableAPI(unittest.TestCase):
    def setUp(self):
        pixels = np.zeros((40, 60, 4), dtype=np.uint8)
        pixels[..., 0] = 180
        pixels[..., 1] = 90
        pixels[..., 2] = 30
        pixels[..., 3] = 255
        self.asset = ImageAsset(pixels)

    def test_chain(self):
        result = (self.asset.resize(30, 20).grayscale().contrast(1.2)
                  .gaussian_blur(0.5).rotate(90))
        self.assertEqual(result.size, (20, 30))

    def test_original_unchanged(self):
        before = self.asset.pixels.copy()
        self.asset.grayscale().resize(20, 20)
        np.testing.assert_array_equal(self.asset.pixels, before)

    def test_metadata_is_independent(self):
        result = self.asset.grayscale()
        result.metadata.extra["new"] = True
        self.assertNotIn("new", self.asset.metadata.extra)

    def test_to_jpeg(self):
        import tempfile
        from pathlib import Path
        from PIL import Image
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "image.jpg"
            self.asset.save(path)
            with Image.open(path) as im:
                self.assertEqual(im.mode, "RGB")

if __name__ == "__main__":
    unittest.main()
