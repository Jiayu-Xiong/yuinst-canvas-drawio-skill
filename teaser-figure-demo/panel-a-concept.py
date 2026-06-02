import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from matplotlib.patches import Circle, Rectangle, FancyBboxPatch, Polygon, Arc
from matplotlib.path import Path
from matplotlib.patches import PathPatch

# ============================================================
# Canvas
# ============================================================
W, H = 600, 800
DPI = 100
GRID = 10

sns.set_theme(style="white")

plt.rcParams["font.family"] = ["Bahnschrift", "DejaVu Sans"]
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42

fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI)
fig.patch.set_alpha(0.0)

ax = plt.axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.set_aspect("equal")
ax.axis("off")
ax.set_facecolor((1, 1, 1, 0))


# ============================================================
# Palette
# ============================================================
BLUE = "#2F86A6"        # 晴山蓝
ORANGE = "#F2B33D"      # 橙黄
PINK = "#D85C7A"        # 桃红
DECISION = "#B0A4E3"    # 雪青色
INK = "#183040"
GRAY = "#66717C"
SHARED = "#6B5846"

MODALITIES = {
    "Visual": {
        "color": BLUE,
        "main": "image",
        "unique_icons": ["cube", "palette", "texture", "motion"],
    },
    "Audio": {
        "color": ORANGE,
        "main": "speaker",
        "unique_icons": ["note", "bars", "mic", "metronome"],
    },
    "Text": {
        "color": PINK,
        "main": "text",
        "unique_icons": ["aa", "tree", "book", "globe"],
    },
}

# shared 只画弱共享线索，不画 Object / Category / Decision
SHARED_ICONS = ["clock", "link", "eye", "overlap"]


# ============================================================
# Helpers
# ============================================================
def snap(v):
    return round(v / GRID) * GRID


def label(text, x, y, size=9, color=INK, weight="regular",
          ha="center", va="center", alpha=1.0, z=80):
    size = size * 1.20
    ax.text(
        snap(x), snap(y), text,
        fontsize=size,
        color=color,
        fontweight=weight,
        ha=ha,
        va=va,
        alpha=alpha,
        zorder=z,
    )


def round_box(x, y, w, h, color, alpha=0.08, lw=1.0, r=10, z=1):
    p = FancyBboxPatch(
        (snap(x), snap(y)),
        snap(w),
        snap(h),
        boxstyle=f"round,pad=0,rounding_size={r}",
        facecolor=color,
        edgecolor=color,
        linewidth=lw,
        alpha=alpha,
        zorder=z,
    )
    ax.add_patch(p)
    return p


def line(x1, y1, x2, y2, color=INK, lw=1.2, alpha=1.0, ls="-", z=20):
    ax.plot(
        [snap(x1), snap(x2)],
        [snap(y1), snap(y2)],
        color=color,
        lw=lw,
        alpha=alpha,
        ls=ls,
        zorder=z,
    )


# ============================================================
# Icon library
# ============================================================
def icon(name, cx, cy, s=24, color=INK, lw=1.6, alpha=1.0, z=90):
    cx, cy = snap(cx), snap(cy)
    h = s / 2

    if name == "image":
        ax.add_patch(Rectangle(
            (cx - h, cy - h), s, s,
            fill=False, edgecolor=color, linewidth=lw, alpha=alpha, zorder=z
        ))
        ax.add_patch(Circle(
            (cx + 0.25 * s, cy + 0.25 * s), 0.08 * s,
            fill=False, edgecolor=color, linewidth=lw, alpha=alpha, zorder=z
        ))
        ax.add_patch(Polygon(
            [(cx - 0.42*s, cy - 0.35*s),
             (cx - 0.15*s, cy + 0.02*s),
             (cx + 0.02*s, cy - 0.35*s)],
            fill=False, closed=False, edgecolor=color, linewidth=lw, alpha=alpha, zorder=z
        ))
        ax.add_patch(Polygon(
            [(cx - 0.02*s, cy - 0.35*s),
             (cx + 0.18*s, cy + 0.08*s),
             (cx + 0.42*s, cy - 0.35*s)],
            fill=False, closed=False, edgecolor=color, linewidth=lw, alpha=alpha, zorder=z
        ))

    elif name == "wave":
        xs = np.linspace(cx - h, cx + h, 80)
        ys = cy + np.sin(np.linspace(0, 2*np.pi, 80)) * 0.18*s
        ax.plot(xs, ys, color=color, lw=lw, alpha=alpha, zorder=z)

    elif name == "text":
        ax.add_patch(Rectangle(
            (cx - 0.38*s, cy - 0.48*s), 0.76*s, 0.96*s,
            fill=False, edgecolor=color, linewidth=lw, alpha=alpha, zorder=z
        ))
        for i in range(4):
            yy = cy + 0.25*s - i * 0.17*s
            line(cx - 0.22*s, yy, cx + 0.22*s, yy,
                 color=color, lw=lw*0.7, alpha=alpha, z=z)

    elif name == "texture":
        q = s / 4
        for i in range(3):
            for j in range(3):
                x = cx - 0.36*s + i*q
                y = cy - 0.36*s + j*q
                if (i + j) % 2 == 0:
                    ax.add_patch(Rectangle(
                        (x, y), q, q,
                        facecolor=color, edgecolor=color,
                        lw=0.4, alpha=0.55*alpha, zorder=z
                    ))
                else:
                    ax.add_patch(Rectangle(
                        (x, y), q, q,
                        fill=False, edgecolor=color,
                        lw=lw*0.55, alpha=alpha, zorder=z
                    ))

    elif name == "cube":
        front = [
            (cx - 0.30*s, cy - 0.18*s),
            (cx + 0.05*s, cy - 0.34*s),
            (cx + 0.34*s, cy - 0.12*s),
            (cx - 0.02*s, cy + 0.08*s),
        ]
        top = [
            (cx - 0.30*s, cy - 0.18*s),
            (cx - 0.02*s, cy + 0.10*s),
            (cx + 0.30*s, cy + 0.26*s),
            (cx + 0.05*s, cy - 0.34*s),
        ]
        side = [
            (cx - 0.02*s, cy + 0.08*s),
            (cx + 0.30*s, cy + 0.26*s),
            (cx + 0.34*s, cy - 0.12*s),
            (cx + 0.05*s, cy - 0.34*s),
        ]
        for pts in [front, top, side]:
            ax.add_patch(Polygon(
                pts,
                fill=False,
                closed=True,
                edgecolor=color,
                linewidth=lw,
                alpha=alpha,
                zorder=z,
            ))

    elif name == "palette":
        ax.add_patch(Circle(
            (cx, cy),
            0.34*s,
            fill=False,
            edgecolor=color,
            linewidth=lw,
            alpha=alpha,
            zorder=z,
        ))
        ax.add_patch(Circle(
            (cx + 0.17*s, cy - 0.12*s),
            0.09*s,
            facecolor="white",
            edgecolor=color,
            linewidth=lw*0.65,
            alpha=alpha,
            zorder=z,
        ))
        for dx, dy in [(-0.12, 0.12), (0.08, 0.18), (-0.20, -0.06)]:
            ax.add_patch(Circle(
                (cx + dx*s, cy + dy*s),
                0.055*s,
                facecolor=color,
                edgecolor=color,
                alpha=alpha,
                zorder=z,
            ))

    elif name == "edge":
        pts = [
            (cx - 0.42*s, cy - 0.18*s),
            (cx - 0.18*s, cy + 0.24*s),
            (cx + 0.02*s, cy - 0.10*s),
            (cx + 0.20*s, cy + 0.22*s),
            (cx + 0.42*s, cy - 0.18*s),
        ]
        ax.plot(
            [p[0] for p in pts],
            [p[1] for p in pts],
            color=color,
            lw=lw,
            alpha=alpha,
            zorder=z,
        )

    elif name == "depth":
        for dx, dy in [(0, 0), (0.12*s, 0.12*s), (0.24*s, 0.24*s)]:
            ax.add_patch(Rectangle(
                (cx - 0.36*s + dx, cy - 0.32*s + dy),
                0.5*s,
                0.5*s,
                fill=False,
                edgecolor=color,
                linewidth=lw*0.75,
                alpha=alpha,
                zorder=z,
            ))

    elif name == "motion":
        path = Path(
            [
                (cx - 0.40*s, cy - 0.18*s),
                (cx - 0.10*s, cy + 0.28*s),
                (cx + 0.34*s, cy + 0.02*s),
            ],
            [Path.MOVETO, Path.CURVE3, Path.CURVE3],
        )
        ax.add_patch(PathPatch(
            path,
            fill=False,
            edgecolor=color,
            lw=lw,
            alpha=alpha,
            zorder=z,
        ))
        ax.add_patch(Polygon(
            [
                (cx + 0.34*s, cy + 0.02*s),
                (cx + 0.22*s, cy + 0.08*s),
                (cx + 0.24*s, cy - 0.04*s),
            ],
            closed=True,
            facecolor=color,
            edgecolor=color,
            alpha=alpha,
            zorder=z,
        ))

    elif name == "note":
        line(cx + 0.10*s, cy - 0.25*s, cx + 0.10*s, cy + 0.35*s,
             color=color, lw=lw, alpha=alpha, z=z)
        line(cx + 0.10*s, cy + 0.35*s, cx + 0.36*s, cy + 0.25*s,
             color=color, lw=lw, alpha=alpha, z=z)
        ax.add_patch(Circle(
            (cx - 0.12*s, cy - 0.25*s),
            0.16*s,
            fill=False,
            edgecolor=color,
            linewidth=lw,
            alpha=alpha,
            zorder=z,
        ))

    elif name == "bars":
        heights = [0.28, 0.48, 0.75, 0.42]
        for i, hh in enumerate(heights):
            x = cx - 0.34*s + i * 0.20*s
            ax.add_patch(Rectangle(
                (x, cy - 0.36*s),
                0.12*s,
                hh*s,
                facecolor=color,
                edgecolor=color,
                lw=0.4,
                alpha=0.75*alpha,
                zorder=z,
            ))

    elif name == "metronome":
        ax.add_patch(Polygon(
            [
                (cx - 0.28*s, cy - 0.36*s),
                (cx + 0.28*s, cy - 0.36*s),
                (cx + 0.12*s, cy + 0.34*s),
                (cx - 0.12*s, cy + 0.34*s),
            ],
            fill=False,
            closed=True,
            edgecolor=color,
            linewidth=lw,
            alpha=alpha,
            zorder=z,
        ))
        line(cx, cy - 0.25*s, cx + 0.18*s, cy + 0.22*s,
             color=color, lw=lw, alpha=alpha, z=z)
        ax.add_patch(Circle(
            (cx + 0.18*s, cy + 0.22*s),
            0.055*s,
            facecolor=color,
            edgecolor=color,
            alpha=alpha,
            zorder=z,
        ))

    elif name == "timbre":
        xs = np.linspace(cx - 0.44*s, cx + 0.44*s, 80)
        ys = np.sin(np.linspace(0, 4*np.pi, 80)) * 0.13*s
        ys += np.sin(np.linspace(0, 8*np.pi, 80)) * 0.05*s
        ax.plot(xs, cy + ys, color=color, lw=lw, alpha=alpha, zorder=z)

    elif name == "speaker":
        ax.add_patch(Polygon(
            [
                (cx - 0.38*s, cy - 0.12*s),
                (cx - 0.16*s, cy - 0.12*s),
                (cx + 0.06*s, cy - 0.30*s),
                (cx + 0.06*s, cy + 0.30*s),
                (cx - 0.16*s, cy + 0.12*s),
                (cx - 0.38*s, cy + 0.12*s),
            ],
            fill=False,
            closed=True,
            edgecolor=color,
            linewidth=lw,
            alpha=alpha,
            zorder=z,
        ))
        ax.add_patch(Arc(
            (cx + 0.10*s, cy),
            0.42*s,
            0.42*s,
            theta1=-40,
            theta2=40,
            color=color,
            lw=lw*0.8,
            alpha=alpha,
            zorder=z,
        ))
        ax.add_patch(Arc(
            (cx + 0.15*s, cy),
            0.68*s,
            0.68*s,
            theta1=-38,
            theta2=38,
            color=color,
            lw=lw*0.65,
            alpha=alpha,
            zorder=z,
        ))

    elif name == "mic":
        ax.add_patch(FancyBboxPatch(
            (cx - 0.16*s, cy - 0.08*s),
            0.32*s,
            0.42*s,
            boxstyle=f"round,pad=0,rounding_size={0.10*s}",
            fill=False,
            edgecolor=color,
            linewidth=lw,
            alpha=alpha,
            zorder=z,
        ))
        ax.add_patch(Arc(
            (cx, cy - 0.04*s),
            0.58*s,
            0.55*s,
            theta1=205,
            theta2=335,
            color=color,
            lw=lw,
            alpha=alpha,
            zorder=z,
        ))
        line(cx, cy - 0.32*s, cx, cy - 0.48*s,
             color=color, lw=lw, alpha=alpha, z=z)
        line(cx - 0.22*s, cy - 0.48*s, cx + 0.22*s, cy - 0.48*s,
             color=color, lw=lw, alpha=alpha, z=z)

    elif name == "book":
        ax.add_patch(PathPatch(
            Path(
                [
                    (cx - 0.42*s, cy + 0.32*s),
                    (cx - 0.12*s, cy + 0.22*s),
                    (cx, cy + 0.30*s),
                    (cx + 0.12*s, cy + 0.22*s),
                    (cx + 0.42*s, cy + 0.32*s),
                    (cx + 0.42*s, cy - 0.28*s),
                    (cx + 0.12*s, cy - 0.20*s),
                    (cx, cy - 0.28*s),
                    (cx - 0.12*s, cy - 0.20*s),
                    (cx - 0.42*s, cy - 0.28*s),
                    (cx - 0.42*s, cy + 0.32*s),
                ],
                [Path.MOVETO] + [Path.LINETO] * 10,
            ),
            fill=False,
            edgecolor=color,
            lw=lw,
            alpha=alpha,
            zorder=z,
        ))
        line(cx, cy + 0.28*s, cx, cy - 0.28*s,
             color=color, lw=lw*0.75, alpha=alpha, z=z)

    elif name == "aa":
        label("Aa", cx, cy, size=s*0.65, color=color, weight="bold", z=z)

    elif name == "tree":
        pts = [
            (cx, cy + 0.30*s),
            (cx - 0.28*s, cy - 0.18*s),
            (cx, cy - 0.18*s),
            (cx + 0.28*s, cy - 0.18*s),
        ]
        for p in pts[1:]:
            line(pts[0][0], pts[0][1], p[0], p[1],
                 color=color, lw=lw*0.65, alpha=alpha, z=z)
        for p in pts:
            ax.add_patch(Circle(
                p,
                0.065*s,
                facecolor=color,
                edgecolor=color,
                alpha=alpha,
                zorder=z,
            ))

    elif name == "pen":
        line(cx - 0.30*s, cy - 0.28*s, cx + 0.25*s, cy + 0.25*s,
             color=color, lw=lw, alpha=alpha, z=z)
        ax.add_patch(Polygon(
            [
                (cx + 0.22*s, cy + 0.30*s),
                (cx + 0.36*s, cy + 0.36*s),
                (cx + 0.30*s, cy + 0.20*s),
            ],
            fill=False,
            closed=True,
            edgecolor=color,
            linewidth=lw,
            alpha=alpha,
            zorder=z,
        ))

    elif name == "globe":
        ax.add_patch(Circle(
            (cx, cy),
            0.36*s,
            fill=False,
            edgecolor=color,
            linewidth=lw,
            alpha=alpha,
            zorder=z,
        ))
        ax.add_patch(Arc(
            (cx, cy),
            0.52*s,
            0.72*s,
            theta1=90,
            theta2=270,
            color=color,
            lw=lw*0.65,
            alpha=alpha,
            zorder=z,
        ))
        ax.add_patch(Arc(
            (cx, cy),
            0.52*s,
            0.72*s,
            theta1=-90,
            theta2=90,
            color=color,
            lw=lw*0.65,
            alpha=alpha,
            zorder=z,
        ))
        line(cx - 0.30*s, cy, cx + 0.30*s, cy,
             color=color, lw=lw*0.65, alpha=alpha, z=z)

    elif name == "clock":
        ax.add_patch(Circle(
            (cx, cy),
            0.36*s,
            fill=False,
            edgecolor=color,
            linewidth=lw,
            alpha=alpha,
            zorder=z,
        ))
        line(cx, cy, cx, cy + 0.18*s, color=color, lw=lw, alpha=alpha, z=z)
        line(cx, cy, cx + 0.16*s, cy - 0.10*s, color=color, lw=lw, alpha=alpha, z=z)

    elif name == "link":
        ax.add_patch(Arc(
            (cx - 0.12*s, cy),
            0.44*s,
            0.28*s,
            theta1=60,
            theta2=300,
            color=color,
            lw=lw,
            alpha=alpha,
            zorder=z,
        ))
        ax.add_patch(Arc(
            (cx + 0.12*s, cy),
            0.44*s,
            0.28*s,
            theta1=-120,
            theta2=120,
            color=color,
            lw=lw,
            alpha=alpha,
            zorder=z,
        ))

    elif name == "eye":
        path = Path(
            [
                (cx - 0.42*s, cy),
                (cx - 0.20*s, cy + 0.24*s),
                (cx, cy + 0.28*s),
                (cx + 0.20*s, cy + 0.24*s),
                (cx + 0.42*s, cy),
                (cx + 0.20*s, cy - 0.24*s),
                (cx, cy - 0.28*s),
                (cx - 0.20*s, cy - 0.24*s),
                (cx - 0.42*s, cy),
            ],
            [Path.MOVETO] + [Path.CURVE3] * 8,
        )
        ax.add_patch(PathPatch(
            path,
            fill=False,
            edgecolor=color,
            lw=lw,
            alpha=alpha,
            zorder=z,
        ))
        ax.add_patch(Circle(
            (cx, cy),
            0.10*s,
            fill=False,
            edgecolor=color,
            linewidth=lw,
            alpha=alpha,
            zorder=z,
        ))

    elif name == "overlap":
        ax.add_patch(Circle(
            (cx - 0.10*s, cy),
            0.25*s,
            fill=False,
            edgecolor=color,
            linewidth=lw,
            alpha=alpha,
            zorder=z,
        ))
        ax.add_patch(Circle(
            (cx + 0.10*s, cy),
            0.25*s,
            fill=False,
            edgecolor=color,
            linewidth=lw,
            alpha=alpha,
            zorder=z,
        ))


# ============================================================
# Top modality cards
# ============================================================
def draw_icon_card(name, x, y, w=180, h=162):
    cfg = MODALITIES[name]
    c = cfg["color"]

    # title outside card, so card contains icons only
    label(name, x + w / 2, y + h + 18, size=15.5, color=c, weight="bold")

    round_box(x, y, w, h, c, alpha=0.075, lw=1.0, r=14, z=1)

    # left: modality icon in a separated badge
    ax.add_patch(Circle(
        (snap(x + 43), snap(y + 100)),
        32,
        facecolor=(1, 1, 1, 0),
        edgecolor=c,
        linewidth=1.5,
        alpha=0.25,
        zorder=3,
    ))
    icon(cfg["main"], x + 43, y + 100, s=42, color=c, lw=2.35, z=50)

    # right: four representative modality cues, spaced as a clean 2x2 group
    cue_positions = [
        (x + 100, y + 122),
        (x + 145, y + 122),
        (x + 100, y + 82),
        (x + 145, y + 82),
    ]
    for (ix, iy), ic in zip(cue_positions, cfg["unique_icons"]):
        ax.add_patch(Circle(
            (snap(ix), snap(iy)),
            19,
            facecolor="white",
            edgecolor=c,
            linewidth=0.9,
            alpha=0.28,
            zorder=3,
        ))
        icon(ic, ix, iy, s=27, color=c, lw=2.0, z=50)

    # shared cues appear inside every modality, separated from modality-specific cues
    for ix, iy, ic in zip(
        [x + 50, x + 80, x + 110, x + 140],
        [y + 28, y + 28, y + 28, y + 28],
        SHARED_ICONS,
    ):
        ax.add_patch(Circle(
            (snap(ix), snap(iy)),
            12,
            facecolor="white",
            edgecolor=SHARED,
            linewidth=0.8,
            alpha=0.22,
            zorder=3,
        ))
        icon(ic, ix, iy, s=18, color=SHARED, lw=1.25, alpha=0.95, z=50)


draw_icon_card("Visual", 20, 600)
draw_icon_card("Audio", 210, 600)
draw_icon_card("Text", 400, 600)


# ============================================================
# Main Venn
# ============================================================
label("Evidence distribution", 300, 572, size=17, color=INK, weight="bold")

CX, CY = 300, 300
R = 165

V_CENTER = (220, 360)
A_CENTER = (380, 360)
T_CENTER = (300, 220)

# decision support circle behind Venn
ax.add_patch(Circle(
    (CX, CY - 12),
    180,
    facecolor=DECISION,
    edgecolor=DECISION,
    linewidth=2.1,
    linestyle=(0, (8, 5)),
    alpha=0.12,
    zorder=3,
))

ax.add_patch(Circle(
    (CX, CY - 12),
    180,
    fill=False,
    edgecolor=DECISION,
    linewidth=2.1,
    linestyle=(0, (8, 5)),
    alpha=0.95,
    zorder=15,
))

# modality circles
for name, center in [
    ("Visual", V_CENTER),
    ("Audio", A_CENTER),
    ("Text", T_CENTER),
]:
    color = MODALITIES[name]["color"]

    ax.add_patch(Circle(
        center,
        R,
        facecolor=color,
        edgecolor=color,
        linewidth=2.2,
        alpha=0.30,
        zorder=5,
    ))

    ax.add_patch(Circle(
        center,
        R,
        fill=False,
        edgecolor=color,
        linewidth=2.2,
        alpha=0.98,
        zorder=8,
    ))

# ============================================================
# Venn icons only, no text inside Venn
# ============================================================

# Shared points: strictly inside all three circles
shared_points = [
    (280, 350),
    (320, 350),
    (285, 315),
    (315, 315),
]
for ic, (x, y) in zip(SHARED_ICONS, shared_points):
    icon(ic, x, y, s=38, color=SHARED, lw=2.0, alpha=0.95, z=70)

# Visual-specific safe points: inside V only, outside A/T
visual_points = [
    (110, 415),
    (105, 355),
    (135, 300),
    (180, 470),
]
for ic, (x, y) in zip(MODALITIES["Visual"]["unique_icons"], visual_points):
    icon(ic, x, y, s=46, color=BLUE, lw=2.35, z=70)

# Audio-specific safe points: inside A only, outside V/T
audio_points = [
    (490, 415),
    (495, 355),
    (465, 300),
    (420, 470),
]
for ic, (x, y) in zip(MODALITIES["Audio"]["unique_icons"], audio_points):
    icon(ic, x, y, s=46, color=ORANGE, lw=2.35, z=70)

# Text-specific safe points: inside T only, outside V/A
text_points = [
    (245, 135),
    (355, 135),
    (220, 200),
    (380, 200),
]
for ic, (x, y) in zip(MODALITIES["Text"]["unique_icons"], text_points):
    icon(ic, x, y, s=46, color=PINK, lw=2.35, z=70)


# ============================================================
# Venn explanation texts outside the Venn
# Moved to lower-left and lower-right to fill empty regions
# ============================================================
label("Visual circle", 65, 552, size=9.8, color=BLUE, weight="bold", ha="left", z=95)
label("visual-specific cues", 65, 535, size=8.0, color=BLUE, ha="left", z=95)

label("Audio circle", 430, 552, size=9.8, color=ORANGE, weight="bold", ha="left", z=95)
label("audio-specific cues", 430, 535, size=8.0, color=ORANGE, ha="left", z=95)

label("Text circle", 40, 118, size=9.8, color=PINK, weight="bold", ha="left", z=95)
label("text-specific cues", 40, 101, size=8.0, color=PINK, ha="left", z=95)

# Small external labels for shared and decision ring
label("weak shared cues", 300, 495, size=10.8, color=SHARED, weight="bold")


# ============================================================
# Detailed legend, vertical unboxed column on the right
# ============================================================
legend_items = [
    (BLUE, "visual", 470, 160),
    (ORANGE, "audio", 470, 136),
    (PINK, "text", 470, 112),
    (SHARED, "shared", 470, 88),
    (DECISION, "decision support", 470, 64),
]

for color, txt, x, y in legend_items:
    ax.add_patch(Circle(
        (snap(x), snap(y)),
        5,
        facecolor=color,
        edgecolor=color,
        alpha=0.95,
        zorder=90,
    ))
    label(txt, x + 12, y, size=7.8, color=color, weight="bold", ha="left")


# ============================================================
# Export
# ============================================================
plt.savefig(
    "panel-a-concept.png",
    dpi=DPI,
    transparent=True,
    bbox_inches=None,
    pad_inches=0,
)

plt.savefig(
    "panel-a-concept.svg",
    transparent=True,
    bbox_inches=None,
    pad_inches=0,
)

plt.close(fig)

print("Saved: panel-a-concept.png")
print("Saved: panel-a-concept.svg")
