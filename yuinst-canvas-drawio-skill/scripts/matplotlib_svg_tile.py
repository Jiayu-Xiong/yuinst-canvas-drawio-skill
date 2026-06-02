#!/usr/bin/env python
"""Create fixed-size, no-margin SVG tiles for draw.io grid figures.

Use this as a template for block-level matplotlib/seaborn artwork. The
examples are intentionally generic: adapt the geometry and labels, but keep
major explanatory text editable in draw.io whenever possible.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

try:
    import seaborn as sns
except ImportError:  # Keep the template usable before seaborn is installed.
    sns = None


def make_canvas(width: int, height: int, dpi: int):
    fig = plt.figure(figsize=(width / dpi, height / dpi), dpi=dpi)
    fig.patch.set_alpha(0)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, width)
    ax.set_ylim(height, 0)
    ax.set_aspect("equal")
    ax.set_axis_off()
    return fig, ax


def draw_blank(ax, width: int, height: int) -> None:
    ax.set_xlim(0, width)
    ax.set_ylim(height, 0)


def label(ax, text: str, x: float, y: float, size: float = 12, color: str = "#1F2937", weight: str = "normal") -> None:
    ax.text(x, y, text, ha="center", va="center", fontsize=size, color=color, fontweight=weight)


def icon_circle(ax, x: float, y: float, r: float, color: str, fill_alpha: float = 0.12) -> None:
    ax.add_patch(patches.Circle((x, y), r, facecolor=color, edgecolor=color, alpha=fill_alpha, lw=1.4))


def draw_line(ax, width: int, height: int) -> None:
    x = np.linspace(0, width, 160)
    y = height * 0.52 + height * 0.18 * np.sin(2 * np.pi * x / width)
    y += height * 0.08 * np.cos(7 * np.pi * x / width)
    ax.plot(x, y, color="#2563EB", lw=3)
    ax.fill_between(x, y, height * 0.82, color="#60A5FA", alpha=0.25)


def draw_heatmap(ax, width: int, height: int) -> None:
    rng = np.random.default_rng(7)
    data = rng.normal(size=(12, 18))
    if sns is not None:
        sns.heatmap(data, ax=ax, cbar=False, xticklabels=False, yticklabels=False, cmap="viridis")
    else:
        ax.imshow(data, cmap="viridis", aspect="auto", interpolation="nearest", extent=[0, width, height, 0])
    ax.set_axis_off()


def draw_icon_card(ax, width: int, height: int) -> None:
    colors = ["#2563EB", "#F59E0B", "#EF4444"]
    names = ["Visual", "Audio", "Text"]
    margin = 16
    card_h = (height - 4 * margin) / 3
    for i, (name, color) in enumerate(zip(names, colors)):
        y = margin + i * (card_h + margin)
        ax.add_patch(
            patches.FancyBboxPatch(
                (margin, y),
                width - 2 * margin,
                card_h,
                boxstyle="round,pad=0,rounding_size=9",
                facecolor="none",
                edgecolor=color,
                lw=1.6,
            )
        )
        label(ax, f"{name} cues", width * 0.50, y + 16, size=12, color=color, weight="bold")
        for j in range(8):
            cx = margin + 38 + (j % 4) * ((width - 92) / 3)
            cy = y + 48 + (j // 4) * 38
            if j % 3 == 0:
                ax.add_patch(patches.Rectangle((cx - 10, cy - 10), 20, 20, fill=False, edgecolor=color, lw=1.8))
            elif j % 3 == 1:
                icon_circle(ax, cx, cy, 10, color, fill_alpha=0.08)
            else:
                ax.plot([cx - 10, cx, cx + 10], [cy + 8, cy - 8, cy + 8], color=color, lw=1.8)


def draw_venn_teaser(ax, width: int, height: int) -> None:
    colors = ["#3B82F6", "#F59E0B", "#EF4444"]
    cx, cy = width / 2, height * 0.55
    r = min(width, height) * 0.24
    centers = [(cx - r * 0.58, cy - r * 0.25), (cx + r * 0.58, cy - r * 0.25), (cx, cy + r * 0.55)]
    for center, color in zip(centers, colors):
        ax.add_patch(patches.Circle(center, r, facecolor=color, edgecolor=color, lw=1.4, alpha=0.28))
    label(ax, "Shared\nEvidence", cx, cy, size=11, color="#111827", weight="bold")
    for color, (x, y) in zip(colors, centers):
        for dx, dy in [(-36, -18), (0, 26), (38, -2)]:
            icon_circle(ax, x + dx, y + dy, 9, color, fill_alpha=0.18)
    ax.add_patch(
        patches.FancyBboxPatch(
            (width * 0.18, height - 62),
            width * 0.64,
            38,
            boxstyle="round,pad=0,rounding_size=7",
            facecolor="#F8FAFC",
            edgecolor="#A3A3A3",
            lw=1.1,
        )
    )
    label(ax, "Decision = shared + unique", width / 2, height - 43, size=13, color="#111827", weight="bold")


def draw_distribution_triplet(ax, width: int, height: int) -> None:
    colors = ["#60A5FA", "#FBBF24", "#F87171", "#A855F7"]
    panels = 3
    gap = 18
    panel_w = (width - gap * (panels + 1)) / panels
    panel_h = height - 2 * gap
    rng = np.random.default_rng(5)
    for i in range(panels):
        x0 = gap + i * (panel_w + gap)
        y0 = gap
        ax.add_patch(patches.Rectangle((x0, y0), panel_w, panel_h, fill=False, edgecolor="#CBD5E1", lw=1))
        ax.arrow(x0 + 18, y0 + panel_h - 22, panel_w - 40, 0, width=0.0, head_width=7, head_length=8, color="#111827")
        ax.arrow(x0 + 18, y0 + panel_h - 22, 0, -panel_h + 42, width=0.0, head_width=7, head_length=8, color="#111827")
        for k, color in enumerate(colors[: 3 if i < 2 else 4]):
            mx = x0 + panel_w * (0.30 + 0.18 * k) + rng.normal(0, 3)
            my = y0 + panel_h * (0.45 + 0.10 * np.sin(k + i))
            ax.add_patch(
                patches.Ellipse(
                    (mx, my),
                    panel_w * (0.30 - 0.02 * k),
                    panel_h * 0.22,
                    angle=-28 + 24 * k,
                    facecolor=color,
                    edgecolor=color,
                    alpha=0.34,
                    lw=1.1,
                )
            )
        ax.add_patch(patches.Rectangle((x0 + panel_w * 0.60, y0 + 22), panel_w * 0.25, panel_h * 0.28, fill=False, edgecolor="#111827", lw=1.2, linestyle=(0, (4, 4))))


def draw_flow_lane(ax, width: int, height: int) -> None:
    colors = ["#2563EB", "#0F766E", "#F97316"]
    rows = [height * 0.22, height * 0.50, height * 0.78]
    stages = [width * 0.12, width * 0.34, width * 0.58, width * 0.82]
    for row, color in zip(rows, colors):
        for x in stages:
            ax.add_patch(
                patches.FancyBboxPatch(
                    (x - 34, row - 18),
                    68,
                    36,
                    boxstyle="round,pad=0,rounding_size=7",
                    facecolor="white",
                    edgecolor=color,
                    lw=1.4,
                )
            )
        for x1, x2 in zip(stages[:-1], stages[1:]):
            ax.annotate("", xy=(x2 - 42, row), xytext=(x1 + 42, row), arrowprops=dict(arrowstyle="-|>", lw=1.7, color="#111827"))
        ax.add_patch(patches.Rectangle((stages[1] - 24, row - 9), 48, 18, facecolor=color, edgecolor=color, alpha=0.16, hatch="///"))
        ax.add_patch(patches.Rectangle((stages[2] - 24, row - 9), 48, 18, facecolor=color, edgecolor=color, alpha=0.10, hatch="..."))


def save_svg(fig, output: Path, dpi: int) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        output,
        format="svg",
        dpi=dpi,
        transparent=True,
        bbox_inches=None,
        pad_inches=0,
        facecolor="none",
        edgecolor="none",
    )
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Export a fixed-size transparent SVG tile.")
    parser.add_argument("output", type=Path)
    parser.add_argument("--width", type=int, default=420, help="Tile width in pixels.")
    parser.add_argument("--height", type=int, default=240, help="Tile height in pixels.")
    parser.add_argument("--dpi", type=int, default=100)
    parser.add_argument(
        "--example",
        choices=["blank", "line", "heatmap", "icon-card", "venn-teaser", "distribution-triplet", "flow-lane"],
        default="blank",
    )
    args = parser.parse_args()

    fig, ax = make_canvas(args.width, args.height, args.dpi)
    if args.example == "line":
        draw_line(ax, args.width, args.height)
    elif args.example == "heatmap":
        draw_heatmap(ax, args.width, args.height)
    elif args.example == "icon-card":
        draw_icon_card(ax, args.width, args.height)
    elif args.example == "venn-teaser":
        draw_venn_teaser(ax, args.width, args.height)
    elif args.example == "distribution-triplet":
        draw_distribution_triplet(ax, args.width, args.height)
    elif args.example == "flow-lane":
        draw_flow_lane(ax, args.width, args.height)
    else:
        draw_blank(ax, args.width, args.height)
    save_svg(fig, args.output, args.dpi)


if __name__ == "__main__":
    main()
