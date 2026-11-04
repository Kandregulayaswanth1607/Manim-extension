from manim import *
import manim_pics as mp

class CinematicPhoto(Scene):
    def construct(self):
        asset = (mp.load('examples/assets/sample.png')
                 .resize(1200, 800)
                 .contrast(1.12))
        # Film finish is performed on pixels, before Manim creates the image.
        asset = mp.color_grade(asset, contrast=1.12, saturation=1.18)
        asset = mp.vignette(asset, strength=0.55)
        asset = mp.film_grain(asset, amount=0.025, seed=7)
        photo = asset.to_mobject()
        photo.scale_to_fit_width(config.frame_width * 0.82)
        self.play(mp.zoom_in(photo, scale=0.82), run_time=1.4)
        self.play(mp.shake(photo, duration=0.35, amplitude=0.035))
        self.wait(0.5)
        self.play(mp.fade_out(photo))


class ParticlePortrait(Scene):
    def construct(self):
        asset = mp.load('examples/assets/sample.png').resize(480, 320)
        dots = mp.image_particles(asset, count=650, point_radius=0.018, max_width=6.2, seed=4)
        self.play(LaggedStart(*(FadeIn(d, scale=0.1) for d in dots), lag_ratio=0.001), run_time=2)
        self.wait(0.5)
        self.play(AnimationGroup(*(FadeOut(d, shift=2*RIGHT) for d in dots), lag_ratio=0.001), run_time=1.4)


class KineticTitle(Scene):
    def construct(self):
        title = Text('BEYOND THE FRAME', weight=BOLD, font_size=54)
        title.set_color_by_gradient(BLUE, TEAL, PURPLE)
        title.move_to(ORIGIN)
        self.play(mp.typewriter(title, run_time=1.8, lag_ratio=0.035))
        self.play(mp.glow_pulse(title, color=TEAL, min_width=1, max_width=5, cycles=2, duration=2))
        self.wait()
