# Search Phase

## Scripts

| Script | Database | Method |
|--------|----------|--------|
| `01_pubmed_search.py` | PubMed/MEDLINE | NCBI E-utilities API with Boolean query |
| `02_openalex_search.py` | OpenAlex | REST API with title/abstract filter + keyword post-filter |

## Running

```bash
python3 search/01_pubmed_search.py    # Outputs search/results/pubmed_results.csv
python3 search/02_openalex_search.py  # Outputs search/results/openalex_results.csv
```

No API keys required. Both scripts log the exact query, date, and result count.

## Results

All raw search results are in `results/`. Each CSV contains: DOI, title, authors, year, journal, abstract, and database-specific IDs.

Search logs (JSON) record the exact query strings, timestamps, and hit counts for PRISMA documentation.
