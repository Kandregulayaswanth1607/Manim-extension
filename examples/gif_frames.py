"""Inspect and export frames from an animated GIF."""
import manim_pics as mp

sequence = mp.load_gif("animation.gif")
print(f"Frames: {sequence.frame_count}")
print(f"Dimensions: {sequence.size}")
print(f"Duration: {sequence.total_duration} ms")

# Export an individual frame for use in another project.
sequence.frames[0].save("first-frame.png")

# Save the complete sequence again after processing each frame.
processed = [frame.grayscale().contrast(1.15) for frame in sequence.frames]
mp.ImageSequence(processed, sequence.durations, sequence.loop).save_gif("processed.gif")
