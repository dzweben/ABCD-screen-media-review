# Screening Criteria

This review uses a two-stage screening process per PRISMA 2020 guidelines.

---

## Stage 1: Title and Abstract Screening

### Inclusion Criteria

Studies were included at Stage 1 if they met ALL of the following:

| Code | Criterion | Operationalization |
|------|-----------|-------------------|
| **IC1** | Uses data from the Adolescent Brain Cognitive Development (ABCD) Study | The U.S. longitudinal cohort initiated in 2015 (N ~ 11,878). Must reference the ABCD Study by name or use ABCD data accessed through the NIMH Data Archive (NDA). Papers using the Amsterdam Born Children and their Development (ABCD) cohort are excluded. |
| **IC2** | Includes a screen or digital media variable | Any measured variable capturing screen-based media exposure, including but not limited to: screen time (total or modality-specific), social media use, smartphone/mobile phone use, internet use, texting/text messaging, video gaming, television viewing, digital media use, passive screen sensing (e.g., EARS), or problematic/compulsive use scales (e.g., SMAQ). The variable may serve as exposure, outcome, mediator, moderator, or covariate. |
| **IC3** | Reports original empirical findings | Presents quantitative analysis of ABCD data with extractable results. Includes secondary data analyses, methodological papers with empirical demonstrations, and preregistered analyses with reported results. |
| **IC4** | Published in a peer-reviewed journal | Full-text article in a peer-reviewed outlet. |

### Exclusion Criteria

Studies were excluded at Stage 1 if ANY of the following applied:

| Code | Criterion | Operationalization |
|------|-----------|-------------------|
| **EC1** | Does not use ABCD Study data | Includes papers using other datasets (e.g., MTF, NHANES, MCS, Generation R), the Amsterdam ABCD cohort, or papers that reference the ABCD Study only in the introduction/discussion without analyzing ABCD data. |
| **EC3** | No original empirical analysis | Reviews, editorials, commentaries, letters to the editor, study protocols, meta-analyses pooling across studies, book chapters, news summaries, and policy briefs without original ABCD data analysis. |
| **EC4** | Conference abstract only | Abstracts from conference proceedings (e.g., SLEEP, AHA, ACSM, SAHM) without a corresponding full-text peer-reviewed publication. If a published version exists, the published version is retained and the abstract is excluded as EC5. |
| **EC5** | Duplicate | Preprints (bioRxiv, medRxiv, SSRN, OSF, ResearchSquare) where the peer-reviewed version is already included; supplementary data deposits (Figshare, Zenodo); identical analyses published in multiple venues. The peer-reviewed version is always retained. |

---

## Stage 2: Full-Text Eligibility Review

All papers that passed Stage 1 (INCLUDE, n = 171) are assessed against the full-text eligibility criteria below. Two independent coders review each full text. Disagreements are resolved by discussion or a third reviewer.

### Full-Text Inclusion Criteria

Studies were retained at Stage 2 if they met ALL of the following:

| Code | Criterion | Operationalization |
|------|-----------|-------------------|
| **FT-IC1** | Screen media is a focal variable | Screen media must function as a primary predictor, outcome, mediator, or moderator in at least one analytic model. Papers in which screen media appears **only** as a covariate or control variable are excluded. |
| **FT-IC2** | Tests an association between screen media and at least one substantive outcome | The paper must report a quantitative association (correlation, regression coefficient, odds ratio, group comparison, path coefficient, prediction accuracy, etc.) linking a screen media variable to at least one outcome. Eligible outcome domains include but are not limited to: |
| | | - **Neural/brain:** structural MRI, fMRI activation, connectivity, white matter, cortical thickness |
| | | - **Mental health:** internalizing, externalizing, depression, anxiety, suicidality, psychotic-like experiences, emotion dysregulation |
| | | - **Behavioral:** substance use/initiation, risk-taking, aggression, conduct problems, impulsivity |
| | | - **Cognitive:** executive function, working memory, attention, academic achievement, IQ/fluid/crystallized intelligence |
| | | - **Sleep:** duration, quality, latency, bedtime behaviors |
| | | - **Physical health:** BMI, obesity, physical activity, cardiometabolic markers |
| | | - **Social:** peer relationships, family conflict, cyberbullying, dating, social functioning |
| | | - **Clinical:** ADHD symptoms, gaming disorder, problematic media use scales, eating disorder symptoms |
| **FT-IC3** | Quantitative results are extractable | At minimum, the paper reports an effect size, test statistic, or p-value for the screen-media-to-outcome association. If only a figure is shown with no numeric values, the paper is flagged for contact with authors but provisionally included. |

### Full-Text Exclusion Criteria

Each excluded paper is assigned exactly one primary reason — the **first** criterion failed in the hierarchy below.

| Code | Criterion | Operationalization | Example |
|------|-----------|-------------------|---------|
| **FT-EC1** | Not ABCD data (discovered at full text) | Full-text review reveals the paper does not actually analyze ABCD data, despite appearance at abstract stage. | Paper references ABCD in introduction but analyses use a different sample. |
| **FT-EC2** | Screen media is covariate only | Screen media appears **exclusively** as a statistical control (covariate) in every model. No model in the paper treats screen media as a predictor, outcome, mediator, or moderator — it is only included to adjust for confounding. Papers that test screen media in **any** analytic role (even as one mediator among many, or one predictor among many) do **not** meet this exclusion. | Paper predicts brain volume from adverse childhood experiences, controlling for screen time. Screen time has no hypothesis, no dedicated model, and no results interpreted. |
| **FT-EC3** | No association tested | Screen media and a substantive outcome are both measured but no statistical association between them is modeled. Purely descriptive reporting of screen media prevalence or means does not qualify. | Paper reports screen time means by demographic group but never tests whether screen time relates to any outcome. |
| **FT-EC4** | Psychometric only | Paper solely validates or develops a screen media measurement instrument without testing associations with substantive outcomes. | Paper reports factor structure and test-retest reliability of the SMAQ with no outcome analyses. |
| **FT-EC5** | Full text not obtainable | Full text could not be retrieved through institutional access, open access, or interlibrary loan after reasonable effort. Papers coded FT-EC5 are marked **UNSURE** (not EXCLUDE) until all retrieval options are exhausted. | Paper behind paywall with no OA version; ILL request returned no results. |
| **FT-EC6** | Duplicate sample (discovered at full text) | Full-text review reveals the paper uses an identical sample, exposure, and outcome as another included study. The more comprehensive or more recent version is retained. | Two papers from the same lab report the same baseline cross-sectional model with trivial covariate differences. |

### Directionality Decision Rules

The following edge cases are **included** and coded for directionality during data extraction:

| Scenario | Decision | Rationale |
|----------|----------|-----------|
| Screen media is the **DV** (e.g., predictors of screen time such as ADHD, ACEs, parenting, SES) | **INCLUDE** | Papers examining what predicts screen media use are informative about the functional role of screen media in youth development. Directionality is a coding variable, not an eligibility criterion. |
| Screen media is a **mediator** between two other variables (e.g., ACEs → screen time → depression) | **INCLUDE** | Screen media is a focal variable, and the mediation path tests its association with an outcome. |
| Screen media is a **moderator** (e.g., the effect of peer victimization on depression varies by screen time level) | **INCLUDE** | Screen media is a focal variable that modifies the relationship between a predictor and outcome. |
| Bidirectional model (e.g., CLPM testing screen time → depression AND depression → screen time simultaneously) | **INCLUDE** | Both directions test screen-media-to-outcome associations. |

### Notes

- **No modality-based exclusion.** Papers examining any screen media modality (TV, gaming, social media, smartphone, internet, total screen time) are eligible. Modality is coded during full-text data extraction, not used as a screening criterion.
- **Aggregate screen time.** Papers reporting only total screen time without modality breakdown are included. Whether modality-specific data are available is assessed during full-text coding.
- **Exclusion hierarchy.** When a paper fails multiple criteria, assign the first applicable code in order: FT-EC1 → FT-EC2 → FT-EC3 → FT-EC4 → FT-EC5 → FT-EC6.
- **PRISMA flow.** Stage 2 results are reported as: "Full-text articles assessed for eligibility (n = X)" → "Full-text articles excluded, with reasons (n = Y)" with counts itemized by FT-EC code → "Studies included in quantitative synthesis (n = Z)."
