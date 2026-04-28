# ABCD Smartphone & Social Media Systematic Review

A PRISMA 2020 systematic review of publications using U.S. Adolescent Brain Cognitive Development (ABCD) Study data that examine associations involving youth **smartphone** or **social media** use.

---

## Repository structure

```
00-search/         Phase 0 — database searches, deduplication
  search-terms-platforms.md      Exact Boolean queries per database
  search-results.md              Per-platform yield summary
  deduplication.md               Dedup logic and counts
  01_pubmed_search.py            Reproducible search scripts
  01_scrape_publications.py
  02_openalex_search.py
  03_google_scholar_search.py
  03_fetch_abstracts.py
  03_deduplicate.py
  pubmed_results.csv
  openalex_results.csv
  google_scholar_results.csv
  *_search_log.json              API call logs
  deduplicated.csv               620 unique records after dedup
  prisma_counts.json             Historical PRISMA flow counts

01-L1/             Phase 1 — Title/abstract screening
  1L-criteria.md                 Stage 1 eligibility criteria
  1L-scoring.csv                 620 papers × (metadata + Coder1 + Coder2 + L1_decision)

02-L2/             Phase 2 — Full-text eligibility
  2L-criteria.md                 Stage 2 criteria (smartphone/SM scope, FT-EC7 directionality)
  2L-scoring.csv                 171 Stage-1 includes × per-criterion C1/C2/Resolver/FINAL
  2L-INCLUDE.csv                 Slim list: 94 included papers
  2L-EXCLUDE.csv                 Slim list: 61 excluded papers with codes
  2L-UNSURE.csv                  Slim list: 16 papers pending retrieval/clarification

claude-search-subrepo/          AI processing artifacts (not part of PRISMA output)
  v4_screening/                  Per-coder JSON outputs (C1, C2, resolver), batch inputs
  ai_validation/                 Earlier AI-only screening passes (pre-PRISMA)
  ...                            (old dashboards, logs, intermediate CSVs)

METHODS.md                      Overall methods overview
README.md                       This file
```

---

## PRISMA flow (current — v5 tightened criteria)

| Stage | Records |
|---|---:|
| **Identification**: Records from PubMed, OpenAlex, Google Scholar, ABCD website | 1,165 |
| **Deduplication**: Unique records | 620 |
| **Stage 1 (title/abstract)**: Advanced to full-text | 171 |
| **Stage 1 excluded (by code)**: EC1–EC5 | 449 |
| **Stage 2 (full-text)**: Included in synthesis | **107** |
| **Stage 2 excluded with reason**: FT-EC1–FT-EC7 | **62** |
| &nbsp;&nbsp;&nbsp;FT-EC1 (not U.S. ABCD) | 6 |
| &nbsp;&nbsp;&nbsp;FT-EC2 (no smartphone/SM variable) | 48 |
| &nbsp;&nbsp;&nbsp;FT-EC4 (no smartphone/SM ↔ non-SM test or no extractable estimate) | 5 |
| &nbsp;&nbsp;&nbsp;FT-EC7 (longitudinal demographic → SM epidemiology) | 3 |
| **Stage 2 NA_FOR_NOW** (no PDF; criteria unverifiable) | 2 |

---

## Stage 2 screening pipeline (2L)

Each of the 171 Stage-1 includes is screened atomically against six criteria (FT-IC1 through FT-IC6) and a directionality gate (FT-EC7):

1. **C1_AI** — independent AI coder, full PDF review, per-criterion MET/NOT_MET/UNKNOWN with evidence
2. **C2_AI** — independent AI coder, blinded to C1
3. **Resolver** — independent AI pass only on criteria where C1 ≠ C2
4. **Algorithmic aggregation** — hierarchical exclusion codes; no subjective judgment

**C1 vs C2 agreement (v5, pre-resolver):**
- Pooled criterion-level: 88.4% agreement, Cohen's κ = **0.77** (substantial)
- Paper-level full agreement: 69.6% (119/171)
- Resolver adjudicated 52 papers with at least one criterion-level disagreement

The v5 criteria (with 20 binding borderline rules B1–B20) substantially improved IRR over v4 (κ=0.51 → 0.77).

See `02-L2/2L-criteria.md` for full criteria and edge-case rules (E1–E18).

---

## Reproducing the search

```bash
cd 00-search/
python 01_pubmed_search.py                   # → pubmed_results.csv
python 01_scrape_publications.py              # → ABCD website candidates
python 02_openalex_search.py                  # → openalex_results.csv
python 03_google_scholar_search.py $SERPAPI_KEY   # → google_scholar_results.csv
python 03_fetch_abstracts.py                  # fill in missing abstracts
python 03_deduplicate.py                      # → deduplicated.csv (n=620)
```

---

## Notes

- **v4 criteria** narrow Stage 2 to smartphone/social-media-specific exposures (superseding earlier v1–v3 passes, preserved only in git history).
- **FT-EC7** excludes longitudinal demographic-only prediction of future smartphone/SM use (epidemiology-of-adoption is out of scope). Cross-sectional demographic → SM associations remain eligible.
- **Apps = smartphone** (any app use qualifies as a smartphone exposure).
- **Cyberbullying alone** does not qualify; requires a separately measured smartphone or SM variable.
- Generic "screen time" composites without modality breakdowns are excluded.
