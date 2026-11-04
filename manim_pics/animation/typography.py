"""Kinetic typography helpers."""
def typewriter(text_mobject, run_time=2.0, lag_ratio=0.04):
    """Return a staggered character-by-character FadeIn animation."""
    from manim import AnimationGroup, FadeIn, VGroup
    chars=VGroup(*text_mobject.submobjects) if text_mobject.submobjects else VGroup(text_mobject)
    return AnimationGroup(*(FadeIn(char,shift=(0,-0.12,0)) for char in chars),lag_ratio=lag_ratio,run_time=run_time)

def word_reveal(text_mobject, run_time=1.5, lag_ratio=0.12):
    """Stagger a Text/Paragraph object by word (when word submobjects exist)."""
    from manim import AnimationGroup, FadeIn
    parts=list(text_mobject.submobjects) or [text_mobject]
    return AnimationGroup(*(FadeIn(part,shift=(0,-0.15,0)) for part in parts),lag_ratio=lag_ratio,run_time=run_time)
