"""
03 - The .animate Syntax
========================

The single most useful trick in Manim. Any method you can call on a mobject,
you can call on `mobject.animate.method(...)` to turn it into an animation.

    mobject.set_color(RED)             # instant change
    mobject.animate.set_color(RED)     # animated change, wrap in self.play()

Run:
    manimgl exploration-samples/03_animate_syntax.py AnimateSyntaxDemo -l
"""

from manimlib import *


class AnimateSyntaxDemo(Scene):
    def construct(self):
        sq = Square(color=BLUE, side_length=2)
        self.add(sq)

        # One animated method call.
        self.play(sq.animate.shift(RIGHT * 2))

        # Chain multiple methods — they all happen in the same animation.
        self.play(sq.animate.shift(LEFT * 4).set_color(RED).rotate(PI / 4))

        # Each .animate.* is its own animation, so play() takes multiple of them.
        circle = Circle(color=YELLOW).shift(UP * 2)
        triangle = Triangle(color=GREEN).shift(DOWN * 2)
        self.add(circle, triangle)
        self.play(
            circle.animate.shift(RIGHT * 3),
            triangle.animate.shift(LEFT * 3).scale(1.5),
            sq.animate.set_fill(PURPLE, opacity=0.7),
        )
        self.wait(1)


class AnimateVsTransform(Scene):
    """
    Underneath, .animate creates a Transform from the original to a copy with
    the methods applied. So these two are equivalent:
    """
    def construct(self):
        sq1 = Square(color=BLUE).shift(LEFT * 3)
        sq2 = Square(color=BLUE).shift(RIGHT * 3)
        self.add(sq1, sq2)
        self.wait(0.5)

        # Way 1: .animate
        self.play(sq1.animate.set_color(RED).scale(1.5))

        # Way 2: explicit Transform — copy, modify the copy, morph original to it
        target = sq2.copy().set_color(RED).scale(1.5)
        self.play(Transform(sq2, target))

        self.wait(1)
