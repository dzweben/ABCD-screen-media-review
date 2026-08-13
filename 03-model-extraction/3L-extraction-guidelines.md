# Stage 3 Extraction Guidelines — Phone/SM Models from INCLUDE Papers

These rules govern what gets extracted from each of the 72 INCLUDE papers and how it is structured in `3L-models.html`. They are derived from iterative review of paper 394 (Nagata 2024, BMC Public Health) as the calibration case.

---

## 1. What counts as "a model"

A *model* is **one analytical specification that produces an estimate** — defined by the combination of:

- **Analytical class** — regression (linear, logistic, multilevel, mixed-effects, GEE), structural equation model (SEM, CLPM, mediation path model), machine-learning fit (XGBoost / random forest / Lasso with specific hyperparameters and feature importance method), factor analysis (EFA, CFA, group factor analysis), network analysis (graphical lasso, GVAR, mixed graphical), causal inference framework (target trial emulation, propensity matching, instrumental variable, Mendelian randomization), Bayesian hierarchical model, or any other formal analytical recipe
- **Analytic sample** — N, age range, subgrouping
- **Design** — cross-sectional vs. longitudinal; if longitudinal, the wave structure and whether the outcome is a single follow-up or repeated measures
- **Equation or specification form** — the structural relationship being estimated, including which variables enter as IVs, DVs, mediators, moderators, or controls
- **Set of covariates / adjustment variables**
- **Random effects, weighting, multiple-comparison correction, software**

When a paper applies a single analytical specification to multiple IV / DV combinations — same sample, same controls, same procedure — that is **one model**, not many. Document the model once and present the per-combination estimates as a results matrix with one cell per (IV × DV).

If a paper genuinely contains two distinct citable analyses (e.g., a longitudinal mixed-effects regression and a separate cross-sectional SEM, both used by the authors to support claims), each gets its own model card.

---

## 2. Which model to extract — the spec the paper uses to interpret *this finding*

For each phone/SM finding the paper reports, extract the analytical specification the paper itself uses to characterize and interpret that finding.

This is **not** the same as "the model central to the paper." Many of our INCLUDE papers were brought in because they finally isolated a phone/SM variable in a side analysis, supplementary table, or sensitivity model — not because phone/SM was the paper's central thesis. The phone/SM finding may be peripheral to the paper, but the model the authors apply to that peripheral finding is still what we extract.

The principle: **for each phone/SM estimate the paper reports, capture the analytical specification the authors use when they interpret it.**

Practical applications:

- **Stepwise / hierarchical model-building.** If the paper builds Model 1 → Model 2 → Model 3 and interprets Model 3 (the "final model") in the discussion, extract Model 3. The earlier steps are model-development scaffolding, not findings.
- **Adjusted alongside unadjusted.** If a results table shows an unadjusted Model 1 next to an adjusted Model 2 and the authors anchor their claims to the adjusted version, extract Model 2 only. The unadjusted version is a transparency artifact.
- **Side or supplementary analyses.** If the qualifying phone/SM estimate comes from a supplementary analysis (e.g., a per-modality breakout in a sensitivity table) and the authors discuss that estimate, extract the analytical specification of that supplementary analysis — not the headline analysis the paper is built around.
- **Sensitivity-only models reported but not referenced.** If a sensitivity model is mentioned narratively as "results similar after adjusting for X" without being printed or interpreted, do not extract it.

A useful test: *if a meta-analysis cited this paper for this specific phone/SM association, which estimate would they pull?* That is the one to extract, along with the model that produced it.

---

## 3. Per-model fields to record

The following describe the model itself and are shared across every estimate produced by it:

1. **Design** — cross-sectional / longitudinal / cross-lagged. If longitudinal, the wave structure (which wave the IV is measured at, which wave(s) the DV; whether the DV is a single follow-up or repeated measures across multiple waves; whether time × IV interactions were tested)
2. **Sample** — analytic N, age range, sociodemographic descriptors, exclusions, ABCD release version
3. **Analytical class** — the exact class (mixed-effects linear regression, multilevel logistic regression, generalized linear mixed model, structural equation model, group factor analysis followed by GLMM, machine-learning ensemble with SHAP feature importance, network model with edge weights, etc.)
4. **Software / package** — Stata 18.0, R::lme4, SAS GLIMMIX, Python scikit-learn, lavaan, etc.
5. **Specification or equation** — for regression-style models, the equation with the focal effect highlighted; for SEM, the path model structure; for ML, the algorithm and hyperparameters; for networks, the estimator and tuning. IV and DV are shown as slots if multiple combinations share the model.
6. **Adjusted for / controlled** — the complete enumerated list of covariates, mediators that were partialed out, etc.
7. **Random effects / clustering** — site, family, scanner, etc.
8. **Weighting** — propensity weights, sample weights, design weights
9. **Multiple-comparison correction** — FDR / Bonferroni / Benjamini-Hochberg / none
10. **Effect-modification or interaction tests** — whether sex, race, age, or other interactions were tested, and whether stratified results were reported

---

## 4. Per-estimate fields to record

For each (IV × DV) cell within the model's results matrix:

- IV name + measurement (units, instrument, wave if relevant)
- DV name + measurement (units, instrument, wave if relevant)
- Estimate type (β, OR, RR, IRR, SHAP value, edge weight, factor loading, path coefficient, etc.)
- Estimate value (the **native metric** as reported by the paper)
- 95% confidence interval (or credible interval, posterior interval, etc.)
- p-value
- FDR-q (if reported)
- Significance at the paper's stated α (typically 0.05)
- Direction of effect (interpretive: "more SM → higher depression" etc.)
- Location in source paper (e.g., "Table 2, Model 2" or "Figure 4B" or "Supplementary Table A7")
- **Inputs needed to derive a Cohen's d** for cross-paper comparison (see Section 4a below)

### 4a. Derived Cohen's d (cross-paper common metric)

Native metrics across the 69 INCLUDE papers are heterogeneous (B, OR, RR, β_std, raw d, IRR, path coefficients, etc.) and not directly comparable cell-to-cell. To enable visual cross-paper comparison, every cell that comes from a regression-style model also gets a **derived Cohen's d** displayed beneath the native metric in `3L-models.html`. The native metric stays visible — d is added, not substituted.

Conversion is performed by `scripts/effect_sizes.py` (with unit tests in `scripts/test_effect_sizes.py`); `scripts/build_matrices.py` reads `scripts/paper_<id>.json` and emits the rendered matrix table. The pipeline is reproducible: editing the JSON and re-running the script regenerates the matrix.

Conversions used:

- **Linear regression, continuous IV → continuous DV.** Capture B, B_lo, B_hi (95 % CI), SD<sub>IV</sub>, SD<sub>DV</sub>. Derived d = 2·β<sub>std</sub> / √(1 − β<sub>std</sub>²) where β<sub>std</sub> = B · SD<sub>IV</sub> / SD<sub>DV</sub> (Borenstein et al. 2009 eq 7.1).
- **Linear regression, dichotomous IV → continuous DV.** If the paper reports d directly (paper 156 case), passthrough. Otherwise compute d from the adjusted group-mean difference and pooled SD: d = (M₁ − M₀) / SD<sub>pooled</sub>.
- **Logistic regression, OR.** d = ln(OR) · √3/π (Chinn 2000).
- **Logistic regression, RR.** Convert RR → OR using the baseline event rate p₀ in the unexposed group: OR = RR · (1 − p₀) / (1 − RR · p₀); then OR → d via Chinn. If the paper only reports a marginal sample base rate, that is an acceptable approximation when exposure prevalence is < ~10 % (record the assumption and the rate).
- **Standardized β reported directly.** Treat as approximate r and apply the same r → d formula.
- **SEM path coefficients.** If standardized, treat as β_std → d. If unstandardized, require the path's SD<sub>IV</sub> / SD<sub>DV</sub> (typically reported in the paper or computable from the covariance matrix).
- **IRR / Poisson rate ratios.** Treat as OR → d at first approximation; note in the paper's JSON.
- **Non-convertible (ML feature importance, network edge weights).** Display the native metric alone and explicitly mark "no common-scale d available."

CIs on d are obtained by applying the same conversion to each endpoint of the CI on the native metric; this is monotonic for every conversion above and gives a valid d CI (pivotal-CI approach). When the paper does not print a CI on the native metric, omit the d CI as well.

The derived d is **always** displayed as `d ≈ X.XXX` (with the ≈ symbol) so it is never confused with a paper-reported d. A paper-reported d appears as `d = X.XX` with no ≈.

---

## 5. Composite-inclusion handling

For papers included on Stage 2 because of a phone/SM-specific composite or supplementary breakout:

- **If the composite is built exclusively from phone or social media items** (e.g., "digital socializing = texting + video chat + social media networking"), the composite *is* the qualifying analysis. Extract it directly as a phone/SM IV with the units and components named.
- **If the composite includes non-phone or non-SM items** (e.g., total screen time bundling TV and console gaming) but the paper reports a phone/SM-isolated subcategory analysis in supplementary or sensitivity tables, extract only the isolated subcategory analysis. Do not extract the headline composite.
- **Supplementary or sensitivity analyses count** as long as the paper reports a numeric estimate for the phone/SM-isolated breakout. A null result is still a numeric estimate.

---

## 6. What NOT to extract

- Headline analyses where the IV is a non-phone/non-SM composite (e.g., total screen time bundling TV + gaming + phone + SM with no breakout)
- Demographic-only stratified analyses where the focal IV is not a phone/SM modality
- Sensitivity-mentioned-but-not-printed analyses (no extractable numbers)
- Earlier stepwise models when the authors anchor claims to a final adjusted model
- Unrelated analyses in the paper that do not involve a phone/SM variable

---

## 7. Repeated-measures and longitudinal structure

When the DV is a repeated measure across multiple follow-up waves entered into a mixed-effects, GEE, or comparable model:

- Note that the outcome is **not** averaged into a single number per person; it enters the model as repeated measures with within-person correlation handled by the random structure or working covariance
- Note the focal estimate represents the *average* association across waves unless the model includes a wave × IV interaction
- If wave-specific estimates are reported separately, extract them as separate cells (each wave is its own DV)

---

## 8. Display structure (`3L-models.html`)

For each paper:

1. **Paper header** — title, citation, DOI, authors, journal, year
2. **One model card per distinct citable analysis**, in fixed-section order:
   - Header: model name + one-line synopsis identifying the model template
   - Design (with timeline diagram if longitudinal)
   - Sample
   - Analytical class
   - Specification / equation (with focal effect highlighted, IV/DV shown as slots if reused)
   - Adjusted for
   - Specs (software, weighting, random effects, MC correction, effect-modification tests)
3. **Results matrix at the bottom of each card** — rows = IVs, columns = DVs (or whichever orientation reads more cleanly), each cell showing the estimate + CI + p, with significant cells visually distinguished
4. **No transparency-only matrices** (unadjusted comparisons, model-development scaffolding) when the paper anchors its claims to a different specification
