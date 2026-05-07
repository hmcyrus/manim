"""
02 - A Tour of Common Animations
================================

The animations you'll reach for 90% of the time. Run any one:

    manimgl exploration-samples/02_common_animations.py FadeTour -l
    manimgl exploration-samples/02_common_animations.py CreateTour -l
    manimgl exploration-samples/02_common_animations.py TransformTour -l
    manimgl exploration-samples/02_common_animations.py IndicateTour -l

If you just run the file with no scene name, Manim asks which one to render.
"""

from manimlib import *


class FadeTour(Scene):
    # FadeIn / FadeOut / FadeTransform: visibility transitions.
    def construct(self):
        a = Circle(color=BLUE).shift(LEFT * 3)
        b = Square(color=GREEN)
        c = Triangle(color=RED).shift(RIGHT * 3)

        self.play(FadeIn(a))
        self.play(FadeIn(b, shift=UP))           # fade in while sliding down from above
        self.play(FadeIn(c, shift=LEFT * 0.5))   # fade in while sliding from the right
        self.wait(0.5)
        self.play(FadeOut(a), FadeOut(b), FadeOut(c))


class CreateTour(Scene):
    # ShowCreation, Write, DrawBorderThenFill: building things up.
    def construct(self):
        circle = Circle(color=BLUE).shift(LEFT * 3)
        word = Text("Hello", font_size=72)
        square = Square(fill_opacity=0.7, color=YELLOW).shift(RIGHT * 3)

        self.play(ShowCreation(circle))                  # traces the outline
        self.play(Write(word))                           # word-by-word reveal
        self.play(DrawBorderThenFill(square))            # outline first, then fill
        self.wait(1)


class TransformTour(Scene):
    # Transform: morph one mobject into another.
    def construct(self):
        circle = Circle(color=BLUE)
        square = Square(color=YELLOW)
        star = RegularPolygon(n=5, color=RED)

        self.play(ShowCreation(circle))
        self.play(Transform(circle, square))             # circle becomes square
        self.play(Transform(circle, star))               # square becomes star
        # Note: we keep referring to it as `circle` because Transform mutates
        # the original mobject. ReplacementTransform swaps references instead.
        self.wait(1)


class RotateAndScaleTour(Scene):
    # Rotate, scaling, and movement animations.
    def construct(self):
        sq = Square(color=YELLOW, side_length=2)
        self.add(sq)
        self.play(Rotate(sq, angle=PI))                  # half turn
        self.play(sq.animate.scale(0.5))                 # .animate syntax — see file 03
        self.play(sq.animate.shift(UP * 2))
        self.wait(0.5)


class IndicateTour(Scene):
    # Animations that point things out without permanently changing them.
    def construct(self):
        target = Text("Look here!", font_size=72)
        self.add(target)
        self.wait(0.3)
        self.play(Indicate(target))                      # quick pulse
        self.play(Flash(target.get_center()))            # burst of lines
        self.play(FlashAround(target))                   # rectangle sweep
        self.play(ApplyWave(target))                     # ripple distortion
        self.play(WiggleOutThenIn(target))               # wobble
        self.wait(0.5)
