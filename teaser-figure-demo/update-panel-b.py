import io
from pathlib import Path
from urllib.parse import quote
import xml.etree.ElementTree as ET

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parent
DRAW_PY = ROOT / "panel-b-mechanism.py"
DRAWIO = ROOT / "result.drawio"


def load_draw_functions():
    src = DRAW_PY.read_text(encoding="utf-8")
    marker = "# =========================================================\n# 5. Figure layout"
    if marker not in src:
        raise RuntimeError("Cannot find Figure layout marker in panel-b-mechanism.py")
    ns = {}
    exec(src.split(marker)[0], ns)
    return ns


def render_distribution_svg(draw_func):
    fig, ax = plt.subplots(figsize=(2.60, 2.15), facecolor="white")
    draw_func(ax)
    buf = io.StringIO()
    fig.savefig(buf, format="svg", facecolor="white")
    plt.close(fig)
    svg = buf.getvalue()
    start = svg.find("<svg")
    return svg[start:] if start >= 0 else svg


def image_style(svg):
    data = quote(svg, safe="")
    return (
        "shape=image;html=1;verticalLabelPosition=bottom;verticalAlign=top;"
        f"imageAspect=1;image=data:image/svg+xml,{data};"
    )


def set_geometry(cell, x, y, w, h):
    geom = cell.find("mxGeometry")
    if geom is None:
        geom = ET.SubElement(cell, "mxGeometry", {"as": "geometry"})
    geom.set("x", str(x))
    geom.set("y", str(y))
    geom.set("width", str(w))
    geom.set("height", str(h))
    geom.set("as", "geometry")


def main():
    ns = load_draw_functions()
    order = [
        ("c59", "row1_unimodal", 820, 170, 180, 150),
        ("c60", "row1_mechanism", 1040, 170, 180, 150),
        ("c62", "row1_result", 1260, 170, 180, 150),
        ("c70", "row2_unimodal", 820, 410, 180, 150),
        ("c71", "row2_mechanism", 1040, 410, 180, 150),
        ("c73", "row2_result", 1260, 410, 180, 150),
        ("c81", "row3_unimodal", 820, 650, 180, 150),
        ("cB_row3_mechanism", "row3_mechanism", 1040, 650, 180, 150),
        ("c82", "row3_result", 1260, 650, 180, 150),
    ]

    tree = ET.parse(DRAWIO)
    root = tree.getroot()
    graph_root = root.find(".//root")
    parent_map = {child: parent for parent in root.iter() for child in parent}
    cells = {c.get("id"): c for c in root.iter("mxCell")}

    for cell_id, func_name, x, y, w, h in order:
        svg = render_distribution_svg(ns[func_name])
        if cell_id in cells:
            cell = cells[cell_id]
            current_parent = parent_map.get(cell)
            if current_parent is not None and current_parent is not graph_root:
                current_parent.remove(cell)
                graph_root.append(cell)
        else:
            cell = ET.SubElement(graph_root, "mxCell", id=cell_id, value="", vertex="1", parent="1")
        cell.set("style", image_style(svg))
        cell.set("value", "")
        cell.set("vertex", "1")
        cell.set("parent", "1")
        set_geometry(cell, x, y, w, h)

    ET.indent(root, space="  ")
    txt = ET.tostring(root, encoding="unicode")
    txt = txt.replace("as_=", "as=")
    DRAWIO.write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + txt, encoding="utf-8")


if __name__ == "__main__":
    main()
