
from manim import *
from manim.mobject.opengl.opengl_image_mobject import OpenGLImageMobject

from PIL import Image
import numpy as np


class PixelReveal(Scene):
    def construct(self):

        # 1. Load the original photograph
        image_path = (
            "examples/inside_an_ais_mind/assets/cat_master.png"
        )

        original = Image.open(image_path).convert("RGB")
        image_array = np.array(original)

        H, W, _ = image_array.shape

        # 2. Display the photograph
        photo = OpenGLImageMobject(image_path)
        photo.scale_to_fit_height(config.frame_height)
        photo.scale_to_fit_width(config.frame_width)

        self.add(photo)
        self.wait(2)

        # 3. Select a 64 x 64 region at the image centre
        crop_size = 64

        cx = W // 2
        cy = H // 2

        x1 = cx - crop_size // 2
        y1 = cy - crop_size // 2

        crop = image_array[
            y1:y1 + crop_size,
            x1:x1 + crop_size
        ]

        # 4. Highlight the selected region
        image_width = photo.width
        image_height = photo.height

        crop_width = crop_size / W * image_width
        crop_height = crop_size / H * image_height

        crop_x = (cx - W / 2) / W * image_width
        crop_y = (H / 2 - cy) / H * image_height

        selection = Rectangle(
            width=crop_width,
            height=crop_height,
            color=YELLOW,
            stroke_width=2
        ).move_to([crop_x, crop_y, 0])

        self.play(Create(selection), run_time=1)
        self.wait(1)

        # 5. Zoom into the selected region
        zoomed_photo = OpenGLImageMobject(crop)
        zoomed_photo.scale_to_fit_width(config.frame_width * 0.75)
        zoomed_photo.move_to(ORIGIN)

        self.play(
            FadeOut(photo),
            FadeOut(selection),
            FadeIn(zoomed_photo),
            run_time=1.5
        )

        self.wait(1)

        # 6. Generate progressively detailed pixel images
        def create_pixel_image(resolution):

            small = Image.fromarray(crop).resize(
                (resolution, resolution),
                Image.Resampling.NEAREST
            )

            enlarged = small.resize(
                (512, 512),
                Image.Resampling.NEAREST
            )

            return OpenGLImageMobject(np.array(enlarged))

        # 7. Reveal increasing pixel resolution
        current = zoomed_photo

        for resolution in [4, 8, 16, 32, 64]:

            next_image = create_pixel_image(resolution)

            next_image.scale_to_fit_width(config.frame_width * 0.75)
            next_image.move_to(ORIGIN)

            self.play(
                FadeOut(current),
                FadeIn(next_image),
                run_time=1
            )

            current = next_image
            self.wait(0.5)

        # 8. Display the mathematical representation
        # 8. Display the mathematical representation
        equation = Text(
           "I ∈ {0, ..., 255}^(H × W × 3)",
            font_size=30,
            color=WHITE
        ).to_edge(DOWN)

        self.play(FadeIn(equation), run_time=1)
        self.wait(3)