# Reference Image Briefs

Use this reference when the task is to polish a prompt before generating a reference image.

## What Makes a Useful Reference Image

A useful `ref.png` is not merely attractive. It is easy to reconstruct as editable geometry.

Require these properties:

- A clear reading order: left-to-right, top-to-bottom, radial, or panel A/B/C.
- A visible grid: columns, rows, gutters, panel boundaries, repeated lanes, or repeated cards.
- Stable rectangular regions for labels, charts, diagrams, legends, and icons.
- Simple connectors between regions. Complex mechanics should stay inside local panels.
- Text placed in predictable locations, not scattered over dense artwork.
- No decorative background that competes with diagram structure.
- No photorealistic rendering, perspective camera, shadows that imply 3D, or painterly texture.

## Flowchart Prompt Template

```text
Create a clean scientific workflow diagram on a white background, [aspect ratio].
Organize it as a strict grid with [number] vertical stages and [number] horizontal lanes.

Stage 1: [input objects], repeated once per lane.
Stage 2: [transformation], shown as simple boxes and compact icons.
Stage 3: [central mechanism], shown as one bounded circular or schematic panel.
Stage 4: [projection or output construction], shown as repeated lane-specific blocks.
Stage 5: [objectives or outputs], shown as a compact right column.

Use simple straight arrows between neighboring regions. Use dashed vertical separators
between stages. Keep all labels readable and aligned to the grid. Use a restrained palette
with one accent color per lane. Avoid photorealism, decorative backgrounds, complex freehand
arrows, and overlapping text.
```

## Teaser Prompt Template

```text
Create a multi-panel scientific teaser figure on a white background, wide landscape aspect.
Panel A: concept overview with modality or source cards on the left, a central Venn/overlap
or shared-vs-unique mechanism, and a compact decision/output summary at the bottom.
Panel B: mechanism explanation in a row-by-column grid. Each row is one failure case or
scenario. Columns show source, before state, mechanism, and after state. Use small plots,
icons, or schematic distributions as bounded panels.
Panel C: quantitative evidence column with stacked bar-chart panels and a small legend.

Use panel badges A/B/C, aligned titles, thin separators, and consistent gutters. Keep chart
axes and tiny plot annotations inside plot tiles, but keep panel titles and major labels in
editable text regions. Avoid poster styling and avoid dense visual noise.
```

## Reconstruction Plan to Return With a Prompt

Always attach a plan like this:

```text
Canvas: 2050 x 900
Panels:
- A: x=0, y=0, w=640, h=900, role=concept overview, method=hybrid
- B: x=640, y=0, w=820, h=900, role=mechanism grid, method=hybrid
- C: x=1460, y=0, w=590, h=900, role=evidence charts, method=hybrid
Tile candidates:
- A_icon_cards.svg, A_overlap_diagram.svg
- B_row1_before.svg, B_row1_mechanism.svg, B_row1_after.svg, ...
- C_dataset1_bars.svg, C_dataset2_bars.svg, C_dataset3_bars.svg
Editable draw.io text:
- panel badges, panel titles, row labels, column headers, legend labels, main conclusions
```
