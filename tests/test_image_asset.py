import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

from manim_pics.core import ImageAsset


class TestImageAsset(unittest.TestCase):

    def setUp(self):
        self.pixels = np.zeros((100, 200, 4), dtype=np.uint8)
        self.pixels[:, :, 0] = 255
        self.pixels[:, :, 3] = 255
        self.asset = ImageAsset(self.pixels)

    def test_dimensions(self):
        self.assertEqual(self.asset.width, 200)
        self.assertEqual(self.asset.height, 100)
        self.assertEqual(self.asset.size, (200, 100))

    def test_rgba_representation(self):
        self.assertEqual(self.asset.pixels.shape, (100, 200, 4))
        self.assertEqual(self.asset.pixels.dtype, np.uint8)

    def test_copy_is_independent(self):
        duplicate = self.asset.copy()
        duplicate.pixels[0, 0] = [0, 255, 0, 255]

        self.assertFalse(
            np.array_equal(duplicate.pixels, self.asset.pixels)
        )

    def test_transparency_detection(self):
        transparent_pixels = self.pixels.copy()
        transparent_pixels[0, 0, 3] = 100

        asset = ImageAsset(transparent_pixels)

        self.assertTrue(asset.metadata.has_alpha)

    def test_save_and_reload(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "test.png"

            self.asset.save(path)
            loaded = ImageAsset.from_file(path)

            self.assertEqual(loaded.size, self.asset.size)
            np.testing.assert_array_equal(
                loaded.pixels,
                self.asset.pixels,
            )

    def test_invalid_array_shape(self):
        with self.assertRaises(ValueError):
            ImageAsset(np.zeros((100, 200, 3), dtype=np.uint8))

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            ImageAsset.from_file("this_file_does_not_exist.png")


if __name__ == "__main__":
    unittest.main()
