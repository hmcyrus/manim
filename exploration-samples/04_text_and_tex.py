"""
04 - Text and LaTeX
===================

Two ways to put words on screen:

  Text(...)   — uses system fonts (via Pango). Fast, supports any font you
                have installed, good for UI labels and titles.
  Tex(...)    — uses LaTeX. Required for real math notation. Slower because
                it shells out to a LaTeX compiler the first time.
                (You need a LaTeX install on your machine — see README.)

Run:
    manimgl exploration-samples/04_text_and_tex.py TextStyling -l
    manimgl exploration-samples/04_text_and_tex.py TexBasics -l
    manimgl exploration-samples/04_text_and_tex.py TexIndexing -l
"""

from manimlib import *


class TextStyling(Scene):
    def construct(self):
        # Plain text.
        title = Text("Hello, Manim", font_size=72)
        self.play(Write(title))
        self.wait(0.3)

        # Per-substring color via t2c (text-to-color).
        styled = Text(
            "red blue green",
            font_size=72,
            t2c={"red": RED, "blue": BLUE, "green": GREEN},
        )
        self.play(Transform(title, styled))
        self.wait(0.5)

        # Slant and weight via t2s (text-to-slant) and t2w (text-to-weight).
        emph = Text(
            "bold and italic",
            font_size=72,
            t2w={"bold": BOLD},
            t2s={"italic": ITALIC},
        )
        self.play(Transform(title, emph))
        self.wait(1)


class TexBasics(Scene):
    def construct(self):
        # LaTeX math. Use raw strings (r"...") so backslashes survive.
        formula = Tex(r"e^{i\pi} + 1 = 0", font_size=96)
        self.play(Write(formula))
        self.wait(1)

        # Inline color via t2c — works on substrings.
        colored = Tex(
            r"x^2 + y^2 = r^2",
            font_size=96,
            t2c={"x": BLUE, "y": RED, "r": YELLOW},
        )
        self.play(Transform(formula, colored))
        self.wait(1)


class TexIndexing(Scene):
    """
    Tex objects let you grab pieces of the rendered formula by substring.
    Useful for highlighting, isolating, or animating one term.
    """
    def construct(self):
        eq = Tex(r"a^2 + b^2 = c^2", font_size=120)
        self.play(Write(eq))
        self.wait(0.5)

        # Pulse just the c^2 part.
        self.play(Indicate(eq[r"c^2"], color=YELLOW, scale_factor=1.5))
        self.wait(0.3)

        # Color the a^2 part by directly setting it.
        self.play(eq[r"a^2"].animate.set_color(RED))
        self.play(eq[r"b^2"].animate.set_color(BLUE))
        self.wait(1)
