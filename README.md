# ABCD Study Screen Media Systematic Review

A systematic review of publications using Adolescent Brain Cognitive Development (ABCD) Study data to examine associations between screen media use (smartphone, social media, internet, texting, digital media) and youth outcomes.

## Purpose

This review audits **how effect sizes are interpreted** in ABCD screen media research. Specifically:

- Are small effect sizes (beta < 0.10, OR < 1.20) acknowledged or obscured by significance-first language?
- Do papers issue clinical/policy recommendations despite trivially small associations?
- What rhetorical patterns (population-level override, modifiable-factor framing, per-unit framing) are used to bridge the gap between small effects and strong conclusions?

## Repo Structure

```
search/                 # Phase 1: Database searches
  01_pubmed_search.py   # PubMed E-utilities API search
  02_openalex_search.py # OpenAlex API search
  search_strings.md     # Exact Boolean queries
  results/              # Raw search exports with logs

screening/              # Phase 2: Title/abstract screening
  03_deduplicate.py     # Merge + dedup across sources
  04_screen_abstracts.py
  screening_criteria.md # Inclusion/exclusion criteria
  results/
    deduplicated.csv    # All unique papers
    screening_decisions.csv  # Multi-coder screening database

coding/                 # Phase 3: Full-text coding
  05_code_paper.py
  coding_rubric.md      # Operationalized decision rules
  papers/               # One JSON per coded paper

data/
  abstracts.csv         # All abstracts in one place
  pdfs/                 # Full-text PDFs (gitignored)

output/                 # Final deliverables
```

## Search Strategy

- **Databases:** PubMed/MEDLINE, OpenAlex
- **Supplementary:** abcdstudy.org hand-searched publication list
- **Search date:** 2026-04-06
- **Results:** 171 (PubMed) + 450 (OpenAlex) + 101 (ABCD website) = 545 unique after deduplication

See [METHODS.md](METHODS.md) for full search documentation and [search/search_strings.md](search/search_strings.md) for exact queries.

## Screening

All screening decisions are in `screening/results/screening_decisions.csv`. Each row contains the full abstract, the coder's decision, exclusion code, and notes. Multiple coders add separate rows for the same paper.

See [screening/screening_criteria.md](screening/screening_criteria.md) for inclusion/exclusion criteria.

## Coding

Full-text coding uses an operationalized rubric with forced-choice fields. Every effect size is extracted verbatim. Interpretation and rhetorical patterns are coded independently.

See [coding/coding_rubric.md](coding/coding_rubric.md) for the complete rubric.

## Reproducing the Search

```bash
# PubMed search (requires internet, no API key)
python3 search/01_pubmed_search.py

# OpenAlex search (requires internet, no API key)
python3 search/02_openalex_search.py

# Deduplicate
python3 screening/03_deduplicate.py
```

## Multi-Coder Workflow

1. Open `screening/results/screening_decisions.csv`
2. Filter to rows where `coder = AI`
3. Add your own row for any paper you want to screen independently
4. Use the same `decision` and `exclusion_code` fields
5. Disagreements resolved by comparing notes

## License

This is an academic research project. Data and methods are shared for transparency and reproducibility.
