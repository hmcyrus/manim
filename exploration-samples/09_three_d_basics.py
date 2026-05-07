"""
09 - 3D Basics
==============

Subclass ThreeDScene and animate self.camera.frame to move the camera.
You don't move the world — you orbit it.

Run:
    manimgl exploration-samples/09_three_d_basics.py SpinningSphere -l
    manimgl exploration-samples/09_three_d_basics.py ParametricSurface -l
"""

from manimlib import *
import numpy as np


class SpinningSphere(ThreeDScene):
    def construct(self):
        sphere = Sphere(radius=1.5, color=BLUE)
        axes = ThreeDAxes()

        # Tilt the camera so we can see depth.
        self.camera.frame.set_euler_angles(theta=-30 * DEGREES, phi=70 * DEGREES)

        self.play(ShowCreation(axes))
        self.play(FadeIn(sphere))

        # Orbit by rotating the camera frame, not the sphere.
        self.play(
            self.camera.frame.animate.set_euler_angles(theta=150 * DEGREES, phi=70 * DEGREES),
            run_time=4,
        )
        self.wait(1)


class ParametricSurface(ThreeDScene):
    """A wavy sheet defined as z = f(x, y)."""
    def construct(self):
        axes = ThreeDAxes()

        surface = Surface(
            uv_func=lambda u, v: [u, v, 0.5 * np.sin(u) * np.cos(v)],
            u_range=(-3, 3),
            v_range=(-3, 3),
            color=BLUE,
        )

        self.camera.frame.set_euler_angles(theta=-30 * DEGREES, phi=60 * DEGREES)

        self.play(ShowCreation(axes))
        self.play(ShowCreation(surface))

        # Slowly orbit the camera.
        self.play(
            self.camera.frame.animate.increment_theta(2 * PI),
            run_time=6,
        )
        self.wait(1)
