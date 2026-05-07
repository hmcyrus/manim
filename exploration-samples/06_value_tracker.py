"""
06 - ValueTracker and Updaters
==============================

The pattern that unlocks really fluid animations:

  1. Make a ValueTracker holding a number.
  2. Bind one or more mobjects to it via updaters or always_redraw.
  3. Animate the tracker. Everything bound to it moves in sync.

Run:
    manimgl exploration-samples/06_value_tracker.py NumberCounter -l
    manimgl exploration-samples/06_value_tracker.py CircleRadiusGrows -l
    manimgl exploration-samples/06_value_tracker.py AlwaysRedrawDemo -l
"""

from manimlib import *
import numpy as np


class NumberCounter(Scene):
    # Animate a number ticking from 0 to 100.
    def construct(self):
        tracker = ValueTracker(0)
        number = DecimalNumber(0, num_decimal_places=1, font_size=120)

        # f_always: call number.set_value(tracker.get_value()) each frame.
        # The magic is passing tracker.get_value (without parens) — Manim
        # calls it for us each frame.
        number.f_always.set_value(tracker.get_value)

        self.add(number)
        self.play(tracker.animate.set_value(100), run_time=4)
        self.wait(1)


class CircleRadiusGrows(Scene):
    # A circle whose radius is bound to a tracker.
    def construct(self):
        r = ValueTracker(0.5)

        # always_redraw recreates the mobject from scratch each frame.
        # Use it when changing geometry, not just color or position.
        circle = always_redraw(lambda: Circle(radius=r.get_value(), color=BLUE))

        # A label that updates with the radius.
        label = DecimalNumber(0, num_decimal_places=2, font_size=48)
        label.f_always.set_value(r.get_value)
        label.always.next_to(circle, UP)         # call next_to(circle, UP) each frame

        self.add(circle, label)
        self.play(r.animate.set_value(3), run_time=3)
        self.play(r.animate.set_value(0.5), run_time=2)
        self.wait(1)


class AlwaysRedrawDemo(Scene):
    """
    A line whose endpoints follow two moving dots.
    Classic always_redraw use case.
    """
    def construct(self):
        a = Dot(color=RED).move_to(LEFT * 3)
        b = Dot(color=GREEN).move_to(RIGHT * 3)

        # Recreate the line each frame using a's and b's current positions.
        line = always_redraw(lambda: Line(a.get_center(), b.get_center(), color=YELLOW))

        self.add(a, b, line)
        self.play(a.animate.shift(UP * 2), b.animate.shift(DOWN * 2), run_time=2)
        self.play(a.animate.shift(RIGHT * 5), run_time=2)
        self.wait(1)
