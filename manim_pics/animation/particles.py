"""Image-to-particle conversion and deterministic particle animations."""
import numpy as np

def image_particles(asset, count=500, point_radius=0.025, max_width=7.0, seed=0, alpha_threshold=24):
    """Sample visible image pixels into a Manim VGroup of colored dots.

    Coordinates preserve image aspect ratio and are centered at the origin.
    `count` is a maximum approximate sample count, not a fixed output size.
    """
    from manim import VGroup, Dot, rgb_to_color
    if count < 1 or point_radius <= 0 or max_width <= 0: raise ValueError('count, point_radius and max_width must be positive')
    p=asset.pixels; h,w=p.shape[:2]; step=max(1,int(np.sqrt((h*w)/count)))
    ys,xs=np.mgrid[0:h:step,0:w:step]; ys=ys.ravel(); xs=xs.ravel()
    valid=p[ys,xs,3]>=alpha_threshold; ys,xs=ys[valid],xs[valid]
    rng=np.random.default_rng(seed)
    if len(xs)>count:
        idx=rng.choice(len(xs),count,replace=False); ys,xs=ys[idx],xs[idx]
    scale=max_width/w; x=(xs-(w-1)/2)*scale; y=((h-1)/2-ys)*scale
    group=VGroup()
    for xx,yy,rgba in zip(x,y,p[ys,xs]):
        group.add(Dot([xx,yy,0],radius=point_radius,color=rgb_to_color(rgba[:3]/255)))
    return group


def particle_reveal(scene, particles, run_time=2.0, lag_ratio=0.002):
    """Animate sampled image particles into place using a staggered FadeIn."""
    from manim import LaggedStart, FadeIn
    return scene.play(LaggedStart(*(FadeIn(dot,scale=0.1) for dot in particles),lag_ratio=lag_ratio),run_time=run_time)


def particle_dissolve(scene, particles, distance=2.0, run_time=1.5, seed=0):
    """Scatter particles away from their image positions."""
    from manim import AnimationGroup, FadeOut
    rng=np.random.default_rng(seed); animations=[]
    for dot in particles:
        vector=np.array([*rng.normal(size=2),0.0]); norm=np.linalg.norm(vector[:2]) or 1
        animations.append(FadeOut(dot,shift=vector/norm*distance))
    return scene.play(AnimationGroup(*animations,lag_ratio=0.001),run_time=run_time)
