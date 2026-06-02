from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns

sns.set_theme(style="white")

OUT_DIR = Path(__file__).resolve().parents[1] / "input-tiles"
OUT_DIR.mkdir(parents=True, exist_ok=True)

COLORS = {
    "A": {
        "main": "#2F6FB6",
        "light": "#EAF2FF",
        "mid": "#8FB8E8",
    },
    "B": {
        "main": "#2B9A9A",
        "light": "#E9F7F7",
        "mid": "#84CACA",
    },
    "C": {
        "main": "#F06A4A",
        "light": "#FFF0EC",
        "mid": "#FFAD9A",
    },
    "gray": "#8A8A8A",
    "gray_light": "#F5F5F5",
}


def setup_canvas(width=100, height=80):
    fig = plt.figure(figsize=(width / 100, height / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)
    return fig, ax


def save_svg(fig, path):
    fig.savefig(
        path,
        format="svg",
        transparent=True,
        bbox_inches="tight",
        pad_inches=0,
    )
    plt.close(fig)


def rounded_box(ax, x, y, w, h, edge, face, lw=2, radius=10):
    box = patches.FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        linewidth=lw,
        edgecolor=edge,
        facecolor=face,
    )
    ax.add_patch(box)
    return box


def draw_waveform_icon(ax, cx, cy, color):
    xs = np.array([-22, -16, -10, -4, 2, 8, 14, 20])
    heights = np.array([8, 15, 24, 34, 28, 18, 12, 7])
    for x, h in zip(xs, heights):
        ax.plot(
            [cx + x, cx + x],
            [cy - h / 2, cy + h / 2],
            color=color,
            lw=3,
            solid_capstyle="round",
        )
    ax.plot([cx - 28, cx - 25], [cy, cy], color=color, lw=3, solid_capstyle="round")
    ax.plot([cx + 25, cx + 28], [cy, cy], color=color, lw=3, solid_capstyle="round")


def draw_image_icon(ax, cx, cy, color):
    rounded_box(
        ax,
        cx - 24,
        cy - 20,
        48,
        40,
        edge=color,
        face="white",
        lw=2,
        radius=4,
    )
    ax.add_patch(
        patches.Circle(
            (cx - 12, cy + 8),
            5,
            facecolor=color,
            edgecolor="none",
            alpha=0.85,
        )
    )
    mountain = patches.Polygon(
        [
            (cx - 22, cy - 16),
            (cx - 6, cy + 2),
            (cx + 3, cy - 8),
            (cx + 13, cy + 5),
            (cx + 23, cy - 16),
        ],
        closed=True,
        facecolor=color,
        edgecolor="none",
        alpha=0.75,
    )
    ax.add_patch(mountain)


def draw_text_icon(ax, cx, cy, color):
    rounded_box(
        ax,
        cx - 20,
        cy - 24,
        40,
        48,
        edge=COLORS["gray"],
        face="white",
        lw=2,
        radius=3,
    )
    ax.plot(
        [cx + 11, cx + 20, cx + 20],
        [cy + 24, cy + 15, cy + 24],
        color=COLORS["gray"],
        lw=1.6,
    )
    ax.text(
        cx,
        cy,
        "T",
        ha="center",
        va="center",
        fontsize=26,
        fontweight="bold",
        color=color,
        family="DejaVu Sans",
    )


def draw_modality_icon(modality, save_name):
    color = COLORS[modality]["main"]
    light = COLORS[modality]["light"]

    fig, ax = setup_canvas(120, 100)

    rounded_box(
        ax,
        2,
        2,
        116,
        96,
        edge=color,
        face=light,
        lw=2,
        radius=12,
    )

    if modality == "A":
        draw_waveform_icon(ax, 60, 58, color)
    elif modality == "B":
        draw_image_icon(ax, 60, 58, color)
    elif modality == "C":
        draw_text_icon(ax, 60, 58, color)

    ax.text(
        60,
        24,
        f"Modality {modality}",
        ha="center",
        va="center",
        fontsize=14,
        fontweight="bold",
        color=color,
        family="DejaVu Sans",
    )

    save_svg(fig, OUT_DIR / save_name)


def draw_vector_icon(modality, save_name):
    color = COLORS[modality]["main"]
    mid = COLORS[modality]["mid"]

    fig, ax = setup_canvas(30, 40)

    rounded_box(
        ax,
        1,
        1,
        28,
        38,
        edge="#8A8A8A",
        face="#F7F7F7",
        lw=1.4,
        radius=5,
    )

    ys = [30, 20, 10]
    for y in ys:
        ax.add_patch(
            patches.Circle(
                (15, y),
                4.8,
                facecolor=mid,
                edgecolor=color,
                linewidth=1.2,
            )
        )

    save_svg(fig, OUT_DIR / save_name)


draw_modality_icon("A", "input-card-a.svg")
draw_vector_icon("A", "vector-token-a.svg")

draw_modality_icon("B", "input-card-b.svg")
draw_vector_icon("B", "vector-token-b.svg")

draw_modality_icon("C", "input-card-c.svg")
draw_vector_icon("C", "vector-token-c.svg")

print(f"Saved SVG files to: {OUT_DIR}")
