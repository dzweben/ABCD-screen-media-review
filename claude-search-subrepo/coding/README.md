# Full-Text Coding Phase

## Files

| File | Purpose |
|------|---------|
| `coding_rubric.md` | Complete operationalized coding rubric |
| `papers/coding_NNN.json` | One JSON per coded paper |

## JSON Structure

Each paper is coded into sections:
- `3A_Bibliographic` — Citation, DOI, journal, year, authors
- `3B_Sample` — N, ABCD release, timepoints
- `3C_Exposure` — What was measured, how, which modalities
- `3D_Outcome` — Primary outcome, measure, base rate
- `3E_Design_Analysis` — Study design, model, covariates, SES in model
- `3F_Effect_Sizes` — Every effect size extracted verbatim
- `3G_Interpretation` — How findings are framed (significance-first vs ES-first)
- `3H_Rhetorical` — Specific rhetorical moves (population override, modifiable factor, etc.)
- `3I_Flags` — Exclusion flags, ambiguity notes

## Multi-Coder

AI-coded files have fields noting `coder = AI`. Human coders can create parallel JSON files (e.g., `coding_003_DZ.json`) for inter-rater reliability comparison.
