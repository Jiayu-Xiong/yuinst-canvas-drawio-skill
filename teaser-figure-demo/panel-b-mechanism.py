import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import font_manager
import seaborn as sns

# =========================================================
# 0. 全局可调参数
# =========================================================
np.random.seed(12)
sns.set_theme(style="white")

# ---------- Font ----------
available_fonts = {f.name for f in font_manager.fontManager.ttflist}
FONT_FAMILY = "Bahnschrift"

TITLE_SIZE = 20.5
HEADER_SIZE = 11.4
CARD_LABEL_SIZE = 15
AXIS_LABEL_SIZE = 12
GT_SIZE = 10.6
LEGEND_FONT_SIZE = 12

# ---------- Left draw.io banner ----------
CARD_OUTER_X = 0.10
CARD_OUTER_Y = 0.055
CARD_OUTER_W = 0.80
CARD_OUTER_H = 0.89

CARD_INNER_X = 0.17
CARD_INNER_Y = 0.13
CARD_INNER_W = 0.66
CARD_INNER_H = 0.74

CARD_ICON_Y = 0.66
CARD_TEXT_Y = 0.265
CARD_TEXT_LINE_SPACING = 1.00

# ---------- Legend ----------
LEGEND_X_RIGHT = 0.975
LEGEND_Y_BOTTOM = 0.105
LEGEND_WIDTH = 0.330
LEGEND_LINE_H = 0.100
LEGEND_HEIGHT = None    # 设为数值可手动固定图例总高度，None则自动计算
LEGEND_ALPHA = 0.90

# ---------- Layout ----------
FIG_SIZE = (10.8, 10.8)
TOP = 0.895
BOTTOM = 0.045
LEFT = 0.035
RIGHT = 0.982
WSPACE = 0.025
HSPACE = 0.075

plt.rcParams["font.family"] = FONT_FAMILY
plt.rcParams["font.sans-serif"] = [FONT_FAMILY, "DejaVu Sans", "Arial"]
plt.rcParams["axes.linewidth"] = 0.8
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42
plt.rcParams["svg.fonttype"] = "none"

C = {
    "blue": "#5B7EAA",
    "yellow": "#D8A24A",
    "pink": "#D97A8C",
    "purple": "#8B6BB3",
    "teal": "#0E5A74",
    "red": "#C94F4F",
    "ink": "#26323F",
    "gray": "#8E99A4",

    # draw.io B-column banner colors
    "banner_blue": "#1f5db8",
    "banner_orange": "#d45a00",
    "banner_red": "#b24040",
    "banner_blue_bg": "#f7fbff",
    "banner_orange_bg": "#fff7ed",
    "banner_red_bg": "#fff5f5",
    "banner_outer_bg": "#fbfbfb",
    "banner_border": "#d6d6d6",
}

# =========================================================
# 1. 基础绘图函数
# =========================================================
def sample_gaussian(mean, cov, n=260):
    return np.random.multivariate_normal(mean, cov, n)


def cov_ellipse_params(mean, cov, n_std=2.0):
    vals, vecs = np.linalg.eigh(cov)
    order = vals.argsort()[::-1]
    vals = vals[order]
    vecs = vecs[:, order]
    angle = np.degrees(np.arctan2(vecs[1, 0], vecs[0, 0]))
    width = 2 * n_std * np.sqrt(vals[0])
    height = 2 * n_std * np.sqrt(vals[1])
    return width, height, angle


def setup_dist_ax(ax):
    ax.set_xlim(-2.4, 2.4)
    ax.set_ylim(-2.2, 2.2)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])

    for s in ax.spines.values():
        s.set_visible(False)

    ax.annotate(
        "",
        xy=(2.14, -1.84),
        xytext=(-2.08, -1.84),
        arrowprops=dict(arrowstyle="-|>", lw=1.1, color=C["ink"]),
        clip_on=False,
    )
    ax.annotate(
        "",
        xy=(-1.86, 2.02),
        xytext=(-1.86, -2.02),
        arrowprops=dict(arrowstyle="-|>", lw=1.1, color=C["ink"]),
        clip_on=False,
    )

    ax.text(2.17, -1.93, r"$z_1$", fontsize=AXIS_LABEL_SIZE, color=C["ink"], ha="right", va="top")
    ax.text(-1.96, 2.04, r"$z_2$", fontsize=AXIS_LABEL_SIZE, color=C["ink"], ha="right", va="center")


def draw_cloud(
    ax,
    mean,
    cov,
    color,
    alpha_fill=0.24,
    alpha_pts=0.10,
    n=260,
    lw=1.0,
    z=2,
    edge=True,
):
    pts = sample_gaussian(mean, cov, n)
    ax.scatter(
        pts[:, 0],
        pts[:, 1],
        s=5,
        color=color,
        alpha=alpha_pts,
        linewidths=0,
        zorder=z,
        clip_on=True,
    )

    for nstd, a in [(2.0, alpha_fill), (1.15, alpha_fill * 0.68)]:
        w, h, angle = cov_ellipse_params(mean, cov, n_std=nstd)
        ax.add_patch(
            patches.Ellipse(
                mean,
                w,
                h,
                angle=angle,
                facecolor=color,
                edgecolor=color if edge else "none",
                lw=lw,
                alpha=a,
                zorder=z + 1,
            )
        )


def draw_joint(
    ax,
    mean,
    cov,
    color=C["purple"],
    alpha_fill=0.32,
    alpha_pts=0.16,
    n=300,
    z=7,
):
    pts = sample_gaussian(mean, cov, n)
    ax.scatter(
        pts[:, 0],
        pts[:, 1],
        s=6,
        color=color,
        alpha=alpha_pts,
        linewidths=0,
        zorder=z,
        clip_on=True,
    )

    for nstd, a in [(2.05, alpha_fill), (1.25, alpha_fill * 0.72), (0.65, alpha_fill * 0.55)]:
        w, h, angle = cov_ellipse_params(mean, cov, n_std=nstd)
        ax.add_patch(
            patches.Ellipse(
                mean,
                w,
                h,
                angle=angle,
                facecolor=color,
                edgecolor=color,
                lw=1.15,
                alpha=a,
                zorder=z + 1,
            )
        )


def draw_outline_distribution(
    ax,
    mean,
    cov,
    color,
    lw=2.4,
    ls=(0, (5, 4)),
    alpha=1.0,
    z=30,
):
    w, h, angle = cov_ellipse_params(mean, cov, n_std=1.95)
    ax.add_patch(
        patches.Ellipse(
            mean,
            w,
            h,
            angle=angle,
            facecolor="none",
            edgecolor=color,
            lw=lw,
            linestyle=ls,
            alpha=alpha,
            zorder=z,
        )
    )


def add_gt(ax, xy, w, h, label="GT", label_xy=None):
    rect = patches.FancyBboxPatch(
        xy,
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.04",
        fill=False,
        edgecolor=C["ink"],
        lw=1.55,
        linestyle=(0, (4, 4)),
        zorder=40,
    )
    ax.add_patch(rect)

    if label_xy is None:
        label_xy = (xy[0] + w - 0.03, xy[1] + h + 0.06)

    ax.text(
        label_xy[0],
        label_xy[1],
        label,
        fontsize=GT_SIZE,
        color=C["ink"],
        ha="right",
        va="bottom",
        weight="bold",
        zorder=41,
    )


def add_note(ax, items, x_right=LEGEND_X_RIGHT, y_bottom=LEGEND_Y_BOTTOM):
    items = items[:2]
    width = LEGEND_WIDTH
    height = LEGEND_HEIGHT if LEGEND_HEIGHT is not None else (0.050 + len(items) * LEGEND_LINE_H)

    x0 = x_right - width
    y0 = y_bottom

    bg = patches.FancyBboxPatch(
        (x0, y0),
        width,
        height,
        boxstyle="round,pad=0.010,rounding_size=0.020",
        transform=ax.transAxes,
        facecolor="white",
        edgecolor="#D5D5D5",
        lw=0.65,
        alpha=LEGEND_ALPHA,
        zorder=80,
    )
    ax.add_patch(bg)

    for i, (color, text) in enumerate(items):
        y = y0 + height - 0.030 - i * LEGEND_LINE_H

        ax.add_patch(
            patches.Rectangle(
                (x0 + 0.023, y - 0.008),
                0.024,
                0.016,
                transform=ax.transAxes,
                facecolor=color,
                edgecolor=color,
                lw=0,
                alpha=0.95,
                zorder=81,
            )
        )

        ax.text(
            x0 + 0.072,
            y,
            text,
            transform=ax.transAxes,
            fontsize=LEGEND_FONT_SIZE,
            color=C["ink"],
            ha="left",
            va="center",
            zorder=82,
        )


def draw_arrow_axis(ax):
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.annotate(
        "",
        xy=(0.84, 0.50),
        xytext=(0.16, 0.50),
        arrowprops=dict(arrowstyle="-|>", lw=2.7, color=C["ink"], mutation_scale=20),
    )


# =========================================================
# 2. draw.io B列 banner 风格左侧栏
# =========================================================
def make_icon_axis(parent_ax):
    icon_ax = parent_ax.inset_axes([0.255, 0.535, 0.49, 0.30])
    icon_ax.set_xlim(0, 130)
    icon_ax.set_ylim(120, 0)
    icon_ax.set_aspect("equal")
    icon_ax.axis("off")
    return icon_ax


def draw_drawio_missing_svg(icon_ax):
    color = C["banner_blue"]

    # From embedded draw.io SVG c57:
    # circle cx=65 cy=60 r=38 dash
    icon_ax.add_patch(
        patches.Circle(
            (65, 60),
            38,
            fill=False,
            edgecolor=color,
            lw=5,
            linestyle=(0, (10, 9)),
            capstyle="round",
            joinstyle="round",
        )
    )

    # path: M47 45v28c0 15 36 15 36 0V45
    path = patches.PathPatch(
        patches.Path(
            [
                (47, 45),
                (47, 73),
                (47, 88),
                (83, 88),
                (83, 73),
                (83, 45),
            ],
            [
                patches.Path.MOVETO,
                patches.Path.LINETO,
                patches.Path.CURVE4,
                patches.Path.CURVE4,
                patches.Path.CURVE4,
                patches.Path.LINETO,
            ],
        ),
        fill=False,
        edgecolor=color,
        lw=5,
        capstyle="round",
        joinstyle="round",
    )
    icon_ax.add_patch(path)

    icon_ax.plot([55, 55], [45, 59], color=color, lw=5, solid_capstyle="round")
    icon_ax.plot([75, 75], [45, 59], color=color, lw=5, solid_capstyle="round")

    # path: M48 82c-22 3-16 33 8 25
    p1 = patches.PathPatch(
        patches.Path(
            [(48, 82), (26, 85), (32, 115), (56, 107)],
            [patches.Path.MOVETO, patches.Path.CURVE4, patches.Path.CURVE4, patches.Path.CURVE4],
        ),
        fill=False,
        edgecolor=color,
        lw=5,
        capstyle="round",
        joinstyle="round",
    )
    icon_ax.add_patch(p1)

    # path: M83 82c18 4 13 28-6 25
    p2 = patches.PathPatch(
        patches.Path(
            [(83, 82), (101, 86), (96, 114), (77, 107)],
            [patches.Path.MOVETO, patches.Path.CURVE4, patches.Path.CURVE4, patches.Path.CURVE4],
        ),
        fill=False,
        edgecolor=color,
        lw=5,
        capstyle="round",
        joinstyle="round",
    )
    icon_ax.add_patch(p2)


def draw_drawio_conflict_svg(icon_ax):
    color = C["banner_orange"]

    # From embedded draw.io SVG c68:
    # M22 30c40 0 35 60 82 60
    p1 = patches.PathPatch(
        patches.Path(
            [(22, 30), (62, 30), (57, 90), (104, 90)],
            [patches.Path.MOVETO, patches.Path.CURVE4, patches.Path.CURVE4, patches.Path.CURVE4],
        ),
        fill=False,
        edgecolor=color,
        lw=7,
        capstyle="round",
        joinstyle="round",
    )
    icon_ax.add_patch(p1)

    # M22 90c40 0 35-60 82-60
    p2 = patches.PathPatch(
        patches.Path(
            [(22, 90), (62, 90), (57, 30), (104, 30)],
            [patches.Path.MOVETO, patches.Path.CURVE4, patches.Path.CURVE4, patches.Path.CURVE4],
        ),
        fill=False,
        edgecolor=color,
        lw=7,
        capstyle="round",
        joinstyle="round",
    )
    icon_ax.add_patch(p2)

    # Arrow heads
    icon_ax.plot([95, 115, 95], [18, 30, 42], color=color, lw=7, solid_capstyle="round", solid_joinstyle="round")
    icon_ax.plot([95, 115, 95], [78, 90, 102], color=color, lw=7, solid_capstyle="round", solid_joinstyle="round")


def draw_drawio_rigid_svg(icon_ax):
    color = C["banner_red"]

    # Main strokes from embedded draw.io SVG c79
    icon_ax.plot([35, 110], [95, 95], color=color, lw=6, solid_capstyle="round")
    icon_ax.plot([73, 73], [28, 95], color=color, lw=6, solid_capstyle="round")
    icon_ax.plot([58, 88], [28, 28], color=color, lw=6, solid_capstyle="round")
    icon_ax.plot([48, 98], [44, 44], color=color, lw=6, solid_capstyle="round")
    icon_ax.plot([51, 95], [61, 61], color=color, lw=6, solid_capstyle="round")

    # Rectangles from SVG
    icon_ax.add_patch(
        patches.Rectangle((28, 84), 28, 22, facecolor=color, edgecolor="none", alpha=0.22)
    )
    icon_ax.add_patch(
        patches.Rectangle((84, 12), 18, 18, facecolor=color, edgecolor="none", alpha=0.70)
    )
    icon_ax.add_patch(
        patches.Rectangle((88, 34), 12, 12, facecolor=color, edgecolor="none", alpha=0.70)
    )


def draw_source_card_drawio(ax, row_id):
    """
    Match draw.io B-column banner:
    outer card: 120x220, #fbfbfb, #d6d6d6
    inner card: 100x200, color-coded
    icon: embedded SVG-like vector
    text: bold multiline
    """
    configs = {
        1: {
            "label": "1. Missing\nmodality /\ndistribution\nshift",
            "color": C["banner_blue"],
            "bg": C["banner_blue_bg"],
            "icon": draw_drawio_missing_svg,
        },
        2: {
            "label": "2. Objective\nconflict",
            "color": C["banner_orange"],
            "bg": C["banner_orange_bg"],
            "icon": draw_drawio_conflict_svg,
        },
        3: {
            "label": "3. Rigid\nequal-length\nalignment",
            "color": C["banner_red"],
            "bg": C["banner_red_bg"],
            "icon": draw_drawio_rigid_svg,
        },
    }

    cfg = configs[row_id]
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Outer banner
    ax.add_patch(
        patches.FancyBboxPatch(
            (CARD_OUTER_X, CARD_OUTER_Y),
            CARD_OUTER_W,
            CARD_OUTER_H,
            boxstyle="round,pad=0.012,rounding_size=0.055",
            facecolor=C["banner_outer_bg"],
            edgecolor=C["banner_border"],
            lw=1.0,
        )
    )

    # Inner colored banner
    ax.add_patch(
        patches.FancyBboxPatch(
            (CARD_INNER_X, CARD_INNER_Y),
            CARD_INNER_W,
            CARD_INNER_H,
            boxstyle="round,pad=0.012,rounding_size=0.050",
            facecolor=cfg["bg"],
            edgecolor="none",
            lw=0,
        )
    )

    # SVG icon, drawn as vector
    icon_ax = make_icon_axis(ax)
    cfg["icon"](icon_ax)

    # Text
    ax.text(
        0.50,
        CARD_TEXT_Y,
        cfg["label"],
        fontsize=CARD_LABEL_SIZE,
        color=cfg["color"],
        ha="center",
        va="center",
        weight="bold",
        linespacing=CARD_TEXT_LINE_SPACING,
    )


# =========================================================
# 3. 分布参数
# =========================================================
BLUE_MEAN = (-0.72, 0.62)
BLUE_COV = np.array([[0.30, -0.10], [-0.10, 0.54]])

YELLOW_MEAN = (0.58, 0.55)
YELLOW_COV = np.array([[0.46, 0.12], [0.12, 0.31]])

PINK_MEAN = (-0.03, -0.30)
PINK_COV = np.array([[0.56, 0.10], [0.10, 0.34]])

GT3_XY = (-1.02, 0.22)
GT3_W = 1.38
GT3_H = 1.05

M1_MEAN = (-0.72, 0.50)
M1_COV = np.array([[0.45, -0.12], [-0.12, 0.42]])

M2_MEAN = (0.68, 0.34)
M2_COV = np.array([[0.43, 0.10], [0.10, 0.32]])

ALIGN_MEAN = (-0.02, 0.34)
ALIGN_COV = np.array([[0.16, 0.02], [0.02, 0.11]])

GT2_XY = (0.10, 0.18)
GT2_W = 1.28
GT2_H = 0.98

GT1_XY = (0.20, 0.00)
GT1_W = 1.12
GT1_H = 0.88


# =========================================================
# 4. 三行内容
# =========================================================
def draw_three_modal_base(ax, fade=False):
    setup_dist_ax(ax)

    ab, pb = (0.28, 0.10)
    if fade:
        ab, pb = (0.05, 0.02)

    draw_cloud(ax, BLUE_MEAN, BLUE_COV, C["blue"], ab, pb, z=2)
    draw_cloud(ax, YELLOW_MEAN, YELLOW_COV, C["yellow"], 0.28, 0.10, z=3)
    draw_cloud(ax, PINK_MEAN, PINK_COV, C["pink"], 0.28, 0.10, z=4)

    draw_joint(
        ax,
        mean=(-0.22, 0.52),
        cov=np.array([[0.18, 0.03], [0.03, 0.12]]),
        color=C["purple"],
        alpha_fill=0.14,
        alpha_pts=0.06,
        n=110,
        z=7,
    )

    add_gt(ax, GT3_XY, GT3_W, GT3_H)


def row1_unimodal(ax):
    draw_three_modal_base(ax, fade=False)
    add_note(ax, [(C["blue"], "unique"), (C["purple"], "joint")])


def row1_mechanism(ax):
    draw_three_modal_base(ax, fade=True)

    ax.add_patch(
        patches.Circle(
            (-0.88, 0.92),
            0.20,
            fill=False,
            edgecolor=C["blue"],
            lw=1.9,
            linestyle="--",
            zorder=30,
        )
    )
    ax.plot([-1.01, -0.75], [0.79, 1.05], color=C["blue"], lw=2.2, zorder=31)
    ax.plot([-1.01, -0.75], [1.05, 0.79], color=C["blue"], lw=2.2, zorder=31)

    add_note(ax, [(C["blue"], "missing"), (C["ink"], "GT fixed")])


def row1_result(ax):
    setup_dist_ax(ax)

    draw_cloud(ax, YELLOW_MEAN, YELLOW_COV, C["yellow"], 0.13, 0.040, z=2)
    draw_cloud(ax, PINK_MEAN, PINK_COV, C["pink"], 0.13, 0.040, z=2)

    add_gt(ax, GT3_XY, GT3_W, GT3_H)

    ax.add_patch(
        patches.FancyBboxPatch(
            (-0.84, 0.72),
            0.50,
            0.35,
            boxstyle="round,pad=0.01,rounding_size=0.03",
            facecolor="white",
            edgecolor=C["blue"],
            lw=1.0,
            linestyle=(0, (3, 3)),
            alpha=0.70,
            zorder=42,
        )
    )

    shifted_mean = (0.54, 0.02)
    shifted_cov = np.array([[0.30, 0.13], [0.13, 0.20]])
    draw_joint(ax, shifted_mean, shifted_cov, color=C["purple"], alpha_fill=0.34, alpha_pts=0.14, n=280)

    old_center = (-0.36, 0.72)
    ax.scatter([old_center[0]], [old_center[1]], s=34, color=C["ink"], alpha=0.72, zorder=43)
    ax.annotate(
        "",
        xy=shifted_mean,
        xytext=old_center,
        arrowprops=dict(arrowstyle="->", lw=2.0, linestyle=(0, (3, 3)), color=C["purple"]),
    )

    add_note(ax, [(C["blue"], "blank"), (C["purple"], "shifted")])


def draw_two_modal_base(ax, show_gt=True, show_align=True):
    setup_dist_ax(ax)

    draw_cloud(ax, M1_MEAN, M1_COV, C["blue"], 0.31, 0.10, z=2)
    draw_cloud(ax, M2_MEAN, M2_COV, C["pink"], 0.31, 0.10, z=3)

    if show_align:
        draw_outline_distribution(ax, ALIGN_MEAN, ALIGN_COV, C["yellow"], lw=2.4, z=32)

    if show_gt:
        add_gt(ax, GT2_XY, GT2_W, GT2_H)


def row2_unimodal(ax):
    draw_two_modal_base(ax, show_gt=True, show_align=True)
    add_note(ax, [(C["yellow"], "intersect"), (C["ink"], "unique")])


def row2_mechanism(ax):
    draw_two_modal_base(ax, show_gt=True, show_align=True)

    ax.annotate(
        "",
        xy=(-0.12, 0.38),
        xytext=(-0.88, 0.58),
        arrowprops=dict(arrowstyle="-|>", lw=3.3, color=C["yellow"]),
        zorder=36,
    )
    ax.annotate(
        "",
        xy=(0.10, 0.32),
        xytext=(0.72, 0.34),
        arrowprops=dict(arrowstyle="-|>", lw=3.3, color=C["yellow"]),
        zorder=36,
    )

    task_origin = (0.05, 0.34)
    for p in [(0.52, 0.52), (0.82, 0.92), (1.16, 0.62)]:
        ax.annotate(
            "",
            xy=p,
            xytext=task_origin,
            arrowprops=dict(arrowstyle="-|>", lw=2.5, color=C["blue"]),
            zorder=37,
        )

    add_note(ax, [(C["yellow"], "align"), (C["blue"], "task")])


def row2_result(ax):
    setup_dist_ax(ax)

    add_gt(ax, GT2_XY, GT2_W, GT2_H)

    disturbed_mean = ALIGN_MEAN
    disturbed_cov = np.array([[0.20, 0.02], [0.02, 0.13]])
    draw_joint(ax, disturbed_mean, disturbed_cov, color=C["purple"], alpha_fill=0.36, alpha_pts=0.16, n=300)

    draw_outline_distribution(ax, disturbed_mean, disturbed_cov, C["yellow"], lw=2.3, alpha=0.85, z=32)

    ax.add_patch(
        patches.FancyBboxPatch(
            (0.72, 0.56),
            0.43,
            0.32,
            boxstyle="round,pad=0.01,rounding_size=0.03",
            facecolor="white",
            edgecolor=C["purple"],
            lw=1.15,
            linestyle=(0, (3, 3)),
            alpha=0.72,
            zorder=45,
        )
    )

    add_note(ax, [(C["purple"], "aligned"), (C["ink"], "GT gap")])


def row3_unimodal(ax):
    setup_dist_ax(ax)

    rich_mean = (0.15, 0.40)
    rich_cov = np.array([[0.74, 0.28], [0.28, 0.36]])
    draw_cloud(ax, rich_mean, rich_cov, C["blue"], 0.27, 0.11, n=300)
    add_gt(ax, GT1_XY, GT1_W, GT1_H)

    for i in range(8):
        ax.add_patch(
            patches.FancyBboxPatch(
                (-1.62 + i * 0.17, 1.42),
                0.12,
                0.09,
                boxstyle="round,pad=0.005,rounding_size=0.015",
                facecolor=C["blue"],
                edgecolor=C["blue"],
                alpha=0.72,
            )
        )

    add_note(ax, [(C["blue"], "rich 2D"), (C["ink"], "GT")])


def row3_mechanism(ax):
    setup_dist_ax(ax)

    rich_mean = (0.15, 0.40)
    rich_cov = np.array([[0.74, 0.28], [0.28, 0.36]])
    draw_cloud(ax, rich_mean, rich_cov, C["blue"], 0.10, 0.035, n=230)
    add_gt(ax, GT1_XY, GT1_W, GT1_H)

    line_x = np.linspace(-1.30, 1.52, 100)
    line_y = 0.23 + 0.35 * line_x
    ax.plot(line_x, line_y, color=C["red"], lw=3.2, alpha=0.86, zorder=30)

    for x0 in [-0.85, -0.25, 0.35, 0.95]:
        y_line = 0.23 + 0.35 * x0
        ax.annotate(
            "",
            xy=(x0, y_line),
            xytext=(x0 - 0.18, y_line + 0.55),
            arrowprops=dict(arrowstyle="->", lw=2.2, color=C["red"], alpha=0.92),
            zorder=31,
        )
        ax.annotate(
            "",
            xy=(x0, y_line),
            xytext=(x0 + 0.18, y_line - 0.55),
            arrowprops=dict(arrowstyle="->", lw=2.2, color=C["red"], alpha=0.92),
            zorder=31,
        )

    add_note(ax, [(C["red"], "reduce"), (C["gray"], "cue loss")])


def row3_result(ax):
    setup_dist_ax(ax)

    reduced_mean = (0.82, 0.52)
    reduced_cov = np.array([[0.58, 0.38], [0.38, 0.28]])
    draw_joint(ax, reduced_mean, reduced_cov, color=C["purple"], alpha_fill=0.34, alpha_pts=0.13, n=300)

    band_mean = (0.15, -0.22)
    band_cov = np.array([[0.72, 0.43], [0.43, 0.28]])
    draw_cloud(ax, band_mean, band_cov, C["purple"], 0.10, 0.055, n=140, z=4, edge=False)

    add_gt(ax, (0.42, 0.22), 1.00, 0.78)

    add_note(ax, [(C["purple"], "thin"), (C["ink"], "partial")])


# =========================================================
# 5. Figure layout
# =========================================================
fig = plt.figure(figsize=FIG_SIZE, facecolor="none")
fig.patch.set_alpha(0.0)

gs = fig.add_gridspec(
    nrows=4,
    ncols=6,
    height_ratios=[0.12, 1, 1, 1],
    width_ratios=[0.66, 1.15, 0.15, 1.15, 0.15, 1.15],
    left=LEFT,
    right=RIGHT,
    top=TOP,
    bottom=BOTTOM,
    wspace=WSPACE,
    hspace=HSPACE,
)

# ---------- Title ----------
badge_x, badge_y, badge_s = 0.040, 0.925, 0.030
fig.patches.append(
    patches.FancyBboxPatch(
        (badge_x, badge_y),
        badge_s,
        badge_s,
        boxstyle="round,pad=0.003,rounding_size=0.004",
        transform=fig.transFigure,
        facecolor=C["teal"],
        edgecolor="none",
        zorder=100,
    )
)
fig.text(
    badge_x + badge_s / 2,
    badge_y + badge_s / 2,
    "B",
    color="white",
    fontsize=15,
    weight="bold",
    ha="center",
    va="center",
    zorder=101,
)
fig.text(
    0.095,
    0.942,
    "How fusion disturbs the joint distribution",
    fontsize=TITLE_SIZE,
    color=C["ink"],
    weight="bold",
    ha="left",
    va="center",
)

# ---------- Headers ----------
header_axes = [
    fig.add_subplot(gs[0, 0]),
    fig.add_subplot(gs[0, 1]),
    fig.add_subplot(gs[0, 3]),
    fig.add_subplot(gs[0, 5]),
]
headers = [
    "Disturbance source",
    "Unimodal distributions",
    "Disturbance mechanism",
    "Disturbed joint distribution",
]
for axh, h in zip(header_axes, headers):
    axh.axis("off")
    axh.text(
        0.50,
        0.45,
        h,
        ha="center",
        va="center",
        fontsize=HEADER_SIZE,
        color=C["ink"],
        weight="bold",
    )

for c in [2, 4]:
    axh = fig.add_subplot(gs[0, c])
    axh.axis("off")

# ---------- Row 1 ----------
ax11 = fig.add_subplot(gs[1, 0])
draw_source_card_drawio(ax11, 1)
ax12 = fig.add_subplot(gs[1, 1])
row1_unimodal(ax12)
ax1a = fig.add_subplot(gs[1, 2])
draw_arrow_axis(ax1a)
ax13 = fig.add_subplot(gs[1, 3])
row1_mechanism(ax13)
ax1b = fig.add_subplot(gs[1, 4])
draw_arrow_axis(ax1b)
ax14 = fig.add_subplot(gs[1, 5])
row1_result(ax14)

# ---------- Row 2 ----------
ax21 = fig.add_subplot(gs[2, 0])
draw_source_card_drawio(ax21, 2)
ax22 = fig.add_subplot(gs[2, 1])
row2_unimodal(ax22)
ax2a = fig.add_subplot(gs[2, 2])
draw_arrow_axis(ax2a)
ax23 = fig.add_subplot(gs[2, 3])
row2_mechanism(ax23)
ax2b = fig.add_subplot(gs[2, 4])
draw_arrow_axis(ax2b)
ax24 = fig.add_subplot(gs[2, 5])
row2_result(ax24)

# ---------- Row 3 ----------
ax31 = fig.add_subplot(gs[3, 0])
draw_source_card_drawio(ax31, 3)
ax32 = fig.add_subplot(gs[3, 1])
row3_unimodal(ax32)
ax3a = fig.add_subplot(gs[3, 2])
draw_arrow_axis(ax3a)
ax33 = fig.add_subplot(gs[3, 3])
row3_mechanism(ax33)
ax3b = fig.add_subplot(gs[3, 4])
draw_arrow_axis(ax3b)
ax34 = fig.add_subplot(gs[3, 5])
row3_result(ax34)

# ---------- Row boxes ----------
for row_axes in [
    [ax11, ax12, ax1a, ax13, ax1b, ax14],
    [ax21, ax22, ax2a, ax23, ax2b, ax24],
    [ax31, ax32, ax3a, ax33, ax3b, ax34],
]:
    x0 = min(ax.get_position().x0 for ax in row_axes)
    y0 = min(ax.get_position().y0 for ax in row_axes)
    x1 = max(ax.get_position().x1 for ax in row_axes)
    y1 = max(ax.get_position().y1 for ax in row_axes)

    rect = patches.FancyBboxPatch(
        (x0 - 0.006, y0 - 0.007),
        (x1 - x0) + 0.012,
        (y1 - y0) + 0.014,
        transform=fig.transFigure,
        boxstyle="round,pad=0.002,rounding_size=0.006",
        facecolor=(1, 1, 1, 0.0),
        edgecolor=(0.86, 0.86, 0.86, 1.0),
        lw=0.8,
        zorder=-10,
    )
    fig.patches.append(rect)

plt.savefig("panel-b-mechanism.png", dpi=300, bbox_inches="tight", facecolor="none", transparent=True)
plt.savefig("panel-b-mechanism.pdf", bbox_inches="tight", facecolor="none", transparent=True)
plt.savefig("panel-b-mechanism.svg", bbox_inches="tight", facecolor="none", transparent=True)
plt.show()
