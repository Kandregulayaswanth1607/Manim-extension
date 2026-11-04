from manim import *
import manim_pics as mp


class ProcessedPhoto(Scene):
    def construct(self):
        asset = (
            mp.load("C:\Users\USER\OneDrive\Pictures\test1.png")
            .resize(900, 600)
            .saturation(0.35)
            .contrast(1.2)
        )
        photo = asset.to_mobject(scale_to=4.5)
        title = Text("Image processing with manim-pics", font_size=30)
        title.to_edge(UP)
        self.play(Write(title), FadeIn(photo))
        self.wait(2)
