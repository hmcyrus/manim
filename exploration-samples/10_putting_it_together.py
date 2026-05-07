"""
10 - Putting It Together
========================

A small scene that uses several of the techniques from earlier files:
axes, a graph, a tracker-driven dot, a brace, and a value display.
This is roughly the structure of a real explanatory animation.

Run:
    manimgl exploration-samples/10_putting_it_together.py AreaUnderCurve -l
"""

from manimlib import *
import numpy as np


class AreaUnderCurve(Scene):
    """
    Show the area under y = x^2 from 0 to t, with t animated from 0 to 2.
    The shaded region grows, a brace tracks its width, and a number ticks up.
    """
    def construct(self):
        # 1. Coordinate system + curve.
        axes = Axes(
            x_range=(0, 2.5, 0.5),
            y_range=(0, 5, 1),
            width=10,
            height=6,
        )
        axes.add_coordinate_labels()
        graph = axes.get_graph(lambda x: x ** 2, color=YELLOW)
        graph_label = axes.get_graph_label(graph, "y = x^2")

        self.play(ShowCreation(axes), Write(graph_label))
        self.play(ShowCreation(graph))
        self.wait(0.5)

        # 2. ValueTracker for the upper bound t.
        t = ValueTracker(0.01)

        # 3. Shaded area, recomputed each frame.
        area = always_redraw(
            lambda: axes.get_riemann_rectangles(
                graph,
                x_range=(0, t.get_value()),
                dx=0.05,
                colors=(BLUE_E, BLUE),
                fill_opacity=0.6,
            )
        )

        # 4. A vertical line at x = t.
        v_line = always_redraw(
            lambda: DashedLine(
                axes.c2p(t.get_value(), 0),
                axes.c2p(t.get_value(), t.get_value() ** 2),
                color=WHITE,
            )
        )

        # 5. Numeric area readout: integral of x^2 from 0 to t = t^3 / 3.
        readout = VGroup(
            Tex(r"\text{Area} \approx", font_size=48),
            DecimalNumber(0, num_decimal_places=3, font_size=48),
        ).arrange(RIGHT).to_corner(UR)
        readout[1].f_always.set_value(lambda: t.get_value() ** 3 / 3)

        self.add(area, v_line, readout)

        # 6. Animate t from 0 to 2.
        self.play(t.animate.set_value(2), run_time=5)
        self.wait(1)

        # 7. A flourish: pulse the readout to underline the result.
        self.play(Indicate(readout[1], color=YELLOW, scale_factor=1.3))
        self.wait(1)
