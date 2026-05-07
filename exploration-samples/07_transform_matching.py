"""
07 - Transforming Equations
===========================

When two equations share substrings, TransformMatchingStrings reuses the
matching glyphs and only morphs the bits that actually changed. The result
looks much nicer than a generic Transform.

Run:
    manimgl exploration-samples/07_transform_matching.py EquationMorph -l
    manimgl exploration-samples/07_transform_matching.py StepByStepAlgebra -l
"""

from manimlib import *


class EquationMorph(Scene):
    def construct(self):
        eq1 = Tex(r"a^2 + b^2 = c^2", font_size=120)
        eq2 = Tex(r"c^2 - b^2 = a^2", font_size=120)

        self.play(Write(eq1))
        self.wait(0.5)
        # path_arc makes the matching pieces curve to their new spots.
        self.play(TransformMatchingStrings(eq1, eq2, path_arc=PI / 2))
        self.wait(1)


class StepByStepAlgebra(Scene):
    """A short algebraic derivation, one step at a time."""
    def construct(self):
        steps = [
            Tex(r"2x + 3 = 11", font_size=96),
            Tex(r"2x = 11 - 3", font_size=96),
            Tex(r"2x = 8", font_size=96),
            Tex(r"x = 4", font_size=96),
        ]

        self.play(Write(steps[0]))
        self.wait(0.5)
        for prev, nxt in zip(steps, steps[1:]):
            self.play(TransformMatchingStrings(prev, nxt, path_arc=PI / 4))
            self.wait(0.5)
        self.wait(1)
