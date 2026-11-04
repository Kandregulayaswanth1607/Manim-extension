
from manim import *
from pathlib import Path


class OpeningScene(MovingCameraScene):

    def construct(self):

        self.camera.background_color = "#030609"

        # -----------------------------------
        # 1. BACKGROUND IMAGE
        # -----------------------------------

        IMAGE_PATH = (
              Path(__file__).parent
              / "assets"
              / "how_ai_learns"
              / "scene1_opening.png"
       )

        background = ImageMobject(str(IMAGE_PATH))

        background.scale_to_fit_width(config.frame_width)
        background.move_to(ORIGIN)

        self.add(background)

        # -----------------------------------
        # 2. TITLE DESIGN
        # -----------------------------------

        eyebrow = Text(
            "THE SCIENCE OF INTELLIGENCE",
            font_size=17,
            color="#56DFFF",
            weight=BOLD
        )

        title1 = Text(
            "HOW DOES AI",
            font_size=39,
            color=WHITE,
            weight=BOLD
        )

        title2 = Text(
            "ACTUALLY LEARN?",
            font_size=39,
            color="#56DFFF",
            weight=BOLD
        )

        subtitle = Text(
            "A journey inside artificial intelligence",
            font_size=17,
            color="#A9B7C6"
        )

        title_group = VGroup(
            eyebrow,
            title1,
            title2,
            subtitle
        ).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.22
        )

        title_group.move_to(
            [-3.35, 0.15, 0]
        )

        # -----------------------------------
        # 3. CENTRAL NODE GLOW
        # -----------------------------------

        node_position = [2.05, 0.18, 0]

        glow_outer = Circle(
            radius=0.28,
            color="#00DFFF",
            stroke_width=2,
            stroke_opacity=0.18
        ).move_to(node_position)

        glow_inner = Circle(
            radius=0.15,
            color="#00DFFF",
            stroke_width=2,
            stroke_opacity=0.55
        ).move_to(node_position)

        self.add(glow_outer, glow_inner)

        # -----------------------------------
        # 4. CINEMATIC OPENING
        # -----------------------------------

        self.camera.frame.scale(1.04)

        self.play(
            self.camera.frame.animate.scale(1 / 1.04),
            run_time=1.5,
            rate_func=smooth
        )

        self.play(
            FadeIn(eyebrow, shift=RIGHT * 0.2),
            FadeIn(title1, shift=RIGHT * 0.2),
            FadeIn(title2, shift=RIGHT * 0.2),
            FadeIn(subtitle, shift=RIGHT * 0.2),
            run_time=1.8
        )

        # -----------------------------------
        # 5. NODE PULSE
        # -----------------------------------

        self.play(
            glow_outer.animate.scale(1.8).set_stroke(
                opacity=0.0
            ),
            glow_inner.animate.scale(1.5).set_stroke(
                opacity=0.0
            ),
            run_time=1.5,
            rate_func=smooth
        )

        # -----------------------------------
        # 6. SLOW CAMERA MOVEMENT
        # -----------------------------------

        self.play(
            self.camera.frame.animate.scale(0.96).shift(
                RIGHT * 0.25
            ),
            run_time=2.2,
            rate_func=smooth
        )

        self.wait(1)
