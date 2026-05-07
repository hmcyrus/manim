"""
01 - Hello Scene
================

The smallest possible Manim animation. Covers:
  - what a Scene is
  - the construct() method
  - creating a mobject
  - playing a single animation
  - waiting

Run it:
    manimgl exploration-samples/01_hello_scene.py HelloScene -l

The -l flag means low quality (faster preview).
Drop -l for full quality, add -w to write to a file in videos/.
"""

from manimlib import *


class HelloScene(Scene):
    # Every animation lives inside a Scene subclass.
    # Manim calls construct() to figure out what to draw.

    def construct(self):
        # 1. Make a mobject (mathematical object).
        circle = Circle(color=BLUE, radius=2)

        # 2. Animate it onto the screen.
        #    ShowCreation traces the outline as if drawing with a pen.
        self.play(ShowCreation(circle))

        # 3. Pause for a beat so the viewer can see it.
        self.wait(1)

        # 4. Fade it out.
        self.play(FadeOut(circle))


class TwoShapes(Scene):
    # Multiple mobjects, two different intro animations.

    def construct(self):
        square = Square(color=YELLOW, side_length=2).shift(LEFT * 3)
        triangle = Triangle(color=RED).scale(1.5).shift(RIGHT * 3)

        # Play two animations at the same time by passing both to play().
        self.play(
            FadeIn(square),
            ShowCreation(triangle),
        )
        self.wait(1)

        # Remove without animation.
        self.remove(square, triangle)
