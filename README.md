# ABCD Study Screen Media Systematic Review

A systematic review of publications using Adolescent Brain Cognitive Development (ABCD) Study data to examine associations between screen media use and youth outcomes.

## Repo Structure

```
search/                          # Phase 1: Database searches (fully reproducible, no AI)
  01_pubmed_search.py            # PubMed via NCBI E-utilities API
  02_openalex_search.py          # OpenAlex via REST API
  03_google_scholar_search.py    # Google Scholar via SerpAPI
  search_strings.md              # Exact search queries for each database
  results/                       # Raw search exports + logs

screening/                       # Phase 2: Title/abstract screening
  screening_criteria.md          # Inclusion/exclusion criteria
  results/
    screening-all.csv            # PRIMARY: Human-validated screening (620 papers)
    deduplicated.csv             # All 620 unique papers merged across sources
    prisma_counts.json           # PRISMA flow numbers
  ai_validation/                 # SUPPLEMENTARY: AI screening process
    screening_decisions.csv      # 6 AI screening passes (1298 rows)
    screening_prompt.md          # AI screening methodology
    disagreements.csv            # Inter-rater disagreements
    ...                          # Individual AI coder outputs

coding/                          # Phase 3: Full-text coding
  coding_rubric.md               # Operationalized coding rubric
  papers/                        # One JSON per coded paper

data/
  abstracts.csv                  # All 620 abstracts
  ABCD_SM_Screening_Workbook.xlsx
  pdfs/                          # Full-text PDFs (gitignored)
```

## Search Strategy

| Database | Tool | Records |
|----------|------|---------|
| PubMed/MEDLINE | NCBI E-utilities API | 171 |
| OpenAlex | REST API | 450 |
| Google Scholar | SerpAPI | 443 |
| abcdstudy.org | Web scrape | 101 |
| **Total** | | **1,165** |
| **After dedup** | | **620** |

All searches are fully reproducible Python scripts — no AI required. See [search/search_strings.md](search/search_strings.md) for exact queries.

## Screening

`screening/results/screening-all.csv` is the primary screening database:
- 620 papers, each with title, abstract, DOI, journal, year, sources
- Human coder decisions in `coder1_decision` and `coder_2_decision`
- AI consensus available as reference

See [screening/screening_criteria.md](screening/screening_criteria.md) for inclusion/exclusion criteria.

### AI Validation (Supplementary)

The `screening/ai_validation/` folder documents an independent AI screening process that ran 6 passes over the same 620 papers before human review. This serves as methodological validation — the AI decisions aligned with the human coder, documented transparently for reproducibility. See [screening/ai_validation/screening_prompt.md](screening/ai_validation/screening_prompt.md) for methodology.

## Reproducing the Search

```bash
python3 search/01_pubmed_search.py
python3 search/02_openalex_search.py
python3 search/03_google_scholar_search.py YOUR_SERPAPI_KEY
python3 screening/03_deduplicate.py
```
