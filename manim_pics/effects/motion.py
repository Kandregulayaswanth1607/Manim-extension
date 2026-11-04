"""Manim-native motion effects. Import functions inside Scene.construct()."""

def shake(mobject, duration=0.5, amplitude=0.08, frequency=18, seed=0):
    """Return an UpdateFromAlphaFunc that shakes an object and restores its position."""
    import numpy as np
    from manim import UpdateFromAlphaFunc
    origin=mobject.get_center().copy(); rng=np.random.default_rng(seed)
    phases=rng.uniform(0,2*np.pi,2)
    def update(mob, alpha):
        envelope=np.sin(np.pi*alpha)
        t=alpha*duration*frequency*2*np.pi
        mob.move_to(origin + amplitude*envelope*np.array([np.sin(t+phases[0]),np.cos(t*1.17+phases[1]),0]))
    return UpdateFromAlphaFunc(mobject,update,run_time=duration)


def glow_pulse(mobject, color='#7DF9FF', min_width=2, max_width=12, cycles=2, duration=2):
    """Pulse stroke width/color on a VMobject; returns an updater animation."""
    from manim import UpdateFromAlphaFunc
    def update(mob, alpha):
        width=min_width+(max_width-min_width)*(0.5-0.5*__import__('math').cos(2*__import__('math').pi*cycles*alpha))
        mob.set_stroke(color=color,width=width)
    return UpdateFromAlphaFunc(mobject,update,run_time=duration)
