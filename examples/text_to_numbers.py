
from manim import *
import numpy as np


class TextToNumbers(MovingCameraScene):
    def construct(self):

        # --------------------------------------------------
        # CONFIGURATION
        # --------------------------------------------------

        self.camera.background_color = "#080B14"

        CYAN = "#35D6F5"
        VIOLET = "#9B72F2"
        WHITE = "#F2F5FA"
        GREY = "#8792A5"
        DARK = "#151C2B"
        GREEN = "#68E0B5"

        # --------------------------------------------------
        # BACKGROUND GRID
        # --------------------------------------------------

        grid = NumberPlane(
            x_range=[-8, 8, 1],
            y_range=[-4.5, 4.5, 1],
            background_line_style={
                "stroke_color": "#283247",
                "stroke_width": 0.6,
                "stroke_opacity": 0.25,
            },
            axis_config={
                "stroke_opacity": 0,
            },
        )

        self.add(grid)

        # --------------------------------------------------
        # TITLE
        # --------------------------------------------------

        title = Text(
            "FROM LANGUAGE TO NUMBERS",
            font_size=32,
            weight=BOLD,
            color=WHITE,
        ).to_edge(UP, buff=0.45)

        title_line = Line(
            LEFT * 5.5,
            RIGHT * 5.5,
            color=CYAN,
            stroke_width=1.2,
        ).next_to(title, DOWN, buff=0.22)

        self.play(
            FadeIn(title, shift=DOWN * 0.2),
            Create(title_line),
            run_time=1.2,
        )

        self.wait(0.5)

        # --------------------------------------------------
        # STEP 1: INPUT SENTENCE
        # --------------------------------------------------

        section_label = Text(
            "01  /  INPUT TEXT",
            font_size=19,
            color=CYAN,
            weight=BOLD,
        )

        section_label.move_to(UP * 1.65)

        sentence = Text(
            "The cat sat.",
            font_size=54,
            color=WHITE,
        )

        sentence.move_to(ORIGIN)

        sentence_glow = SurroundingRectangle(
            sentence,
            color=CYAN,
            buff=0.25,
            corner_radius=0.12,
            stroke_width=2,
        )

        input_caption = Text(
            "A sentence enters the model.",
            font_size=21,
            color=GREY,
        ).next_to(sentence, DOWN, buff=0.65)

        self.play(
            FadeIn(section_label, shift=UP * 0.2),
            Write(sentence),
            run_time=1.5,
        )

        self.play(
            Create(sentence_glow),
            FadeIn(input_caption),
            run_time=0.8,
        )

        self.wait(1)

        # --------------------------------------------------
        # STEP 2: TOKENIZATION
        # --------------------------------------------------

        token_label = Text(
            "TOKENIZATION",
            font_size=25,
            color=CYAN,
            weight=BOLD,
        ).move_to(UP * 1.15)

        token_explanation = Text(
            "The sentence is divided into smaller units called tokens.",
            font_size=20,
            color=GREY,
        ).move_to(DOWN * 2.0)

        words = ["The", "cat", "sat", "."]

        token_texts = VGroup(
            *[
                Text(
                    word,
                    font_size=43,
                    color=WHITE,
                )
                for word in words
            ]
        )

        token_texts.arrange(RIGHT, buff=0.35)
        token_texts.move_to(ORIGIN)

        token_boxes = VGroup(
            *[
                SurroundingRectangle(
                    token,
                    color=CYAN,
                    buff=0.16,
                    corner_radius=0.08,
                    stroke_width=2,
                )
                for token in token_texts
            ]
        )

        self.play(
            FadeOut(sentence_glow),
            FadeOut(input_caption),
            FadeOut(section_label),
            FadeOut(sentence),
            FadeIn(token_label),
            run_time=0.8,
        )

        # Transform the original sentence into individual tokens.
        self.play(
            FadeIn(token_texts, scale=0.8),
            run_time=1.0,
        )

        self.play(
            *[Create(box) for box in token_boxes],
            run_time=0.9,
        )

        self.play(
            FadeIn(token_explanation, shift=UP * 0.15),
            run_time=0.7,
        )

        self.wait(1.5)

        # --------------------------------------------------
        # STEP 3: TOKEN IDS
        # --------------------------------------------------

        id_label = Text(
            "TOKEN IDs",
            font_size=25,
            color=VIOLET,
            weight=BOLD,
        ).move_to(UP * 1.15)

        id_explanation = Text(
            "Each token is assigned an integer lookup index.",
            font_size=20,
            color=GREY,
        ).move_to(DOWN * 2.0)

        illustrative_ids = ["464", "3797", "3332", "13"]

        id_texts = VGroup(
            *[
                Text(
                    value,
                    font_size=43,
                    color=VIOLET,
                    weight=BOLD,
                )
                for value in illustrative_ids
            ]
        )

        id_texts.arrange(RIGHT, buff=0.8)
        id_texts.move_to(ORIGIN)

        id_boxes = VGroup(
            *[
                SurroundingRectangle(
                    item,
                    color=VIOLET,
                    buff=0.18,
                    corner_radius=0.08,
                    stroke_width=2,
                )
                for item in id_texts
            ]
        )

        self.play(
            FadeOut(token_label),
            FadeOut(token_explanation),
            FadeOut(token_boxes),
            FadeIn(id_label),
            FadeIn(id_explanation),
            run_time=0.8,
        )

        self.play(
            *[
                Transform(token_texts[i], id_texts[i])
                for i in range(4)
            ],
            run_time=1.2,
        )

        self.play(
            *[Create(box) for box in id_boxes],
            run_time=0.8,
        )

        self.wait(1.5)

        # --------------------------------------------------
        # STEP 4: EMBEDDING LOOKUP TABLE
        # --------------------------------------------------

        lookup_title = Text(
            "EMBEDDING LOOKUP",
            font_size=25,
            color=CYAN,
            weight=BOLD,
        ).move_to(UP * 1.15)

        table_caption = Text(
            "An ID retrieves its learned vector from an embedding table.",
            font_size=19,
            color=GREY,
        ).move_to(DOWN * 2.7)

        # Illustrative vector values.
        embedding_values = [
            ["0.21", "-0.43", "0.81", "0.12"],
            ["0.67", "0.18", "-0.24", "0.92"],
            ["-0.31", "0.75", "0.42", "-0.16"],
            ["0.54", "-0.09", "0.63", "0.37"],
        ]

        row_labels = VGroup()
        vector_rows = VGroup()
        row_outlines = VGroup()

        row_y_positions = [0.75, -0.05, -0.85, -1.65]

        for i in range(4):

            id_label_item = Text(
                illustrative_ids[i],
                font_size=27,
                color=VIOLET,
                weight=BOLD,
            )

            id_label_item.move_to(LEFT * 3.0 + UP * row_y_positions[i])

            vector_items = VGroup(
                *[
                    Text(
                        value,
                        font_size=25,
                        color=CYAN,
                    )
                    for value in embedding_values[i]
                ]
            )

            vector_items.arrange(RIGHT, buff=0.35)
            vector_items.move_to(
                RIGHT * 1.25 + UP * row_y_positions[i]
            )

            row_outline = RoundedRectangle(
                width=7.5,
                height=0.58,
                corner_radius=0.08,
                color="#34435C",
                stroke_width=1,
            )

            row_outline.move_to(
                UP * row_y_positions[i]
            )

            row_labels.add(id_label_item)
            vector_rows.add(vector_items)
            row_outlines.add(row_outline)

        self.play(
            FadeOut(id_label),
            FadeOut(id_explanation),
            FadeOut(id_boxes),
            FadeIn(lookup_title),
            FadeIn(table_caption),
            run_time=0.9,
        )

        # Transform the visible token ID objects into table row labels.
        self.play(
            *[
                Transform(token_texts[i], row_labels[i])
                for i in range(4)
            ],
            run_time=1.3,
        )

        # Reveal the corresponding embedding vectors.
        self.play(
            *[
                Create(row_outlines[i])
                for i in range(4)
            ],
            *[
                FadeIn(vector_rows[i], shift=RIGHT * 0.2)
                for i in range(4)
            ],
            run_time=1.2,
        )

        self.wait(1.5)

        # --------------------------------------------------
        # STEP 5: SELECT ONE EMBEDDING
        # --------------------------------------------------

        selected_vector = vector_rows[0].copy()

        self.play(
            *[
                FadeOut(token_texts[i])
                for i in range(4)
            ],
            *[
                FadeOut(vector_rows[i])
                for i in range(1, 4)
            ],
            *[
                FadeOut(row_outlines[i])
                for i in range(1, 4)
            ],
            FadeOut(vector_rows[0]),
            FadeOut(row_outlines[0]),
            FadeOut(table_caption),
            run_time=1.1,
        )

        vector_heading = Text(
            "A LEARNED VECTOR",
            font_size=27,
            color=CYAN,
            weight=BOLD,
        ).move_to(UP * 1.35)

        vector_note = Text(
            "A point in a high-dimensional mathematical space.",
            font_size=20,
            color=GREY,
        ).move_to(DOWN * 1.5)

        self.play(
            FadeOut(lookup_title),
            FadeIn(vector_heading),
            FadeIn(selected_vector),
            run_time=1.0,
        )

        self.play(
            selected_vector.animate.scale(1.55).move_to(ORIGIN),
            run_time=1.3,
        )

        self.play(
            FadeIn(vector_note, shift=UP * 0.2),
            run_time=0.8,
        )

        # Highlight individual dimensions.
        dimension_labels = VGroup(
            *[
                Text(
                    f"dimension {i + 1}",
                    font_size=16,
                    color=GREY,
                )
                for i in range(4)
            ]
        )

        for i, label in enumerate(dimension_labels):
            label.next_to(selected_vector[i], DOWN, buff=0.45)

        self.play(
            *[
                FadeIn(label)
                for label in dimension_labels
            ],
            run_time=0.8,
        )

        self.wait(2)

        # --------------------------------------------------
        # STEP 6: KEY IDEA
        # --------------------------------------------------

        self.play(
            FadeOut(selected_vector),
            FadeOut(vector_heading),
            FadeOut(vector_note),
            FadeOut(dimension_labels),
            run_time=0.8,
        )

        final_statement = Text(
            "LANGUAGE BECOMES MATHEMATICS",
            font_size=32,
            color=WHITE,
            weight=BOLD,
        ).move_to(UP * 0.5)

        final_subtitle = Text(
            "The model processes numerical representations, not raw words.",
            font_size=20,
            color=GREY,
        ).next_to(final_statement, DOWN, buff=0.5)

        final_line = Line(
            LEFT * 3.2,
            RIGHT * 3.2,
            color=CYAN,
            stroke_width=3,
        ).next_to(final_subtitle, DOWN, buff=0.55)

        self.play(
            Write(final_statement),
            FadeIn(final_subtitle, shift=UP * 0.15),
            run_time=1.5,
        )

        self.play(
            Create(final_line),
            run_time=0.8,
        )

        self.wait(2)

        # --------------------------------------------------
        # END
        # --------------------------------------------------

        self.play(
            *[
                FadeOut(mob)
                for mob in list(self.mobjects)
            ],
            run_time=1.2,
        )

        self.wait(0.5)
