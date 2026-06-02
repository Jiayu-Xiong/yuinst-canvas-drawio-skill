from pathlib import Path
import seaborn as sns
from matplotlib.colors import to_hex

# =========================
# 输出目录
# =========================
out_dir = Path(__file__).resolve().parents[1] / "component-tiles"
out_dir.mkdir(parents=True, exist_ok=True)

# =========================
# 颜色：A / B / C
# 你也可以自己改
# =========================
palette = sns.color_palette(["#3B78C2", "#2D9C9A", "#F46D4D"])
colors = {
    "A": to_hex(palette[0]),  # 蓝
    "B": to_hex(palette[1]),  # 青绿
    "C": to_hex(palette[2]),  # 橙红
}

# =========================
# SVG pattern 定义
# shared: 斜杠
# specific: 密集点
# =========================
def svg_defs(key, color):
    return f"""
  <defs>
    <pattern id="stripe_{key}" patternUnits="userSpaceOnUse" width="10" height="10">
      <rect width="10" height="10" fill="{color}" fill-opacity="0.08"/>
      <path d="M-4,10 L10,-4 M0,14 L14,0 M6,16 L16,6"
            stroke="{color}" stroke-width="1.6" stroke-linecap="round" opacity="0.9"/>
    </pattern>

    <pattern id="dots_{key}" patternUnits="userSpaceOnUse" width="6" height="6">
      <rect width="6" height="6" fill="{color}" fill-opacity="0.05"/>
      <circle cx="2" cy="2" r="0.9" fill="{color}" opacity="0.9"/>
    </pattern>
  </defs>
"""

def save_svg(path: Path, content: str):
    path.write_text(content.strip() + "\n", encoding="utf-8")

# =========================
# Stage 2:
# 一个完整框，左 shared，右 specific
# 无白边，图形占满整个 SVG
# =========================
def make_stage2_svg(mod, color, width=110, height=40):
    half_w = width // 2
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
{svg_defs(mod, color)}
  <clipPath id="clip_stage2_{mod}">
    <rect x="0" y="0" width="{width}" height="{height}" rx="8"/>
  </clipPath>

  <g clip-path="url(#clip_stage2_{mod})">
    <rect x="0" y="0" width="{half_w}" height="{height}" fill="url(#stripe_{mod})"/>
    <rect x="{half_w}" y="0" width="{width - half_w}" height="{height}" fill="url(#dots_{mod})"/>
    <line x1="{half_w}" y1="0" x2="{half_w}" y2="{height}"
          stroke="{color}" stroke-width="1.2" opacity="0.7"/>
  </g>

  <rect x="0" y="0" width="{width}" height="{height}" rx="8"
        fill="none" stroke="{color}" stroke-width="1.6"/>
</svg>"""

# =========================
# Stage 4:
# 单独一个 shared 或 specific 图标
# 无白边，图形占满整个 SVG
# =========================
def make_stage4_svg(mod, pattern_type, color, width=40, height=20):
    fill_id = "stripe" if pattern_type == "shared" else "dots"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
{svg_defs(mod, color)}
  <rect x="0" y="0" width="{width}" height="{height}" rx="5"
        fill="url(#{fill_id}_{mod})" stroke="{color}" stroke-width="1.6"/>
</svg>"""


def make_legend_component_svg(mod, pattern_type, color, width=30, height=30):
    fill_id = "stripe" if pattern_type == "shared" else "dots"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
{svg_defs(mod, color)}
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="4"
        fill="url(#{fill_id}_{mod})" stroke="{color}" stroke-width="1.6"/>
</svg>"""


def make_legend_shared_from_svg(mod, color, fill, width=30, height=30):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="5"
        fill="{fill}" stroke="{color}" stroke-width="1.6"/>
</svg>"""

# =========================
# 生成 stage2 三个
# =========================
for mod in ["A", "B", "C"]:
    svg = make_stage2_svg(mod, colors[mod], width=110, height=40)
    save_svg(out_dir / f"factor-{mod.lower()}.svg", svg)

# =========================
# 生成 stage4 六个
# 对应你的图里：
# Z(A) = [specific(A); shared(B)]
# Z(B) = [specific(B); shared(C)]
# Z(C) = [specific(C); shared(A)]
# =========================
stage4_specs = [
    ("a", "A", "specific"),
    ("a", "B", "shared"),
    ("b", "B", "specific"),
    ("b", "C", "shared"),
    ("c", "C", "specific"),
    ("c", "A", "shared"),
]

for output, mod, ptype in stage4_specs:
    svg = make_stage4_svg(mod, ptype, colors[mod], width=40, height=20)
    suffix = "specific" if ptype == "specific" else f"shared-from-{mod.lower()}"
    save_svg(out_dir / f"output-{output}-{suffix}.svg", svg)

save_svg(out_dir / "legend-shared.svg", make_legend_component_svg("A", "shared", colors["A"]))
save_svg(out_dir / "legend-specific.svg", make_legend_component_svg("A", "specific", colors["A"]))
save_svg(out_dir / "legend-from-a.svg", make_legend_shared_from_svg("A", colors["A"], "#EEF4FF"))
save_svg(out_dir / "legend-from-b.svg", make_legend_shared_from_svg("B", colors["B"], "#EEF9F7"))
save_svg(out_dir / "legend-from-c.svg", make_legend_shared_from_svg("C", colors["C"], "#FFF2ED"))

print("完成，文件保存在：", out_dir.resolve())
print("共生成 9 个 SVG 文件。")
