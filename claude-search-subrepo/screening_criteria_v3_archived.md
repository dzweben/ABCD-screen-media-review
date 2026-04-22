# Screening Criteria — v3 DRAFT (PRISMA 2020-aligned)

This document specifies **a priori** eligibility criteria, selection procedure, and exclusion codes for the full-text (Stage 2) eligibility assessment of this systematic review. Structured to satisfy PRISMA 2020 items 5 (eligibility criteria), 8 (search strategy — separate document), 9 (selection process), 10a (data collection process), 15 (reporting bias assessment — separate document), and 16 (PRISMA flow diagram).

Review protocol: this criteria document serves as the pre-specified screening protocol. No criterion is modified after full-text screening begins.

---

## 1. Research Question (PRISMA item 4)

**Among publications that analyze data from the U.S. Adolescent Brain Cognitive Development (ABCD) Study, what associations have been reported between youth screen/digital media exposure and youth psychosocial, health, cognitive, behavioral, neural, social, or sociodemographic variables?**

---

## 2. Eligibility Criteria — PECOS (PRISMA item 5)

### 2.1 Population (P)

| | Criterion |
|---|---|
| **Include** | Participants enrolled in the U.S. Adolescent Brain Cognitive Development (ABCD) Study (N ~ 11,878 youth, ages 9–10 at baseline in 2016–2018, with annual follow-ups through age 19). Includes all ABCD data releases (2.0, 3.0, 4.0, 5.0, 5.1). Sub-samples of ABCD (e.g., the N = 640 EARS passive-sensing sub-study) qualify. |
| **Exclude (FT-EC1)** | Amsterdam Born Children and their Development (Dutch ABCD) cohort. Other datasets (NHANES, MTF, Generation R, MCS, etc.) used without U.S. ABCD data. Papers that mention the ABCD Study only in introduction/discussion but analyze a different cohort. |
| **Pooled-cohort edge case** | Paper combining U.S. ABCD with another cohort → INCLUDE if U.S.-ABCD-specific results are extractable (e.g., cohort-stratified table); EXCLUDE (FT-EC1) if only pooled estimates are reported. |

### 2.2 Exposure (E)

| | Criterion |
|---|---|
| **Include** | At least one measured variable capturing screen-based digital-media exposure or engagement in the ABCD sample. Qualifying exposures include (non-exhaustive): total screen time, modality-specific screen time (TV, video streaming, gaming, social media, texting, video chat, browsing, e-mail), smartphone ownership or age of acquisition, passive sensing (EARS, screen-state, app categories, notifications), problematic / compulsive / addictive screen-use scales (SMAQ, IGDS9-SF, VGAQ, PSMUS, SNS-A), bedtime screen use, parent-report of child screen use, social-media-platform membership, gaming frequency, online dating/hookup-app use, mature-rated media content exposure (R-rated movies, mature video games). |
| **Exclude (FT-EC2)** | No screen/digital-media variable is measured or entered into any analysis in the paper. |
| **Cyberbullying decision rule** | Cyberbullying victimization/perpetration **alone** is not a screen-media exposure. Included only if the same paper also measures a separate screen-exposure variable (time, dose, platform use, frequency). If cyberbullying is the only screen-adjacent measure → EXCLUDE (FT-EC2). |
| **Media-content decision rule** | Mature-rated content exposure (movies, games) counts as a screen-media exposure because engagement necessarily involves screen use. |

### 2.3 Comparator (C)

Not applicable. This review synthesizes observational association studies; comparator is typically "lower screen exposure" vs "higher screen exposure" but formal comparator is not a screening requirement.

### 2.4 Outcomes (O)

| | Criterion |
|---|---|
| **Include** | ANY non-screen variable measured on ABCD participants or their environment, entered into an association with the screen variable. Qualifying outcome domains (non-exhaustive): mental health (depression, anxiety, internalizing, externalizing, suicidality, psychotic-like experiences, ADHD, OCD, conduct, emotion dysregulation); physical health (BMI, obesity, cardiometabolic, puberty); sleep (duration, quality, latency, bedtime behaviors); substance use (alcohol, nicotine, cannabis, other); cognitive (executive function, working memory, attention, IQ, academic achievement, picture vocabulary, crystallized/fluid intelligence); neural / brain (structural MRI, functional MRI, connectivity, white matter, cortical thickness, cortical volume); social (peer relationships, family conflict, dating, bullying, cyberbullying); recreational / lifestyle (sports, music, hobbies, outdoor time, religious activity, physical activity, diet); sociodemographic (SES, race/ethnicity, sex, gender identity, sexual orientation, immigration status, age, household income, parental education); environmental (urbanicity, neighborhood, school type); family/parenting (parental monitoring, family conflict, media parenting practices, parent screen use); adverse experiences (ACEs, trauma exposure); clinical (autism, ADHD, eating disorder symptoms, gaming disorder); genetic (polygenic scores). |
| **Exclude (FT-EC4)** | Only screen ↔ screen associations tested (e.g., EARS objective vs self-report concordance; gaming screen time vs social-media screen time correlation; test-retest of a screen scale). |

### 2.5 Study Design (S)

| | Criterion |
|---|---|
| **Include** | Original empirical analyses of ABCD data — cross-sectional, longitudinal, mediation, moderation, machine-learning, causal-inference frameworks. Secondary analyses. Pre-registered replications. |
| **Exclude (FT-EC3)** | Narrative reviews, systematic reviews, meta-analyses without new ABCD analyses, editorials, commentaries, letters to the editor, opinion pieces, study protocols describing planned (not completed) analyses, resource/data papers describing the ABCD battery without screen↔outcome analyses, book chapters, news summaries. |
| **Include (borderline)** | Measurement / psychometric papers that ALSO report at least one screen ↔ non-screen-outcome association as validity evidence. |
| **Exclude (FT-EC5)** | Measurement / psychometric papers whose entire empirical content is factor structure, reliability, concordance, or method comparison of a screen instrument with no external outcome tested. |

### 2.6 Reporting

| | Criterion |
|---|---|
| **Include (FT-IC4)** | At least one qualifying association yields a numeric result extractable for evidence synthesis: β, OR, RR, HR, Cohen's d, Pearson/Spearman/partial r, F, t, χ², η², R², p-value, or confidence interval. Numeric results may appear in the main text, tables, figures with numeric labels, or supplementary materials. |
| **Exclude (FT-EC4)** | Results reported only as narrative claims (e.g., "screen time was associated with depression") without any numeric coefficient, CI, or p-value. Figures without numeric values and no corresponding table. |
| **Edge case** | Paper shows a figure without numeric labels but references a supplementary table with numerics → INCLUDE. |
| **Independence (FT-IC6)** | Paper is not a duplicate of an already-included paper. Preprint of an included published paper → EXCLUDE (FT-EC6). Conference abstract of an included full-text paper → EXCLUDE (FT-EC6). Supplementary data deposits → EXCLUDE (FT-EC6). Same-sample, different-analysis papers are both INCLUDE (overlap handled at data-extraction and synthesis stages). |

---

## 3. Full-Text Exclusion Codes (hierarchical)

Assigned in order; first applicable code is recorded.

| Code | Label | Operationalization |
|---|---|---|
| **FT-EC1** | Not U.S. ABCD Study | Population fails (Amsterdam ABCD, other cohort, or ABCD mentioned only in intro/discussion). |
| **FT-EC2** | No screen media variable analyzed | Screen only in narrative; no screen variable in any model/table. Cyberbullying-only (no separate screen exposure) falls here. |
| **FT-EC3** | Non-empirical or no original ABCD analysis | Reviews, editorials, commentaries, letters, protocols, resource/data papers, book chapters. |
| **FT-EC4** | No inferential test of screen ↔ non-screen association | Only screen ↔ screen associations, or only descriptive statistics (means, SDs, prevalences) with no hypothesis test. |
| **FT-EC5** | Psychometric / measurement-only paper | Empirical content limited to factor structure, reliability, concordance, or method comparison of a screen instrument. |
| **FT-EC6** | Duplicate / overlapping with included paper | Preprint of included paper; conference abstract of included full paper; supplementary data deposit. |

**UNSURE** (PRISMA category: "retrieval pending" or "further information required") is reserved for papers where the full text cannot be retrieved and the abstract is insufficient to judge FT-IC2/3/4. These are not EXCLUDE; they are carried forward for retrieval. Reported separately in the PRISMA flow.

---

## 4. Directionality

Consistent with PRISMA eligibility-based (not exposure/outcome-restricted) screening, directionality is **not** an eligibility criterion. All four patterns below are **INCLUDE** when an extractable stat exists; direction is coded during data extraction.

| Pattern | Decision |
|---|---|
| Screen predicts non-screen outcome (e.g., social media → depression) | INCLUDE |
| Non-screen predicts screen outcome (e.g., ACEs → screen time; pet ownership → screen time; sexual orientation → screen use) | INCLUDE |
| Screen is a mediator (ACEs → screen time → depression) | INCLUDE |
| Screen is a moderator (peer victimization × screen time → depression) | INCLUDE |
| Bidirectional / cross-lagged (CLPM of screen ↔ depression) | INCLUDE |

---

## 5. Edge Cases — Binding Decision Rules

Every disagreement case encountered in prior screening rounds is resolved by one of the rules below. Coders must apply these rules verbatim and may not re-interpret them.

### E1. Screen as one of many predictors in a multivariable model
- Screen's own coefficient (β, OR, CI, p) is reported anywhere in the paper → **INCLUDE**.
- Screen is listed only as an adjustment covariate with no coefficient reported anywhere → **EXCLUDE (FT-EC4)**.

### E2. Screen inside a 24-hour movement / compositional framework
- Any results table row, column, or figure panel reports a "screen time only" coefficient, an isotemporal substitution involving screen, or a separate effect estimate for the screen component → **INCLUDE**.
- Only whole-composite effects reported (e.g., "meets all 24-h guidelines" vs "does not") with no screen-specific estimate → **EXCLUDE (FT-EC4)**.

### E3. Screen bundled in a latent construct
- Latent-variable model where screen is one of several indicators and only the latent's path is reported, with no screen-specific pathway extractable → **EXCLUDE (FT-EC4)**.
- Loadings or pathway estimates allow screen-specific indirect effect to be computed → **INCLUDE**.

### E4. Machine-learning models
- Any coefficient reported (linear β, logistic OR, penalized β, GLM β) for the screen feature → **INCLUDE**.
- Only SHAP values / permutation importances / Gini indices reported with no coefficient → **EXCLUDE (FT-EC4)**.

### E5. Measurement / method-validation papers
- Paper reports any screen → non-screen-outcome association (even framed as criterion validity) → **INCLUDE**.
- Paper reports only measurement concordance, reliability, factor structure, or method comparison → **EXCLUDE (FT-EC5)**.

### E6. Cyberbullying papers
- Paper measures cyberbullying **and** a separate screen-exposure variable, with at least one statistical test involving the screen variable → **INCLUDE**.
- Paper measures cyberbullying only, with no screen time / dose / platform-use variable → **EXCLUDE (FT-EC2)**.

### E7. Screen as the outcome
- Any non-screen predictor with an extractable coefficient predicting screen outcome (sociodemographic, psychosocial, behavioral, clinical, lifestyle) → **INCLUDE**.

### E8. Descriptive papers
- Paper reports at least one chi-square, t-test, ANOVA, or regression comparing screen across a non-screen grouping → **INCLUDE**.
- Paper reports only means, SDs, percentages with no inferential test → **EXCLUDE (FT-EC4)**.

### E9. Recreation / activity-displacement papers
- Screen use tested for association with participation in other recreational activities (sports, music, hobbies, religious activity, outdoor time, reading, clubs, community involvement) → **INCLUDE**. Recreational participation is a behavioral/lifestyle outcome domain.
- Only screen-to-screen (e.g., gaming time vs video-streaming time displacement) → **EXCLUDE (FT-EC4)**.

### E10. Special-issue introductions / resource papers
- Paper itself reports at least one original screen ↔ outcome analysis → **INCLUDE**.
- No original analysis → **EXCLUDE (FT-EC3)**.

### E11. Null results
- Reported but non-significant coefficient with numeric β / OR / CI / p → **INCLUDE**. Non-significance is not exclusion.

### E12. Figure-only results
- Numeric supplementary table exists → **INCLUDE**.
- No numeric values anywhere → flag for author contact, **UNSURE** until retrieval resolves.

### E13. Screen ownership as exposure
- Smartphone ownership / age-of-acquisition tested for association with any non-screen outcome (depression, obesity, sleep, cognition, etc.) → **INCLUDE**.

### E14. Sociodemographic predictors of screen use
- Sex, race/ethnicity, SES, gender identity, sexual orientation, immigration status, age, household income predict a screen variable → **INCLUDE** (sociodemographics are eligible non-screen predictors). Consistent with E7.

### E15. Parenting / family-environment predictors of screen
- Parental monitoring, media parenting practices, parental mental health, family conflict, family structure, pet ownership predict screen use → **INCLUDE**.

---

## 6. Selection Process (PRISMA item 9)

### 6.1 Screening pipeline

| Stage | Screener | Blinding |
|---|---|---|
| Stage 1 — Title/abstract | Lead author (human) + AI-coder validation | N/A |
| Stage 2a — Full-text, independent coder 1 (C1_AI) | AI coder (Haiku) with PDF + criteria | Blind to C2 |
| Stage 2b — Full-text, independent coder 2 (C2_AI) | AI coder (Haiku) with PDF + criteria | Blind to C1 |
| Stage 2c — Adjudication | AI resolver (Haiku) with PDF, criteria, and both C1/C2 reasons | Triggered only when C1 ≠ C2 |
| Stage 2d — Human spot-check | Lead author | Reviews all EXCLUDE and UNSURE decisions; can override to HUMAN_OVERRIDE |

### 6.2 Final decision rule

```
IF C1_AI == C2_AI:
    FINAL_DECISION = C1_AI
ELSE:
    FINAL_DECISION = RESOLVE
IF HUMAN_OVERRIDE is not empty:
    FINAL_DECISION = HUMAN_OVERRIDE
```

### 6.3 Inter-rater reliability

Cohen's κ between C1_AI and C2_AI is reported. All disagreements are itemized in a supplementary table with C1, C2, and RESOLVE reasons.

### 6.4 Human spot-check scope

Lead author reviews:
- All papers where FINAL_DECISION = EXCLUDE (to catch false negatives).
- All papers where FINAL_DECISION = UNSURE.
- A 10% random sample of FINAL_DECISION = INCLUDE (to catch false positives).

---

## 7. PRISMA Flow Reporting (PRISMA item 16)

Stage 2 will report, at minimum:

- Full-text articles assessed for eligibility: **n = 171**
- Full-text articles excluded, by reason:
  - FT-EC1 (not U.S. ABCD): n = ___
  - FT-EC2 (no screen variable): n = ___
  - FT-EC3 (non-empirical): n = ___
  - FT-EC4 (no screen↔non-screen test): n = ___
  - FT-EC5 (psychometric-only): n = ___
  - FT-EC6 (duplicate): n = ___
- Full-text articles included in qualitative synthesis: n = ___
- Full-text articles included in quantitative synthesis: n = ___
- UNSURE (retrieval pending): n = ___

---

## 8. Pre-registration and protocol deviations

This review is registered / protocol-deposited (OSF or equivalent — to be confirmed). This v3 criteria document reflects revisions from the v1 ("focal variable" criterion) and v2 (FT-IC2 revised) after early piloting revealed inter-rater reliability problems with the original operationalization. The revision itself is a protocol deviation and will be reported in the PRISMA paper's Methods as such, with rationale.

All screening after the date of this v3 document uses v3 criteria verbatim. Screening performed against v1 and v2 criteria is re-run under v3.

---

## What to review / redline before we re-screen

Things that still need your sign-off:

1. **Research question** (Section 1) — is this actually what we're answering?
2. **P / E / O scope** (Section 2) — anything I've marked "include" that should be out? Anything I've excluded that should be in?
3. **Cyberbullying rule** (E6) — strict rule is "screen variable must be separately measured." Confirm.
4. **ML rule** (E4) — "coefficient required, SHAP alone doesn't count." Confirm.
5. **Null results** (E11) — confirm you want these INCLUDED.
6. **Human spot-check scope** (6.4) — 10% of INCLUDES enough? All EXCLUDES enough?
7. **Pre-registration** — do we have an OSF registration to cite, or do we need to file one now?
8. **Any E# rule you want added** — every disagreement the pipeline produces should end up as an explicit binding rule here.
