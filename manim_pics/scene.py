from __future__ import annotations

from manim import *

from .pic import Pic
from .widgets import SpeechBubble


class PicScene(Scene):
    """Scene with a dark background plus a narrator who can talk.

        class Demo(PicScene):
            def construct(self):
                self.show_narrator()                 # built-in robot, bottom-left
                self.say("Hello!", hold=1)
                self.say("Any picture can be the narrator.")
                self.clear_scene()
    """

    background = "#0f1117"

    def setup(self):
        self.camera.background_color = self.background
        self.narrator = None
        self.bubble = None

    def show_narrator(self, pic="robot", pos=(-5.9, -2.75, 0), height=1.5):
        self.narrator = (pic if isinstance(pic, Mobject) else Pic(pic, height=height)).move_to(list(pos))
        self.bubble = None
        self.play(FadeIn(self.narrator, shift=UP * 0.3), run_time=0.5)
        return self.narrator

    def say(self, text, hold=0.0, **bubble_kw):
        if self.narrator is None:
            raise RuntimeError("Call show_narrator() before say().")
        new = SpeechBubble(text, **bubble_kw).beside(self.narrator)
        if self.bubble is not None:
            self.play(FadeOut(self.bubble), run_time=0.3)
        self.play(FadeIn(new, shift=UP * 0.15), run_time=0.5)
        self.bubble = new
        if hold:
            self.wait(hold)

    def clear_scene(self):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects])
        self.narrator, self.bubble = None, None
        self.wait(0.3)
