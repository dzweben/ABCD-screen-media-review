# 2L Criteria — Full-Text Eligibility (PRISMA 2020)

**Stage:** Level 2 — full-text eligibility review.
**Scope:** Narrowed relative to 1L. Only papers reporting associations involving **smartphone use or social media use** (as defined below) are retained. Papers measuring only TV, console/PC video games, streaming on non-phone devices, generic "screen time" without phone/SM specificity, "internet use," reading on screens, or cyberbullying alone are excluded at 2L.

This document specifies **a priori** eligibility criteria, exclusion codes, directionality rules, edge cases, and the screening pipeline. Structured to satisfy PRISMA 2020 items 4 (question), 5 (eligibility criteria), 9 (selection process), 10a (data collection), and 16 (PRISMA flow).

---

## 1. Research Question

**Among publications that analyze data from the U.S. Adolescent Brain Cognitive Development (ABCD) Study, what associations have been reported between youth smartphone or social media use and psychosocial, health, cognitive, behavioral, neural, social, or sociodemographic variables?**

---

## 2. Eligibility Criteria — PECOS

### 2.1 Population (P)

| | Criterion |
|---|---|
| **Include** | U.S. ABCD Study participants. All data releases (2.0–5.1). Sub-samples (e.g., EARS N=640) qualify. |
| **Exclude (FT-EC1)** | Amsterdam Born Children and their Development (Dutch ABCD) cohort. Other datasets (NHANES, MTF, Generation R, MCS, etc.). ABCD mentioned only in intro/discussion without analysis. |
| **Pooled-cohort rule** | ABCD combined with another cohort → INCLUDE only if U.S.-ABCD-specific results are extractable (cohort-stratified estimates). Pooled-only → FT-EC1. |

### 2.2 Exposure (E) — narrowed to smartphone / social media

A paper qualifies on exposure only if it measures and analyzes at least one **specifically identifiable** smartphone-use or social-media-use variable. The qualifying question is: *Can the reader extract a coefficient, correlation, or test statistic that specifically represents smartphone or social media use (and not a broader screen composite)?*

| | Criterion |
|---|---|
| **Include** | Smartphone ownership / age of acquisition. Time on smartphone (self-report, parent-report, or passive/EARS). Any app-category use (apps inherently = smartphone). Social media (platform-specific or aggregated): time on social media, TikTok, Instagram, Snapchat, YouTube, Facebook, Twitter/X, Reddit, Pinterest, Tumblr. Problematic or addictive smartphone/SM use scales: SMAQ (Social Media Addiction Questionnaire), MPIQ (Mobile Phone Involvement Questionnaire), PSMUS, SNS-A, Bergen Facebook Addiction Scale, or adaptations. Number of social media accounts; secret/private social media accounts. Platform membership. Texting (phone-based). Video chat (phone-based). Online dating / hookup-app use. Bedtime phone/SM use. |
| **Exclude (FT-EC2)** | No qualifying smartphone or social media variable is measured, or measured but not separately extractable. **The following are NOT sufficient on their own:** television viewing; video streaming (YouTube/Netflix on non-phone devices, unspecified device); video games (console/PC/unspecified platform); reading on screens; e-mail (unspecified device); "internet use" (too ambiguous); "screen time" without modality breakdown; radio; podcasts; mature-rated movie content without phone/SM link. |
| **Mixed-modality rule** | Papers using the Youth Screen Time Survey that **separately report** smartphone-specific (e.g., texting, video chat) or social-media-specific coefficients → INCLUDE. Papers reporting only aggregate "total screen time" or composites where smartphone/SM contribution is not extractable → EXCLUDE (FT-EC2). |
| **"Internet use" judgment** | If the paper says "internet use" without clarifying smartphone- or social-media-based access → EXCLUDE (FT-EC2) as ambiguous. |
| **Video games judgment** | Console / PC video games alone → EXCLUDE (FT-EC2). Mobile / app-based games → INCLUDE (apps = smartphone). Unspecified platform → EXCLUDE as ambiguous. Problematic video-gaming scales (VGAQ, IGDS) → EXCLUDE unless the paper also measures smartphone or social media separately. |
| **Cyberbullying rule** | Cyberbullying alone is NOT a smartphone/SM variable. Qualifies only if the paper also measures smartphone or SM use separately with an extractable coefficient. Cyberbullying-only → FT-EC2. |

### 2.3 Comparator (C)
Not applicable. Observational association studies.

### 2.4 Outcomes (O)
Any non-smartphone/SM variable measured on ABCD participants: mental health, physical health, sleep, substance use, cognitive, neural, social, recreational, sociodemographic, parenting, family, ACEs, clinical, genetic, environmental.

### 2.5 Study Design (S)

| | Criterion |
|---|---|
| **Include** | Original empirical ABCD analyses — cross-sectional, longitudinal, mediation, moderation, machine-learning, causal-inference, target trial emulation. |
| **Exclude (FT-EC3)** | Reviews, meta-analyses without new ABCD analysis, editorials, commentaries, letters, protocols, resource/data descriptions, book chapters, news. |
| **Measurement papers** | INCLUDE if paper also reports at least one smartphone/SM ↔ non-SM-outcome association. EXCLUDE (FT-EC5) if content is limited to factor structure / reliability / concordance / method comparison of a phone/SM instrument with no external outcome. |

### 2.6 Reporting

| | Criterion |
|---|---|
| **Include (FT-IC4)** | At least one qualifying association yields a numeric result: β, OR, RR, HR, Cohen's d, r, F, t, χ², η², R², p-value, or CI. In main text, tables, labeled figures, or supplement. |
| **Exclude (FT-EC4)** | Narrative claims only; no numeric value for any smartphone/SM association. |
| **Independence (FT-IC6)** | Not a duplicate. Preprint of an included published paper → FT-EC6. Conference abstract of an included full paper → FT-EC6. |

---

## 3. Directionality

Direction is **not** an eligibility filter in most patterns. But prospective demographic-only prediction of smartphone/SM is out of scope.

| Pattern | Decision |
|---|---|
| Smartphone/SM → non-SM outcome (e.g., Instagram → depression) | INCLUDE |
| Smartphone/SM as mediator or moderator | INCLUDE |
| Bidirectional / cross-lagged models involving smartphone/SM | INCLUDE |
| **Cross-sectional**: any predictor (including demographic) → smartphone/SM use | INCLUDE — direction is not asserted at a single timepoint, so "DV" and "IV" are arbitrary labels. |
| **Longitudinal / prospective**: individual psychological or clinical predictor → future smartphone/SM use (e.g., ADHD → later smartphone use, impulsivity → later SM use, depression → later SM use, sensation seeking → later SM) | INCLUDE — individual characteristics as antecedents of smartphone/SM use is substantive. |
| **Longitudinal / prospective**: demographic or contextual predictor ONLY (no individual characteristic) → future smartphone/SM use (e.g., SES → later smartphone ownership; race × age → later SM use) | **EXCLUDE (FT-EC7)** — epidemiology-of-adoption question, out of scope. |
| Smartphone/SM used only as a covariate with no reported coefficient | EXCLUDE (FT-EC4) |

**FT-EC7 applies only when every reported analysis involving smartphone/SM fits the "longitudinal demographic → future SM" pattern.** If the paper also reports cross-sectional models with demographic predictors, OR any individual-characteristic predictor, OR any smartphone/SM → outcome model, FT-EC7 does not apply.

---

## 4. Full-Text Exclusion Codes (hierarchical)

Assigned in order; first applicable code wins.

| Code | Label | When to assign |
|---|---|---|
| **FT-EC1** | Not U.S. ABCD | Population fails. Amsterdam ABCD, other cohort, or ABCD cited only in intro. |
| **FT-EC2** | No smartphone/SM variable | No qualifying exposure (see 2.2). Generic "screen time" / TV / console-gaming / streaming / "internet use" without phone/SM breakdown. Cyberbullying-only. |
| **FT-EC3** | Non-empirical | Reviews, editorials, commentaries, protocols, resource papers. |
| **FT-EC4** | No inferential test of smartphone/SM ↔ non-SM | Descriptive-only without any hypothesis test. Or smartphone/SM included only as adjustment covariate with no reported coefficient. |
| **FT-EC5** | Psychometric / measurement-only | Factor structure, reliability, concordance, method comparison of a phone/SM instrument with no external outcome. |
| **FT-EC6** | Duplicate | Preprint, conference abstract, or supplement of an included paper. |
| **FT-EC7** | **Longitudinal demographic/contextual → future smartphone/SM (epidemiology of adoption)** | All reported smartphone/SM analyses fit the prospective demographic-only → SM pattern, with no individual psychological/clinical predictor and no cross-sectional model. |

**UNSURE** is reserved for papers where the full text cannot be retrieved and the abstract is insufficient to judge eligibility. Carried forward for retrieval; not EXCLUDE.

---

## 5. Edge Cases (binding)

Every edge case the pipeline has encountered has a verbatim decision rule. Coders apply these without re-interpretation.

### E1 — Smartphone/SM as one of many predictors in a multivariable model
Own coefficient reported → INCLUDE. Only covariate with no coefficient → EXCLUDE (FT-EC4).

### E2 — Smartphone/SM inside a 24-hour movement composite
If any "social media only" / "phone only" row or isotemporal substitution is extractable → INCLUDE. Whole-composite-only coefficients with no phone/SM pathway → EXCLUDE (FT-EC2).

### E3 — Smartphone/SM bundled in a latent construct
If loadings allow a smartphone/SM-specific pathway to be computed → INCLUDE. Latent-only path with no phone/SM-specific estimate → EXCLUDE (FT-EC4).

### E4 — Machine-learning models
Any coefficient (linear, logistic, penalized β, GLM β) reported for the phone/SM feature → INCLUDE. Only SHAP / permutation importance / Gini → EXCLUDE (FT-EC4).

### E5 — Measurement / method-validation papers
Also reports any phone/SM ↔ non-SM-outcome association → INCLUDE. Only factor structure / reliability / concordance → EXCLUDE (FT-EC5).

### E6 — Cyberbullying papers
Also measures smartphone or SM separately with own coefficient → INCLUDE. Cyberbullying-only → EXCLUDE (FT-EC2).

### E7 — Smartphone/SM as the outcome (see §3)
- Cross-sectional with any predictor → INCLUDE.
- Longitudinal with individual psychological/clinical predictor → INCLUDE.
- Longitudinal with demographic or contextual predictor only → EXCLUDE (FT-EC7).

### E8 — Descriptive vs. inferential
At least one χ², t-test, ANOVA, or regression comparing phone/SM across a non-SM grouping → INCLUDE. Only means, SDs, frequencies → EXCLUDE (FT-EC4).

### E9 — Recreation / activity-displacement
Tests smartphone/SM use vs. participation in other recreational activities (sports, music, hobbies, outdoor time, religious activity) → INCLUDE. Replaced by TV or console gaming only → does not qualify under v4 unless phone/SM is specifically involved.

### E10 — Special-issue introductions / resource papers
Own original smartphone/SM analysis → INCLUDE. No original analysis → EXCLUDE (FT-EC3).

### E11 — Null results
Reported non-significant coefficient with numeric β / OR / CI / p → INCLUDE.

### E12 — Figure-only results
Numeric supplementary table exists → INCLUDE. No numerics anywhere → UNSURE pending retrieval.

### E13 — Smartphone ownership as exposure
Against any non-screen outcome → INCLUDE. As outcome: cross-sectional any predictor → INCLUDE; longitudinal demographic-only → EXCLUDE (FT-EC7); longitudinal individual → INCLUDE.

### E14 — Sociodemographic predictors of smartphone/SM
Cross-sectional → INCLUDE. Longitudinal-only demographic → EXCLUDE (FT-EC7).

### E15 — Parenting / family environment predictors of smartphone/SM
Cross-sectional → INCLUDE. Longitudinal-only parenting/family → EXCLUDE (FT-EC7) **unless** the paper also reports a downstream non-SM outcome (e.g., parenting → SM → depression).

### E16 — Individual-characteristic predictors of smartphone/SM
ADHD, autism, depression, anxiety, personality, executive function, impulsivity, reward sensitivity, sensation seeking, sleep, cognitive ability, neural features, genetic risk → INCLUDE regardless of direction or timeframe.

### E17 — Video games on unspecified platform
→ EXCLUDE (FT-EC2) as ambiguous. INCLUDE only if the paper also measures smartphone/SM separately with extractable coefficient, OR clarifies mobile/app-based gaming.

### E18 — "Internet use" on unspecified device
→ EXCLUDE (FT-EC2) as ambiguous. INCLUDE only if the paper also measures smartphone or SM separately.

---

## 6. Adjudication Pipeline

| Step | Role | Blinding |
|---|---|---|
| 2L-a | C1_AI — independent AI coder, PDF + criteria | Blind to C2 |
| 2L-b | C2_AI — independent AI coder, same criteria | Blind to C1 |
| 2L-c | RESOLVE — third AI coder with access to PDF + C1 and C2 reasons | Only fires when C1 ≠ C2 on at least one criterion |
| 2L-d | Human spot-check — lead author | Reviews all EXCLUDE, all UNSURE, and a 10% random INCLUDE sample; can override with `HUMAN_OVERRIDE` + cited rule |

### Final-decision algorithm (no subjective judgment)

For each of FT-IC1..FT-IC6:
1. If C1 = C2 → that status.
2. If one UNKNOWN, one known → UNKNOWN (conservative, flagged for retrieval).
3. MET vs NOT_MET → resolver's independent call.

Then:
- First NOT_MET in hierarchy [FT-IC1, FT-IC2, FT-IC5, FT-IC3, FT-IC4, FT-IC6] → EXCLUDE with corresponding FT-EC code.
- FT-EC7 is checked separately after all FT-IC are MET: if smartphone/SM is the DV and all reported analyses are prospective demographic-only → EXCLUDE (FT-EC7).
- Any remaining UNKNOWN → UNSURE.
- All 6 criteria MET and FT-EC7 not triggered → INCLUDE.

### Inter-rater reliability
Cohen's κ reported per criterion between C1 and C2 in `2L-scoring.csv`.

---

## 7. Reported in `2L-scoring.csv`

Workbook structure (two tabs): **Tab 1 (1L)** holds the title/abstract scoring for all 620 papers (same columns as `1L-scoring.csv`). **Tab 2 (2L)** holds full-text scoring for the 171 papers that passed 1L, with per-criterion columns:

- Metadata: `paper_id, doi, title, first_author, year, journal, has_pdf`
- 1L decision carried forward: `L1_decision`
- Per criterion (FT-IC1..FT-IC6): `C1`, `C2`, `C1_evidence`, `C2_evidence`, `RESOLVE`, `RESOLVE_evidence`, `FINAL`
- Directionality / FT-EC7: `EC7_triggered`, `EC7_reason`
- Final: `FINAL_DECISION` ∈ {INCLUDE, EXCLUDE, UNSURE}, `FINAL_EXCLUSION_CODE`, `FINAL_FAILED_CRITERION`, `FINAL_REASON`
- Edge cases: `C1_edge_cases`, `C2_edge_cases`, `RESOLVER_edge_cases`
- Human override: `HUMAN_OVERRIDE`, `HUMAN_OVERRIDE_reason`

---

## 8. Protocol deviations

This v4 criteria set narrows 1L's broad screen-media scope to smartphone/SM-specific exposures and adds FT-EC7 for longitudinal demographic-only predictions of smartphone/SM use. All 171 papers that passed 1L are re-screened against the v4 2L criteria; prior v1/v2/v3 2L decisions are superseded and retained only in git history.
