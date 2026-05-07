# ManimGL Knowledge Base

A working guide to this fork of [3b1b/manim](https://github.com/3b1b/manim) (ManimGL v1.7.2). Built for someone who wants to make cool animations and actually understand the engine underneath.

---

## 1. What this repo is (and isn't)

**ManimGL** is the original Manim by Grant Sanderson (3Blue1Brown). It renders animations in real-time using OpenGL via `moderngl`, which is what the **GL** stands for. This is a different project from **ManimCommunity** (`manim` on PyPI), which forked off in 2020 with different goals (stability, tests, friendlier onboarding).

| | ManimGL (this repo) | ManimCommunity |
|---|---|---|
| PyPI name | `manimgl` | `manim` |
| Renderer | OpenGL (real-time) | Cairo → ffmpeg |
| Live preview | Yes, with mouse/keyboard interaction | Limited |
| API stability | Changes when Grant needs it to | Stable, versioned |
| Best for | 3b1b-style videos, live exploration, GPU effects | Production pipelines, teaching |

Don't mix instructions between the two — install commands, imports, and class names diverge.

---

## 2. Getting started

```bash
pip install -e .                                     # editable install from this checkout
manimgl example_scenes.py OpeningManimExample        # render a scene
manimgl example_scenes.py OpeningManimExample -w     # write to file (videos/)
manimgl example_scenes.py OpeningManimExample -ws    # write + skip animations (final frame only)
manimgl example_scenes.py OpeningManimExample -l     # low quality (fast iteration, 480p)
manimgl                                              # blank scene with IPython shell
```

System deps: **FFmpeg**, **OpenGL**, **LaTeX** (optional, for `Tex` / `TexText`), **Pango** (Linux, for `Text`).

Both `manimgl` and `manim-render` are entry points to `manimlib.__main__:main` (see `setup.cfg`).

### CLI flags worth knowing

| Flag | Meaning |
|---|---|
| `-w` | Write video to disk |
| `-s` | Skip animations, render only the final frame |
| `-o` | Open the rendered video when done |
| `-p` | Preview in a window |
| `-f` | Full screen |
| `-l` / `-m` / `--hd` / `--uhd` | 480p / 720p / 1080p / 4K |
| `-n N` | Start at animation N (skips earlier ones) |
| `-e LINE` | Insert `self.embed()` at line N — instant IPython REPL inside the scene |
| `--config_file path.yml` | Custom config |

---

## 3. Repo layout

```
manim/
├── manimlib/                # the engine
│   ├── __main__.py          # CLI entry point
│   ├── extract_scene.py     # loads scene module, picks scenes, computes frame counts
│   ├── config.py            # CLI parser + config loader
│   ├── default_config.yml   # all defaults (resolution, colors, key bindings, …)
│   ├── constants.py         # UP, DOWN, ORIGIN, PI, color constants, …
│   ├── tex_templates.yml    # LaTeX preambles
│   ├── window.py            # ModernGL window + input handling
│   ├── shader_wrapper.py    # compiles GLSL programs, manages uniforms/textures
│   ├── module_loader.py     # dynamic import of user scene files
│   ├── logger.py
│   ├── typing.py
│   ├── animation/           # Animation classes
│   ├── camera/              # Camera + CameraFrame
│   ├── event_handler/       # mouse/keyboard event bus
│   ├── mobject/             # mathematical objects (everything you draw)
│   ├── scene/               # Scene, InteractiveScene, ThreeDScene, file writer
│   ├── shaders/             # GLSL programs (.glsl files)
│   └── utils/               # bezier, color, space ops, rate functions, tex, …
├── docs/                    # Sphinx documentation
├── example_scenes.py        # 12 example scenes — read this first
├── logo/
├── setup.cfg                # version, deps, entry points
└── README.md
```

---

## 4. The four core abstractions

Everything in Manim composes from these four:

### Mobject (Mathematical Object)
The base class for anything you draw. Holds points (numpy array), color, opacity, submobjects (children), and updaters (per-frame callbacks). `manimlib/mobject/mobject.py`.

- **VMobject** — vectorized mobject. The most common kind: 2D vector graphics with stroke + fill, built from quadratic Bezier curves. `manimlib/mobject/types/vectorized_mobject.py`.
- **VGroup** — a group of VMobjects. Use `arrange()`, indexing, `.scale()`, etc.
- **Surface / DotCloud / ImageMobject / PointCloudMobject** — non-vector mobject types in `manimlib/mobject/types/`.

### Animation
Wraps a Mobject and describes how it changes over `run_time` seconds. Base class in `manimlib/animation/animation.py`. Key params:
- `run_time` (default 1.0)
- `rate_func` (easing, default `smooth`)
- `lag_ratio` (stagger across submobjects, 0 = simultaneous, 1 = strict sequence)
- `remover` (auto-remove from scene on finish)

### Scene
The container that holds mobjects, plays animations, and gets rendered. You override `construct()`. `manimlib/scene/scene.py`.

### Camera + CameraFrame
The OpenGL rendering context (`Camera`) and the viewing transform (`CameraFrame`: position, orientation, FOV). `manimlib/camera/`. `self.camera.frame` is what you animate to pan/zoom/rotate.

---

## 5. `manimlib/` — module-by-module map

### `animation/`

| Module | Classes |
|---|---|
| `animation.py` | `Animation` (base) |
| `composition.py` | `AnimationGroup`, `Succession`, `LaggedStart`, `LaggedStartMap` |
| `creation.py` | `ShowCreation`, `Uncreate`, `DrawBorderThenFill`, `Write`, `ShowIncreasingSubsets` |
| `fading.py` | `FadeIn`, `FadeOut`, `FadeTransform`, `FadeTransformPieces`, `VFadeIn`, `VFadeOut` |
| `growing.py` | `GrowFromPoint`, `GrowFromCenter`, `GrowFromEdge`, `GrowArrow` |
| `indication.py` | `FocusOn`, `Indicate`, `Flash`, `CircleIndicate`, `ShowPassingFlash`, `FlashAround`, `ApplyWave`, `WiggleOutThenIn`, `TurnInsideOut`, `FlashyFadeIn` |
| `movement.py` | `Homotopy`, `MoveAlongPath`, `PhaseFlow`, `ComplexHomotopy` |
| `numbers.py` | `ChangingDecimal`, `ChangeDecimalToValue` |
| `rotation.py` | `Rotate`, `Rotating` |
| `transform.py` | `Transform`, `ReplacementTransform`, `TransformFromCopy`, `ApplyMethod`, `ApplyFunction`, `ApplyMatrix`, `ApplyComplexFunction`, `Restore`, `CyclicReplace`, `Swap` |
| `transform_matching_parts.py` | `TransformMatchingShapes`, `TransformMatchingStrings`, `TransformMatchingTex` |
| `update.py` | `UpdateFromFunc`, `UpdateFromAlphaFunc`, `MaintainPositionRelativeTo` |
| `specialized.py` | `Broadcast` |

### `mobject/`

| Module | What's in it |
|---|---|
| `mobject.py` | `Mobject` base class. Family management, updaters, transforms, color/opacity, GPU data. |
| `geometry.py` | `Arc`, `Circle`, `Dot`, `Ellipse`, `Line`, `DashedLine`, `Arrow`, `Vector`, `Polygon`, `RegularPolygon`, `Triangle`, `Rectangle`, `Square`, `RoundedRectangle`, `CubicBezier`, `Annulus`, `Sector`, `ArrowTip`, … |
| `coordinate_systems.py` | `Axes`, `ThreeDAxes`, `NumberPlane`, `ComplexPlane` (with `c2p`, `p2c`, `get_graph`) |
| `three_dimensions.py` | `Sphere`, `Torus`, `Cylinder`, `Cone`, `Cube`, `Prism`, `Dodecahedron`, `SurfaceMesh`, `Prismify` |
| `numbers.py` | `DecimalNumber`, `Integer` |
| `matrix.py` | `Matrix`, `IntegerMatrix` |
| `functions.py` | `ParametricCurve`, `FunctionGraph`, `ImplicitFunctionGraph` |
| `vector_field.py` | `VectorField`, `StreamLines`, `AnimatedStreamLines` |
| `value_tracker.py` | `ValueTracker` (animatable scalar) |
| `changing.py` | `TracedPath`, `TracingTail` |
| `boolean_ops.py` | `Union`, `Difference`, `Intersection`, `Exclusion` (skia-pathops) |
| `mobject_update_utils.py` | `always_redraw`, `always`, `f_always`, `cycle_animation`, `turn_animation_into_updater` |
| `interactive.py` | `Button`, `Checkbox`, `LinearNumberSlider`, `ColorSliders`, `Textbox`, `ControlPanel`, `MotionMobject` |
| `shape_matchers.py` | `BackgroundRectangle`, `SurroundingRectangle`, `Cross`, `Underline` |
| `frame.py` | `FullScreenFadeRectangle`, `PictureInPictureFrame` |
| `probability.py` | `BarChart`, `SampleSpace` |
| `types/vectorized_mobject.py` | `VMobject`, `VGroup`, `VHighlight`, `DashedVMobject`, `CurvesAsSubmobjects` |
| `types/dot_cloud.py` | `DotCloud`, `TrueDot`, `GlowDot`, `GlowDots` |
| `types/surface.py` | `Surface`, `ParametricSurface`, `SGroup`, `TexturedSurface` |
| `types/image_mobject.py` | `ImageMobject` |
| `types/point_cloud_mobject.py` | `PointCloudMobject` |
| `svg/svg_mobject.py` | `SVGMobject` |
| `svg/tex_mobject.py` | `Tex`, `TexText` (LaTeX rendering) |
| `svg/text_mobject.py` | `Text`, `MarkupText`, `Code` (system fonts via Pango) |
| `svg/brace.py` | `Brace`, `BraceBetweenPoints`, `UnderBrace`, `OverBrace`, `BraceText` |
| `svg/drawings.py` | Pre-built complex objects: `Lightbulb`, `Speedometer`, `Laptop`, `VideoIcon`, `Clock`, `SpeechBubble`, `ThoughtBubble`, `Piano`, `Dartboard` |

### `scene/`

| Module | Classes |
|---|---|
| `scene.py` | `Scene` (base, line 1), `ThreeDScene` (line 930) |
| `interactive_scene.py` | `InteractiveScene` (line 66) — adds live mouse/keyboard editing |
| `scene_file_writer.py` | `SceneFileWriter` — drives ffmpeg, manages partial movie files |
| `scene_embed.py` | `InteractiveSceneEmbed`, `CheckpointManager` — IPython embedding + checkpoint/paste |

### `camera/`

| Module | Classes |
|---|---|
| `camera.py` | `Camera` — ModernGL context, FBO, multisampling |
| `camera_frame.py` | `CameraFrame` — viewing transform; this is what you animate for pan/zoom/rotation |

### `event_handler/`

The event bus that powers `InteractiveScene` and any custom mouse/keyboard handlers on mobjects. `EVENT_DISPATCHER` is a singleton.

### `utils/` — pick from these constantly

| Module | Highlights |
|---|---|
| `bezier.py` | `bezier`, `interpolate`, `inverse_interpolate`, `find_intersection`, `quadratic_bezier_points_for_arc`, `partial_quadratic_bezier_points` |
| `color.py` | `color_to_rgb`, `rgb_to_hex`, `color_gradient`, `get_colormap_list` |
| `space_ops.py` | `normalize`, `get_norm`, `angle_of_vector`, `rotation_matrix`, `cross2d`, `earclip_triangulation`, `compass_directions` |
| `rate_functions.py` | `smooth`, `linear`, `there_and_back`, `wiggle`, `rush_from`, `rush_into`, `slow_into`, full set of `ease_in_*` / `ease_out_*` (sine, quad, cubic, quart, quint, expo, circ, back, elastic, bounce), `squish_rate_func`, `exponential_decay` |
| `paths.py` | `straight_path`, `clockwise_path`, `counterclockwise_path` (use as `path_func` on Transform) |
| `iterables.py` | `batch_by_property`, `resize_array`, `resize_with_interpolation`, `listify` |
| `tex.py`, `tex_file_writing.py` | LaTeX → DVI → SVG pipeline, hash-based caching |
| `shaders.py` | `get_shader_code_from_file`, `set_program_uniform`, `image_path_to_texture`, `get_colormap_code` |
| `simple_functions.py` | `clip`, `fdiv` |
| `dict_ops.py` | `merge_dicts_recursively` |
| `family_ops.py`, `directories.py`, `file_ops.py`, `images.py`, `sounds.py`, `cache.py`, `debug.py` | Misc plumbing |

---

## 6. The shader layer (what makes ManimGL fast)

ManimGL renders every frame on the GPU through GLSL. Every Mobject has a `shader_folder` field that points to a directory under `manimlib/shaders/`. `ShaderWrapper` (in `manimlib/shader_wrapper.py`) compiles the programs and feeds them numpy data per frame.

| Shader folder | Purpose |
|---|---|
| `quadratic_bezier/stroke/` | Stroked vector paths (lines, joins, caps). The geometry shader does the heavy lifting. |
| `quadratic_bezier/fill/` | Filled vector paths. Uses earclip triangulation (mapbox-earcut). |
| `quadratic_bezier/depth/` | Z-buffer pass for layered shapes. |
| `surface/` | Smooth 3D mesh with per-vertex normals + lighting. |
| `textured_surface/` | UV-mapped textures on surfaces. |
| `true_dot/` | GPU-accelerated round dots — much faster than drawing actual circles. |
| `image/` | Raster image rendering. |
| `mandelbrot_fractal/`, `newton_fractal/` | Real-time fractal computation in the fragment shader. |
| `inserts/` | Reusable GLSL fragments: `complex_functions.glsl`, `get_unit_normal.glsl`, `emit_gl_Position.glsl`, `finalize_color.glsl`, `get_xyz_to_uv.glsl`. |
| `simple_vert.glsl` | Plain pass-through vertex shader. |

Shaders support **code replacement** — `ShaderWrapper.replace_code(old, new)` lets you swap in custom GLSL without rewriting the whole shader. This is how `ComplexPlane.apply_complex_function` works on `Surface` — it injects a different complex function into the fragment shader. Recent change (PR #2424) makes replacements aware of program type (vert vs geom vs frag).

---

## 7. Configuration

`manimlib/default_config.yml` is the source of truth. Override it via:
- `--config_file my_config.yml` on the CLI, or
- a `custom_config.yml` in the working directory, or
- environment-specific overrides via `manimlib.config`.

Sections:
- `directories` — output paths (`videos/`, `latex_cache/`, `raster_images/`)
- `window` — position, size, monitor, full screen
- `camera` — resolution `(1920, 1080)`, `background_color`, `fps: 30`, `background_opacity`
- `file_writer` — ffmpeg binary, codec, pixel format, saturation, gamma
- `scene` — progress bars, `default_wait_time`, `preview_while_skipping`
- `vmobject` / `mobject` — default stroke/fill colors and widths
- `key_bindings` — `select`, `grab`, `x_grab`, `y_grab`, `z_grab`, `color`, `information`, `cursor`, `unselect`, `resize`

`manimlib/constants.py` exports the constants you'll use in code: directions (`UP`, `DOWN`, `LEFT`, `RIGHT`, `IN`, `OUT`, `UL`, `UR`, `DL`, `DR`, `ORIGIN`), `PI`, `TAU`, `DEGREES`, color names (`BLUE`, `RED`, `YELLOW`, `GREEN`, `TEAL`, `PURPLE`, `MAROON`, `GOLD`, `GREY`, `WHITE`, `BLACK`, …), and frame dimensions (`FRAME_WIDTH`, `FRAME_HEIGHT`).

---

## 8. The 12 example scenes (`example_scenes.py`)

Read these in order. Each is short and demonstrates one concept.

| Line | Scene | Demonstrates |
|---|---|---|
| 12 | `OpeningManimExample` | Linear transforms on a `NumberPlane`, then a complex-function map (z²) |
| 71 | `AnimatingMethods` | The `.animate` syntax — call any mobject method as an animation |
| 115 | `TextExample` | `Text` vs `TexText`; per-substring styling via `t2c`, `t2f`, `t2s`, `t2w` |
| 156 | `TexTransformExample` | LaTeX rendering; `TransformMatchingStrings` / `TransformMatchingShapes` for smart equation morphing |
| 228 | `TexIndexing` | Indexing `Tex` objects by substring (e.g. `tex[r"\pi"]`), regex, `isolate=` |
| 281 | `UpdatersExample` | `always_redraw`, `add_updater`, `.always`, `f_always` for live binding |
| 341 | `CoordinateSystemExample` | `Axes`, `c2p` / `p2c`, axis labels, decorations |
| 420 | `GraphExample` | Function graphs, parametric curves, discontinuities |
| 498 | `TexAndNumbersExample` | Animating `DecimalNumber` alongside Tex |
| 566 | `SurfaceExample(ThreeDScene)` | 3D parametric surfaces, lighting, camera moves |
| 648 | `InteractiveDevelopment` | `self.embed()` — drop into IPython mid-scene |
| 694 | `ControlsExample` | Live UI: buttons, sliders, checkboxes from `mobject/interactive.py` |

---

## 9. Idioms and patterns

### The `.animate` syntax (the most useful trick)
Any method call chained off `.animate` becomes a `Transform` animation:
```python
self.play(square.animate.shift(RIGHT).set_color(BLUE).rotate(PI/4))
```
This is just sugar for: copy the mobject, apply the methods, `Transform` original → copy.

### Composition
```python
self.play(
    Succession(FadeIn(a), FadeOut(b)),                # sequential
    AnimationGroup(GrowFromCenter(c), Rotate(d)),      # simultaneous
    LaggedStart(*[FadeIn(x) for x in group], lag_ratio=0.1),  # staggered
)
```

### Updaters (live bindings each frame)
Three flavors, increasing in convenience:
```python
# 1. Raw updater — full control
mob.add_updater(lambda m: m.next_to(other, UP))

# 2. .always / f_always — bind a method call
label.always.next_to(brace, UP)                # call next_to(brace, UP) each frame
number.f_always.set_value(square.get_width)    # set_value(square.get_width()) each frame

# 3. always_redraw — recreate the mobject each frame
brace = always_redraw(Brace, square, UP)
```

### `ValueTracker` — animate a number, drive everything else off it
```python
t = ValueTracker(0)
dot.add_updater(lambda d: d.move_to(axes.c2p(t.get_value(), np.sin(t.get_value()))))
self.add(dot)
self.play(t.animate.set_value(2 * PI), run_time=4)
```

### LaTeX styling and indexing
```python
eq = Tex(r"x^2 + y^2 = r^2", t2c={"x": BLUE, "y": RED, "r": YELLOW}, font_size=72)
self.play(Indicate(eq[r"x^2"]))   # substring indexing
```
Caveat: substring indexing breaks if LaTeX draws glyphs in a different order than the source. When that happens, use `isolate=[...]` to force the substring to be its own submobject.

### Transform matching
```python
# Reuse glyphs that haven't changed; cleanly morph the rest
self.play(TransformMatchingStrings(eq1, eq2, path_arc=PI/2))
self.play(TransformMatchingShapes(blob1, blob2))   # geometry-based
```

### Coordinate systems
```python
axes = Axes(x_range=(-3, 3, 1), y_range=(-2, 2, 0.5), height=6, width=10)
graph = axes.get_graph(lambda x: np.sin(x), color=BLUE)
label = axes.get_graph_label(graph, "\\sin(x)")
dot = Dot(axes.c2p(1, np.sin(1)))   # data coords → scene point
x, y = axes.p2c(dot.get_center())   # scene point → data coords
```

### 3D
```python
class MyScene(ThreeDScene):
    def construct(self):
        sphere = Sphere(radius=1.5)
        self.play(ShowCreation(sphere))
        self.play(self.camera.frame.animate.set_euler_angles(theta=PI/4, phi=PI/3),
                  run_time=3)
```
Pan/zoom/rotate is done by animating `self.camera.frame`, not the scene.

### Live exploration
Drop `self.embed()` anywhere in `construct()` and you get an IPython REPL with the scene state loaded. Type expressions, see them rendered immediately. Combine with `manimgl -e LINE_NUMBER` to inject `embed()` without editing the file.

### `InteractiveScene` shortcuts
When your scene subclasses `InteractiveScene` (or you call `self.embed()`), these keys work in the preview window:
- `ctrl` — select; click to add to selection
- `g` — grab (move with mouse)
- `h` / `v` — grab constrained to horizontal / vertical
- `t` — resize
- `c` — color picker
- `i` — info on selected
- `cmd+c` / `cmd+v` — copy/paste mobject definitions to/from clipboard

---

## 10. What's stable vs. experimental

### Stable / production-ready
- **All animation classes** (`animation/`) — these are what 3b1b uses daily.
- **VMobject + geometry** — rock solid.
- **`Tex` / `Text` / `MarkupText`** rendering, `TransformMatchingStrings`.
- **`Axes`, `NumberPlane`, `ComplexPlane`** and their `c2p` / `p2c` / `get_graph` API.
- **Updaters and `ValueTracker`**.
- **3D primitives** (`Sphere`, `Torus`, `Cube`, etc.) and `ParametricSurface`.
- **The shader pipeline for stroke/fill/surface** — battle-tested across hundreds of videos.

### Use with awareness — recently churning
Recent commits (last 50) touched these areas — they work but might shift:
- **Shader code replacement** is now program-type aware (PR #2424).
- **Multiple clip planes** for 3D scenes (PR #2437).
- **`TracedPath` / traced points** had a shared-reference bug fix (#2426).
- **Stroke arrow tip preservation** (#2419-ish).
- **LaTeX cache directory** behavior changed.
- **Text scale factor** is now dynamically calculated rather than a hard constant (#2423).
- **`checkpoint_paste`** dedents copied code (#2432).
- **SVG path parsing** efficiency improvements.

### Experimental / WIP / known-rough
- **`InteractiveScene`** — the file itself contains a comment (~line 63): *"a lot of the functionality here is still buggy and very much a work in progress."* Use it for exploration, not production.
- **Resize key binding** — `TODO` in `interactive_scene.py:47`.
- **Surface event handling** — `TODO` in `mobject/types/surface.py`.
- **Auto discontinuity detection** in `FunctionGraph` — `TODO` in `mobject/functions.py`.
- **`SampleSpaceScene`** in `mobject/probability.py` — flagged for review.
- **`drawings.resize_to_content()`** — not implemented.
- **`old_tex_mobject.py`** — legacy, deprecated, kept for compatibility.
- **Tex substring indexing** — fragile when LaTeX reorders glyph rendering. Use `isolate=` as a workaround.

---

## 11. A practical workflow for building cool stuff

1. **Start a scratch file.** Copy `example_scenes.py` to `my_scenes.py`. Pick the example closest to what you want and modify it.
2. **Iterate fast with `-l` and `-p`.** Low quality + window preview means each render is ~1 second.
3. **Use `self.embed()` liberally.** When you're not sure how a transform will look, drop into IPython mid-scene and try expressions until it works.
4. **`InteractiveScene` for choreography.** Position objects with the mouse, then `cmd+c` to copy the resulting code back into your script.
5. **`TransformMatchingStrings` is your friend** for equation manipulation videos.
6. **Bind everything with updaters or `ValueTracker`** rather than playing many small animations. One `ValueTracker.animate.set_value(...)` driving five mobjects looks much better than five overlapping `Transform`s.
7. **For 3D, animate `self.camera.frame`** — never move the world to fake camera motion.
8. **Render the final cut at full quality with `-w --hd`** (or `--uhd` for 4K). Add `-o` to auto-open.
9. **Check `docs/source/getting_started/` and `docs/source/documentation/`** when you're stuck — Sphinx-built reference is at https://3b1b.github.io/manim/.

### Where ideas come from
- Grant's video repo: https://github.com/3b1b/videos — every 3b1b video's source code, a goldmine of patterns.
- The `mobject/svg/drawings.py` file — unusual pre-built objects (lightbulbs, speech bubbles, pianos) you can crib from.
- The fractal shaders (`shaders/mandelbrot_fractal/`, `shaders/newton_fractal/`) — a starting point if you want to add your own GPU effects.

---

## 12. Quick reference: imports

The conventional star import surfaces almost everything:
```python
from manimlib import *
import numpy as np
```
That gives you every Mobject, Animation, constant, color, and rate function. If you prefer explicit imports, follow the module map in section 5.

---

## 13. File-pointer cheat sheet

When you want to know how something works, go straight to:

| Question | File |
|---|---|
| How does `self.play()` work? | `manimlib/scene/scene.py` |
| How is an Animation interpolated? | `manimlib/animation/animation.py` (`begin`, `interpolate`, `finish`) |
| How are Bezier curves drawn on the GPU? | `manimlib/shaders/quadratic_bezier/stroke/*.glsl` + `mobject/types/vectorized_mobject.py` |
| How is LaTeX rendered? | `manimlib/utils/tex_file_writing.py` + `mobject/svg/tex_mobject.py` |
| How does `.animate` work? | `manimlib/mobject/mobject.py` (search for `_AnimationBuilder`) |
| What flags does the CLI take? | `manimlib/config.py` (`parse_cli`) |
| How does `embed()` integrate IPython? | `manimlib/scene/scene_embed.py` |
| How do interactive key bindings work? | `manimlib/scene/interactive_scene.py` + `event_handler/` |
| What rate functions exist? | `manimlib/utils/rate_functions.py` |
| What constants are exported? | `manimlib/constants.py` |
