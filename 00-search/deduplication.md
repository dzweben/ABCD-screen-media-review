# Deduplication (PRISMA item 8)

**Purpose:** Merge records retrieved from PubMed, OpenAlex, Google Scholar, and the ABCD Study website hand search into a single de-duplicated dataset for 1L screening.

**Script:** `03_deduplicate.py` (reproducible).

---

## Input

| Source file | Records |
|---|---:|
| `pubmed_results.csv` | 171 |
| `openalex_results.csv` | 450 |
| `google_scholar_results.csv` | 443 |
| ABCD website hand-search candidates (via `01_scrape_publications.py`) | 101 |
| **Total across sources** | **1,165** |

## Deduplication logic

Each record is assigned a canonical key with the following priority:

1. **DOI** (normalized: lowercased, stripped of URL prefix, trailing punctuation, and version suffixes like `v1`, `v2`).
2. **PMID** if DOI is absent.
3. **Title+first-author+year fingerprint** if both DOI and PMID are absent (normalized title: lowercased, stripped of punctuation, collapsed whitespace).

Records sharing a canonical key are collapsed into a single row. When duplicates disagree on metadata, the following order of precedence is used for each field:

- **Abstract:** PubMed > OpenAlex > ABCD-website scrape > Google Scholar
- **Title / authors / year / journal:** PubMed > OpenAlex > ABCD-website > Google Scholar
- **DOI:** whichever source has a valid registered DOI

A `sources` column lists every platform that contributed a matching record (semicolon-delimited), and four boolean columns (`source_pubmed`, `source_openalex`, `source_google_scholar`, `source_abcd_website`) indicate per-source presence.

## Output

| | Records |
|---|---:|
| Before dedup | 1,165 |
| Duplicates removed | 545 |
| **Unique records advancing to 1L** | **620** |

Output file: `deduplicated.csv` (this folder). The same 620 records are carried forward to `../01-L1/1L-scoring.csv` with additional Coder 1 / Coder 2 screening columns.

## Reproducibility

```bash
cd 00-search/
python 03_deduplicate.py  # reads the four *_results.csv files, writes deduplicated.csv
```

Script logs dedup statistics to stdout and updates `prisma_counts.json` with identification and deduplication counts.
