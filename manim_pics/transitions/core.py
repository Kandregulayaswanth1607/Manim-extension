"""Reusable Manim transition constructors. Each returns a Manim Animation."""

def fade_in(mobject, **kwargs):
    from manim import FadeIn
    return FadeIn(mobject, **kwargs)

def fade_out(mobject, **kwargs):
    from manim import FadeOut
    return FadeOut(mobject, **kwargs)

def slide_in(mobject, direction='right', distance=1.0, **kwargs):
    from manim import FadeIn, RIGHT, LEFT, UP, DOWN
    vectors={'right':RIGHT,'left':LEFT,'up':UP,'down':DOWN}
    if direction not in vectors: raise ValueError("direction must be right, left, up, or down")
    return FadeIn(mobject,shift=vectors[direction]*distance,**kwargs)

def zoom_in(mobject, scale=0.15, **kwargs):
    from manim import FadeIn
    if scale <= 0: raise ValueError('scale must be positive')
    return FadeIn(mobject, scale=scale, **kwargs)

def spin_in(mobject, angle=6.283185307179586, **kwargs):
    from manim import SpinInFromNothing
    return SpinInFromNothing(mobject, angle=angle, **kwargs)

def wipe_in(mobject, direction='left', **kwargs):
    """Directional edge reveal for vector objects via Create; raster objects use FadeIn."""
    from manim import Create, FadeIn, VMobject
    if isinstance(mobject, VMobject):
        return Create(mobject, **kwargs)
    return FadeIn(mobject, **kwargs)
