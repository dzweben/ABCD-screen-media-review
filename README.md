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

## PRISMA flow (current — v7 mechanical IC2 + cross-sectional EC7 carve-out)

| Stage | Records |
|---|---:|
| **Identification**: Records from PubMed, OpenAlex, Google Scholar, ABCD website | 1,165 |
| **Deduplication**: Unique records | 620 |
| **Stage 1 (title/abstract)**: Advanced to full-text | 171 |
| **Stage 1 excluded (by code)**: EC1–EC5 | 449 |
| **Stage 2 (full-text)**: Included in synthesis | **69** |
| **Stage 2 excluded with reason**: FT-EC1–FT-EC7 | **87** |
| &nbsp;&nbsp;&nbsp;FT-EC1 (not U.S. ABCD) | 5 |
| &nbsp;&nbsp;&nbsp;FT-EC2 (no qualifying smartphone/SM ↔ individual-trait analysis) | 71 |
| &nbsp;&nbsp;&nbsp;FT-EC3 (non-empirical: review, commentary, protocol, resource paper) | 5 |
| &nbsp;&nbsp;&nbsp;FT-EC7 (longitudinal SM-as-DV-only with no SM-as-IV analysis) | 6 |
| **Stage 2 UNSURE** (C1≠C2 substantive disagreement; awaiting human review) | 1 |
| **Stage 2 NA_FOR_NOW** (no PDF; pre-tagged, never sent to coders) | 15 |

---

## Stage 2 screening pipeline (2L) — v6

Each of the 171 Stage-1 includes is screened atomically against six criteria (FT-IC1, FT-IC5, FT-IC6, FT-IC2, FT-IC3, FT-IC4) and a directionality gate (FT-EC7), in cascade order:

1. **C1_AI** — independent AI coder, full PDF review, per-criterion MET/NOT_MET/UNKNOWN/DEFERRED with evidence
2. **C2_AI** — independent AI coder, blinded to C1
3. **Algorithmic aggregation** — hierarchical exclusion codes; no resolver, no subjective judgment

The v6 criteria removed the resolver entirely. Tighter criteria (conceptual smartphone/SM exposure, individual-trait outcome requirement, broader IC4, simplified FT-EC7, cascade-DEFERRED convention) produce convergent C1/C2 decisions by construction. Residual disagreements (21 papers) route to UNSURE for human review rather than algorithmic adjudication.

**C1 vs C2 agreement, by version:**

| Version | Coder model | Pooled κ | Paper-level full agreement | Substantive disagreements |
|---|---|---:|---:|---:|
| v4 | Haiku | 0.51 (moderate) | — | — |
| v5 (B1–B20 binding rules + resolver) | Haiku | 0.77 (substantial) | 69.6% (119/171) | 52 papers |
| v6 (conceptual + cascade-DEFERRED, no resolver) | Haiku | 0.90 (almost perfect) | 83.6% (143/171) | 21 papers |
| v7 (mechanical 2-step IC2, no-PDF pre-tagged) | Haiku | 0.87 | 80.1% (125/156) | 31 papers |
| **v7 (same criteria, Sonnet coders)** | **Sonnet** | **0.996** | **99.36% (155/156)** | **1 paper** |

Per-criterion v7-Sonnet agreement (n=156 PDF-having papers):
- FT-IC1, IC2, IC3, IC4, IC6, EC7: **all κ=1.00 (100%)**
- FT-IC5 κ=0.91 (99.3%, single 1-paper disagreement)

The single biggest IRR improvement came from switching the coder model from Haiku to Sonnet — the v7 criteria were sound; Haiku's reading comprehension was the bottleneck. Sonnet reads PDFs reliably enough that two independent passes converge on identical answers for every paper except one borderline empirical-vs-perspective call.

v7-Sonnet final flow: 69 INCLUDE / 87 EXCLUDE / 1 UNSURE / 15 NA_FOR_NOW.

See `02-L2/2L-criteria.md` for full v6 criteria.

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
