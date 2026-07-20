"""
Generates Figure 2 and Figure 3 for the manuscript directly from values computed
in barrier_model.py. Unlike an anatomical schematic, every number plotted here is
a value this repository's own model computes at run time, not a hand-placed
illustration.

  "Glomerular barrier permeability and the limits of passive nanocarrier delivery
  to podocytes in chronic kidney disease: a quantitative sieving analysis"

Figure 2: each carrier's margin against two computed ceilings, the urine-side
shunt-pore ceiling (section 3.1-3.2) and the stricter blood-side, GBM-only
ceiling (section 3.3).

Figure 3: the two margins computed in barrier_model.py's VERDICT section that
section 3.4 compares directly, the payload-carrier oversize range and the
erythrocyte/splenic-slit deformability precedent, used to argue that the
deformability rescue argument fails on mechanism, not on scale.
"""
from __future__ import annotations

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from barrier_model import (  # noqa: E402
    R_SHUNT, R_GBM_DISEASED, CARRIERS, CARRIER_RANGE_NM,
    RBC_DIAMETER_UM, SPLENIC_SLIT_WIDTH_UM,
)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.size": 9,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.titlesize": 9,
    "axes.titleweight": "bold",
    "figure.dpi": 500,
})
C_URINE = "#2471a3"
C_BLOOD = "#c0392b"
C_BAD = "#c0392b"
C_NEUTRAL = "#566573"


def build_fig2():
    labels = [name.split(" (")[0] for name, _ in CARRIERS]
    radii = np.array([r for _, r in CARRIERS])
    urine_margin = radii / R_SHUNT
    blood_margin = radii / R_GBM_DISEASED

    fig, ax = plt.subplots(figsize=(7.6, 4.2))
    x = np.arange(len(labels))
    w = 0.35
    ax.bar(x - w / 2, urine_margin, w, color=C_URINE, label=f"urine-side ceiling ({R_SHUNT:g} nm)")
    ax.bar(x + w / 2, blood_margin, w, color=C_BLOOD, label=f"blood-side, GBM-only ceiling ({R_GBM_DISEASED:g} nm)")
    ax.axhline(1.0, color="black", lw=1.0, ls="--")
    ax.text(len(labels) - 0.5, 1.05, "ceiling (margin = 1)", fontsize=7, color="black", ha="right")

    # Exact margin values are given in Table 2 rather than repeated here, so this
    # panel and the table do not duplicate the same numbers (JCR guide: "ensure
    # that any data presented in tables is not duplicating results described
    # elsewhere in the article").

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("margin (carrier radius / ceiling radius)")
    ax.legend(frameon=False, fontsize=7.5, loc="upper left")
    ax.set_ylim(0, max(blood_margin) * 1.35)

    fig.tight_layout()
    p = os.path.join(OUT, "fig2_jcr_two_ceilings.png")
    fig.savefig(p, bbox_inches="tight")
    plt.close(fig)
    return p


def build_fig3():
    lo, hi = CARRIER_RANGE_NM
    carrier_lo, carrier_hi = lo / R_SHUNT, hi / R_SHUNT
    rbc_margin = RBC_DIAMETER_UM / SPLENIC_SLIT_WIDTH_UM

    rows = [
        ("Payload carrier oversize\n(50-150 nm vs 11 nm shunt ceiling)", carrier_lo, carrier_hi, C_URINE),
        ("Erythrocyte / splenic-slit\ndeformability precedent", rbc_margin, rbc_margin, C_BAD),
    ]

    fig, ax = plt.subplots(figsize=(7.2, 2.6))
    y = np.arange(len(rows))
    for yi, (label, lo_v, hi_v, color) in enumerate(rows):
        if lo_v == hi_v:
            ax.plot([lo_v], [yi], "o", color=color, ms=8, zorder=5)
            ax.text(lo_v, yi + 0.26, f"{lo_v:.0f}x", ha="center", fontsize=8, color=color, fontweight="bold")
        else:
            ax.plot([lo_v, hi_v], [yi, yi], "-", color=color, lw=6, solid_capstyle="round", alpha=0.85)
            ax.text((lo_v + hi_v) / 2, yi + 0.26, f"{lo_v:.1f}x - {hi_v:.1f}x", ha="center",
                    fontsize=8, color=color, fontweight="bold")

    ax.set_yticks(y)
    ax.set_yticklabels([r[0] for r in rows], fontsize=8)
    ax.set_xlabel("fold-margin (linear scale)")
    ax.set_xlim(0, 32)
    ax.set_ylim(-0.6, len(rows) - 0.4)

    fig.tight_layout()
    p = os.path.join(OUT, "fig3_jcr_bounding_margins.png")
    fig.savefig(p, bbox_inches="tight")
    plt.close(fig)
    return p


if __name__ == "__main__":
    p2 = build_fig2()
    p3 = build_fig3()
    print("Figure 2 (JCR submission):", p2)
    print("Figure 3 (JCR submission):", p3)
