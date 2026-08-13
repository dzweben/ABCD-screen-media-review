# Stage 2 Eligibility Criteria -- Full-Text Review (PRISMA 2020)

**Stage:** Level 2 (L2) -- full-text eligibility review.

## Scope

A study is eligible for inclusion if it reports an inferential association between **smartphone or social media use** (as independent or dependent variable) and an **individual-trait-level outcome** (neural, behavioral, health, cognitive, well-being, personality, substance use, sleep, academic, or analogous within-person construct) in participants of the **U.S. Adolescent Brain Cognitive Development (ABCD) Study**.

The criteria below apply to what each paper actually measured and analyzed, not to the labels chosen by its authors. A composite variable named "screen time" must satisfy the same test as a variable named "social media use" if the items inside the composite differ. Screening is conceptual, not label-driven.

## Research question

Among publications analyzing data from the U.S. Adolescent Brain Cognitive Development Study, what associations have been reported between youth smartphone or social media use and individual-trait-level outcomes (neural, behavioral, health, cognitive, well-being, personality, substance use, sleep, academic, or analogous constructs)?

## How the criteria are applied

Criteria are evaluated **in the sequence shown below**. The first criterion that a paper fails determines its exclusion category, and subsequent criteria are not assessed. A paper that satisfies every inclusion criterion (FT-IC1 through FT-IC4) and is not captured by the exclusion criterion (FT-EC7) is included.

**Sequence:** FT-IC1 -> FT-IC5 -> FT-IC6 -> FT-IC2 -> FT-IC3 -> FT-IC4 -> FT-EC7.

Exclusion codes (FT-EC1 through FT-EC7) map directly onto the criterion that determined exclusion (see Section Exclusion codes).

---

## FT-IC1 -- Population: U.S. ABCD Study

The qualifying cohort is the U.S. Adolescent Brain Cognitive Development Study: NIH-funded, 21 U.S. recruitment sites, baseline ages 9-10, any data release (2.0-5.1 or later).

**Met.** The paper analyzes data from the U.S. ABCD Study. ABCD subsamples -- Effortless Assessment Research System (EARS), autism subsample, ABCD COVID-19 rapid-response surveys, and similar derivatives -- qualify. Pooled multi-cohort analyses combining the U.S. ABCD with another cohort qualify only if at least one ABCD-specific estimate (in main, supplementary, or sensitivity analyses) is extractable.

**Not met.** A different cohort sharing the "ABCD" acronym, including the **Amsterdam Born Children and their Development (Dutch ABCD)** study, "Adolescent Behavior and Cognitive Development" cohorts in other countries, and any non-U.S. ABCD initiative. Cohort identity is verified from the recruitment description and methods section, not from the acronym alone. Studies that cite ABCD only in the introduction or discussion without analyzing ABCD data do not qualify.

-> Exclusion code **FT-EC1**.

---

## FT-IC5 -- Original empirical analysis

**Met.** The paper reports an original empirical analysis of ABCD data. Eligible designs include cross-sectional, longitudinal, mediation, moderation, machine learning, causal inference, target-trial emulation, network analysis, mixed-effects, and factor models with reported pathway estimates.

**Not met.** Reviews, meta-analyses without new ABCD analysis, editorials, commentaries, perspectives, letters, study protocols, resource and data-availability descriptions, special-issue introductions, conference abstracts (single-page summaries of meeting talks, with no methods section, results tables, or full statistical reporting), book chapters, and news pieces.

-> Exclusion code **FT-EC3**.

---

## FT-IC6 -- Non-duplicate

**Met (default).** Published peer-reviewed paper.

**Not met.** The paper is a preprint of a peer-reviewed article also included in the corpus, a conference abstract of an already-included full paper, or a re-analysis of identical data with no new statistical content beyond an already-included paper.

-> Exclusion code **FT-EC6**.

---

## FT-IC2 -- Qualifying smartphone or social media exposure

FT-IC2 is direction-agnostic. A qualifying smartphone or social media variable may appear as the independent or dependent variable in an analysis. It does not qualify if it appears only as a mediator, moderator, or covariate.

The paper must, in at least one analysis, pair a qualifying smartphone or social media variable with an **individual-trait-level** variable on the other side of the relationship.

### Two-step test

**Step 1: Search for a phone or social media-specific numeric estimate.**

Examine all results locations -- main tables, supplementary tables, appendices, sensitivity analyses, robustness checks, alternative specifications, and sub-group breakouts -- for at least one numeric estimate (β, OR, RR, HR, IRR, r, mean difference, SHAP value, feature importance, path coefficient, network edge weight, Bayesian posterior, etc.) where the variable label is one of the following phone or social media-specific items:

- Time on phone; smartphone ownership; age of first smartphone; phone time
- Time on social media; time on a named social media platform (TikTok, Instagram, Snapchat, YouTube, Facebook, Twitter/X, Reddit, Pinterest, Tumblr, Discord, BeReal)
- Texting; video chat; video calling
- App use; app-category time; notification volume; passively sensed phone or app time
- Problematic or addictive phone scales (Mobile Phone Involvement Questionnaire [MPIQ], Problematic Smartphone Use Scale [PSMUS], mobile-phone-checking measures)
- Problematic or addictive social media scales (Social Media Addiction Questionnaire [SMAQ], Bergen Social Media/Facebook Addiction Scale, Social Networking Sites-Addiction Scale [SNS-A])
- Online dating apps; hookup apps; number of social media accounts; secret or private social media accounts

If such an estimate exists and is paired with an individual-trait-level variable on the other side, FT-IC2 is met. The paper's headline analysis may use a composite variable; it is sufficient that a per-modality estimate exists in a supplementary or sensitivity table.

**Step 2: If Step 1 returns no qualifying estimate, evaluate the composite variable's contents.**

The label of the composite is irrelevant. "Screen time," "screen media activity," "digital socializing," "recreational screen use," and "media use" are all evaluated by the same rule: whether the items the methods report as components are exclusively phone or social media-related.

- **Met** when the composite is built **exclusively** from phone, social media, or digital-socializing items. Examples: "digital socializing = texting + video chat + social media"; "phone-based media time = social media + texting + video chat + app use."
- **Not met** when the composite includes any non-phone, non-social-media activity that is not separately broken out elsewhere in the paper. Disqualifying ingredients include television, movies on television, video streaming on a non-phone device, console video games, PC video games, unspecified-platform video games, reading on screens, computer-only time, music listening, and generic "internet browsing."

### Individual-trait-level variables

The other side of the relationship must be an individual-trait-level construct. Eligible constructs include:

> Neural; behavioral; physical health; mental health; cognitive; well-being; personality; substance use; sleep; academic; psychiatric symptom; genetic or polygenic; biological (BMI, puberty, biomarker); clinical diagnosis; adverse childhood experiences (ACEs) or trauma exposure; parenting practices; parental psychopathology; family functioning; peer associations; school engagement; extracurricular activities; or any other within-person psychosocial or behavioral construct that varies developmentally and is the kind of outcome that smartphone or social media use could plausibly affect.

### Variables that do not qualify on the other side

- **Demographic-only.** Age; sex; race or ethnicity; household income; parental education; household composition; marital status; immigration status; urbanicity; study site; **sexual orientation; sexual minority status; gender identity; transgender or gender-questioning status**. Identity characteristics that describe who a participant is (rather than how they are doing developmentally) are demographic for this rule, regardless of how the source paper labels them.
- **Contextual-only.** Neighborhood quality; school district; region; season; COVID-19 timing; year of survey; **religious participation; pet ownership** (and analogous family- or household-level lifestyle variables).

If the only analyses pair the smartphone or social media variable with demographic-only or contextual-only variables on the other side, FT-IC2 is not met regardless of whether the smartphone or social media variable itself satisfies Step 1 or Step 2.

A useful test: if the analysis is best described as "*do members of group X use [SM modality] more than members of group Y?*", that is a demographic correlate of screen use and does not satisfy the individual-trait other-side requirement, even when the grouping variable is an identity construct (e.g., sexual minority vs. heterosexual; transgender vs. cisgender).

### Clarifications

1. **Problematic-use scales are smartphone or social media variables, not individual-trait outcomes.** The SMAQ, MPIQ, VGAQ, PSMU, Bergen Social Media/Facebook Addiction Scale, and SNS-A all measure smartphone or social media use. When the only analysis is a sociodemographic predictor -> SMAQ or MPIQ as dependent variable, the other side is still demographic, and FT-IC2 is not met. The scale is the smartphone/social-media variable; it cannot also serve as the non-SM other-side variable.

2. **Generic gaming does not qualify** unless the gaming variable is explicitly mobile or phone-based, or the paper separately measures a qualifying phone or social media variable with its own coefficient. This includes the VGAQ (Bergen Video Game Addiction Questionnaire), IGDS9-SF, generic "video gaming hours," "gaming duration," problematic-gaming scales without explicit mobile or phone modality, console gaming, PC gaming, "video games" with platform unspecified, and "gaming addiction." If the paper measures only gaming and does not isolate phone-based gaming or pair it with a phone or social media variable, FT-IC2 is not met.

3. **Cyberbullying alone does not qualify.** Cyberbullying is itself a phone- or social-media-mediated phenomenon and therefore does not satisfy the individual-trait other-side requirement when no external trait outcome is analyzed. Cyberbullying counts only when paired with a separately measured phone or social media variable that has its own coefficient *and* an external individual-trait outcome.

4. **Mature-rated or R-rated content alone does not qualify.** Content rating is not a modality. "Mature-rated video games" or "R-rated movies" qualify only if the paper also reports a separate phone or social media variable with its own coefficient.

5. **Multi-device aggregated time fails Step 2.** A variable defined as "minutes per week on computer, tablet, cellphone, or other electronic device" reported as a single number bundles the smartphone with non-phone devices and does not qualify unless a per-device breakout (cellphone alone) appears somewhere. Activity-specific items that aggregate across devices but where the activity is itself phone- or social-media-defined (e.g., "texting on cell phone, tablet, or computer") are treated as qualifying because the activity, rather than the device, defines the modality.

6. **Pure psychometric or validation papers do not qualify.** Factor structure of the SMAQ, reliability of the MPIQ, EARS-versus-self-report concordance, or similar scale-development analyses with no external outcome do not satisfy FT-IC2 (and frequently fail FT-IC5 as well).

7. **Smartphone or social media variables used only as covariates, mediators, or moderators do not qualify.** The variable must appear as an independent or dependent variable in at least one analysis where it has its own reported coefficient or estimate.

-> Exclusion code **FT-EC2**.

---

## FT-IC3 and FT-IC4 -- Inferential analysis with numeric result

These two criteria are evaluated together. The paper must conduct an inferential analysis involving the qualifying smartphone or social media variable and an individual-trait-level variable, and must report at least one numeric result for that relationship.

**Met.** Any quantitative result for the smartphone/social media <-> individual-trait relationship, reported anywhere (main, supplementary, sensitivity, appendix). Eligible result types include regression coefficients (β, OR, RR, HR, IRR, aOR, aRR, PR, aPR); penalized-regression coefficients (Lasso, Ridge, Elastic Net); path coefficients (direct, indirect, total) from structural equation modeling, cross-lagged panel models, or mediation analyses; Pearson, Spearman, or partial correlations; mean differences with associated test statistics (t, F, p); η^2, R^2, adjusted prevalence ratios; SHAP values; permutation feature importances; random-forest, gradient-boosting, or XGBoost variable importances; model-level metrics (AUC, R^2) involving the smartphone or social media variable; Bayesian posterior estimates; network edge weights; and target-trial-emulation contrasts.

**Not met.** The paper claims a smartphone/social media -> outcome association narratively but reports no numeric quantification anywhere. (This is rare in real empirical papers.)

-> Exclusion code **FT-EC4**.

---

## FT-EC7 -- Longitudinal smartphone or social media-as-dependent-variable-only

FT-EC7 is an exclusion criterion that targets a specific design: longitudinal studies in which the smartphone or social media variable functions only as the outcome of interest, with no analysis treating it as a predictor. These are studies of *who develops* particular phone or social media use patterns, rather than studies of how phone or social media use is associated with individual-trait outcomes. Such studies fall outside the review's scope.

FT-EC7 applies when **all three** of the following conditions are simultaneously true:

1. The design is **longitudinal** (a baseline measurement predicts a later wave).
2. Smartphone or social media is the **dependent variable** in every analysis involving smartphone or social media in the paper.
3. There is **no analysis anywhere in the paper** in which smartphone or social media is the independent variable, including cross-lagged or bidirectional models in which it appears as both independent and dependent within the same model.

### Cross-sectional carve-out

If the paper contains **any** cross-sectional analysis with smartphone or social media as the dependent variable -- with the same predictors as in the longitudinal analyses, or with any other predictors -- FT-EC7 does not apply. This holds regardless of how many longitudinal smartphone/social-media-as-dependent-variable analyses are present. Evidence of any cross-sectional smartphone/social-media-as-DV analysis anywhere in the paper (main, supplementary, or sensitivity) disqualifies FT-EC7.

### When FT-EC7 does not apply

- The design is cross-sectional, or the paper has any cross-sectional smartphone/social-media-as-DV analysis (cross-sectional carve-out, above).
- Smartphone or social media is the independent variable in any analysis anywhere in the paper, on any topic.
- Bidirectional or cross-lagged design (smartphone or social media is both IV and DV in the same model).

The type of predictor on the other side (demographic, individual-trait, family, lifestyle, ACEs, parental psychopathology) does not affect the FT-EC7 evaluation. Predictor-type judgments belong at FT-IC2 (the individual-trait other-side requirement), not at FT-EC7.

-> Exclusion code **FT-EC7**.

---

## Exclusion codes

Exclusion codes are assigned in cascade order. The first applicable code is the one recorded for an excluded paper.

| Code | Label | Trigger |
|---|---|---|
| FT-EC1 | Not U.S. ABCD | FT-IC1 not met. |
| FT-EC3 | Non-empirical | FT-IC5 not met (review, editorial, commentary, protocol, resource paper, conference abstract, etc.). |
| FT-EC6 | Duplicate | FT-IC6 not met (preprint of an already-included paper, conference abstract of an already-included full paper, or identical re-analysis). |
| FT-EC2 | No qualifying smartphone or social media exposure, or no individual-trait variable on the other side | FT-IC2 not met. |
| FT-EC4 | No numeric result for smartphone or social media <-> outcome | FT-IC3 or FT-IC4 not met. |
| FT-EC7 | Longitudinal smartphone or social media-as-dependent-variable-only | All three FT-EC7 conditions met simultaneously, with no cross-sectional carve-out applicable. |

---

## Coding output

The screening decisions for each Stage-1 include are reported in `2L-scoring.csv`. Each row represents one paper and contains: paper identifier, title, year, DOI, the coder's decision (INCLUDE or EXCLUDE), the exclusion code where applicable, and the substantive reason supporting the decision.
