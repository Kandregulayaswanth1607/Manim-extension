
import unittest
import numpy as np

from manim_pics.core import ImageAsset
from manim_pics.processing import crop, rotate, flip


class TestExtendedTransforms(unittest.TestCase):

    def setUp(self):
        pixels = np.zeros((4, 6, 4), dtype=np.uint8)

        for y in range(4):
            for x in range(6):
                pixels[y, x] = [x * 30, y * 50, 100, 255]

        self.asset = ImageAsset(pixels)

    def test_crop_dimensions(self):
        result = crop(self.asset, 1, 1, 3, 2)
        self.assertEqual(result.size, (3, 2))

    def test_crop_pixel_values(self):
        result = crop(self.asset, 1, 1, 3, 2)
        np.testing.assert_array_equal(
            result.pixels[0, 0],
            self.asset.pixels[1, 1],
        )

    def test_crop_outside_image(self):
        with self.assertRaises(ValueError):
            crop(self.asset, 5, 3, 3, 2)

    def test_rotate_dimensions(self):
        result = rotate(self.asset, 90)
        self.assertEqual(result.size, (4, 6))

    def test_horizontal_flip(self):
        result = flip(self.asset, "horizontal")
        np.testing.assert_array_equal(
            result.pixels,
            np.flip(self.asset.pixels, axis=1),
        )

    def test_vertical_flip(self):
        result = flip(self.asset, "vertical")
        np.testing.assert_array_equal(
            result.pixels,
            np.flip(self.asset.pixels, axis=0),
        )

    def test_invalid_flip_direction(self):
        with self.assertRaises(ValueError):
            flip(self.asset, "diagonal")

    def test_original_unchanged(self):
        original = self.asset.pixels.copy()
        crop(self.asset, 1, 1, 2, 2)
        rotate(self.asset, 45)
        flip(self.asset)
        np.testing.assert_array_equal(self.asset.pixels, original)


if __name__ == "__main__":
    unittest.main()
