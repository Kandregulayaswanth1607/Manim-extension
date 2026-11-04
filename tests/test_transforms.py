import unittest

import numpy as np

from manim_pics.core import ImageAsset
from manim_pics.processing import resize


class TestResize(unittest.TestCase):

    def setUp(self):
        pixels = np.zeros((100, 200, 4), dtype=np.uint8)
        pixels[:, :, 0] = 255
        pixels[:, :, 3] = 255

        self.asset = ImageAsset(pixels)

    def test_resize_dimensions(self):
        result = resize(self.asset, 100, 50)

        self.assertEqual(result.size, (100, 50))

    def test_original_unchanged(self):
        resize(self.asset, 50, 50)

        self.assertEqual(self.asset.size, (200, 100))

    def test_new_object(self):
        result = resize(self.asset, 50, 50)

        self.assertIsNot(result, self.asset)

    def test_invalid_dimensions(self):
        with self.assertRaises(ValueError):
            resize(self.asset, 0, 100)

    def test_invalid_asset(self):
        with self.assertRaises(TypeError):
            resize("image.png", 100, 100)


if __name__ == "__main__":
    unittest.main()