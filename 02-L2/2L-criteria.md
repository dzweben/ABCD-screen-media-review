# 2L Criteria — Full-Text Eligibility (PRISMA 2020) — v7

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

### 2.4 FT-IC2 — Qualifying smartphone/SM exposure (MECHANICAL TWO-STEP TEST)

**FT-IC2 is direction-agnostic.** A qualifying smartphone or social-media variable can appear as **IV** or **DV** of an analysis. It does not qualify if it appears *only* as a mediator, moderator, or covariate.

The paper must, in at least one analysis, pair a qualifying smartphone/SM variable with an **individual-trait-level** variable on the other side of the relationship.

#### The IC2 test has two steps. Run them in order; stop as soon as Step 1 returns a hit.

**Step 1 — broad search for a phone/SM-specific estimate.**

Search **every results location** in the paper — main tables, supplementary tables, appendices, sensitivity analyses, robustness checks, alternative specifications, sub-group breakouts — for at least one numeric estimate (β / OR / RR / HR / IRR / r / mean diff / SHAP value / feature importance / path coefficient (direct, indirect, total) / network edge weight / Bayesian posterior) where the variable label is one of these phone/SM-specific items:

- time on phone · smartphone ownership (yes/no) · age of first smartphone · phone time
- time on social media · time on a named SM platform (TikTok / Instagram / Snapchat / YouTube / Facebook / Twitter / X / Reddit / Pinterest / Tumblr / Discord / BeReal)
- texting · video chat · video calling
- app use · app-category time · notification volume · passive-sensed phone/app time
- problematic / addictive phone scales (MPIQ, PSMUS, mobile-phone-checking)
- problematic / addictive SM scales (SMAQ, Bergen SM/Facebook Addiction Scale, SNS-A)
- online dating apps / hookup apps · number of SM accounts · secret/private SM accounts

**If you find any such estimate paired with an individual-trait variable on the other side (see below) → FT-IC2 = MET. Stop.** The paper's headline analysis being on a composite does not disqualify the paper if a per-modality estimate exists in a supplement or sensitivity table.

**Step 2 — composite-content check (only if Step 1 finds nothing).**

Identify the composite/sum variable being analyzed. **The variable's label is irrelevant** — "screen time," "screen media activity," "digital socializing," "recreational screen use," "media use," etc. all need the same test. What matters is **what items the methods say are inside the composite**:

- **MET** if the composite is built **exclusively** from phone/SM/digital-socializing items. Examples: "digital socializing = texting + video chat + social media"; "phone-based media time = SM + texting + video chat + app use"; "smartphone use composite = social media + texting + phone time."
- **NOT_MET** if the composite includes **any** non-phone/non-SM activity that is not separately broken out elsewhere in the paper. Disqualifying non-phone/non-SM ingredients include: TV, movies on TV, video streaming on a non-phone device, console video games, PC video games, unspecified-platform video games, reading on screens, computer-only time, "music" listening, "internet browsing" generic.

#### What qualifies as "individual-trait-level" on the other side

Neural · behavioral · physical health · mental health · cognitive · well-being · personality · substance use · sleep · academic · psychiatric symptom · genetic / polygenic · biological (BMI, puberty, biomarker) · clinical diagnosis · ACEs / trauma exposure · parenting practices · parental psychopathology · family functioning · sexual orientation · gender identity · sexual minority status · transgender / gender-questioning status · religious participation · pet ownership · peer associations · school engagement · extracurricular activities · any other within-person psychosocial / identity / behavioral construct.

Identity variables (sexual orientation, gender identity, transgender/gender-questioning status) and psychosocial lifestyle variables (religious participation, pet ownership, peer associations) qualify as individual-trait on the other side — they are NOT classified as demographic for this rule.

#### What does NOT qualify on the other side

- **Demographic-only** (age, sex, race/ethnicity, household income, parental education, household composition, marital status, immigration status, urbanicity, study site)
- **Contextual-only** (neighborhood quality, school district, region, season, COVID-timing, year-of-survey)

If the only analyses pair the SM/phone variable with demographic-only or contextual-only on the other side, FT-IC2 = NOT_MET regardless of whether the SM/phone variable itself qualifies on Step 1 or Step 2.

#### Critical clarifications (BINDING)

1. **Problematic-use scales are SM/phone variables, not "other-side individual-trait" outcomes.** SMAQ, MPIQ, VGAQ, PSMU, Bergen SM/Facebook Addiction, SNS-A all measure smartphone or SM use. When the only analysis is sociodemographic predictor → SMAQ/MPIQ as DV, the other side is still demographic — **FT-IC2 = NOT_MET**. The scale is the SM variable; it cannot also serve as the non-SM other-side variable.

2. **Gaming alone does not qualify** unless it is explicitly mobile/phone-based, OR the paper also separately measures a qualifying phone/SM variable with its own coefficient. This includes: VGAQ (Bergen Video Game Addiction Questionnaire), IGDS9-SF, generic "video gaming hours," "gaming duration," problematic-gaming scales without explicit mobile/phone modality, console gaming, PC gaming, "video games" with platform unspecified, "gaming addiction." If the paper measures only gaming and does not isolate phone-based gaming or pair it with phone/SM, **FT-IC2 = NOT_MET**.

3. **Cyberbullying alone does not qualify.** Cyberbullying counts only when paired with a separately-measured phone/SM variable that has its own coefficient.

4. **Mature-rated / R-rated content alone does not qualify.** Content rating is not modality. "Mature-rated video games" or "R-rated movies" qualify only if the paper also reports a separate phone/SM variable with its own coefficient.

5. **Multi-device aggregated time fails Step 2.** "Minutes per week on computer, tablet, cellphone, or other electronic device" reported as a single number bundles smartphone with non-phone devices. NOT_MET unless a per-device breakout (cellphone alone) exists somewhere.

6. **Pure psychometric/validation papers fail.** Factor structure of SMAQ, reliability of MPIQ, EARS-vs-self-report concordance with no external outcome → FT-IC2 NOT_MET (they may also fail FT-IC5; either route is fine).

7. **SM as covariate / mediator / moderator-only fails.** The qualifying variable must appear as IV or DV in at least one analysis where it has its own reported coefficient or estimate.

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
3. There is **no analysis anywhere in the paper** with smartphone/SM as IV (or as both IV and DV in a bidirectional/cross-lagged model).

If all three hold → exclusion code **FT-EC7**.

#### Cross-sectional carve-out (BINDING)

If the paper contains **any** cross-sectional analysis where smartphone/SM is the DV — with the same predictors as in the longitudinal analyses, or with any other predictors — FT-EC7 does **NOT** apply. This holds regardless of how many longitudinal SM-as-DV-only analyses are also present in the paper. Evidence of any cross-sectional SM-as-DV analysis anywhere in the paper (main, supplementary, sensitivity) disqualifies FT-EC7.

#### FT-EC7 does NOT apply when any of these is true

- The design is cross-sectional, **OR** the paper has any cross-sectional SM-as-DV analysis (cross-sectional carve-out, above)
- Smartphone/SM is IV in any analysis anywhere in the paper, on any topic
- Bidirectional / cross-lagged design (SM is both IV and DV in the same model)

The predictor type is **not** part of the FT-EC7 rule. Demographic, individual-trait, family, lifestyle, ACEs, parental psychopathology — none of it matters. What matters is (a) design (longitudinal) and (b) SM side of the equation (DV-only with no IV analysis anywhere). Predictor-type judgments belong at FT-IC2 (other-side individual-trait requirement), not at FT-EC7.

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

## 7. Protocol deviations

### v7 (current) — five fixes targeting v6's residual UNSURE cluster

v6 produced 21 papers with substantive C1≠C2 disagreement (out of 171). A forensic audit of those 21 identified five specific sources of remaining ambiguity. v7 makes each one mechanical:

- **FT-IC2 reframed as a two-step mechanical test.** Step 1: search every results location (main, supplementary, sensitivity, appendix) for a numeric estimate where the variable label is phone/SM-specific — if found, MET, stop. Step 2 (only if Step 1 fails): check what items make up the composite per the methods. Composite labeled "screen time" or "screen media activity" qualifies only if its items are exclusively phone/SM/digital-socializing. Any TV / console / PC / unspecified-gaming / music / non-phone item bundled in without a separate breakout → NOT_MET. The label is irrelevant; what's inside the composite is what matters.
- **Problematic-use scales clarified.** SMAQ, MPIQ, VGAQ, PSMU, Bergen, SNS-A are SM/phone variables, not "individual-trait" outcomes on the other side. Sociodemographic → SMAQ-as-DV alone still fails FT-IC2 (the other side is demographic).
- **Identity variables explicitly classified as individual-trait.** Sexual orientation, gender identity, transgender/gender-questioning status, religious participation, pet ownership, peer associations, school engagement, extracurricular activities are individual-trait — NOT classified as demographic for the FT-IC2 other-side rule.
- **Gaming carve-out made salient.** VGAQ, IGDS9-SF, generic "gaming hours," "gaming duration," problematic-gaming scales without explicit mobile/phone modality, console gaming, PC gaming, "video games" with platform unspecified — all fail FT-IC2 unless paired with a separately-measured phone/SM variable.
- **FT-EC7 cross-sectional carve-out made explicit.** Any cross-sectional analysis with SM as DV anywhere in the paper (main, supplementary, sensitivity) disqualifies FT-EC7, regardless of how many longitudinal SM-as-DV analyses are present.

All five v7 changes are clarifications of v6 intent — no new logic, no new scope. They replace interpretive judgment with mechanical lookups so that C1 and C2 converge by construction.

### v6 — conceptual rewrite (replaces v5 B1–B20)

v6 replaced v5's twenty binding rules (B1–B20) with conceptual criteria that hinge on what the paper actually measured and analyzed, not on which YSTS items were named or which scale was cited:

- **FT-IC2 conceptual.** Composite "screen time" qualifies if the construct isolates phone/SM use; does not qualify if it bundles TV/console/phone with no breakdown. Mature/R-rated content alone, multi-device aggregated time alone, and SM-as-covariate/mediator/moderator-only all fail FT-IC2. The other side of the SM relationship must be individual-trait-level.
- **FT-IC3 + FT-IC4 collapsed and broadened.** Any quantitative result counts: traditional regression coefficients, ML feature importance, SHAP values, R², AUC, Bayesian posteriors, etc.
- **FT-EC7 simplified.** Drops the v5 "demographic-only predictor" qualifier. EC7 now hinges on design (longitudinal) and SM side of the equation (DV-only with no SM-as-IV analysis), nothing else.
- **Cascade reordered.** FT-IC5 (empirical) and FT-IC6 (non-duplicate) are tested before FT-IC2, so reviews/commentaries/preprints don't generate spurious FT-IC2 disagreements.
- **Cascade-DEFERRED convention.** Once a criterion fails, all downstream are marked DEFERRED, eliminating cascade-stage coding artifacts that produced false IRR splits in v5.
- **No resolver.** Criteria are tightened so that C1 and C2 converge by construction. Residual disagreements route to UNSURE for human review.

All Stage-2 screening prior to v7 is superseded; v7 results overwrite v6 in `02-L2/2L-scoring.csv`. Earlier passes remain in git history.
