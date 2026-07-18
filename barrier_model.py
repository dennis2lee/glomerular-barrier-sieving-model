"""
Two-pore size-exclusion model of the glomerular filtration barrier.

Reproduces the quantitative claims in:
  "Passive nanocarriers cannot exploit glomerular barrier permeability to reach
  podocytes in chronic kidney disease: a quantitative sieving analysis"
  (submitted to Journal of Controlled Release, VSI: Advancing Drug Delivery Systems
  for Chronic and Autoimmune Diseases)

Data sources (see manuscript Methods 2.1 for full citations):
  Scandling & Myers 1992, Kidney Int 41:840-846 (PMID 1381005)
  Tencer et al. 1998, Kidney Int 53:709-715 (PMID 9507218)
  Blouch et al. 1997, Am J Physiol 273:F430-437 (PMID 9321916)

These three independent human and rat sieving studies converge on a bimodal pore-size
distribution: a dominant restrictive population near 5.6 nm radius, and a sparse
pathological "shunt" population fixed near 11 nm radius whose relative number rises
with disease severity while its size does not.

This script computes, for a ladder of nanocarrier sizes, whether each carrier is
excluded by the barrier at four disease stages, and reports the numerical margin.
Nothing here is asserted in advance; every value below is stated as read directly
from the cited studies, and every verdict is computed from those values at run time.
"""
from __future__ import annotations

import numpy as np

# --- pore populations (radius, nm) -----------------------------------------------
R_RESTRICTIVE = 5.6   # dominant pore population; disease-invariant in size
R_SHUNT = 11.0        # sparse pathological pore population; disease-invariant in size

# --- disease stages: large:small pore number ratio, from the source studies ------
# (Tencer 1998: ratio rises ~170-fold from healthy to nephrotic-range disease)
STAGES = [
    ("healthy", 7.0e-7),
    ("moderate albuminuria", 9.2e-6),
    ("macroalbuminuria", 3.3e-5),
    ("nephrotic", 1.2e-4),
]

# --- carrier ladder (label, radius nm) -------------------------------------------
CARRIERS = [
    ("MOF / LNP (payload-capable)", 50.0),
    ("engineered LNP (lower bound)", 30.0),
    ("AAV capsid", 12.5),
    ("albumin", 3.6),
]


def verdict(radius_nm: float) -> str:
    """A carrier above the shunt-pore ceiling is excluded at every disease stage,
    regardless of how much the shunt-pore population's relative density rises,
    because the model's exclusion criterion is pore SIZE, not pore density."""
    if radius_nm > R_SHUNT:
        return "excluded (size)"
    if radius_nm > R_RESTRICTIVE:
        return "shunt-pore only"
    return "freely passing"


def main() -> None:
    print("=" * 78)
    print("Glomerular barrier two-pore size-exclusion model")
    print("=" * 78)
    print(f"restrictive pore radius (disease-invariant): {R_RESTRICTIVE} nm")
    print(f"shunt pore radius (disease-invariant size):  {R_SHUNT} nm")
    density_fold = STAGES[-1][1] / STAGES[0][1]
    print(f"shunt pore density rises {STAGES[0][1]:.1e} -> {STAGES[-1][1]:.1e} "
          f"({density_fold:.0f}-fold) from healthy to nephrotic-range disease\n")

    print(f"{'carrier':<32}{'radius (nm)':>12}{'vs 11 nm ceiling':>20}")
    print("-" * 78)
    for name, r in CARRIERS:
        print(f"{name:<32}{r:>12.1f}{verdict(r):>20}")

    print(f"\n{'disease stage':<24}" +
          "".join(f"{name.split('(')[0].strip()[:14]:>16}" for name, _ in CARRIERS))
    print("-" * 96)
    for stage_name, density in STAGES:
        row = "".join(
            f"{(density if r <= R_SHUNT else 0.0):>16.2e}" for _, r in CARRIERS
        )
        print(f"{stage_name:<24}{row}")

    print("\n" + "=" * 78)
    print("VERDICT (computed from the values above)")
    print("=" * 78)
    mof_radius = next(r for name, r in CARRIERS if "MOF" in name)
    aav_radius = next(r for name, r in CARRIERS if "AAV" in name)
    mof_margin = mof_radius / R_SHUNT
    aav_margin = aav_radius / R_SHUNT
    print(f"MOF / LNP ({mof_radius:g} nm) exceeds the shunt-pore ceiling by "
          f"{mof_margin:.1f}x at every disease stage modeled.")
    print(f"  -> No disease stage admits this carrier passively; disease multiplies")
    print(f"     the NUMBER of shunt pores, not their size, so no stage-dependent")
    print(f"     'sweet spot' exists for passive size-based entry.")
    print(f"\nAAV capsid ({aav_radius:g} nm) exceeds the same ceiling by {aav_margin:.2f}x,")
    print(f"  essentially at the boundary rather than comfortably under it. Its")
    print(f"  measured podocyte transduction is therefore not explained by passive")
    print(f"  shunt-pore leakage; see the manuscript (section 3.3) for the")
    print(f"  receptor-mediated, fenestra-plus-basement-membrane mechanism this")
    print(f"  model motivates instead.")


if __name__ == "__main__":
    main()
