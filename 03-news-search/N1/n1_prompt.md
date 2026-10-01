# N1 Linkage Coder — Prompt

You are an independent screener determining whether each candidate news article in this batch covers one of the 69 ABCD-included papers.

## Inputs

You will be given:
1. `candidate_papers.json` — the 69 INCLUDE papers with metadata (paper_id, doi, title, first_author, all_authors_last, affiliation, venue, year, topic, and the substantive finding from L2 screening).
2. `articles_batch.json` — a batch of news articles to screen, each with: article_id, title, outlet, URL, summary (Google search snippet), published_date, and provisional_paper_ids (paper_ids tentatively mapped from the search query that returned the article — these are *priors*, not ground truth).

## Linkage criteria (per `N1-linkage-criteria.md`)

An article qualifies as coverage of paper X if **any one** of:

- **L1 — Direct identifier link.** The article URL or text contains a hyperlink to paper X's DOI / journal article URL / PMID.
- **L2 — Author + journal naming.** The article body contains both the lead author's surname AND the journal name (e.g., "Nagata" + "BMC Public Health").
- **L3 — Distinctive paraphrase.** The article paraphrases a finding that uniquely maps to paper X (any two of: sample size, outcome, effect direction, exposure modality, effect magnitude, subgroup specifications).
- **L4 — Institution + topic + ABCD configuration.** The article names paper X's lead institution + the study topic + the ABCD Study, in a configuration uniquely consistent with paper X.

If multiple papers could match, the article is **multi-mapped**. Tag all matching paper_ids — multi-mapping is a feature, not an error.

If **none** of L1-L4 are met, the article is excluded at N1.

## Important interpretive guidance

- **Treat provisional_paper_ids as a hint, not an answer.** The query that returned the article had a paper_id attached because of keyword overlap, but the article may actually be about a different INCLUDE paper, or about a non-INCLUDE topic, or a generic ABCD overview. Re-evaluate from scratch using L1-L4.
- **Articles about ABCD generally** (e.g., "ABCD Study turns 10," overview pieces) without referencing a specific paper from `candidate_papers.json` should be **excluded** with reason "general ABCD coverage, no specific paper from corpus."
- **Articles about ABCD topics outside the corpus** (e.g., substance use, brain imaging unrelated to phone/SM, racial discrimination findings) should be excluded with reason "ABCD coverage of out-of-corpus topic."
- **Articles about smartphone/SM research from a different cohort** (e.g., NHANES, NIMH, MTF, NLSY) may have surfaced in the search via keyword overlap. Exclude with reason "non-ABCD cohort."
- **Press releases, EurekAlert items, journal-page summaries** still need to meet L1-L4. Many will trivially satisfy L2 (author + journal named), so those typically pass.
- **Aggregator articles citing other articles**: if the aggregator paraphrases a paper's finding clearly enough to satisfy L3 or L4, count as coverage even if it doesn't link the DOI.

## Output

Output a JSON array with one object per article in this batch. Schema per article:

```json
{
  "article_id": "A0001",
  "matched_paper_ids": ["3", "144"],
  "linkage_test": "L3",
  "confidence": 0.9,
  "excluded": false,
  "exclusion_reason": "",
  "evidence": "Article paraphrases SM use trajectories → cognitive performance with sample n=6,554 ages 9-13 — uniquely maps to paper 3 (Xiao 2025 JAMA). Also discusses paper 144 (Nagata 2026 SM trajectories) for related social media trajectory finding."
}
```

Notes on each field:
- `matched_paper_ids`: array of paper_ids (from candidate_papers.json) the article covers; `[]` if excluded.
- `linkage_test`: `"L1"`, `"L2"`, `"L3"`, `"L4"`, or `"multi"` (when more than one criterion is satisfied across mapped papers).
- `confidence`: float 0-1. ≥0.9 = certain; 0.7-0.89 = likely; <0.7 = uncertain (flagged for human review).
- `excluded`: true if no L1-L4 satisfied.
- `exclusion_reason`: short string when excluded ("general ABCD coverage" / "out-of-corpus topic" / "non-ABCD cohort" / "duplicate/syndicated of A####" / etc.).
- `evidence`: short specific quote or paraphrase from article + which paper(s) it maps to and why.

Output ONLY the JSON array, no surrounding prose. Escape internal `"` as `\"`.
