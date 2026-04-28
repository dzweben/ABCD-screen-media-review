# 2L Criteria — Full-Text Eligibility (PRISMA 2020) — v6

**Stage:** Level 2 — full-text eligibility review.

**Scope:** Only papers reporting an **inferential association** between **smartphone or social media use** (as IV or DV) and an **individual-trait-level** variable (neural, behavioral, health, cognitive, well-being, personality, substance use, sleep, academic, or similar within-person construct) on **U.S. ABCD Study** participants are retained.

This document specifies a-priori eligibility criteria. Coders apply these rules conceptually, not by label-matching. The criterion is "what was actually measured and analyzed," not "what label the authors chose."

---

## 1. Research question

**Among publications analyzing data from the U.S. Adolescent Brain Cognitive Development (ABCD) Study, what associations have been reported between youth smartphone or social media use and individual-trait-level variables (neural, behavioral, health, cognitive, well-being, personality, substance use, sleep, academic, etc.)?**

---

## 2. Eligibility criteria

The criteria are evaluated in cascade order. **As soon as any criterion returns NOT_MET, all subsequent criteria are marked `DEFERRED` with evidence string `"prior criterion failed; not evaluated"`.** Do not score downstream criteria with MET / NOT_MET / UNKNOWN once a prior NOT_MET has occurred.

**Cascade order:** FT-IC1 → FT-IC5 → FT-IC6 → FT-IC2 → FT-IC3 → FT-IC4 → FT-EC7.

---

### 2.1 FT-IC1 — Population (U.S. ABCD)

The qualifying cohort is the **U.S. Adolescent Brain Cognitive Development Study** — NIH-funded, 21 U.S. recruitment sites, baseline ages 9–10, any data release (2.0–5.1+).

| Status | When |
|---|---|
| **MET** | Paper analyzes data from the U.S. ABCD Study. Sub-samples qualify (EARS subsample, autism subsample, ABCD-COVID rapid-response, etc.). Pooled multi-cohort analyses combining U.S. ABCD with another cohort qualify **only if** at least one ABCD-specific estimate (in main, supplementary, or sensitivity analyses) is extractable. |
| **NOT_MET** | Different cohort sharing the "ABCD" acronym — including **Amsterdam Born Children and their Development (Dutch ABCD)**, Adolescent Behavior and Cognitive Development cohorts in other countries, and any non-U.S. ABCD initiative. NHANES, MTF, MCS, Generation R, INMA, etc. ABCD cited only in introduction/discussion without analyzing ABCD data. Pooled analyses with no ABCD-specific estimate extractable. **Verify cohort identity by reading the recruitment/methods description, not just the acronym.** |
| **UNKNOWN** | No PDF AND the abstract genuinely does not identify which cohort is used. **Default rule:** if the title or abstract says "Adolescent Brain Cognitive Development Study" / "ABCD Study" with U.S. or NIH context (U.S. sample, ages 9–10 baseline, 21 sites, NDA release reference, etc.), default to **MET** even without a PDF. |

If FT-IC1 = NOT_MET → exclusion code **FT-EC1**.

---

### 2.2 FT-IC5 — Original empirical analysis

| Status | When |
|---|---|
| **MET** | Paper reports an original empirical analysis of ABCD data. Cross-sectional, longitudinal, mediation, moderation, ML, causal inference, target-trial emulation, network analysis, mixed-effects, factor models with reported pathway estimates. |
| **NOT_MET** | Reviews, meta-analyses without new ABCD analysis, editorials, commentaries, perspectives, letters, study protocols, resource/data-availability descriptions, special-issue introductions, book chapters, news pieces. |

If FT-IC5 = NOT_MET → exclusion code **FT-EC3**.

---

### 2.3 FT-IC6 — Non-duplicate

| Status | When |
|---|---|
| **MET** *(default)* | Published peer-reviewed paper. Default presumption. |
| **NOT_MET** | Paper is identified as a preprint version of an already-included peer-reviewed paper *also* in this corpus, OR a conference abstract of an already-included full paper, OR a re-analysis of identical data with no new statistical content beyond an already-included paper. |

If FT-IC6 = NOT_MET → exclusion code **FT-EC6**.

---

### 2.4 FT-IC2 — Qualifying smartphone/SM exposure (CONCEPTUAL)

**FT-IC2 is direction-agnostic.** A qualifying smartphone or social-media variable can appear as **IV** or **DV** of an analysis. It does not qualify if it appears *only* as a mediator, moderator, or covariate.

The paper must, in at least one analysis, pair a qualifying smartphone/SM variable with an **individual-trait-level** variable on the other side of the relationship.

#### What qualifies as "smartphone use"
Any operationalization of phone-specific activity:
- Time on phone (self-report, parent-report, EARS passive sensing)
- Smartphone ownership (yes/no), age of first smartphone
- Problematic / addictive smartphone use scales (MPIQ, PSMUS, mobile-phone-checking)
- Phone-specific items: texting (on phone), video chat (on phone), bedtime phone use
- App use, app-category time, notification volume, passive-sensed app data

#### What qualifies as "social media use"
Any operationalization of SM-platform activity:
- Time on social media (self-report, parent-report, passive)
- Platform-specific use: TikTok, Instagram, Snapchat, YouTube, Facebook, Twitter/X, Reddit, Pinterest, Tumblr, Discord, BeReal
- Number of SM accounts; secret/private accounts; platform-membership indicators
- Online dating apps / hookup apps
- Problematic / addictive SM scales (SMAQ, Bergen SM/Facebook Addiction Scale, SNS-A)

#### What qualifies as "individual-trait-level" on the other side
Neural · behavioral · physical health · mental health · cognitive · well-being · personality · substance use · sleep · academic · psychiatric symptom · genetic / polygenic · biological (BMI, puberty, biomarker) · clinical diagnosis · ACEs / trauma exposure · parenting practices / parental psychopathology · pet ownership · religious participation · school engagement · any other within-person construct.

#### What does NOT qualify
- **Other side is demographic-only** (age, sex, race/ethnicity, household income, parental education, household composition) — paper-level NOT_MET if no individual-trait-level analysis exists anywhere
- **Other side is contextual-only** (neighborhood, school district, region, season, COVID timing) — paper-level NOT_MET if no individual-trait-level analysis exists anywhere
- TV-only · console/PC-gaming-only · unspecified-platform-gaming-only · generic "internet use" without device specificity · radio · podcasts · RF-EMF exposure
- Multi-device aggregated time bundling smartphone with non-smartphone devices ("minutes on computer + tablet + cellphone") with no per-device breakdown
- Composite "screen time" totals that bundle TV/console/phone with no per-modality breakdown isolating phone or SM
- Cyberbullying alone (without a separately-measured smartphone or SM variable)
- Mature-rated content / R-rated content variables alone (content rating ≠ phone/SM modality)
- SM as covariate-only / mediator-only / moderator-only with no IV-or-DV role anywhere

#### Conceptual judgment for borderline labels

The author's chosen variable label is not authoritative — judge what was conceptually measured.

- A paper labeling its variable "screen time" *qualifies* if the methods make clear the construct is phone/SM-based time (e.g., "time on smartphone-based media"). It *does not qualify* if the methods describe a multi-device or multi-activity composite that bundles TV, console, and phone with no breakdown isolating phone or SM.
- A paper labeling its variable "screen media activity" *qualifies* if the methods or results isolate phone or SM activity within the composite. Otherwise it does not.
- A pure psychometric/validation paper (factor structure of SMAQ, reliability of MPIQ, EARS-vs-self-report concordance) does not pair the SM variable with an external individual-trait-level variable as IV or DV → **NOT_MET**. (FT-IC5 may also fail; either route is fine.)

If FT-IC2 = NOT_MET → exclusion code **FT-EC2**.

---

### 2.5 FT-IC3 + FT-IC4 — Inferential analysis with numeric result

These are tested together. The paper must perform an inferential analysis involving the qualifying smartphone/SM variable and an individual-trait-level variable, and must report at least one numeric result for that relationship.

| Status | When |
|---|---|
| **MET** | Any quantitative result for the SM ↔ individual-trait-level relationship is reported anywhere (main, supplementary, sensitivity, appendix): regression β · OR · RR · HR · IRR · aOR · aRR · PR · aPR · penalized-regression β (Lasso/Ridge/Elastic Net) · path coefficient (direct/indirect/total) from SEM/CLPM/mediation · Pearson/Spearman/partial r · mean difference between groups (with t/F/p) · η² · R² · adjusted prevalence ratio · SHAP value · permutation feature importance · RF/GBM/XGBoost variable importance · model-level metric (AUC, R²) involving the SM variable · Bayesian posterior estimate · network edge weight · target-trial-emulation contrast. **Anything quantitative counts.** |
| **NOT_MET** | Paper claims an SM↔outcome association narratively but reports zero numeric quantification anywhere (essentially never occurs in real empirical papers). |

If both = MET, proceed to FT-EC7. If NOT_MET → exclusion code **FT-EC4**.

---

### 2.6 FT-EC7 — Longitudinal SM-as-DV-only exclusion

FT-EC7 applies if **all three** are simultaneously true:

1. The design is **longitudinal** (baseline predicts later wave).
2. Smartphone/SM is the **DV** in every analysis involving smartphone/SM in the paper.
3. There is **no analysis anywhere in the paper** with smartphone/SM as IV.

If all three hold → exclusion code **FT-EC7**.

FT-EC7 does **not** apply (paper kept) when any of these is true:
- Design is cross-sectional (regardless of which side SM is on)
- Smartphone/SM is IV in any analysis (any topic, anywhere in the paper)
- Bidirectional / cross-lagged design (SM is both IV and DV)

The predictor type is **not** part of the FT-EC7 rule. Demographic, individual-trait, family, lifestyle — none of it matters. What matters is design (longitudinal) and SM-side-of-the-equation (DV-only with no IV analysis).

---

## 3. Cascade-DEFERRED convention

The cascade is hierarchical. As soon as a criterion returns NOT_MET (or UNKNOWN that fails to upgrade), every subsequent criterion is recorded as exactly:

```
status: DEFERRED
evidence: "prior criterion failed; not evaluated"
```

Coders **must not** score downstream criteria with MET / NOT_MET / UNKNOWN once a prior NOT_MET has occurred. The aggregator treats DEFERRED as non-disagreement, so cascade-stage coding artifacts cannot generate false IRR splits.

---

## 4. Exclusion codes (hierarchical)

Assigned in cascade order; first applicable code wins.

| Code | Label | Trigger |
|---|---|---|
| **FT-EC1** | Not U.S. ABCD | FT-IC1 NOT_MET. |
| **FT-EC3** | Non-empirical | FT-IC5 NOT_MET (review, editorial, commentary, protocol, resource paper, etc.). |
| **FT-EC6** | Duplicate | FT-IC6 NOT_MET (preprint of an included paper, conference abstract of an included paper, identical re-analysis). |
| **FT-EC2** | No qualifying smartphone/SM variable, or other-side not individual-trait-level | FT-IC2 NOT_MET (composite-only with no phone/SM isolation, TV-only, gaming-only, cyberbullying-only, "internet use" only, RF-EMF, multi-device aggregated, content-rating-only, mediator/covariate-only, demographic-only or contextual-only on the other side, validation-only). |
| **FT-EC4** | No numeric result for SM↔outcome | FT-IC3/IC4 NOT_MET. |
| **FT-EC7** | Longitudinal SM-as-DV-only | All three §2.6 conditions hold. |

**UNSURE** — PDF unavailable AND abstract insufficient to score a criterion. Carry forward for retrieval.

**NA_FOR_NOW** — PDF unavailable; classified separately for tracking.

---

## 5. Adjudication pipeline

| Step | Role | Blinding | Output |
|---|---|---|---|
| 2L-a | C1_AI — independent AI coder, full PDF | Blind to C2 | Per-criterion MET / NOT_MET / UNKNOWN / DEFERRED + evidence |
| 2L-b | C2_AI — independent AI coder | Blind to C1 | Same |
| 2L-c | Algorithmic aggregation | Deterministic | Per-criterion FINAL + paper-level decision |
| 2L-d | Human spot-check | Lead author | All EXCLUDE + all UNSURE + 10% INCLUDE sample |

**No resolver step in v6.** The criteria are tightened so that C1 and C2 converge by construction. Any residual criterion-level disagreement (after the cascade-DEFERRED convention is applied) routes the paper to UNSURE, not to a third AI coder.

### Final-decision algorithm (deterministic)

For each of FT-IC1, FT-IC5, FT-IC6, FT-IC2, FT-IC3, FT-IC4, FT-EC7:

1. If C1 == C2 (including both DEFERRED) → that status.
2. If one is DEFERRED and the other is a substantive value → use the substantive value.
3. If both substantive but differ → **UNSURE** for the paper.
4. If either is UNKNOWN with no PDF → DEFERRED for downstream + paper-level **NA_FOR_NOW**.

Paper-level decision:
1. First NOT_MET in cascade order → EXCLUDE with that exclusion code.
2. All MET and FT-EC7 applies → EXCLUDE with FT-EC7.
3. All MET and FT-EC7 does not apply → INCLUDE.
4. Any UNSURE on a substantive disagreement → UNSURE (queue for human).
5. Any UNKNOWN with no PDF → NA_FOR_NOW.

Cohen's κ between C1 and C2 reported per criterion + pooled.

---

## 6. Reported in `2L-scoring.csv`

One row per Stage-1 include (n = 171). Columns:

- Metadata: `paper_id, doi, title, first_author, year, journal, has_pdf`
- Per criterion (FT-IC1, FT-IC5, FT-IC6, FT-IC2, FT-IC3, FT-IC4): `_C1`, `_C2`, `_FINAL`, `_C1_evidence`, `_C2_evidence`
- FT-EC7: `FT_EC7_C1`, `FT_EC7_C2`, `FT_EC7_FINAL`
- Final: `FINAL_decision` ∈ {INCLUDE, EXCLUDE, UNSURE, NA_FOR_NOW}, `FINAL_EC_code`, `FINAL_reason`

---

## 7. Protocol deviations from v5

v6 replaces v5's twenty binding rules (B1–B20) with conceptual criteria that hinge on what the paper actually measured and analyzed, not on which YSTS items were named or which scale was cited:

- **FT-IC2 is now conceptual.** Composite "screen time" qualifies if the construct isolates phone/SM use; does not qualify if it bundles TV/console/phone with no breakdown. Mature/R-rated content alone, multi-device aggregated time alone, and SM-as-covariate/mediator/moderator-only all fail FT-IC2. The other side of the SM relationship must be individual-trait-level.
- **FT-IC3 + FT-IC4 collapsed and broadened.** Any quantitative result counts: traditional regression coefficients, ML feature importance, SHAP values, R², AUC, Bayesian posteriors, etc.
- **FT-EC7 simplified.** Drops the v5 "demographic-only predictor" qualifier. EC7 now hinges on design (longitudinal) and SM side of the equation (DV-only with no SM-as-IV analysis), nothing else.
- **Cascade reordered.** FT-IC5 (empirical) and FT-IC6 (non-duplicate) are tested before FT-IC2, so reviews/commentaries/preprints don't generate spurious FT-IC2 disagreements.
- **Cascade-DEFERRED convention.** Once a criterion fails, all downstream are marked DEFERRED, eliminating cascade-stage coding artifacts that produced false IRR splits in v5.
- **No resolver.** Criteria are tightened so that C1 and C2 converge by construction. Residual disagreements route to UNSURE for human review.

All Stage-2 screening prior to v6 is superseded; v6 results overwrite v5 in `02-L2/2L-scoring.csv`. Earlier passes remain in git history.
