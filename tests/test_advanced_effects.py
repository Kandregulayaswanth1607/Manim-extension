import unittest
import numpy as np
from manim_pics.core.asset import ImageAsset
from manim_pics.effects.image import vignette, film_grain, bloom, chromatic_aberration, scanlines, color_grade, glitch

class AdvancedEffectsTests(unittest.TestCase):
    def setUp(self):
        y, x = np.mgrid[0:48, 0:64]
        self.asset = ImageAsset(np.dstack([x*4, y*5, (x+y)*2, np.full_like(x,255)]).astype('uint8'))

    def test_effects_return_new_assets(self):
        for fn, args in [(vignette,()),(film_grain,()),(bloom,()),(chromatic_aberration,()),(scanlines,()),(color_grade,()),(glitch,())]:
            out=fn(self.asset,*args)
            self.assertIsInstance(out,ImageAsset)
            self.assertEqual(out.pixels.shape,self.asset.pixels.shape)
            self.assertIsNot(out.pixels,self.asset.pixels)

    def test_grain_is_deterministic(self):
        a=film_grain(self.asset,seed=42); b=film_grain(self.asset,seed=42)
        self.assertTrue(np.array_equal(a.pixels,b.pixels))

    def test_vignette_preserves_alpha(self):
        out=vignette(self.asset)
        self.assertTrue(np.array_equal(out.pixels[:,:,3],self.asset.pixels[:,:,3]))

if __name__ == '__main__': unittest.main()
