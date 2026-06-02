# Teaser Figures

Use this reference for paper teaser figures, graphical abstracts, multi-panel overview figures, and concept + mechanism + evidence compositions.

## Class Definition

`TeaserFigure` is a multi-panel narrative figure.

Required objects:

```text
TeaserFigure
- canvas
- panels: list[Panel]
- shared_style_tokens
- narrative_order

Panel
- id, title, badge, bbox, local_grid, role
- role: concept | mechanism | evidence | comparison | result

PanelTile
- panel_id, row_id, col_id, bbox, kind, output_path
```

Unlike method flowcharts, teaser figures do not need one continuous pipeline. They need a clear narrative hierarchy.

## Reference Image Characteristics

A good teaser reference image has:

- 2-4 large panels with badges such as A/B/C.
- A strong left-to-right or top-to-bottom narrative.
- A concept/overview panel with icons, overlap, or shared-vs-unique structure.
- A mechanism panel with repeated rows or scenarios.
- An evidence/result panel with compact charts, tables, or quantitative summaries.
- Thin separators and consistent panel gutters.
- Titles aligned on a shared baseline.

Reject or rewrite references that:

- Use one giant undifferentiated canvas.
- Mix chart scales without labels.
- Make panel titles tiny or decorative.
- Use raster text as the primary explanation.
- Have no clear relationship between panels.

## Prompt Brief Template

```text
Create a clean multi-panel scientific teaser figure on a white background, wide landscape
aspect. Use three panels arranged left to right.

Panel A: concept overview. Include source/cue cards on the left, a central overlap or
shared-vs-unique schematic, and a compact decision/output summary at the bottom.

Panel B: mechanism explanation. Use a row-by-column grid where each row is one scenario
or failure case and columns show source, before state, mechanism, and after state. Use
small schematic plots or distribution tiles inside bounded cells.

Panel C: evidence summary. Use stacked compact chart panels with aligned axes and a small
legend. Highlight the proposed method or key comparison with a subtle outline or background.

Use panel badges, aligned titles, thin vertical separators, consistent gutters, restrained
colors, and editable-looking text placement. Avoid photorealism, poster background effects,
overlapping labels, and freehand arrows.
```

Return this prompt together with:

```text
Canvas: [w] x [h]
Panels:
- A: bbox=(...), role=concept, method=hybrid
- B: bbox=(...), role=mechanism, method=hybrid
- C: bbox=(...), role=evidence, method=hybrid
Panel-local grids:
- A: cards column + overlap diagram + summary footer
- B: scenario rows x explanation columns
- C: chart rows + legend footer
Tiles:
- A_cards.svg, A_overlap.svg
- B_row1_before.svg, B_row1_mechanism.svg, B_row1_after.svg
- C_chart_1.svg, C_chart_2.svg, C_chart_3.svg
Editable draw.io text:
- panel badges, panel titles, row labels, column headers, chart titles, legend labels
```

## Panel Object Patterns

### Concept Panel

Purpose:

- Explain the intuition of the paper or method.
- Show sources, evidence types, modalities, components, or conceptual factors.

Local grid:

```text
ConceptPanel
- title_band
- left_cards: stacked source/cue cards
- center_diagram: Venn/overlap/tree/composition schematic
- footer_summary: decision/output box
```

Use SVG tiles for icon cards and overlap diagrams. Keep panel title, card category labels, and footer summary editable unless the user wants a fully self-contained panel SVG.

### Mechanism Panel

Purpose:

- Explain multiple scenarios, failure modes, steps, or mechanisms.

Local grid:

```text
MechanismPanel
- header row: source | before | mechanism | after
- scenario rows: repeated
- arrow columns: narrow connector columns
```

Use SVG tiles for distribution sketches, matrices, local failure illustrations, token strips, or dense mechanism drawings. Use draw.io for row labels, column headers, scenario cards, and simple inter-column arrows.

### Evidence Panel

Purpose:

- Summarize quantitative evidence without overwhelming the teaser.

Local grid:

```text
EvidencePanel
- chart_1
- chart_2
- chart_3
- legend
```

Use SVG tiles for charts when they require axes, tick labels, bars, confidence bands, or plot annotations. Keep chart panel titles and the global legend editable in draw.io when feasible.

## Layout Rules

- Use panel-level bboxes first, then local panel grids.
- Align panel badge centers and title baselines across panels.
- Keep panel separators thin and neutral.
- Keep repeated chart panels equal width and height.
- Keep mechanism rows equal height unless one row has a justified special role.
- Use local arrows inside panels; avoid arrows that cross panel boundaries.
- Use one accent family per semantic role, not one color per random object.

## Tile Strategy

Recommended tile kinds:

```text
icon-card tile
- small line icons or cue groups
- fixed card dimensions

overlap-diagram tile
- Venn, shared/unique, hierarchy, evidence composition
- minimal embedded text

distribution-panel tile
- axes, ellipses, point clouds, local annotations

chart-panel tile
- bars/lines/error bands and small axis text

mechanism-tile
- local complex arrows, matrices, tokens, conflict marks
```

## Composer Pattern

The composer should instantiate panels from data:

```python
panels = [
    ("A", 0, 0, 620, 900, "Concept overview"),
    ("B", 620, 0, 850, 900, "Mechanism"),
    ("C", 1470, 0, 580, 900, "Evidence"),
]

for badge, x, y, w, h, title in panels:
    b.panel_badge(badge, x + 24, y + 24)
    b.text(x + 80, y + 18, w - 100, 40, title, size=22, bold=True, align="left")
    b.line(x + w, y + 70, h - 120)
```

Within each panel, use local constants:

```python
A = {"x": 0, "y": 0, "w": 620, "h": 900}
A_LEFT = (A["x"] + 20, A["y"] + 130, 260, 520)
A_CENTER = (A["x"] + 300, A["y"] + 110, 290, 620)
A_FOOTER = (A["x"] + 180, A["y"] + 770, 390, 70)
```

Do not position teaser elements by eye in the composer; derive positions from panel constants.

## Validation Checklist

- Panel badges and titles are editable and aligned.
- Each panel can be understood independently.
- The narrative order is obvious.
- Concept panel is not just decoration; it explains the premise.
- Mechanism panel has repeated rows/columns with consistent geometry.
- Evidence panel charts share comparable axes or explicitly show scale changes.
- All dense visual content is isolated in named SVG tiles.
- The final `.drawio` remains editable at the panel and label level.
