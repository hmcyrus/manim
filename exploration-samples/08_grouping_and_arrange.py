"""
08 - VGroup and arrange
=======================

VGroup bundles several mobjects so you can move/scale/animate them as a unit.
.arrange(...) lays them out in a row/column with consistent spacing.

Run:
    manimgl exploration-samples/08_grouping_and_arrange.py ArrangeDemo -l
    manimgl exploration-samples/08_grouping_and_arrange.py GridOfDots -l
"""

from manimlib import *


class ArrangeDemo(Scene):
    def construct(self):
        # Make some shapes...
        shapes = VGroup(
            Circle(color=BLUE),
            Square(color=YELLOW),
            Triangle(color=RED),
            RegularPolygon(n=6, color=GREEN),
            RegularPolygon(n=5, color=PURPLE),
        )
        # ...then arrange them in a row, spaced 0.5 apart.
        shapes.arrange(RIGHT, buff=0.5)

        self.play(LaggedStart(*[FadeIn(s, shift=UP) for s in shapes], lag_ratio=0.2))
        self.wait(0.5)

        # Operate on the group as one mobject.
        self.play(shapes.animate.scale(0.5).shift(UP * 2))
        self.play(shapes.animate.arrange(DOWN, buff=0.3).shift(LEFT * 4))
        self.wait(1)


class GridOfDots(Scene):
    """A 6x6 grid of dots, animated in with a stagger."""
    def construct(self):
        dots = VGroup(*[Dot() for _ in range(36)])
        dots.arrange_in_grid(n_rows=6, n_cols=6, buff=0.5)
        # Color each dot by its position in the group.
        dots.set_color_by_gradient(BLUE, YELLOW, RED)

        # LaggedStart staggers a list of animations.
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.05))

        # Spin the whole grid.
        self.play(dots.animate.rotate(PI / 4).scale(0.7))
        self.wait(1)
