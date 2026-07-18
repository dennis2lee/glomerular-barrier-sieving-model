# Glomerular barrier sieving model

Code accompanying the manuscript:

**"Passive nanocarriers cannot exploit glomerular barrier permeability to reach
podocytes in chronic kidney disease: a quantitative sieving analysis"**

Submitted to the *Journal of Controlled Release*, Virtual Special Issue "Advancing
Drug Delivery Systems for Chronic and Autoimmune Diseases."

## What this is

Chronic kidney disease is often assumed to open a size-based delivery window for
nanocarriers as the glomerular filtration barrier becomes more permeable with disease
progression. This repository contains the quantitative model used to test that
assumption against published human and rat glomerular sieving data.

The model represents the glomerular barrier as two pore populations, a dominant
restrictive population and a sparse pathological "shunt" population, using size and
density values reported in three independent sieving studies (Scandling and Myers
1992; Tencer et al. 1998; Blouch et al. 1997). It computes, for a ladder of carrier
sizes (a payload-capable metal-organic framework or lipid nanoparticle, an engineered
lipid nanoparticle, an AAV capsid, and albumin as a passing reference), whether each
carrier is excluded at four disease stages spanning healthy kidneys to nephrotic-range
disease.

## Files

- `barrier_model.py` — the size-exclusion model. Running it prints the pore
  parameters, the carrier ladder, and the computed exclusion verdict at each disease
  stage, with no result asserted in advance. It also reproduces every other
  quantitative claim stated in the manuscript text:
  - the 50 to 150 nm carrier range's 4.5x to 13.6x margin against the shunt-pore
    ceiling (manuscript: "oversized by 5 to 15 times"),
  - the Limitations section's electron-microscopy fixation-artifact bound, i.e. how
    much fixation shrinkage would have to inflate reported basement-membrane pore
    sizes (3 to 15 nm) to reach the 50 nm carrier threshold (manuscript: "three to
    sixteen times"),
  - the section 3.4 deformability comparison between the erythrocyte/splenic-slit
    size mismatch and the carrier oversize margin above.
- `make_figure.py` — generates Figure 1 of the manuscript directly from the values in
  `barrier_model.py`, so the figure and the printed verdict cannot silently drift
  apart.
- `figures/` — output directory for the generated figure.
- `requirements.txt` — Python dependencies.

## Running it

```bash
pip install -r requirements.txt
python3 barrier_model.py    # prints the model and its verdict
python3 make_figure.py      # writes figures/fig1_jcr_barrier_exclusion.png
```

## Data sources

All pore-size and pore-density values are taken directly from the published sieving
studies cited in the manuscript's Methods section:

- Scandling JD, Myers BD. Glomerular size-selectivity and microalbuminuria in early
  diabetic glomerular disease. *Kidney Int* 1992;41(4):840-846. PMID 1381005.
- Tencer J, Frick IM, Oquist BW, Alm P, Rippe B. Size-selectivity of the glomerular
  barrier to high molecular weight proteins. *Kidney Int* 1998;53(3):709-715.
  PMID 9507218.
- Blouch K, Deen WM, Fauvel JP, Bialek J, Derby G, Myers BD. Molecular configuration
  and glomerular size selectivity in healthy and nephrotic humans. *Am J Physiol*
  1997;273(3 Pt 2):F430-437. PMID 9321916.
- Yamasaki Y, Makino H, Hironaka K, Hayashi Y, Shikata K, Ota Z. Three-dimensional
  architecture of rat glomerular basement membrane by ultra-high resolution scanning
  electron microscopy. *Acta Med Okayama* 1990;44(6):333-335. PMID 2075832.
- Moreau A, Yaya F, Lu H, et al. Physical mechanisms of red blood cell splenic
  filtration. *Proc Natl Acad Sci U S A* 2023;120(44):e2300095120. PMID 37874856.

Full citations for the manuscript's blood-side barrier anatomy, electron-microscopy,
and receptor-mechanism claims are in the manuscript itself.

## License

MIT. See `LICENSE`.
