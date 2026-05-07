"""
05 - Axes and Function Graphs
=============================

How to plot a function and decorate it. Covers:
  - building Axes
  - get_graph for plotting
  - c2p ("coords to point") for placing things in data coordinates
  - moving a dot along the graph

Run:
    manimgl exploration-samples/05_axes_and_graph.py SineGraph -l
    manimgl exploration-samples/05_axes_and_graph.py DotOnGraph -l
"""

from manimlib import *
import numpy as np


class SineGraph(Scene):
    def construct(self):
        # Axes(...) is your standard 2D coordinate system.
        # x_range / y_range are (min, max, step).
        axes = Axes(
            x_range=(-PI, PI, PI / 2),
            y_range=(-1.5, 1.5, 0.5),
            width=12,
            height=6,
        )
        axes.add_coordinate_labels()

        self.play(ShowCreation(axes))

        # get_graph takes a Python function x -> y and returns a VMobject.
        graph = axes.get_graph(lambda x: np.sin(x), color=BLUE)
        label = axes.get_graph_label(graph, "\\sin(x)")

        self.play(ShowCreation(graph), Write(label))
        self.wait(1)


class DotOnGraph(Scene):
    """
    A dot that walks along a parabola, dragging an x-axis tick with it.
    Demonstrates c2p (coords -> screen point) and updaters.
    """
    def construct(self):
        axes = Axes(x_range=(-3, 3, 1), y_range=(0, 9, 1), width=10, height=6)
        axes.add_coordinate_labels()
        graph = axes.get_graph(lambda x: x ** 2, color=YELLOW)
        self.add(axes, graph)

        # ValueTracker holds a number we'll animate. See file 06 for more.
        x = ValueTracker(-2.5)

        # A dot that lives at (x, x^2). Updater = run this function each frame.
        dot = Dot(color=RED)
        dot.add_updater(lambda m: m.move_to(axes.c2p(x.get_value(), x.get_value() ** 2)))
        self.add(dot)

        # A dashed vertical line from x-axis up to the dot.
        v_line = always_redraw(
            lambda: DashedLine(
                axes.c2p(x.get_value(), 0),
                axes.c2p(x.get_value(), x.get_value() ** 2),
                color=GREY,
            )
        )
        self.add(v_line)

        # Animate the underlying value; everything bound to it follows.
        self.play(x.animate.set_value(2.5), run_time=4)
        self.wait(1)
