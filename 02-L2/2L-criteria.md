# 2L Criteria — Full-Text Eligibility (PRISMA 2020)

**Stage:** Level 2 — full-text eligibility review.
**Scope:** Narrowed relative to 1L. Only papers reporting associations involving **smartphone use or social media use** are retained. Papers measuring only TV, console/PC gaming, streaming on non-phone devices, generic "screen time" without phone/SM specificity, "internet use," cyberbullying alone, or reading on screens are excluded.

This document specifies **a priori** eligibility criteria, exclusion codes, directionality rules, and borderline-case decision rules. Coders must apply these rules **verbatim** with no re-interpretation. Borderline rules in §5 are binding; if a paper matches a §5 rule, that rule's verdict overrides any general intuition.

---

## 1. Research Question

**Among publications that analyze data from the U.S. Adolescent Brain Cognitive Development (ABCD) Study, what associations have been reported between youth smartphone or social media use and psychosocial, health, cognitive, behavioral, neural, social, or sociodemographic variables?**

---

## 2. Eligibility Criteria — PECOS

### 2.1 Population (P) — FT-IC1

| | Rule |
|---|---|
| **MET** | Paper analyzes data from the U.S. ABCD Study. Any release (2.0–5.1). Sub-samples qualify (e.g., EARS N=640, autism subgroup, ABCD-COVID rapid-response survey). |
| **NOT_MET** (FT-EC1) | Amsterdam Born Children and their Development (Dutch ABCD). NHANES, MTF, MCS, Generation R, INMA, or any non-U.S.-ABCD cohort. ABCD cited only in introduction without analysis. Pooled analysis with another cohort where U.S.-ABCD-only estimates are NOT extractable. |
| **UNKNOWN** | No PDF AND abstract is silent on the cohort. |

### 2.2 Exposure (E) — FT-IC2 — *the most common disagreement; read all borderline rules*

A paper meets FT-IC2 if **at least one** of the following is measured AND enters a statistical analysis (regression, correlation, group comparison, network edge, etc.):

**Qualifying smartphone variables:**
- Smartphone ownership (yes/no), age of smartphone acquisition.
- Time on smartphone (self-report, parent-report, EARS passive sensing).
- Any app or app-category use (apps inherently = smartphone). Including: app counts, time per app category, notification volume.
- Mobile-phone-specific items: texting (phone), video chat (phone), bedtime phone use.
- Problematic / addictive smartphone scales: MPIQ, PSMUS, mobile-phone-checking scales.

**Qualifying social-media variables:**
- Time on social media (any modality — self-report, parent-report, passive).
- Platform-specific use: TikTok, Instagram, Snapchat, YouTube, Facebook, Twitter/X, Reddit, Pinterest, Tumblr, Discord, BeReal.
- Number of social media accounts; secret/private accounts; platform-membership indicators.
- Online dating / hookup apps.
- Problematic / addictive SM scales: SMAQ, Bergen SM/Facebook Addiction Scale, SNS-A, Bergen Adolescent Social Media Addiction Scale.
- Cyberbullying **only counts if the paper also separately measures one of the smartphone or social-media variables above with its own coefficient**.

**Does NOT qualify:**
- TV viewing alone, video streaming on unspecified device, console / PC video games, "internet use" without device or platform specification, e-mail, reading on screens, generic "screen time" totals where smartphone/SM contribution is not separately measured, mature-rated movie content alone, radio, podcasts, RF-EMF exposure measures.

#### 2.2.1 Borderline rule — composite measures (BINDING)

ABCD's Youth Screen Time Survey (YSTS) produces six per-day modalities: TV/movies, videos, video games, texting, social media, video chat. Many papers analyze YSTS items. Apply this rule:

> **MET** if the results section, any table, any figure, or any supplement reports a **separate** estimate (β / OR / RR / HR / IRR / r / mean difference / network edge weight / event-time hazard / latent path) for **any one** of the qualifying smartphone or social-media YSTS items (texting, video chat, social media, app/phone use). Other items in the same model (TV, gaming, videos) are irrelevant — what matters is whether *one* qualifying item has its own extractable estimate.
>
> **NOT_MET** if the *only* exposure variable analyzed is a summed/composite "total screen time" (or "total recreational screen use," "weighted average screen hours," "lifestyle factor that includes screen") with no extractable per-item estimate for any qualifying smartphone or social-media item — even when the underlying survey items would have allowed a breakdown.
>
> Latent variables (factor scores, profile membership, principal components) where screen items load alongside non-screen behaviors and only the latent score is reported → **NOT_MET** (FT-EC2 via E3 rule).

#### 2.2.2 Borderline rule — cyberbullying papers (BINDING)

> **MET** if the paper measures cyberbullying **AND** also separately measures at least one qualifying smartphone or SM variable with its own reported coefficient.
>
> **NOT_MET** if cyberbullying is the only screen-adjacent variable; FT-EC2 applies. A note about adolescents using the internet as background does not satisfy FT-IC2.

#### 2.2.3 Borderline rule — gaming-only papers (BINDING)

> **NOT_MET** if the only exposure is video gaming on console or PC, or video gaming with platform unspecified.
> **MET** only if the paper measures gaming via **mobile/app gaming** specifically (e.g., gaming on phone), or also measures a non-gaming smartphone/SM variable with its own coefficient.
> Problematic-gaming scales (VGAQ, IGDS9-SF) alone → **NOT_MET** unless the paper also reports a separately-measured smartphone or SM variable.

### 2.3 Comparator (C)
Not applicable. Observational association studies.

### 2.4 Outcomes (O)
Any non-smartphone-/non-SM-related variable measured on ABCD participants: mental health, physical health, sleep, substance use, cognitive, neural, social, recreational, sociodemographic, parenting, family, ACEs, clinical, genetic, environmental.

### 2.5 Study design (S) — FT-IC5

| | Rule |
|---|---|
| **MET** | Original empirical ABCD analysis: cross-sectional, longitudinal, mediation, moderation, ML, causal inference, target-trial emulation, network analysis, factor models with reported pathway estimates. |
| **MET (borderline — measurement papers)** | Paper develops or validates a smartphone/SM measurement instrument **AND** reports at least one screen → non-screen-outcome association in the same paper (criterion validity). |
| **NOT_MET** (FT-EC3) | Reviews, meta-analyses without new ABCD analysis, editorials, commentaries, letters, study protocols, resource/data descriptions, book chapters, news. |
| **NOT_MET** (FT-EC5) | Measurement-only papers: factor structure, reliability, EARS-vs-self-report concordance, method comparison — with **zero** screen → non-screen association anywhere in the paper. |

### 2.6 Reporting — FT-IC3 (statistical test) and FT-IC4 (extractable numeric)

Treat IC3 and IC4 as a paired check. Apply as follows:

#### 2.6.1 FT-IC3 — was an inferential statistical test reported?

| | Rule |
|---|---|
| **MET** | At least one inferential statistical test linking a qualifying smartphone/SM variable to a non-SM variable is reported. Qualifying tests: regression (OLS, logistic, Poisson, multilevel, GEE, Cox, GLM), SEM path coefficient, mediation indirect effect, moderation interaction, Pearson/Spearman/partial correlation, chi-square, Fisher's exact, t-test, ANOVA, mixed-effects coefficient, network-analysis edge weight, target-trial-emulation contrast. **Ridge / Lasso / GLM / penalized regression coefficients count.** Bayesian posterior estimates count. |
| **NOT_MET** | Only descriptive statistics (means, SDs, prevalences) with no inferential test of a SM↔non-SM association. SM appears only as an adjustment covariate with **no reported coefficient anywhere** in the paper. SM is included only in a latent score/composite with no separately reportable coefficient. |
| **UNKNOWN** | No PDF and the abstract does not allow this judgment. |

#### 2.6.2 FT-IC4 — is a numeric value reportable?

| | Rule |
|---|---|
| **MET** | The paper reports at least one numeric value for the qualifying SM ↔ non-SM association: β / OR / RR / HR / Cohen's d / r / F / t / χ² / η² / R² / p-value / 95% CI / posterior mean / network edge weight. May appear in main text, tables, labeled figures, or supplement. |
| **NOT_MET** | Only narrative claims ("screen time was associated with depression") with no numeric value anywhere. Figure with no numeric labels and no corresponding numeric supplement. |

#### 2.6.3 Borderline rule — machine-learning models (BINDING)

> **MET** if **any analysis in the paper** reports a numeric coefficient (linear β, logistic OR, Cox HR, GLM β, penalized β, Bayesian posterior mean) for the smartphone/SM variable. This includes coefficients reported in supplementary tables, sensitivity analyses, alternative model specifications, robustness checks, or model comparison tables.
>
> **NOT_MET** if the only outputs reported for the SM variable are: SHAP values, permutation importance, Gini importance, gain importance, attention weights, raw feature ranks, or feature-selection counts — with no traditional regression coefficient anywhere in the paper.
>
> Concordance / κ / Pearson correlation between two screen-time measures (e.g., EARS vs. self-report) is **not** a SM↔non-SM test (it's SM↔SM) → does not satisfy FT-IC3.

#### 2.6.4 Borderline rule — covariate-only screen time (BINDING)

> If the paper lists screen time / SM in the covariates section but the results tables do **not** report a coefficient for screen time / SM in any model, FT-IC3 = NOT_MET (E1).
>
> If screen time / SM appears in a model and **any** model in the paper reports its coefficient (even a fully-adjusted final model), FT-IC3 = MET. Look in supplementary tables.

---

## 3. Directionality and FT-EC7

Direction is **not** an eligibility filter, except for the narrow FT-EC7 case below.

| Pattern | Decision |
|---|---|
| Smartphone/SM → non-SM outcome (any timeframe) | **INCLUDE** |
| Non-SM predictor → smartphone/SM, **cross-sectional** | **INCLUDE** |
| Non-SM **individual psychological / clinical / behavioral / cognitive / neural / genetic** predictor → future smartphone/SM, longitudinal | **INCLUDE** |
| Mediation / moderation involving smartphone/SM | **INCLUDE** |
| Bidirectional / cross-lagged | **INCLUDE** |
| Non-SM **demographic-only** predictor → future smartphone/SM, longitudinal | **EXCLUDE (FT-EC7)** |

### 3.1 FT-EC7 — exact rule (BINDING)

FT-EC7 applies if **all three** of the following are simultaneously true:

1. **(a) Smartphone/SM is the dependent variable** in every reported analysis involving smartphone/SM. The paper does not report any analysis where smartphone/SM is the predictor of a non-SM outcome.
2. **(b) Every reported predictor of smartphone/SM is in the demographic/contextual set:** sex / gender, race/ethnicity, age, household income, parental education, parental marital status, immigration status, urbanicity, neighborhood quality, school type, study site, family structure (e.g., single-parent), or geographic region. **No** individual psychological, clinical, behavioral, cognitive, neural, sleep, dietary, ACEs, parenting-style, parental psychopathology, or genetic predictor appears.
3. **(c) Every reported analysis predicting smartphone/SM is longitudinal/prospective.** Baseline demographic predicts a later-wave smartphone/SM outcome. **If the paper also reports any cross-sectional analysis with the same demographics → smartphone/SM, FT-EC7 does NOT apply (cross-sectional carve-out).**

### 3.2 What is NOT FT-EC7 (do not exclude)

- ACEs, parenting practices, parental monitoring, family conflict, parental psychopathology → smartphone/SM (longitudinal or cross-sectional). These are **psychosocial / family** predictors, NOT pure demographics. **INCLUDE.**
- Sexual orientation or gender identity → smartphone/SM. Treated as identity/psychosocial, not pure demographics for this rule. **INCLUDE.**
- Pet ownership, religious participation, school involvement → smartphone/SM. Lifestyle / psychosocial. **INCLUDE.**
- Cross-sectional demographic → smartphone/SM. **INCLUDE** (the cross-sectional carve-out applies).
- Demographic predictors of smartphone/SM that are *also* analyzed alongside smartphone/SM → some non-SM outcome. **INCLUDE.**

---

## 4. Full-Text Exclusion Codes (hierarchical)

Assigned in this order; first applicable code wins.

| Code | Label | Trigger |
|---|---|---|
| **FT-EC1** | Not U.S. ABCD | FT-IC1 NOT_MET. |
| **FT-EC2** | No qualifying smartphone/SM variable | FT-IC2 NOT_MET (composite-only, TV-only, console-gaming-only, cyberbullying-only, "internet use" only, RF-EMF, etc.). |
| **FT-EC3** | Non-empirical | Review, editorial, commentary, protocol, resource/data paper, book chapter. |
| **FT-EC4** | No SM ↔ non-SM inferential test | FT-IC3 NOT_MET. SM is covariate-only with no coefficient. ML with SHAP-only, no coefficient. SM-↔-SM concordance only. Pure descriptive prevalence. |
| **FT-EC5** | Psychometric / measurement-only | Factor structure / reliability / concordance / method comparison of SM instrument with no external outcome. |
| **FT-EC6** | Duplicate | Preprint of an included peer-reviewed paper; conference abstract of an included full paper; supplementary deposit. |
| **FT-EC7** | Longitudinal demographic-only → SM | All three conditions in §3.1 satisfied. |

**UNSURE** — PDF unavailable AND abstract insufficient. Carry forward for retrieval; do not classify as EXCLUDE.

**NA_FOR_NOW** — PDF unavailable; classified separately from UNSURE for tracking.

---

## 5. Binding Edge-Case Rules

These rules are operative; coders apply them mechanically. If a paper matches a rule, the rule's verdict overrides any general intuition.

| Rule | Trigger | Verdict |
|---|---|---|
| **B1** | Paper uses YSTS and reports a separate β/OR for at least one of: social media, texting, video chat, mobile phone, or app-category. | FT-IC2 = MET regardless of whether other modalities (TV, gaming) are also in the same model. |
| **B2** | Paper uses YSTS but reports only a **summed total screen time** estimate (or a single composite) with no per-modality breakdown anywhere. | FT-IC2 = NOT_MET (FT-EC2). |
| **B3** | Paper measures cyberbullying as the only screen-adjacent variable. | FT-IC2 = NOT_MET (FT-EC2). |
| **B4** | Paper measures cyberbullying AND a separately-measured smartphone/SM variable with its own coefficient. | FT-IC2 = MET. |
| **B5** | Paper analyzes only console/PC video games or unspecified-platform video games. | FT-IC2 = NOT_MET (FT-EC2). |
| **B6** | Paper analyzes mobile/app gaming specifically OR analyzes gaming alongside another qualifying SM variable with separate coefficients. | FT-IC2 = MET. |
| **B7** | Paper measures only "internet use" without device or platform specification. | FT-IC2 = NOT_MET (FT-EC2). |
| **B8** | Paper reports any traditional regression coefficient for the SM variable in *any* analysis (main, supplementary, sensitivity). | FT-IC4 = MET (and FT-IC3 = MET if the test type is on the qualifying list). |
| **B9** | Paper reports only SHAP / permutation importance / Gini / attention weights / feature ranks for the SM variable. | FT-IC3 = NOT_MET (FT-EC4). |
| **B10** | SM appears in the covariates list but no coefficient for SM is reported anywhere. | FT-IC3 = NOT_MET (FT-EC4). |
| **B11** | SM is one of multiple variables loading on a single latent score, and only the latent score's coefficient is reported. | FT-IC2 = NOT_MET (FT-EC2). |
| **B12** | EARS vs self-report concordance (or any SM-vs-SM measurement comparison) is the only analysis reported. | FT-IC3 = NOT_MET (FT-EC4) → if also no external outcome, FT-IC5 = NOT_MET (FT-EC5). |
| **B13** | Measurement paper (e.g., scale validation) that ALSO reports any SM ↔ non-SM coefficient. | FT-IC5 = MET. |
| **B14** | Editorial, commentary, special-issue introduction, perspective, or letter with no original ABCD analysis. | FT-IC5 = NOT_MET (FT-EC3). |
| **B15** | Paper has any cross-sectional analysis where SM is DV and demographics are predictors. | FT-EC7 does NOT apply (cross-sectional carve-out). |
| **B16** | Paper's only SM-as-DV analyses are longitudinal AND every predictor is in the demographic-only set (sex, race, age, income, parental education, urbanicity, study site). | FT-EC7 applies → EXCLUDE. |
| **B17** | Paper's SM-as-DV analyses include **any** non-demographic predictor (ACEs, parenting, parental psychopathology, sleep, depression, anxiety, ADHD, impulsivity, sensation-seeking, executive function, neural, genetic, sexual orientation, gender identity, pet ownership, religious participation, etc.). | FT-EC7 does NOT apply. |
| **B18** | Paper reports both SM-as-DV (longitudinal demographic) AND SM-as-IV → non-SM outcome. | FT-EC7 does NOT apply (paper has SM-as-IV analysis). |
| **B19** | Cross-sectional sociodemographic, identity, family, or lifestyle predictor → smartphone/SM. | INCLUDE (FT-EC7 does NOT apply). |
| **B20** | Bidirectional / cross-lagged model where SM is both predictor and outcome. | FT-EC7 does NOT apply. |

---

## 6. Adjudication pipeline

| Step | Role | Blinding | Output |
|---|---|---|---|
| 2L-a | C1_AI — independent AI coder, full PDF | Blind to C2 | Per-criterion MET/NOT_MET/UNKNOWN + evidence + binding-rule references |
| 2L-b | C2_AI — independent AI coder, same criteria | Blind to C1 | Same |
| 2L-c | RESOLVE — independent AI coder | Has C1 + C2 reasons | Fires only on per-criterion disagreement |
| 2L-d | Human spot-check | Lead author | All EXCLUDE + all UNSURE + 10% INCLUDE sample |

### Final-decision algorithm (no subjective judgment)

For each of FT-IC1..FT-IC6:
1. If C1 = C2 → that status.
2. If one UNKNOWN, one known → UNKNOWN (carry to retrieval).
3. MET vs NOT_MET → resolver's call.

Then check FT-EC7 separately. Hierarchical exclusion:
1. First NOT_MET in [FT-IC1, FT-IC2, FT-IC5, FT-IC3, FT-IC4, FT-IC6] → EXCLUDE with that code.
2. If all MET and FT-EC7 applies → EXCLUDE FT-EC7.
3. Any remaining UNKNOWN → UNSURE (or NA_FOR_NOW if no PDF).
4. All MET, no EC7 → INCLUDE.

Cohen's κ between C1 and C2 reported per criterion.

---

## 7. Reported in `2L-scoring.csv`

One row per Stage-1 include (n = 171). Columns:
- Metadata: `paper_id, doi, title, first_author, year, journal, has_pdf`
- 1L decision carried forward: `L1_decision`
- Per criterion (FT-IC1..FT-IC6): `_C1`, `_C2`, `_RESOLVE`, `_FINAL`, `_C1_evidence`, `_C2_evidence`, `_RESOLVE_evidence`
- FT-EC7: `FT_EC7_C1`, `FT_EC7_C2`, `FT_EC7_RESOLVE`, `FT_EC7_FINAL`
- Final: `FINAL_DECISION` ∈ {INCLUDE, EXCLUDE, UNSURE, NA_FOR_NOW}, `FINAL_EXCLUSION_CODE`, `FINAL_FAILED_CRITERION`

---

## 8. Protocol deviations from prior versions

This v5 criteria set tightens FT-IC2/IC3/IC4 borderline language and operationalizes FT-EC7 (§3.1) to remove the agent-level disagreements that produced 75% C1-vs-C2 agreement on the v4 pass. Borderline rules B1–B20 are added as binding decision shortcuts. Coders must apply B1–B20 verbatim.

All Stage-2 screening prior to v5 is superseded; v5 results overwrite v4 in `02-L2/2L-scoring.csv`. Earlier passes remain in git history.
