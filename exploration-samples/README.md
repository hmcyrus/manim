# Exploration Samples

A progression of small, single-concept scenes for getting started with ManimGL.
Each file is heavily commented and meant to be read top-to-bottom.

## How to run

From the repo root:

```bash
manimgl exploration-samples/01_hello_scene.py HelloScene -l
```

- `-l` = low quality (fast iteration). Drop it for full HD.
- `-w` = write the result to `videos/`.
- `-o` = open the file when it's done.
- No scene name? Manim lists the scenes in the file and asks you to pick.

## The progression

| # | File | Concept |
|---|---|---|
| 01 | `01_hello_scene.py` | A Scene, `construct()`, your first animation |
| 02 | `02_common_animations.py` | FadeIn, ShowCreation, Write, Transform, Indicate, Flash |
| 03 | `03_animate_syntax.py` | The `.animate` shortcut for any method call |
| 04 | `04_text_and_tex.py` | `Text` (system fonts) vs `Tex` (LaTeX); styling and indexing |
| 05 | `05_axes_and_graph.py` | `Axes`, `get_graph`, `c2p` — plotting a function |
| 06 | `06_value_tracker.py` | `ValueTracker` + updaters: bind everything to one number |
| 07 | `07_transform_matching.py` | `TransformMatchingStrings` — clean equation morphing |
| 08 | `08_grouping_and_arrange.py` | `VGroup`, `arrange`, `arrange_in_grid`, `LaggedStart` |
| 09 | `09_three_d_basics.py` | `ThreeDScene`, `Sphere`, parametric `Surface`, camera orbit |
| 10 | `10_putting_it_together.py` | A small scene combining axes, tracker, area, brace, readout |

## What to read after this

- `example_scenes.py` (in the repo root) — the official examples, more advanced.
- `KNOWLEDGE_BASE.md` — a map of the codebase, idioms, and what's stable vs experimental.
- `docs/source/getting_started/` — the official Sphinx docs.

## Tips

- Stick `self.embed()` anywhere inside `construct()` to drop into an IPython
  shell with the scene state loaded. Try expressions, see them rendered live.
- LaTeX is required for `Tex` and `TexText`. The first render of a given
  formula is slow because it shells out to LaTeX; subsequent renders use a cache.
- Use `-l` while iterating, `--hd` for the final cut.
