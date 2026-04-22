# Search Results and Yield Summary (PRISMA item 8, 16)

**Date of search execution:** 2026-04-06
**Search terms and platform-specific queries:** `search-terms-platforms.md`
**Scripts used (reproducible):** `01_pubmed_search.py`, `01_scrape_publications.py`, `02_openalex_search.py`, `03_google_scholar_search.py`, `03_fetch_abstracts.py`

---

## Per-platform yield

| Source | Platform | Query method | Records retrieved | Result file |
|---|---|---|---:|---|
| PubMed / MEDLINE | NCBI E-utilities API | Boolean query (see `search-terms-platforms.md` §PubMed) | 171 | `pubmed_results.csv` + `pubmed_search_log.json` |
| OpenAlex | REST API (title + abstract search on "ABCD" terms, then post-filter for screen/media keywords) | Two-step API + keyword filter | 450 | `openalex_results.csv` + `openalex_search_log.json` |
| Google Scholar | SerpAPI | Same Boolean query adapted | 443 | `google_scholar_results.csv` + `google_scholar_search_log.json` |
| ABCD Study website (hand search) | JSON-LD scrape of abcdstudy.org/publications → keyword filter | Python scrape + filter | 101 | included in scraped log (see `01_scrape_publications.py`) |
| **Total before deduplication** | | | **1,165** | |

## Deduplication

Deduplication logic and script: see `deduplication.md` and `03_deduplicate.py`.

- Records merged across sources: 1,165
- Duplicates removed: 545
- **Unique records advancing to 1L screening: 620** (see `../01-L1/1L-scoring.csv`)

## Reproducibility

Rerun the full pipeline with:

```bash
cd 00-search/
python 01_pubmed_search.py                   # → pubmed_results.csv
python 01_scrape_publications.py              # → ABCD website candidates
python 02_openalex_search.py                  # → openalex_results.csv
python 03_google_scholar_search.py $SERPAPI_KEY   # → google_scholar_results.csv
python 03_fetch_abstracts.py                  # enriches missing abstracts via PubMed PMIDs
python 03_deduplicate.py                      # → deduplicated.csv (n=620)
```

All scripts log exact API endpoints, timestamps, and record counts to corresponding `*_search_log.json` files.

Historical PRISMA counts at the time of search execution are preserved in `prisma_counts.json`.
