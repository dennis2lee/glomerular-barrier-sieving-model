"""
Generates Figure 1 for the manuscript from this repository's barrier_model.py values.

  "Passive nanocarriers cannot exploit glomerular barrier permeability to reach
  podocytes in chronic kidney disease: a quantitative sieving analysis"
"""
from __future__ import annotations

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from barrier_model import R_RESTRICTIVE, R_SHUNT, STAGES, CARRIERS  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.size": 9,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.titlesize": 9,
    "axes.titleweight": "bold",
    "figure.dpi": 300,
})
C_BAD = "#c0392b"
C_BLUE = "#2471a3"


def build():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.0, 3.6),
                                   gridspec_kw={"width_ratios": [1.25, 1.0]})

    R_SMALL, R_LARGE = R_RESTRICTIVE, R_SHUNT
    carrier_colors = {"MOF / LNP (payload-capable)": C_BAD,
                       "engineered LNP (lower bound)": C_BAD,
                       "AAV capsid": "#e67e22",
                       "albumin": "#566573"}
    carriers = [(label.split(" (")[0], r, carrier_colors[label]) for label, r in CARRIERS]

    ax1.axhspan(0, R_SMALL, color="#d6eaf8", zorder=0)
    ax1.axhspan(R_SMALL, R_LARGE, color="#fdebd0", zorder=0)
    ax1.axhline(R_SMALL, color="#2471a3", lw=1.2, ls="-")
    ax1.axhline(R_LARGE, color="#ca6f1e", lw=1.6, ls="-")

    xs = np.arange(len(carriers))
    for xi, (lab, r, col) in zip(xs, carriers):
        ax1.bar(xi, r, 0.5, color=col)
        if r > R_LARGE:
            ax1.text(xi, r * 1.16, f"{r:g} nm\nexcluded", ha="center", va="bottom",
                     fontsize=6.8, color=col, fontweight="bold", linespacing=1.3)
        else:
            ax1.text(xi, r * 1.16, f"{r:g} nm, permitted", ha="center", va="bottom",
                     fontsize=6.8, color=col)

    ax1.text(len(carriers) - 0.55, R_SMALL * 1.06, f"restrictive pore  {R_SMALL} nm",
             fontsize=7, color="#2471a3", ha="left", va="bottom")
    ax1.text(len(carriers) - 0.55, R_LARGE * 1.06, f"large / shunt pore\nceiling  {R_LARGE} nm",
             fontsize=7, color="#ca6f1e", ha="left", va="bottom", fontweight="bold",
             linespacing=1.3)

    ax1.set_xticks(xs)
    ax1.set_xticklabels([c[0] for c in carriers], fontsize=7)
    ax1.set_ylabel("particle / pore radius (nm)")
    ax1.set_yscale("log")
    ax1.set_ylim(1, 130)
    ax1.set_xlim(-0.6, len(carriers) + 0.9)
    ax1.set_title("A  Size ceiling excludes payload carriers at every stage")

    stage_labels = {"healthy": "healthy", "moderate albuminuria": "moderate\nalbuminuria",
                    "macroalbuminuria": "macro-\nalbuminuria", "nephrotic": "nephrotic"}
    stages = [stage_labels[name] for name, _ in STAGES]
    dens = np.array([d for _, d in STAGES])
    size = np.full(len(STAGES), R_LARGE)

    x = np.arange(len(stages))
    ax2.bar(x, dens, 0.55, color=C_BLUE, label="large pore density (rises ~170 fold)")
    ax2.set_yscale("log")
    ax2.set_ylabel("large : small pore number ratio", color=C_BLUE)
    ax2.tick_params(axis="y", labelcolor=C_BLUE)
    ax2.set_xticks(x)
    ax2.set_xticklabels(stages, fontsize=7)
    ax2.set_ylim(1e-7, 1e-3)

    ax2b = ax2.twinx()
    ax2b.plot(x, size, "o--", color=C_BAD, lw=1.8, ms=5,
              label="large pore size (flat)")
    ax2b.set_ylabel("large pore radius (nm)", color=C_BAD)
    ax2b.tick_params(axis="y", labelcolor=C_BAD)
    ax2b.set_ylim(0, 60)
    ax2b.spines["right"].set_visible(True)
    ax2b.axhline(50, color=C_BAD, ls=":", lw=1)
    ax2b.text(2.9, 51, "MOF / LNP needs at least 50 nm", fontsize=6.5, color=C_BAD, ha="right")

    ax2.set_title("B  Disease multiplies pore number, not pore size")
    h1, l1 = ax2.get_legend_handles_labels()
    h2, l2 = ax2b.get_legend_handles_labels()
    ax2.legend(h1 + h2, l1 + l2, frameon=False, fontsize=6.8, loc="upper left")

    fig.suptitle("Figure 1. Passive nanocarriers remain size excluded at every disease stage",
                 fontsize=10.5, fontweight="bold", y=1.02)
    fig.tight_layout()
    p = os.path.join(OUT, "fig1_jcr_barrier_exclusion.png")
    fig.savefig(p, bbox_inches="tight")
    plt.close(fig)
    return p


if __name__ == "__main__":
    p = build()
    print("Figure (JCR submission):", p)
