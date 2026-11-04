from __future__ import annotations

import numpy as np
from manim import *


class SpeechBubble(VGroup):
    """SpeechBubble("hello", tail="left").beside(character, RIGHT)"""

    def __init__(self, text, font_size=24, tail="left", fill=WHITE, text_color="#1b1f2a", **kwargs):
        super().__init__(**kwargs)
        t = Text(text, font_size=font_size, color=text_color)
        box = RoundedRectangle(corner_radius=0.2, width=t.width + 0.6, height=t.height + 0.45,
                               fill_color=fill, fill_opacity=1, stroke_width=0)
        t.move_to(box)
        if tail in ("left", "right"):
            out = LEFT if tail == "left" else RIGHT
            edge = box.get_left() if tail == "left" else box.get_right()
            self.add(Polygon(edge - out * 0.02 + UP * 0.1, edge - out * 0.02 + DOWN * 0.25,
                             edge + out * 0.3 + DOWN * 0.3,
                             fill_color=fill, fill_opacity=1, stroke_width=0))
        self.add(box, t)
        self.tail_side = tail

    def beside(self, mob, side=RIGHT, buff=0.35, dy=0.15):
        """Park the bubble next to `mob` so its tail points at it."""
        if side[0] > 0:
            self.move_to([mob.get_right()[0] + buff, mob.get_center()[1] + dy, 0], aligned_edge=LEFT)
        else:
            self.move_to([mob.get_left()[0] - buff, mob.get_center()[1] + dy, 0], aligned_edge=RIGHT)
        return self
