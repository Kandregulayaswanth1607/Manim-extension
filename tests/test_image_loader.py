import tempfile
import unittest
from pathlib import Path

from PIL import Image

from manim_pics.io import load_image, load_raster


class TestImageLoader(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.image_path = Path(self.temp_dir.name) / "sample.png"

        image = Image.new("RGBA", (120, 80), (255, 0, 0, 255))
        image.save(self.image_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_load_image(self):
        asset = load_image(self.image_path)

        self.assertEqual(asset.size, (120, 80))
        self.assertEqual(asset.metadata.format, "PNG")

    def test_load_raster(self):
        asset = load_raster(self.image_path)

        self.assertEqual(asset.size, (120, 80))
        self.assertIn("Decoded raster format: PNG", asset.history)

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            load_image("missing_image.png")

    def test_unsupported_extension(self):
        unsupported_path = Path(self.temp_dir.name) / "sample.xyz"
        unsupported_path.write_bytes(b"dummy content")

        with self.assertRaises(ValueError):
            load_image(unsupported_path)

    def test_gif_loading(self):
        gif_path = Path(self.temp_dir.name) / "sample.gif"
        first = Image.new("RGBA", (12, 8), (255, 0, 0, 255))
        second = Image.new("RGBA", (12, 8), (0, 0, 255, 255))
        first.save(gif_path, save_all=True, append_images=[second], duration=[80, 120], loop=0)
        sequence = load_image(gif_path)
        self.assertEqual(sequence.frame_count, 2)
        self.assertEqual(sequence.size, (12, 8))
        self.assertEqual(sequence.total_duration, 200)
        exported = Path(self.temp_dir.name) / "exported.gif"
        sequence.save_gif(exported)
        reloaded = load_image(exported)
        self.assertEqual(reloaded.frame_count, 2)


if __name__ == "__main__":
    unittest.main()
