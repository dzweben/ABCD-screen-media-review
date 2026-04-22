# Full-Text Coding Rubric

Every field has explicit decision rules so two independent coders reading the same paper arrive at the same codes.

---

## 3A: Bibliographic

| Field | Rule |
|-------|------|
| `candidate_id` | From screening database |
| `citation` | Full APA 7th edition citation |
| `doi` | DOI |
| `journal` | Journal name |
| `year` | Publication year |
| `first_author` | First listed author (Last, Initials) |
| `senior_author` | Last listed author (Last, Initials) |

---

## 3B: Sample

| Field | Rule |
|-------|------|
| `N` | **Analytic sample N** used in the primary model. Not the full ABCD N or recruited N. The N that generated the reported effect sizes. If multiple models with different Ns, use the primary outcome model. |
| `ABCD_release_version` | Extract verbatim from methods (e.g., "4.0", "5.1") |
| `timepoints_used` | Which timepoints: baseline, 1yr, 2yr, 3yr, 4yr |

---

## 3C: Exposure

| Field | Rule |
|-------|------|
| `exposure_measure` | Exactly how screen time was measured and entered into the model |
| `exposure_instrument` | Instrument name (STQ, SMAQ, EARS, parent report, etc.) |
| `modalities_included` | List: social media, texting, video chat, TV, video games, total screen time, etc. |
| `how_operationalized` | Continuous hours/day, categorical, scale score, binary cutoff |
| `reporter` | Self-report / parent-report / device-based |

---

## 3D: Outcome

| Field | Rule |
|-------|------|
| `primary_outcome` | Primary outcome variable name |
| `outcome_domain` | Forced choice: mental_health / cognition / brain / sleep / physical_health / social / academic / substance_use / other |
| `measure_used` | Exact instrument name and subscale |
| `outcome_type` | Binary or continuous |
| `base_rate_if_binary` | If binary: base rate reported in paper. If not reported, write "NOT REPORTED" |

---

## 3E: Design & Analysis

| Field | Rule |
|-------|------|
| `design` | Forced choice: cross-sectional / prospective / longitudinal / mediation / moderation / network / machine_learning |
| `model_type` | Forced choice: linear_regression / logistic_regression / mixed_effects / path_model / SEM / survival / CLPM / RI-CLPM / other |
| `model_type_detail` | More specific (e.g., "multilevel negative binomial with random intercepts for site") |
| `covariates_listed` | Comma-separated list of ALL covariates in the primary model |
| `SES_in_model` | **CRITICAL.** Was income, education, SES, or poverty included as a covariate IN THE SPECIFIC MODEL that produced the screen time effect sizes? `yes` / `no` / `unclear`. Do NOT code `yes` just because SES appears somewhere in the paper. |
| `multiple_comparisons_correction` | None / Bonferroni / FDR / permutation / other |

---

## 3F: Effect Sizes

**One row per reported effect size.** Extract EVERY effect size for the screen-time-to-outcome association. No filtering.

| Field | Rule |
|-------|------|
| `effect_id` | Sequential within paper (1, 2, 3...) |
| `predictor` | What exposure variable |
| `outcome` | What outcome variable |
| `effect_type` | r / beta / B / OR / HR / RR / d / eta2 / R2 / SHAP / other |
| `standardized` | yes / no / unclear. If unstandardized (B), note the outcome scale. |
| `value` | Numeric value |
| `CI_95` | "lower, upper" or blank if not reported |
| `p_value` | Exact or threshold (e.g., "<.001") |
| `outcome_scale_note` | If unstandardized: what units? (e.g., "CBCL T-score points per hour/day") |
| `base_rate_for_OR` | If OR: what is the base rate of the outcome? |
| `variance_explained` | R-squared or partial R-squared if reported |
| `in_supplementary` | yes / no — if effect sizes only appear in supplement, flag explicitly |
| `verbatim_quote` | Exact sentence from paper reporting this effect |
| `context` | primary / sensitivity / subgroup / supplementary |
| `below_threshold` | yes / no. Thresholds: standardized beta < 0.10, OR between 0.80-1.20, r < 0.10, d < 0.20, R-squared < 0.01 |

---

## 3G: Interpretation

| Field | Rule |
|-------|------|
| `significance_first_or_ES_first` | **significance-first**: Abstract/discussion leads with "significant" / "significantly associated" as primary characterization. **ES-first**: Leads with effect magnitude. **balanced**: Reports both without privileging either. |
| `p_values_in_abstract` | yes / no |
| `CIs_reported` | yes / no — for the primary effect |
| `large_N_acknowledged` | **yes**: Paper explicitly states large sample provides power to detect trivially small effects AND connects this to interpretation. **perfunctory**: Mentions large sample in limitations but doesn't connect to ES interpretation. **no**: Not mentioned. |
| `large_N_verbatim` | Exact quote |
| `small_ES_acknowledged` | **yes**: Paper notes small effects and constrains conclusions accordingly. **acknowledged-then-overridden**: Notes small ES in limitations but issues recommendations anyway. **no**: Effect magnitude not discussed. **not_applicable**: Effects genuinely large (OR > 1.50, beta > 0.20, d > 0.50). |
| `small_ES_verbatim` | Exact quote |
| `recommendations_issued` | yes / no — Does the paper issue clinical/policy recommendations? |
| `recommendation_target` | parents / clinicians / policymakers / schools / researchers / none |
| `verbatim_recommendation` | Exact 1-2 sentence recommendation |

---

## 3H: Rhetorical Patterns

Each is coded independently as yes/no. A paper can have multiple.

| Field | Rule |
|-------|------|
| `rhetorical_pattern` | Summary label: significance-primary / population-override / modifiable-factor / acknowledge-then-override / per-unit-OR / none / combination |
| `population_level_override` | Does the paper argue small effects matter due to population-level multiplication? yes/no |
| `population_override_verbatim` | Exact quote |
| `modifiable_factor_framing` | Does the paper use "modifiable" as justification for recommendations? yes/no |
| `modifiable_factor_verbatim` | Exact quote |
| `per_unit_framing` | Does the paper report per-unit effects (per hour/day) implying accumulation? yes/no |
| `per_unit_verbatim` | Exact quote |
| `discussion_characterization` | Free text, 1-3 sentences. AI summary of how the discussion interprets findings. NOT verbatim. |
| `list_1_qualifier` | yes/no — Statistical significance is the primary interpretive lens despite very small effects |
| `list_2_qualifier` | yes/no — Acknowledges small effects but overrides with recommendations |
| `coder_confidence` | high / medium / low. Low = automatic human review. |

---

## 3I: Flags

| Field | Rule |
|-------|------|
| `exclusion_flag` | If paper should be excluded at full-text stage, state reason |
| `ambiguity_notes` | What was unclear and why |
| `screen_time_is_outcome` | yes/no — Flag if screen time is the outcome (not exposure) |
| `not_abcd_data` | yes/no — Flag if discovered at full-text that data is not ABCD |
