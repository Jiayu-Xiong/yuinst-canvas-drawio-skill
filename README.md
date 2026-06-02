# YuInst Canvas Draw.io Skill

`yuinst-canvas-drawio-skill` is a Codex skill for reconstructing and creating editable scientific figures with a grid-first draw.io workflow.

The skill treats draw.io as the editable canvas for layout, labels, equations, panel badges, arrows, and simple shapes. Dense visual content such as icons, distributions, overlap diagrams, mechanism sketches, and chart tiles is generated as bounded SVG and embedded into the editable draw.io page.

## Source Figures

The demo reference figures are reconstructed from the paper:

Jiayu Xiong, Jing Wang, Jun Xue, Wanlong Wang, Jianlong Kwan, Xiaosen Lyu, and Zhouqiang Jiang. "Multimodal Fusion via Self-Consistent Task-Gradient Fields." arXiv:2410.15475. ICML 2026 accepted paper.

Paper link: https://arxiv.org/abs/2410.15475

The reference images are included only as visual reconstruction targets for demonstrating the skill workflow.

## Ref/Result Comparison

### Method Flowchart Demo

| Reference (`ref.png`) | Editable reconstruction export (`result.png`) |
| --- | --- |
| ![Method reference](method-flowchart-demo/ref.png) | ![Method result](method-flowchart-demo/result.png) |

### Teaser Figure Demo

| Reference (`ref.png`) | Editable reconstruction export (`result.png`) |
| --- | --- |
| ![Teaser reference](teaser-figure-demo/ref.png) | ![Teaser result](teaser-figure-demo/result.png) |

## Core Workflow

Each demo follows the same artifact chain:

```text
ref.png -> result.drawio -> result.png
```

Use `ref.png` as the visual target, generate SVG tiles for dense content, compose `result.drawio` with editable text and grid-based draw.io geometry, then export `result.png` as a preview.

## Repository Layout

```text
yuinst-canvas-drawio-skill/
  SKILL.md
  agents/openai.yaml
  references/
    drawio-composer-patterns.md
    method-flowcharts.md
    reconstruction-workflow.md
    ref-image-briefs.md
    teaser-figures.md
  scripts/
    matplotlib_svg_tile.py

method-flowchart-demo/
  ref.png
  result.drawio
  result.png
  compose-result.py
  input-tiles/
  component-tiles/
  scripts/

teaser-figure-demo/
  ref.png
  result.drawio
  result.png
  panel-a-concept.*
  panel-b-mechanism.*
  panel-c-evidence.tex
  update-panel-b.py
```

## Figure Classes

The skill routes work into one primary figure class:

- `method-flowchart`: staged method, algorithm, model pipeline, architecture, or lane-based process.
- `teaser-figure`: paper teaser, graphical abstract, multi-panel overview, concept/mechanism/evidence composition.

The detailed figure rules live in:

- `yuinst-canvas-drawio-skill/references/method-flowcharts.md`
- `yuinst-canvas-drawio-skill/references/teaser-figures.md`

## Requirements

The examples use Python plus common scientific plotting libraries:

```bash
python -m pip install matplotlib numpy seaborn
```

Open `.drawio` files with diagrams.net or draw.io-compatible tooling.

## Notes For Reuse

- Keep important text editable in draw.io.
- Use SVG tiles for dense local visuals.
- Keep tile outputs bounded and margin-free.
- Do not depend on `ref.png` as the final artifact.
- Prefer deterministic composer scripts over hand-positioned layouts.
