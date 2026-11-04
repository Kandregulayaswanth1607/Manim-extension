
import unittest
import numpy as np

from manim_pics.core import ImageAsset
from manim_pics.processing import (
    brightness, contrast, saturation, grayscale,
    gaussian_blur, sharpen,
)


class TestColorsAndFilters(unittest.TestCase):

    def setUp(self):
        pixels = np.zeros((50, 50, 4), dtype=np.uint8)
        pixels[:, :, 0] = 180
        pixels[:, :, 1] = 80
        pixels[:, :, 2] = 40
        pixels[:, :, 3] = 200

        self.asset = ImageAsset(pixels)

    def test_brightness(self):
        result = brightness(self.asset, 1.5)
        self.assertEqual(result.size, self.asset.size)

    def test_contrast(self):
        result = contrast(self.asset, 1.5)
        self.assertEqual(result.size, self.asset.size)

    def test_saturation(self):
        result = saturation(self.asset, 0.0)
        rgb = result.pixels[:, :, :3]
        self.assertTrue(np.all(rgb[:, :, 0] == rgb[:, :, 1]))
        self.assertTrue(np.all(rgb[:, :, 1] == rgb[:, :, 2]))

    def test_grayscale(self):
        result = grayscale(self.asset)
        rgb = result.pixels[:, :, :3]
        self.assertTrue(np.all(rgb[:, :, 0] == rgb[:, :, 1]))
        self.assertTrue(np.all(rgb[:, :, 1] == rgb[:, :, 2]))

    def test_gaussian_blur(self):
        result = gaussian_blur(self.asset, 2)
        self.assertEqual(result.size, self.asset.size)

    def test_sharpen(self):
        result = sharpen(self.asset, 2)
        self.assertEqual(result.size, self.asset.size)

    def test_alpha_preserved(self):
        operations = [
            lambda: brightness(self.asset, 1.5),
            lambda: contrast(self.asset, 1.5),
            lambda: saturation(self.asset, 0.5),
            lambda: grayscale(self.asset),
            lambda: gaussian_blur(self.asset),
            lambda: sharpen(self.asset),
        ]

        for operation in operations:
            result = operation()
            np.testing.assert_array_equal(
                result.pixels[:, :, 3],
                self.asset.pixels[:, :, 3],
            )

    def test_original_unchanged(self):
        original = self.asset.pixels.copy()

        brightness(self.asset, 2)
        grayscale(self.asset)
        gaussian_blur(self.asset)

        np.testing.assert_array_equal(self.asset.pixels, original)


if __name__ == "__main__":
    unittest.main()
