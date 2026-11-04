"""Built-in vector characters, drawn with Manim shapes (no files needed).

Any file in your assets folder with the same name overrides these, e.g.
put cat.png in ./assets and Pic("cat") uses your picture instead.
Add your own with  register("dog", make_dog, height=2).
"""
from __future__ import annotations

import numpy as np
from manim import *

CAT_C = "#F4A259"
VC = "#83C167"


def make_robot():
    body = RoundedRectangle(width=0.9, height=0.8, corner_radius=0.15, fill_color="#4A90D9",
                            fill_opacity=1, stroke_width=0).shift(DOWN * 0.7)
    head = RoundedRectangle(width=1.0, height=0.75, corner_radius=0.2, fill_color="#6BB5F0",
                            fill_opacity=1, stroke_width=0)
    eyes = VGroup(*[VGroup(Circle(radius=0.12, fill_color=WHITE, fill_opacity=1, stroke_width=0),
                           Dot(radius=0.05, color=BLACK)) for _ in range(2)])
    eyes.arrange(RIGHT, buff=0.25).move_to(head.get_center() + UP * 0.06)
    mouth = Arc(radius=0.14, start_angle=PI * 1.15, angle=PI * 0.7, color=WHITE,
                stroke_width=3).move_to(head.get_center() + DOWN * 0.2)
    ant = Line(head.get_top(), head.get_top() + UP * 0.28, color=GREY_B, stroke_width=3)
    tip = Dot(ant.get_end(), color=YELLOW, radius=0.07)
    arms = VGroup(
        Line(body.get_left() + UP * 0.2, body.get_left() + LEFT * 0.3 + DOWN * 0.05, color=GREY_B, stroke_width=5),
        Line(body.get_right() + UP * 0.2, body.get_right() + RIGHT * 0.3 + DOWN * 0.05, color=GREY_B, stroke_width=5))
    chest = Dot(body.get_center() + UP * 0.1, radius=0.08, color=YELLOW)
    return VGroup(arms, body, chest, head, eyes, mouth, ant, tip)


def make_cat(asleep=True, color=CAT_C):
    body = Ellipse(width=1.5, height=1.1, fill_color=color, fill_opacity=1, stroke_width=0).move_to([0, -0.55, 0])
    tail = ArcBetweenPoints([0.65, -0.75, 0], [1.25, -0.05, 0], angle=-PI / 2, color=color, stroke_width=12)
    paws = VGroup(*[Ellipse(width=0.35, height=0.2, fill_color=color, fill_opacity=1,
                            stroke_width=0).move_to([x, -1.05, 0]) for x in (-0.35, 0.35)])
    head = Circle(radius=0.55, fill_color=color, fill_opacity=1, stroke_width=0).move_to([0, 0.35, 0])
    ears = VGroup(*[Triangle(fill_color=color, fill_opacity=1, stroke_width=0).scale(0.22)
                    .move_to([sx * 0.33, 0.85, 0]) for sx in (-1, 1)])
    inner = VGroup(*[Triangle(fill_color="#FFB4A2", fill_opacity=1, stroke_width=0).scale(0.11)
                     .move_to([sx * 0.33, 0.83, 0]) for sx in (-1, 1)])
    if asleep:
        eyes = VGroup(*[Arc(radius=0.09, start_angle=PI, angle=PI, color=BLACK, stroke_width=3)
                        .move_to([sx * 0.2, 0.4, 0]) for sx in (-1, 1)])
    else:
        eyes = VGroup(*[Dot([sx * 0.2, 0.4, 0], radius=0.06, color=BLACK) for sx in (-1, 1)])
    nose = Triangle(fill_color="#E76F8A", fill_opacity=1, stroke_width=0).scale(0.06).rotate(PI).move_to([0, 0.25, 0])
    whisk = VGroup(*[Line([sx * 0.2, 0.2 + dy, 0], [sx * 0.65, 0.2 + dy * 2, 0], color=WHITE, stroke_width=1.5)
                     for sx in (-1, 1) for dy in (-0.05, 0.05)])
    return VGroup(tail, body, paws, head, ears, inner, eyes, nose, whisk)


def make_zzz(color=BLUE_B):
    return VGroup(Text("z", font_size=22, color=color), Text("z", font_size=30, color=color),
                  Text("Z", font_size=40, color=color)).arrange(UR, buff=0.05)


def make_street(width=12.5):
    road = Rectangle(width=width, height=0.9, fill_color="#3a3f4b", fill_opacity=1, stroke_width=0)
    dash = DashedLine(road.get_left() + RIGHT * 0.3, road.get_right() - RIGHT * 0.3,
                      color=YELLOW, stroke_width=3, dash_length=0.3)
    c1 = Line(road.get_corner(UL), road.get_corner(UR), color=GREY_B, stroke_width=4)
    c2 = Line(road.get_corner(DL), road.get_corner(DR), color=GREY_B, stroke_width=4)
    return VGroup(road, dash, c1, c2)


def make_car(color="#E63946"):
    body = RoundedRectangle(width=1.4, height=0.4, corner_radius=0.1, fill_color=color,
                            fill_opacity=1, stroke_width=0)
    top = RoundedRectangle(width=0.8, height=0.3, corner_radius=0.1, fill_color=color,
                           fill_opacity=1, stroke_width=0).next_to(body, UP, buff=-0.05)
    win = Rectangle(width=0.5, height=0.18, fill_color="#A8DADC", fill_opacity=1, stroke_width=0).move_to(top)
    wheels = VGroup(*[Circle(radius=0.15, fill_color=BLACK, fill_opacity=1, stroke_color=GREY,
                             stroke_width=2).move_to(body.get_bottom() + RIGHT * dx) for dx in (-0.4, 0.4)])
    return VGroup(body, top, win, wheels)


def make_gift(color=VC, s=0.5):
    box = Square(s, fill_color=color, fill_opacity=1, stroke_color=WHITE, stroke_width=1.5)
    rv = Line(box.get_top(), box.get_bottom(), color=WHITE, stroke_width=3)
    rh = Line(box.get_left(), box.get_right(), color=WHITE, stroke_width=3)
    bow = VGroup(*[Circle(radius=s * 0.17, color=WHITE, stroke_width=3)
                   .move_to(box.get_top() + RIGHT * sx * s * 0.17 + UP * s * 0.12) for sx in (-1, 1)])
    return VGroup(box, rv, rh, bow)


def make_detective(color="#FFD43B"):
    face = Circle(radius=0.5, fill_color=color, fill_opacity=1, stroke_width=0)
    eyes = VGroup(*[VGroup(Circle(radius=0.1, fill_color=WHITE, fill_opacity=1, stroke_width=0),
                           Dot(radius=0.04, color=BLACK)) for _ in range(2)])
    eyes.arrange(RIGHT, buff=0.18).move_to(face.get_center() + UP * 0.08)
    mouth = Arc(radius=0.15, start_angle=PI * 1.15, angle=PI * 0.7, color="#7a5c00",
                stroke_width=3).move_to(face.get_center() + DOWN * 0.22)
    brim = Rectangle(width=1.0, height=0.08, fill_color="#5b3a1e", fill_opacity=1,
                     stroke_width=0).move_to(face.get_top() + DOWN * 0.02)
    crown = RoundedRectangle(width=0.6, height=0.3, corner_radius=0.08, fill_color="#5b3a1e",
                             fill_opacity=1, stroke_width=0).next_to(brim, UP, buff=-0.02)
    lens = Circle(radius=0.26, color=WHITE, stroke_width=4).move_to(face.get_center() + RIGHT * 0.75 + DOWN * 0.15)
    p = lens.point_at_angle(-PI / 4)
    handle = Line(p, p + np.array([0.3, -0.3, 0]), color=WHITE, stroke_width=5)
    return VGroup(face, eyes, mouth, brim, crown, lens, handle)


# name -> (factory, default size kwargs)
REGISTRY: dict = {
    "cat": (make_cat, {"height": 2}),
    "cat_awake": (lambda: make_cat(asleep=False), {"height": 2}),
    "robot": (make_robot, {"height": 2}),
    "detective": (make_detective, {"height": 1.6}),
    "gift": (make_gift, {"height": 0.8}),
    "car": (make_car, {"width": 1.8}),
    "street": (make_street, {"width": 10}),
    "zzz": (make_zzz, {"height": 0.8}),
}


def register(name: str, factory, **default_size) -> None:
    """Add your own vector picture:  register("dog", make_dog, height=2)."""
    REGISTRY[name] = (factory, default_size or {"height": 2})
