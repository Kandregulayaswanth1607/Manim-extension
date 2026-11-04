import unittest
import numpy as np
from manim_pics.core import ImageAsset
from manim_pics.processing import apply_mask, composite

class TestMasksAndComposite(unittest.TestCase):
    def test_mask_makes_transparent(self):
        px = np.zeros((2, 2, 4), dtype=np.uint8); px[..., :3] = 255; px[..., 3] = 255
        asset = ImageAsset(px)
        mask = np.array([[0, 255], [128, 255]], dtype=np.uint8)
        result = apply_mask(asset, mask)
        self.assertEqual(int(result.pixels[0, 0, 3]), 0)
        self.assertEqual(int(result.pixels[0, 1, 3]), 255)
        self.assertEqual(int(result.pixels[1, 0, 3]), 128)

    def test_inverted_mask(self):
        px = np.zeros((1, 1, 4), dtype=np.uint8); px[..., 3] = 255
        result = apply_mask(ImageAsset(px), np.array([[0]], dtype=np.uint8), invert=True)
        self.assertEqual(int(result.pixels[0, 0, 3]), 255)

    def test_alpha_composite(self):
        bg = np.zeros((2, 2, 4), dtype=np.uint8); bg[...] = [0, 0, 255, 255]
        fg = np.zeros((1, 1, 4), dtype=np.uint8); fg[...] = [255, 0, 0, 128]
        result = composite(ImageAsset(bg), ImageAsset(fg), 1, 1)
        self.assertGreater(int(result.pixels[1, 1, 0]), 100)
        self.assertGreater(int(result.pixels[1, 1, 2]), 100)
        self.assertEqual(int(result.pixels[0, 0, 2]), 255)

    def test_composite_clips(self):
        bg = ImageAsset(np.zeros((2, 2, 4), dtype=np.uint8))
        fg = ImageAsset(np.full((2, 2, 4), 255, dtype=np.uint8))
        result = composite(bg, fg, -1, -1)
        self.assertEqual(result.size, (2, 2))
        self.assertEqual(int(result.pixels[0, 0, 3]), 255)

if __name__ == "__main__": unittest.main()
