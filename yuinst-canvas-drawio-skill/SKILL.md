---
name: yuinst-canvas-drawio-skill
description: Create, refine, or reconstruct editable scientific figures through a grid-first draw.io workflow. Use when Codex must polish prompts for reference images, reproduce ref.png-like raster drafts as editable .drawio files, build teaser figures, build methodology flowcharts, compose Python-generated no-margin SVG tiles with editable draw.io text/shapes, or generate deterministic figure-building scripts.
---

# YuInst Canvas Draw.io Skill

## Core Contract

Use a three-object architecture:

1. `ReferenceBrief`: prompt or raster reference that defines visual intent.
2. `TileSet`: bounded SVG assets for dense visual content.
3. `DrawioComposer`: editable `.drawio` layout with grid geometry, text, simple shapes, simple connectors, and embedded SVG tiles.

The grid owns the figure. SVG tiles conform to the grid. draw.io owns editability.

## Figure Class Router

Choose exactly one primary figure class before implementing:

- **Methodology flowchart**: read [references/method-flowcharts.md](references/method-flowcharts.md) when the figure is a staged method, model pipeline, algorithm diagram, architecture workflow, or lane-based process.
- **Teaser figure**: read [references/teaser-figures.md](references/teaser-figures.md) when the figure is a paper teaser, multi-panel overview, concept + mechanism + evidence composition, or A/B/C style summary figure.

Also read only the references needed for the task:

- Prompt polishing for a future `ref.png`: [references/ref-image-briefs.md](references/ref-image-briefs.md).
- Reconstructing a provided raster reference: [references/reconstruction-workflow.md](references/reconstruction-workflow.md).
- Writing the final `.drawio` XML composer: [references/drawio-composer-patterns.md](references/drawio-composer-patterns.md).

Do not load all references by default.

## Object Model

Use these objects in planning and, when useful, in code comments or data tables:

```text
FigureSpec
- canvas: width, height, margins, background
- class: method-flowchart | teaser-figure
- regions: list[Region]
- tiles: list[TileSpec]
- editable_text: list[TextSpec]
- connectors: list[ConnectorSpec]

Region
- id, bbox=(x,y,w,h), role, local_grid, render_mode
- render_mode: drawio | svg-tile | hybrid

TileSpec
- id, output_path, bbox, generator_script, kind
- kind: icon-card | overlap-diagram | distribution-panel | chart-panel | mechanism-tile | pattern-swatch

DrawioComposer
- page_size, helper_api, style_tokens, layer_order
```

## Required Work Order

Unless the user only asks for prompt polishing, follow this order:

1. Classify the figure as `method-flowchart` or `teaser-figure`.
2. If polishing a prompt, produce a `ReferenceBrief` plus reconstruction plan.
3. If given a raster reference, extract a `FigureSpec` instead of tracing pixels.
4. Write the global grid and any panel-local grids.
5. Mark every region as `drawio`, `svg-tile`, or `hybrid`.
6. Generate/update tile scripts and run them.
7. Generate/update one deterministic draw.io composer script.
8. Run the composer to produce the final `.drawio`.
9. Validate XML structure, page size, embedded tiles, editable text, alignment, and arrow simplicity.

Do not start the final composer before a grid exists.

## Universal Rules

- Keep major labels, titles, equations, legends, panel badges, row labels, and column headers editable in draw.io.
- Use SVG tiles for icons, dense plots, distribution sketches, Venn/overlap mechanisms, matrices, patterned components, and custom local arrows.
- Use draw.io-native geometry for boxes, separators, simple arrows, captions, containers, and global layout.
- Do not put the whole figure into one giant SVG and call it editable.
- Do not depend on `ref.png` as the final artifact.
- Do not create freehand draw.io layouts without numeric row/column geometry.
- Do not bake important text into SVG unless it is a tiny axis label or plot annotation that belongs inside a tile.

## SVG Tile Baseline

Use `scripts/matplotlib_svg_tile.py` as a starting point for fixed-size transparent SVG tiles.

Examples:

```bash
python yuinst-canvas-drawio-skill/scripts/matplotlib_svg_tile.py tile_flow_lane.svg --width 720 --height 220 --example flow-lane
python yuinst-canvas-drawio-skill/scripts/matplotlib_svg_tile.py tile_venn.svg --width 600 --height 500 --example venn-teaser
python yuinst-canvas-drawio-skill/scripts/matplotlib_svg_tile.py tile_distributions.svg --width 700 --height 220 --example distribution-triplet
```

Treat these as generic templates, not final aesthetics. Adapt the geometry and semantics to the current figure class.

## Completion Criteria

A task is complete only when:

- The figure class reference was followed.
- The output `.drawio` has the intended page size.
- All planned regions exist with explicit pixel geometry.
- Important text remains editable in draw.io.
- SVG tiles are bounded, transparent or intentionally backed, and free of accidental white margins.
- The final answer reports what was generated and what validation was performed.
