from pathlib import Path
from urllib.parse import quote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "result.drawio"


def style(parts):
    return ";".join(parts) + ";"


def svg_style(rel_path):
    svg = (ROOT / rel_path).read_text(encoding="utf-8")
    return style(
        [
            "shape=image",
            "html=1",
            "verticalLabelPosition=bottom",
            "verticalAlign=top",
            "imageAspect=0",
            "aspect=fixed",
            "image=data:image/svg+xml," + quote(svg, safe=""),
        ]
    )


class Builder:
    def __init__(self):
        self.mxfile = ET.Element(
            "mxfile",
            {
                "host": "app.diagrams.net",
                "modified": "2026-05-28T00:00:00.000Z",
                "agent": "Codex",
                "version": "24.7.17",
                "type": "device",
            },
        )
        diagram = ET.SubElement(self.mxfile, "diagram", {"id": "method-flowchart", "name": "Method Flowchart 950x400"})
        self.model = ET.SubElement(
            diagram,
            "mxGraphModel",
            {
                "dx": "950",
                "dy": "400",
                "grid": "1",
                "gridSize": "10",
                "guides": "1",
                "tooltips": "1",
                "connect": "1",
                "arrows": "1",
                "fold": "1",
                "page": "1",
                "pageScale": "1",
                "pageWidth": "950",
                "pageHeight": "400",
                "math": "1",
                "shadow": "0",
            },
        )
        self.root = ET.SubElement(self.model, "root")
        ET.SubElement(self.root, "mxCell", {"id": "0"})
        ET.SubElement(self.root, "mxCell", {"id": "1", "parent": "0"})
        self.n = 2

    def new_id(self, prefix="c"):
        out = f"{prefix}{self.n}"
        self.n += 1
        return out

    def rect(self, x, y, w, h, cell_style, value="", cid=None):
        cid = cid or self.new_id()
        cell = ET.SubElement(
            self.root,
            "mxCell",
            {"id": cid, "value": value, "style": cell_style, "parent": "1", "vertex": "1"},
        )
        ET.SubElement(
            cell,
            "mxGeometry",
            {"x": str(x), "y": str(y), "width": str(w), "height": str(h), "as": "geometry"},
        )
        return cid

    def text(self, x, y, w, h, value, size=12, color="#111111", bold=False, align="center", cid=None):
        return self.rect(
            x,
            y,
            w,
            h,
            style(
                [
                    "text",
                    "html=1",
                    "strokeColor=none",
                    "fillColor=none",
                    f"align={align}",
                    "verticalAlign=middle",
                    "whiteSpace=wrap",
                    "rounded=0",
                    "fontFamily=Bahnschrift",
                    f"fontSize={size}",
                    f"fontColor={color}",
                    "fontStyle=1" if bold else "fontStyle=0",
                    "spacing=2",
                ]
            ),
            value,
            cid,
        )

    def image(self, rel_path, x, y, w, h, cid=None):
        return self.rect(x, y, w, h, svg_style(rel_path), "", cid)

    def arrow(self, x1, y1, x2, y2, color="#000000", width="1.2", dashed=False, points=None):
        st = ["endArrow=classic", "html=1", "rounded=0", f"strokeWidth={width}", f"strokeColor={color}"]
        if dashed:
            st += ["dashed=1", "dashPattern=4 4"]
        cell = ET.SubElement(
            self.root,
            "mxCell",
            {"id": self.new_id("e"), "value": "", "style": style(st), "edge": "1", "parent": "1"},
        )
        geo = ET.SubElement(cell, "mxGeometry", {"relative": "1", "as": "geometry"})
        ET.SubElement(geo, "mxPoint", {"x": str(x1), "y": str(y1), "as": "sourcePoint"})
        ET.SubElement(geo, "mxPoint", {"x": str(x2), "y": str(y2), "as": "targetPoint"})
        if points:
            arr = ET.SubElement(geo, "Array", {"as": "points"})
            for x, y in points:
                ET.SubElement(arr, "mxPoint", {"x": str(x), "y": str(y)})

    def line(self, x, y, h):
        self.rect(
            x,
            y,
            0,
            h,
            style(["shape=line", "html=1", "strokeColor=#C7C7C7", "strokeWidth=1", "dashed=1", "dashPattern=5 5"]),
        )

    def write(self):
        ET.indent(ET.ElementTree(self.mxfile), space="  ", level=0)
        ET.ElementTree(self.mxfile).write(OUT, encoding="utf-8", xml_declaration=True)


b = Builder()

box = lambda fill, stroke: style(
    [
        "rounded=1",
        "whiteSpace=wrap",
        "html=1",
        f"fillColor={fill}",
        f"strokeColor={stroke}",
        "arcSize=10",
        "shadow=0",
        "fontFamily=Bahnschrift",
        "fontSize=11",
        "fontStyle=1",
        "align=center",
        "verticalAlign=middle",
    ]
)

header_box = style(
    [
        "rounded=1",
        "whiteSpace=wrap",
        "html=1",
        "fillColor=#EDEBFF",
        "strokeColor=#9EA6E8",
        "arcSize=35",
        "shadow=0",
        "fontFamily=Bahnschrift",
        "fontSize=14",
        "fontStyle=1",
        "fontColor=#34305F",
        "align=center",
        "verticalAlign=middle",
    ]
)

b.rect(0, 0, 950, 400, style(["rounded=0", "whiteSpace=wrap", "html=1", "fillColor=#FFFFFF", "strokeColor=none"]))

headers = [
    (0, 10, 130, "1", "Modality Inputs"),
    (130, 10, 230, "2", "Expand & Factorize<br>(shared / specific)"),
    (360, 10, 250, "3", "Dissociation / Self-consistent<br>Reorganization"),
    (610, 10, 190, "4", "Project & Reconfigure"),
    (800, 10, 150, "5", "Objectives"),
]
for x, y, w, num, label in headers:
    b.rect(x + 10, y + 5, 25, 25, header_box, num)
    b.text(x + 40, y, w - 45, 40, label, size=14, bold=True, align="left")

for x in [130, 360, 610, 800]:
    b.line(x, 20, 300)

rows = [70, 160, 250]
mods = [("A", "#2F6FB6", "#8FB3E8"), ("B", "#2B9A9A", "#8AC7C7"), ("C", "#F06A4A", "#FFB09C")]
for (mod, color, light), y in zip(mods, rows):
    mod_key = mod.lower()
    b.image(f"input-tiles/input-card-{mod_key}.svg", 10, y, 60, 60)
    b.arrow(70, y + 30, 90, y + 30)
    b.image(f"input-tiles/vector-token-{mod_key}.svg", 90, y + 10, 30, 40)
    b.text(80, y + 60, 50, 20, f"\\(\\mathbf{{V}}^{{({mod})}}\\)", size=11)
    b.arrow(120, y + 30, 140, y + 30)
    b.rect(140, y + 10, 60, 40, box("#F9FBFF", "#A9BDD8"), "Expand<br>\\(P_{\\mathrm{expand}}\\)")
    b.arrow(200, y + 30, 220, y + 30)
    b.image(f"component-tiles/factor-{mod_key}.svg", 220, y + 10, 110, 40)

b.text(230, 50, 40, 20, "shared", size=10, color="#2F6FB4")
b.text(290, 50, 50, 20, "specific", size=10, color="#E76F51")
b.arrow(330, 100, 380, 130)
b.arrow(330, 190, 380, 190)
b.arrow(330, 280, 380, 250)

b.image("stage3-reorg.svg", 380, 60, 230, 230)
b.arrow(600, 120, 630, 80, color="#2F6FB4")
b.arrow(600, 170, 630, 180, color="#288B8B")
b.arrow(600, 240, 630, 280, color="#E76F51")

stage4_rows = [
    ("A", "B", "#2F6FB4", 60, "ZA", "specific^{(A)}", "shared^{(B)}"),
    ("B", "C", "#288B8B", 150, "ZB", "specific^{(B)}", "shared^{(C)}"),
    ("C", "A", "#E76F51", 240, "ZC", "specific^{(C)}", "shared^{(A)}"),
]
for left_mod, right_mod, color, y, zname, lab1, lab2 in stage4_rows:
    stroke = {"A": "#A9BDD8", "B": "#8AC7C7", "C": "#FFB09C"}[left_mod]
    b.rect(620, y, 60, 30, box("#FFFFFF", stroke), "\\(P_{\\mathrm{shared}}\\)")
    b.rect(620, y + 40, 60, 30, box("#FFFFFF", stroke), "\\(P_{\\mathrm{specific}}\\)")
    b.arrow(680, y + 20, 700, y + 50, color=color, width="1.0")
    b.arrow(680, y + 60, 700, y + 50, color=color, width="1.0")
    b.rect(700, y + 30, 100, 40, box("#FFFFFF", "#B7C3CE"), "")
    left_key = left_mod.lower()
    right_key = right_mod.lower()
    output_key = left_key
    b.image(f"component-tiles/output-{output_key}-specific.svg", 710, y + 40, 40, 20)
    b.text(750, y + 40, 10, 20, ";", size=10)
    b.image(f"component-tiles/output-{output_key}-shared-from-{right_key}.svg", 760, y + 40, 40, 20)
    b.text(715, y + 10, 70, 20, f"\\(\\mathbf{{Z}}^{{({left_mod})}}\\)", size=12, bold=True)
    b.text(690, y + 75, 120, 20, f"[\\(\\mathrm{{{lab1}}};\\;\\mathrm{{{lab2}}}\\)]", size=8)

b.arrow(800, 110, 835, 80, points=[(805, 110), (805, 80)])
b.arrow(800, 200, 835, 95, points=[(805, 200), (805, 95)])
b.arrow(800, 290, 835, 110, points=[(805, 290), (805, 110)])
b.rect(835, 65, 80, 50, box("#FFF4D6", "#D79A2B"), "Task Head<br>\\(f_\\theta\\)")
b.arrow(915, 90, 940, 90)
b.text(915, 105, 35, 20, "\\(L_{\\mathrm{task}}\\)", size=11)

b.rect(
    825,
    125,
    120,
    190,
    style(["rounded=1", "whiteSpace=wrap", "html=1", "fillColor=none", "strokeColor=#7A45A0", "dashed=1", "dashPattern=5 5", "arcSize=10"]),
)
b.text(850, 295, 80, 20, "Reconstruction", size=10, color="#7A45A0", bold=True)
for mod, y in zip(["A", "B", "C"], [155, 215, 275]):
    b.image(f"input-tiles/vector-token-{mod.lower()}.svg", 845, y, 30, 40)
    b.text(790, y - 10, 40, 20, "\\(P_{\\mathrm{recon}}\\)", size=9, color="#7A45A0")
    b.arrow(825, y + 20, 845, y + 20, color="#7A45A0")
    b.arrow(875, y + 20, 885, y + 20)
    b.text(880, y + 10, 60, 20, f"\\(L^{{({mod})}}_{{\\mathrm{{recon}}}}\\)", size=10)

b.arrow(800, 110, 825, 175, color="#7A45A0", points=[(820, 110), (820, 175)])
b.arrow(800, 200, 825, 235, color="#7A45A0", points=[(820, 200), (820, 235)])
b.arrow(800, 290, 825, 295, color="#7A45A0")
b.arrow(940, 110, 885, 320, color="#E76F51", dashed=True, points=[(940, 320), (885, 320)])
b.arrow(900, 315, 885, 320, color="#E76F51", dashed=True)
b.rect(810, 330, 130, 50, box("#FFF4D6", "#D79A2B"), "Unified Objective<br>\\(\\Phi=L_{\\mathrm{task}}+\\lambda L_{\\mathrm{recon}}\\)")

b.rect(10, 330, 780, 50, style(["rounded=1", "whiteSpace=wrap", "html=1", "fillColor=#FFFFFF", "strokeColor=#C7C7C7", "arcSize=10"]))
b.image("component-tiles/legend-shared.svg", 35, 340, 30, 30)
b.text(75, 340, 70, 30, "Shared<br>Component", size=10)
b.image("component-tiles/legend-specific.svg", 160, 340, 30, 30)
b.text(200, 340, 70, 30, "Specific<br>Component", size=10)
b.image("component-tiles/legend-from-a.svg", 285, 340, 30, 30)
b.text(325, 340, 100, 30, "Shared from A<br>(used by C)", size=10)
b.image("component-tiles/legend-from-b.svg", 435, 340, 30, 30)
b.text(475, 340, 100, 30, "Shared from B<br>(used by A)", size=10)
b.image("component-tiles/legend-from-c.svg", 585, 340, 30, 30)
b.text(625, 340, 100, 30, "Shared from C<br>(used by B)", size=10)
b.arrow(725, 355, 755, 355)
b.text(755, 340, 35, 30, "Flow", size=10)

b.write()
print(f"wrote {OUT}")
