from pathlib import Path
from manim import *
import manim_pics as mp

mp.add_asset_dir(Path(__file__).parent / "assets")


class PicDemo(mp.PicScene):
    def construct(self):
        title = Text("manim_pics demo", font_size=44, weight=BOLD).to_edge(UP, buff=0.5)
        row = mp.pic_row(
            mp.Pic("cat", height=1.8, label="built-in vector"),
            mp.Emoji("🐱", height=1.8, label="emoji (Twemoji)"),
            mp.Pic("sample", height=1.8, circle=True, label="your file, circle crop"),
            mp.Pic("not_there", height=1.8, label="missing: placeholder"),
            buff=0.6,
        ).move_to(UP * 0.4)
        self.play(FadeIn(title))
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in row], lag_ratio=0.25))
        self.show_narrator()
        self.say("Drop PNG / JPG / SVG files in ./assets,\nthen call Pic(\"filename\").", hold=2)
        self.say("Your file overrides a built-in with the same name.", hold=2)
        self.play(row[0].animate.shift(UP * 0.3), Wiggle(row[1]))
        self.wait(1)
        self.clear_scene()
