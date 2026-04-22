# 1L Criteria — Title/Abstract Screening (PRISMA 2020)

**Stage:** Level 1 — title and abstract screening.
**Purpose:** Identify any publication potentially analyzing ABCD Study data with a screen/digital media variable. The 1L stage is deliberately broad to minimize false-negative exclusions; narrowing to smartphone/social media happens at 2L.

---

## 1. Research Question

Among publications that analyze data from the U.S. Adolescent Brain Cognitive Development (ABCD) Study, what associations have been reported between youth screen/digital media exposure and youth psychosocial, health, cognitive, behavioral, neural, social, or sociodemographic variables?

---

## 2. Eligibility Criteria — 1L

A publication passes 1L screening if ALL four inclusion criteria below are met (or appear likely to be met based on title/abstract) AND no exclusion criterion applies.

### 2.1 Inclusion Criteria (IC)

| Code | Criterion | Operationalization (title/abstract) |
|---|---|---|
| **IC1** | Uses data from the U.S. ABCD Study | Title or abstract references "ABCD Study," "Adolescent Brain Cognitive Development," the NDA, or NIMH-ABCD. Ambiguous cases pass to 2L. |
| **IC2** | Includes a screen or digital media variable | Any measured variable capturing screen-based exposure: screen time, social media, smartphone/mobile phone, internet, texting, video gaming, television, video streaming, passive sensing (EARS), problematic/compulsive use scales, cyberbullying paired with media measure, online dating apps, mature-rated media. At 1L we are permissive — narrowing to smartphone/SM happens at 2L. |
| **IC3** | Reports original empirical findings | Abstract indicates quantitative analysis of ABCD data (primary or secondary). |
| **IC4** | Peer-reviewed journal article | Published in a peer-reviewed outlet. Preprints are evaluated case-by-case; if the peer-reviewed version is already indexed, the preprint is FT-EC6 at 2L. |

### 2.2 Exclusion Criteria (EC)

Assigned in order; first applicable code is recorded.

| Code | Label | Operationalization |
|---|---|---|
| **EC1** | Does not use ABCD Study data | Uses Amsterdam Born Children and their Development (Dutch ABCD), NHANES, MTF, MCS, Generation R, or another dataset. ABCD referenced only in intro/discussion. |
| **EC2** | No screen/digital media variable | Title/abstract describe only non-media constructs (e.g., sleep, genetics, brain structure) with no reference to screen, phone, social media, gaming, TV, internet, texting, cyberbullying. |
| **EC3** | No original empirical analysis | Reviews, editorials, commentaries, letters, study protocols, meta-analyses without new ABCD analysis, book chapters, news summaries. |
| **EC4** | Conference abstract only | Abstract from conference proceedings (e.g., SLEEP, AHA, ACSM, SAHM) without a full-text peer-reviewed publication. If a published version exists, the full paper is retained; the abstract is EC5. |
| **EC5** | Duplicate | Preprint (bioRxiv, medRxiv, PsyArXiv, SSRN, OSF) whose peer-reviewed version is already included. Supplementary data deposits (Figshare, Zenodo). Republished analyses. |

---

## 3. Coders and Decision Rule

| Coder | Role |
|---|---|
| **Coder 1** | Lead author, manual title/abstract review. |
| **Coder 2** | Second coder, independent review blinded to Coder 1. |

Each paper receives `coder1_decision`, `coder_2_decision` ∈ {INCLUDE, EXCLUDE, UNSURE}. Disagreements are discussed to consensus. Outcome at 1L: papers coded INCLUDE (or resolved to INCLUDE) advance to 2L full-text screening.

---

## 4. Reported in `1L-scoring.csv`

One row per deduplicated paper (n = 620). Columns include: `paper_id, doi, title, first_author, year, journal, abstract, sources, Coder1_Reason, coder1_decision, coder_2_decision, coder_2_reason, has_pdf`, plus a derived `L1_decision` and `L1_exclusion_code` reflecting the consensus outcome. Papers with `L1_decision = INCLUDE` (n = 171) enter 2L and are also recorded in `2L-scoring.csv`.

---

## 5. Selection Summary (PRISMA item 16, stage 1)

- Records identified after deduplication: 620
- Records excluded at 1L: 449
  - EC1 (not ABCD): counts from `1L-scoring.csv`
  - EC2 (no media variable): counts from `1L-scoring.csv`
  - EC3 (non-empirical): counts from `1L-scoring.csv`
  - EC4 (conference abstract): counts from `1L-scoring.csv`
  - EC5 (duplicate): counts from `1L-scoring.csv`
- Records advanced to 2L full-text: 171
