import tempfile
import unittest
from pathlib import Path
from manim_pics import assets

class TestAssetHelpers(unittest.TestCase):
    def setUp(self):
        self.original_dirs = assets.asset_dirs()

    def tearDown(self):
        assets._dirs[:] = self.original_dirs

    def test_rejects_non_http_url(self):
        with tempfile.TemporaryDirectory() as d:
            assets.add_asset_dir(d)
            with self.assertRaises(ValueError):
                assets.fetch("file:///etc/passwd", "bad")

    def test_rejects_path_traversal_name(self):
        with tempfile.TemporaryDirectory() as d:
            assets.add_asset_dir(d)
            with self.assertRaises(ValueError):
                assets.fetch("https://example.com/a.png", "../escape")

    def test_rejects_path_traversal_subdir(self):
        with tempfile.TemporaryDirectory() as d:
            assets.add_asset_dir(d)
            with self.assertRaises(ValueError):
                assets.fetch("https://example.com/a.png", "safe", "../escape")

if __name__ == "__main__":
    unittest.main()
