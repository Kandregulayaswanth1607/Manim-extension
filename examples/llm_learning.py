
from manim import *


class LLMOpening(Scene):
    def construct(self):
        # Dark cinematic background
        self.camera.background_color = "#050711"

        cyan = "#48DDF5"
        violet = "#A78BFA"
        white = "#F3F4F6"
        muted = "#8993A8"

        # Main title
        title = Text(
            "HOW DO LLMs LEARN?",
            font_size=46,
            weight=BOLD,
            color=white,
        )

        subtitle = Text(
            "From human language to mathematical representations",
            font_size=21,
            color=muted,
        )

        title_group = VGroup(title, subtitle).arrange(
            DOWN, buff=0.25
        )

        self.play(
            FadeIn(title, shift=UP * 0.3),
            run_time=1.5,
        )
        self.play(
            FadeIn(subtitle),
            run_time=1,
        )
        self.wait(1)

        self.play(
            title_group.animate.scale(0.72).to_edge(UP, buff=0.55),
            run_time=1,
        )

        # Text input
        text_label = Text(
            "TEXT",
            font_size=18,
            color=cyan,
            weight=BOLD,
        )

        sentence = Text(
            "The cat sat on the mat.",
            font_size=25,
            color=white,
        )

        text_card = VGroup(
            RoundedRectangle(
                width=5.3,
                height=1.5,
                corner_radius=0.15,
                stroke_color=cyan,
                stroke_width=2,
                fill_color="#101C2B",
                fill_opacity=0.9,
            ),
            VGroup(text_label, sentence).arrange(
                DOWN, buff=0.22
            ),
        )

        text_card.move_to(LEFT * 3.2 + UP * 0.3)

        # Image input
        image_label = Text(
            "IMAGE",
            font_size=18,
            color=violet,
            weight=BOLD,
        )

        image_frame = RoundedRectangle(
            width=2.2,
            height=1.5,
            corner_radius=0.12,
            stroke_color=violet,
            stroke_width=2,
            fill_color="#17142B",
            fill_opacity=1,
        )

        # A simple illustrative picture made from shapes
        sun = Circle(
            radius=0.22,
            color="#F9D66B",
            fill_opacity=1,
            stroke_width=0,
        ).move_to(UP * 0.35 + RIGHT * 0.55)

        hill1 = Polygon(
            [-0.95, -0.5, 0],
            [-0.25, 0.35, 0],
            [0.35, -0.5, 0],
            color="#35C99A",
            fill_opacity=1,
            stroke_width=0,
        )

        hill2 = Polygon(
            [-0.15, -0.5, 0],
            [0.55, 0.2, 0],
            [1.0, -0.5, 0],
            color="#4389C9",
            fill_opacity=1,
            stroke_width=0,
        )

        landscape = VGroup(sun, hill1, hill2)
        landscape.move_to(image_frame.get_center())

        image_visual = VGroup(image_frame, landscape)

        image_group = VGroup(
            image_label,
            image_visual,
        ).arrange(DOWN, buff=0.22)

        image_group.move_to(RIGHT * 3.2 + UP * 0.3)

        # Central AI system
        ai_circle = Circle(
            radius=0.85,
            color=cyan,
            stroke_width=3,
            fill_color="#102638",
            fill_opacity=0.9,
        )

        ai_text = Text(
            "AI",
            font_size=38,
            weight=BOLD,
            color=white,
        )

        ai_group = VGroup(ai_circle, ai_text)
        ai_group.move_to(DOWN * 2.1)

        # Connections
        left_arrow = Arrow(
            text_card.get_bottom(),
            ai_group.get_left(),
            color=cyan,
            buff=0.25,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.12,
        )

        right_arrow = Arrow(
            image_group.get_bottom(),
            ai_group.get_right(),
            color=violet,
            buff=0.25,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.12,
        )

        self.play(
            FadeIn(text_card, shift=RIGHT * 0.3),
            FadeIn(image_group, shift=LEFT * 0.3),
            run_time=1.5,
        )

        self.play(
            GrowArrow(left_arrow),
            GrowArrow(right_arrow),
            FadeIn(ai_group, scale=0.7),
            run_time=1.5,
        )

        self.play(
            Indicate(ai_group, color=cyan),
            run_time=1,
        )

        question = Text(
            "How does a machine learn from both?",
            font_size=27,
            color=white,
        ).to_edge(DOWN, buff=0.35)

        self.play(
            FadeIn(question, shift=UP * 0.2),
            run_time=1,
        )

        self.wait(2)
