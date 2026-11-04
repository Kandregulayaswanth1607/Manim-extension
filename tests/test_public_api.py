import unittest
from pathlib import Path

import manim_pics as mp


class TestPublicAPI(unittest.TestCase):

    def test_version(self):
        self.assertEqual(mp.__version__, "0.3.0")

    def test_load_function(self):
        image_path = (
            Path("examples")
            / "assets"
            / "sample.png"
        )

        asset = mp.load(image_path)

        self.assertIsInstance(asset, mp.ImageAsset)
        self.assertGreater(asset.width, 0)
        self.assertGreater(asset.height, 0)

    def test_original_api_preserved(self):
        self.assertTrue(callable(mp.Pic))
        self.assertTrue(callable(mp.Emoji))
        self.assertTrue(callable(mp.pic_row))
        self.assertTrue(callable(mp.PicScene))
        self.assertTrue(callable(mp.SpeechBubble))


if __name__ == "__main__":
    unittest.main()
