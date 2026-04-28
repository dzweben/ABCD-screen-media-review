# v5 Disagreement Audit — Diagnosing the 52 papers C1≠C2

**Goal:** Identify the criteria-level *gaps* causing C1/C2 to split, so we can write tighter rules that close them — instead of escalating to a resolver.

**Distribution of disagreements by criterion:**

| Criterion | # Disagreements | Notes |
|---|---:|---|
| FT-IC2 (qualifying exposure) | 28 | Root cause — IC3/IC4 cascade from this |
| FT-IC4 (extractable estimate) | 28 | Mostly cascades from IC2 |
| FT-IC3 (inferential test) | 22 | Mostly cascades from IC2 |
| FT-IC5 (original empirical) | 12 |  |
| FT-EC7 (directionality) | 7 |  |
| FT-IC6 (duplicate) | 6 |  |
| FT-IC1 (US ABCD) | 5 |  |

**FT-IC2 is the bottleneck.** Of the 28 IC2 splits, virtually all of the IC3 (22) and IC4 (28) splits are cascades — once two coders disagree on whether the exposure qualifies, the downstream "is there a test on the exposure" and "is there a number on the exposure" automatically split too. Fix IC2 and ≈80% of the noise disappears.

---

## The 7 root-cause clusters

### Cluster 1: "Composite YSTS hours vs. per-item coefficient" — 12 papers
**Papers:** 36, 84, 128, 153, 166, 172, 176, 215, 306, 397, 429, plus 67 in part

The Youth Screen Time Survey (YSTS) measures 6+ modalities (TV, videos, video games, texting, social media, video chat). Papers vary in how they **report**:
- Sum total ("recreational screen time = 6.1 h/day") only
- Sum total stratified by category (low/medium/high)
- Per-item β / OR for one or more YSTS items individually
- Screen time as one node in a latent lifestyle factor with no own coefficient

C1 reads "YSTS measured separately" → B1 → MET.
C2 reads "tables show only sum" → B2 → NOT_MET.

**Diagnosis:** v5's B1 vs B2 distinction depends on what's *reported in the tables* but the rule text emphasizes what's *measured by the survey*. Agents read one and miss the other.

**Proposed v6 rule (replaces B1+B2):**

> **R-EXTRACT.** FT-IC2 is MET only if the paper reports at least one extractable numeric estimate (β / OR / RR / HR / IRR / r / mean difference / indirect or direct effect, each with SE / 95% CI / p) for **a single qualifying smartphone or social-media variable** in main, supplementary, or sensitivity tables.
> - Composite "total screen time" (any sum/average across modalities) → NOT_MET, even if YSTS underlies it.
> - Categorical screen-time bins (low/medium/high hours) where the categories are derived from a composite → NOT_MET.
> - Per-item estimate for one qualifying YSTS modality (e.g., "social media: β=0.13, p=.02") → MET, even if other modalities are also reported in the same model.
> - Latent factor / lifestyle index where screen time is one indicator and no separate path coefficient is reported → NOT_MET.

This makes IC2 a **table-level** test, not a survey-level one. The agent has to point to a specific cell.

---

### Cluster 2: "Screen time as DV vs IV" — 4 papers
**Papers:** 77 (ACEs→ST), 121 (Prospective predictors of ST), 67 (parenting→VG), 384 (media parenting)

C1 marks IC2 = MET (a qualifying variable was measured) and lets FT-EC7 handle directionality.
C2 marks IC2 = NOT_MET because "screen time is the outcome, not the exposure."

**Diagnosis:** v5 already says IC2 is direction-agnostic (B17/B18/B19), but it's not stated forcefully enough. Some agents read "exposure" in the criterion name and assume IV-only.

**Proposed v6 rule:**

> **R-DIRECTION.** FT-IC2 is **direction-agnostic.** A qualifying smartphone/SM variable counts if it appears anywhere in an inferential model — as IV, DV, mediator, or moderator. Directionality is evaluated **only** at FT-EC7. Do not pre-exclude papers where SM is the outcome at IC2.

Make it the first sentence of the FT-IC2 definition.

---

### Cluster 3: "Mediator / covariate / ML feature with no own coefficient" — 5 papers
**Papers:** 91, 122, 176, 185, 130

C1 reads B10 (covariate-only, no extracted coefficient) → NOT_MET.
C2 reads "screen time was in the model" → MET.

The disputes split on what counts as "an extracted coefficient":
- Mediator with reported indirect/direct effect (β, p) — agents disagree on whether B10 applies
- ML feature with SHAP value but no β
- Latent factor indicator with factor loading but no path
- Variable in cluster analysis used to compare groups but no SM↔outcome test

**Diagnosis:** v5 B8/B9/B10 use the phrase "extractable estimate" without defining the allowlist. Different agents draw the line differently.

**Proposed v6 rule (replaces B8+B9+B10):**

> **R-ESTIMATE-ALLOW.** "Extractable numeric estimate" for FT-IC4 means **any of**:
> - Linear / logistic / Poisson / negative-binomial / Cox / mixed-effects regression β (or OR, RR, HR, IRR) with SE or 95% CI or p
> - Penalized regression coefficient (Lasso, Ridge, Elastic Net) where the paper reports the actual β
> - Path coefficient from SEM / SCM / mediation models (direct, indirect, total) with SE / CI / p
> - Pearson / Spearman / partial r with p
> - Mean difference between groups (with SE, t / F / p)
> - Categorical effect estimates (e.g., adjusted prevalence ratio per stratum) with CI
>
> **Does NOT count:**
> - SHAP values, permutation feature importance, variable importance from RF / GBM / XGBoost
> - Model-level fit metrics (R², RMSE, AUC, accuracy)
> - Factor loadings, eigenvalues, communalities (psychometric only)
> - Group comparison without an inferential test (e.g., "Group A had more SM than Group B" with no t/p)
> - Mention of a variable in the model with no reported coefficient anywhere

**Hierarchy:** if the paper reports a qualifying coefficient *anywhere* (main, supp, sensitivity, appendix), IC4 is MET. SHAP-only / variable-importance-only is NOT_MET regardless of what else is in the paper.

---

### Cluster 4: "Mature-rated content as exposure" — 3 papers
**Papers:** 234, 384, 67

YSTS includes a "mature-rated video gaming" item and an "R-rated movie watching" item. Both are content-rating variables, not modality-specific time.

C1 reads B5/B6 differently across papers; C2 calls these out as content-only.

**Diagnosis:** v5 doesn't explicitly handle content-rating variables. Mature-rated games could be on console, PC, or phone.

**Proposed v6 rule:**

> **R-CONTENT.** Content-rating variables (mature-rated video gaming, R-rated movie watching, violent media exposure, etc.) do **not** qualify as smartphone/SM exposures unless they are paired with a modality-specific time-on-platform measure (e.g., "time spent playing mature-rated mobile games"). Content rating ≠ smartphone modality.

---

### Cluster 5: "Resource / commentary / protocol papers" — 4 papers
**Papers:** 98, 103, 178, 291; with 100 (psychometric-only) and 248 (review) adjacent

C1 routinely says NOT_MET via B14 (or UNKNOWN if hesitant about no PDF).
C2 sometimes says MET because the paper "discusses ABCD's SM measures."

**Diagnosis:** Reviews/commentaries reach FT-IC2 evaluation before agents catch them. The paper IS about SM, just not empirically.

**Proposed v6 reordering:**

> Move FT-IC5 (original empirical analysis) to the **second** atomic gate, right after FT-IC1.
> Order: IC1 (population) → IC5 (empirical) → IC6 (non-duplicate) → IC2 (exposure) → IC3 (inferential test) → IC4 (numeric estimate) → EC7 (directionality).
>
> Rationale: a review or commentary fails IC5 unambiguously and shouldn't be tested for SM exposure.

This is a re-ordering of the cascade, not a new rule. The atomic per-criterion scoring stays; only the algorithmic aggregation order changes — which means *both coders* see the same exclusion code and can't differ on it.

---

### Cluster 6: "Generic device-aggregated time" — 2 papers
**Papers:** 166 ("avg minutes per week on computer, cellphone, tablet, or other electronic device"), 397 ("recreational screen time" as single hours/day)

C1 says NOT_MET (lumped, can't isolate smartphone).
C2 says MET (cellphone is included).

**Diagnosis:** v5 covers TV-only and gaming-only carve-outs but doesn't explicitly address "cellphone bundled with computer + tablet" measures.

**Proposed v6 rule (extends B7):**

> **R-DEVICE-AGG.** Multi-device aggregated time measures (e.g., "minutes/day on computer, tablet, cellphone, or other electronic device") that combine smartphone with non-smartphone devices into a single number → FT-IC2 NOT_MET, unless the paper also reports a per-device breakdown with at least one separate cellphone/smartphone coefficient.

---

### Cluster 7: "Bidirectional / cross-lagged → does FT-EC7 apply?" — 7 papers (FT-EC7 disagreements)
**Papers (sample):** 48, 153, 202, 309, 434, 441, etc.

v5 B20 already says bidirectional designs disqualify FT-EC7. Disagreements remain because some bidirectional papers have one direction with demographic-only predictors and one direction with non-demographic predictors. Agents differ on whether B20 fully kills FT-EC7 or only kills the SM→outcome direction.

**Proposed v6 clarification:**

> **R-EC7-BIDIR.** FT-EC7 applies **only** to papers whose **entire empirical contribution** is "longitudinal demographic-only predictors → SM as DV, with no SM→outcome analysis anywhere in the paper." Any cross-lagged / bidirectional / SM-as-IV analysis in the same paper disqualifies FT-EC7 entirely. Pure cross-sectional sociodemographic→SM analysis → INCLUDE under B15 (FT-EC7 does not apply).

Already in v5 but worth restating with examples.

---

## Summary: criteria changes for v6

| Change | Replaces | Net effect |
|---|---|---|
| **R-EXTRACT** (table-level, single-variable estimate) | B1 + B2 | Eliminates Cluster 1 (12 papers) |
| **R-DIRECTION** (IC2 is direction-agnostic) | B17/B18/B19 (made forceful) | Eliminates Cluster 2 (4 papers) |
| **R-ESTIMATE-ALLOW** (concrete allowlist + denylist) | B8 + B9 + B10 | Eliminates Cluster 3 (5 papers) |
| **R-CONTENT** (content-rating ≠ modality) | (new) | Eliminates Cluster 4 (3 papers) |
| **Reorder** (IC5 right after IC1) | (algorithmic, not a rule) | Eliminates Cluster 5 (4 papers) |
| **R-DEVICE-AGG** (multi-device lumped → NOT_MET) | (new, extends B7) | Eliminates Cluster 6 (2 papers) |
| **R-EC7-BIDIR** (any non-demographic-IV analysis kills EC7) | B20 (made forceful) | Eliminates Cluster 7 (7 papers) |

Total expected disagreement reduction: ≈37 of 52 (≈70%).

The remaining ≈15 are likely IC1 (US ABCD vs Dutch ABCD vs pooled) and IC6 (duplicate detection) — both narrower and easier to fix with sharper definitions.

---

## Next step

Rewrite `2L-criteria.md` from B1–B20 into v6 with the seven R-rules above (kept linear, no resolver), wipe v5 C1/C2 outputs, re-run.
