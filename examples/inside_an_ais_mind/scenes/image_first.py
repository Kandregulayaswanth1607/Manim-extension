
from manim import *
from pathlib import Path


class ImageFirst(Scene):
    def construct(self):

        self.camera.background_color = "#080A10"

        # Locate image
        project_dir = Path(__file__).resolve().parents[1]
        image_path = project_dir / "assets" / "cat_master.png"

        # Load and fit image to the screen
        photo = ImageMobject(str(image_path))
        photo.scale_to_fit_width(config.frame_width)
        photo.scale_to_fit_height(config.frame_height)

        photo.move_to(ORIGIN)

        # Opening
        self.wait(1)

        self.play(
            FadeIn(photo),
            run_time=2
        )

        self.wait(2)

        # Cinematic camera push-in
        self.play(
            photo.animate.scale(1.15),
            run_time=4,
            rate_func=smooth
        )

        # Scanning line
        scan_line = Line(
            LEFT * config.frame_width / 2 + UP * 3,
            RIGHT * config.frame_width / 2 + UP * 3,
            color="#00E5FF",
            stroke_width=2
        )

        self.play(Create(scan_line), run_time=0.5)

        self.play(
            scan_line.animate.shift(DOWN * 6),
            run_time=3,
            rate_func=linear
        )

        self.wait(1)
