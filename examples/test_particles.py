
from manim import *
from manim_pics import load, image_particles, particle_reveal, particle_dissolve
from manim_pics import brightness, contrast, saturation
from pathlib import Path


IMAGE_PATH = (
    Path(__file__).parent
    / "assets"
    / "how_ai_learns"
    / "scene1_opening.png"
)


class ParticleTest(Scene):

    def construct(self):

        # Load image
        asset = load(IMAGE_PATH)

        # Brighten and enhance the source image
        asset = brightness(asset, 1.8)
        asset = contrast(asset, 1.25)
        asset = saturation(asset, 1.4)

        # Generate more visible particles
        particles = image_particles(
            asset,
            count=1500,
            point_radius=0.045,
            max_width=11,
            seed=42,
        )

        # Add a soft glow-like layer behind the particles
        glow = particles.copy()
        glow.set_opacity(0.20)
        glow.scale(1.5)

        self.add(glow)

        # Reveal the main particles
        particle_reveal(
            self,
            particles,
            run_time=4,
        )

        self.wait(1)

        # Dissolve
        particle_dissolve(
            self,
            particles,
            distance=3,
            run_time=2.5,
            seed=42,
        )

        self.play(FadeOut(glow), run_time=1)
        self.wait(0.5)
