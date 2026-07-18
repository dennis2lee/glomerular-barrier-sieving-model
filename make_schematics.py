"""
Generates Figure 2 and Figure 3 for the manuscript: schematic diagrams of the
glomerular barrier's two distinct routes, and of the AAV capsid uptake mechanism
these routes imply.

  "Passive nanocarriers cannot exploit glomerular barrier permeability to reach
  podocytes in chronic kidney disease: a quantitative sieving analysis"

These are anatomical/mechanistic schematics, not to scale, illustrating the
argument made quantitatively in sections 3.1-3.3 and barrier_model.py. Layer
pore-size labels are taken directly from the values and citations in the
manuscript (Methods 2.3, Results 3.3).
"""
from __future__ import annotations

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrow, FancyBboxPatch, Circle, FancyArrowPatch
from matplotlib.lines import Line2D

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.size": 9,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.spines.left": False,
    "axes.spines.bottom": False,
    "figure.dpi": 300,
})

C_BLUE = "#2471a3"
C_ORANGE = "#ca6f1e"
C_BAD = "#c0392b"
C_GOOD = "#1e8449"
C_GRAY = "#566573"


def _layer(ax, x0, x1, y0, y1, color, label, sublabel=None):
    box = FancyBboxPatch((x0, y0), x1 - x0, y1 - y0,
                          boxstyle="round,pad=0.01,rounding_size=0.02",
                          linewidth=1.0, edgecolor=color, facecolor=color, alpha=0.18)
    ax.add_patch(box)
    ax.text((x0 + x1) / 2, y1 - 0.35, label, ha="center", va="top",
            fontsize=8, fontweight="bold", color=color, linespacing=1.3)
    if sublabel:
        ax.text((x0 + x1) / 2, y0 + 0.35, sublabel, ha="center", va="bottom",
                fontsize=6.8, color=color, linespacing=1.3)


def build_fig2():
    fig, ax = plt.subplots(figsize=(9.2, 5.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7.2)
    ax.axis("off")

    ax.text(1.4, 7.0, "blood (capillary lumen)", fontsize=8.5, color=C_GRAY, ha="left")
    ax.text(8.6, 7.0, "urinary space", fontsize=8.5, color=C_GRAY, ha="right")

    box_y0, box_y1 = 3.2, 6.5
    _layer(ax, 1.2, 3.4, box_y0, box_y1, C_BLUE, "fenestrated\nendothelium", "70-100 nm,\nno diaphragm")
    _layer(ax, 3.6, 5.6, box_y0, box_y1, C_ORANGE, "glomerular\nbasement membrane", "mesh pores\n~3-15 nm")
    _layer(ax, 5.8, 7.6, box_y0, box_y1, C_BAD, "podocyte foot process\n+ slit diaphragm", "restrictive ~5.6 nm\nshunt ~11 nm")

    for x in (1.2, 3.4, 3.6, 5.6, 5.8, 7.6):
        ax.plot([x, x], [box_y0, 2.6], color="#cccccc", lw=0.6, ls=":", zorder=0)

    y_urine = 2.2
    ax.annotate("", xy=(9.3, y_urine), xytext=(0.9, y_urine),
                arrowprops=dict(arrowstyle="-|>", color=C_GRAY, lw=1.8))
    ax.text(0.9, y_urine + 0.22, "urine-side route (Scandling, Tencer, Blouch sieving coefficient): crosses all 3 layers",
            fontsize=7.2, color=C_GRAY, ha="left", va="bottom")

    y_blood = 0.9
    ax.annotate("", xy=(6.7, y_blood), xytext=(0.9, y_blood),
                arrowprops=dict(arrowstyle="-|>", color=C_BLUE, lw=2.2))
    ax.text(0.9, y_blood + 0.22,
            "blood-to-podocyte route (section 3.3): fenestra + GBM only, bypasses the slit diaphragm",
            fontsize=7.2, color=C_BLUE, ha="left", va="bottom", fontweight="bold")
    ax.plot([6.7], [y_blood], marker="o", ms=7, color=C_BLUE, zorder=5)
    ax.text(6.7, y_blood - 0.55, "podocyte\nabluminal surface", fontsize=6.5, color=C_BLUE,
            ha="center", va="top", linespacing=1.3)

    fig.suptitle("Figure 2. Two distinct routes cross different numbers of barrier layers",
                 fontsize=10.5, fontweight="bold", y=0.98)
    fig.tight_layout()
    p = os.path.join(OUT, "fig2_jcr_barrier_anatomy.png")
    fig.savefig(p, bbox_inches="tight")
    plt.close(fig)
    return p


def build_fig3():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.8, 5.2))
    for ax in (ax1, ax2):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6.6)
        ax.axis("off")

    box_y0, box_y1 = 2.6, 5.4
    for ax in (ax1, ax2):
        _layer(ax, 0.6, 2.9, box_y0, box_y1, C_BLUE, "fenestra", "70-100 nm")
        _layer(ax, 3.1, 5.6, box_y0, box_y1, C_ORANGE, "GBM mesh", "~9-15 nm\n(disease range)")

    y_track = 1.6

    ax1.text(5.0, 6.1, "✗", fontsize=22, ha="center", color=C_BAD, fontweight="bold")
    ax1.set_title("A  Passive size-based leakage (not observed)", fontsize=8.6, color=C_BAD, pad=14)
    cap = Circle((1.75, y_track), 0.22, facecolor="#e67e22", edgecolor="black", lw=0.8, zorder=5)
    ax1.add_patch(cap)
    ax1.text(1.75, y_track - 0.55, "AAV capsid\n~12.5 nm", fontsize=6.8, ha="center", va="top",
             color="#a04000", linespacing=1.3)
    ax1.annotate("", xy=(4.3, y_track), xytext=(2.05, y_track),
                 arrowprops=dict(arrowstyle="-|>", color=C_GRAY, lw=1.6))
    cap2 = Circle((4.5, y_track), 0.22, facecolor="#e67e22", edgecolor="black", lw=0.8, zorder=5)
    ax1.add_patch(cap2)
    ax1.text(4.5, y_track + 0.55, "lodges in GBM mesh\n(passive size ceiling)", fontsize=7.0,
             ha="center", va="bottom", color=C_BAD, fontweight="bold", linespacing=1.3)

    _layer(ax2, 5.8, 8.9, box_y0, box_y1, C_BAD, "podocyte foot process", "AAVR / KIAA0319L\n+ co-receptor")
    ax2.text(7.35, 6.1, "✓", fontsize=22, ha="center", color=C_GOOD, fontweight="bold")
    ax2.set_title("B  Receptor-mediated uptake (consistent with observed transduction)",
                  fontsize=8.6, color=C_GOOD, pad=14)
    cap3 = Circle((1.75, y_track), 0.22, facecolor="#e67e22", edgecolor="black", lw=0.8, zorder=5)
    ax2.add_patch(cap3)
    ax2.text(1.75, y_track - 0.55, "AAV capsid\n~12.5 nm", fontsize=6.8, ha="center", va="top",
             color="#a04000", linespacing=1.3)
    ax2.annotate("", xy=(7.2, y_track), xytext=(2.05, y_track),
                 arrowprops=dict(arrowstyle="-|>", color=C_GOOD, lw=1.8))
    cap4 = Circle((7.35, y_track), 0.2, facecolor="#e67e22", edgecolor="black", lw=0.8, zorder=6)
    ax2.add_patch(cap4)
    ax2.text(7.35, y_track + 0.55, "receptor-mediated entry\n(AAVR-dependent uptake)", fontsize=7.0,
             ha="center", va="bottom", color=C_GOOD, fontweight="bold", linespacing=1.3)

    fig.suptitle("Figure 3. AAV podocyte transduction is consistent with receptor-mediated\n"
                 "uptake, not passive size-based leakage across the GBM",
                 fontsize=10.2, fontweight="bold", y=1.04)
    fig.tight_layout()
    p = os.path.join(OUT, "fig3_jcr_aav_mechanism.png")
    fig.savefig(p, bbox_inches="tight")
    plt.close(fig)
    return p


if __name__ == "__main__":
    p2 = build_fig2()
    p3 = build_fig3()
    print("Figure 2 (JCR submission):", p2)
    print("Figure 3 (JCR submission):", p3)
