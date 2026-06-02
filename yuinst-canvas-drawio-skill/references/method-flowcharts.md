# Methodology Flowcharts

Use this reference for staged method diagrams, model pipelines, algorithm figures, architecture diagrams, and lane-based workflows.

## Class Definition

`MethodFlowchartFigure` is a mostly linear process figure.

Required objects:

```text
MethodFlowchartFigure
- canvas
- stages: list[Stage]
- lanes: list[Lane]
- mechanism_tiles: list[TileSpec]
- objectives_or_outputs: list[Region]
- legend: Region | None

Stage
- id, title, order, bbox, separator_after

Lane
- id, y, h, color, repeated_blocks
```

## Reference Image Characteristics

A good method-flowchart reference image has:

- One dominant reading direction, usually left-to-right.
- Visible stage titles or stage numbers.
- Vertical stage separators or clearly implied columns.
- Repeated horizontal lanes for modalities, samples, modules, or cases.
- A central mechanism or transformation region that can be isolated as one tile.
- A compact objective/output region at the end.
- A legend or notation strip when colors/patterns encode meaning.

Reject or rewrite references that:

- Scatter steps without a grid.
- Use decorative perspective or 3D staging.
- Put crucial labels over detailed artwork.
- Use many crossing arrows that cannot be reduced to local connectors.

## Prompt Brief Template

```text
Create a clean scientific methodology flowchart on a white background, wide landscape aspect.
Use [N] vertical stages and [M] repeated horizontal lanes. Each stage has a bold title at
the top and light dashed separators between stages. Each lane uses a consistent accent color.

Stage 1: [inputs per lane].
Stage 2: [expansion/factorization/encoding block per lane].
Stage 3: [central mechanism], shown as one bounded schematic panel.
Stage 4: [projection/reconfiguration/output construction], repeated by lane.
Stage 5: [objective/loss/result column].

Use simple straight arrows between neighboring stage blocks. Place a legend strip along the
bottom if colors or patterns need explanation. Keep all labels readable and aligned to the
grid. Avoid photorealism, decorative backgrounds, freehand layout, and overlapping text.
```

Return this prompt together with a reconstruction table:

```text
Canvas: [w] x [h]
Stages:
- s1: bbox=(...), title=..., method=hybrid
- s2: bbox=(...), title=..., method=hybrid
Lanes:
- lane1: y=..., h=..., color=...
Tiles:
- tile_s1_lane1_icon.svg
- tile_s3_mechanism.svg
Editable draw.io text:
- stage numbers, stage titles, lane labels, equations, legend labels
```

## Grid Planning

Use a stage/lane grid:

```text
Canvas: 1600 x 700
Margins: 24 24 24 24
Stage columns:
- input: x=0, w=220
- transform: x=220, w=300
- mechanism: x=520, w=420
- construct: x=940, w=360
- objectives: x=1300, w=300
Lane rows:
- header: y=24, h=52
- lane_1: y=100, h=110
- lane_2: y=230, h=110
- lane_3: y=360, h=110
- legend: y=520, h=120
```

Rules:

- Stage columns own all x positions.
- Lane rows own all y positions.
- Repeated lane content should be generated from a data table, not copy-pasted.
- Central mechanism tiles may span lanes if they explain cross-lane behavior.
- Legend should be a draw.io region with SVG swatches only for pattern samples.

## Region Objects

Recommended region types:

```text
InputCard
- render_mode=hybrid
- draw.io label + SVG icon tile

TransformBlock
- render_mode=drawio or hybrid
- draw.io rounded box + optional SVG pattern tile

MechanismPanel
- render_mode=svg-tile or hybrid
- local complex arrows/rings/matrices inside SVG
- major title editable in draw.io if outside the mechanism

OutputAssembly
- render_mode=hybrid
- draw.io container + SVG subtiles + editable equation/label

ObjectivePanel
- render_mode=drawio
- draw.io task/loss boxes and simple arrows

LegendStrip
- render_mode=hybrid
- draw.io labels + SVG swatches
```

## Tile Strategy

Use SVG tiles for:

- Input glyphs.
- Vector stacks, token strips, matrices, or compact arrays.
- Patterned shared/specific components.
- Circular or self-consistency mechanisms.
- Local complex arrows.

Keep in draw.io:

- Stage headers.
- Equations and notation.
- Pipeline arrows.
- Objective boxes.
- Legend text.

## Composer Pattern

The composer should be deterministic and table-driven:

```python
stages = [
    ("s1", 0, 220, "Inputs"),
    ("s2", 220, 300, "Transform"),
]
lanes = [
    ("lane1", 100, 110, "#2563EB"),
    ("lane2", 230, 110, "#0F766E"),
]

for stage_id, x, w, title in stages:
    b.text(x, 24, w, 40, title, bold=True)
    b.line(x + w, 76, 420)

for lane_id, y, h, color in lanes:
    ...
```

Use one composer file for the full `.drawio`; do not generate independent `.drawio` files per stage unless the user requests modular diagrams.

## Validation Checklist

- Stage separators align from header through lanes.
- Repeated lanes use identical geometry.
- Central mechanism has a bounded bbox and does not push nearby layout.
- Arrows connect neighboring regions without dense crossings.
- The legend explains every color/pattern encoding.
- The figure remains understandable if all SVG tiles are temporarily hidden, because editable text and layout still reveal the structure.
