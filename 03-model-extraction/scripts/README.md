# Stage 3 — Effect-size scripts

Pipeline that turns per-paper extracted estimates into the rendered matrix
tables in `../3L-models.html`. Every cell shows its native metric (B / OR /
RR / d / β<sub>std</sub>) plus a derived Cohen's d for cross-paper visual
comparison.

## Files

| file | purpose |
|---|---|
| `effect_sizes.py` | Pure conversion functions (B → d, OR → d, RR → d, passthrough, std-β → d). No I/O. |
| `test_effect_sizes.py` | Unit tests against published reference values (`unittest`, no deps). |
| `paper_<id>.json` | Inputs for one paper: per-model IV/DV axes, sample SDs, native estimates, baseline rates p₀ where applicable. |
| `build_matrices.py` | Reads every `paper_*.json`, computes d (and CI) per cell, writes one HTML snippet per model to `out/`. |
| `out/` | Generated HTML snippets, ready to paste into `../3L-models.html`. Not edited by hand. |

## How to run

```bash
cd 03-model-extraction/scripts
python3 -m unittest test_effect_sizes -v   # run tests; should report 22 OK
python3 build_matrices.py                  # regenerate out/*.html
```

Then paste each `out/paper_<id>__<model>.html` into the corresponding
`<table class="matrix...">…</table>` block in `../3L-models.html`.

## Conversion formulas

All formulas are encoded in `effect_sizes.py` and exercised by
`test_effect_sizes.py`.

| native | conversion | reference |
|---|---|---|
| B (continuous IV → continuous DV) | β<sub>std</sub> = B · SD<sub>IV</sub> / SD<sub>DV</sub>; d = 2β<sub>std</sub> / √(1 − β<sub>std</sub>²) | Borenstein, Hedges, Higgins, Rothstein (2009), *Introduction to Meta-Analysis*, eq 7.1 |
| OR | d = ln(OR) · √3/π | Chinn (2000), *Stat. Med.* 19:3127–3131 |
| RR | OR = RR · (1 − p₀) / (1 − RR · p₀); then OR → d | derived from definitions of RR and OR |
| Cohen's d (paper-reported) | passthrough | — |
| standardized β | treat as r; d = 2r / √(1 − r²) | Borenstein et al. 2009 |

## Caveats (also encoded as `_*_note` keys in the JSON files)

- **r ≈ β<sub>std</sub>** — In multivariable regression, β<sub>std</sub> is not exactly the partial r. The approximation is the standard meta-analytic move and is fine for visual comparison.
- **Chinn's constant** — assumes the latent continuous variable underlying the binary DV is logistic. Normal latent gives ~0.55 instead of 0.5513 (1 % difference).
- **CI on d** — endpoint conversion (pivotal CI). For very small samples, a delta-method SE on d would differ slightly. We are not computing meta-analytic standard errors; the d CI is for visual scale.
- **RR conversion needs p₀** — If a paper only prints a marginal sample base rate, we use that as an approximation when exposure prevalence is < ~10 %. Always recorded in the JSON's DV axis as `p0` plus a `_p0_note`.

## Cell display convention

In `3L-models.html`, derived d values are always rendered as `d ≈ X.XXX`
(with the ≈ symbol) in purple, beneath a dotted divider. Paper-reported d
values appear as `d = X.XX` (with `=` and no ≈) in the cell's main line.
This makes it impossible to mistake a derived value for a paper-reported
value at a glance.

## Adding a new paper

1. Create `paper_<id>.json` mirroring the structure of `paper_394.json` (one model with continuous-IV linear regression) or `paper_156.json` (two models, one passthrough d, one RR with p₀ on each DV).
2. `python3 build_matrices.py` to regenerate `out/`.
3. Paste the generated `out/paper_<id>__<model>.html` into `../3L-models.html` inside the paper's `<div class="matrix-wrap">…</div>` block, replacing any prior placeholder/table.
4. Update the surrounding `<div class="label-meta">` to describe the metric and the conversion (see paper 394's label as a template).
