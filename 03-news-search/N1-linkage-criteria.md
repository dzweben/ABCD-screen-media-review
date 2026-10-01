# N1 — News Linkage Criteria

**Stage:** Level N1 — does this candidate news article cover one of the 72 included ABCD papers, and which one(s)?

**Scope:** Each candidate article retrieved by the search pipeline (Layer A through Layer C) is evaluated against these criteria. Articles that fail all four linkage tests are excluded from the substantive coding stage.

This stage is a factual-matching task, not interpretive coding. Inter-rater reliability is not required at this stage; a single AI coder with confidence threshold suffices, with human spot-check on low-confidence cases.

---

## Linkage tests (any one is sufficient)

An article qualifies as coverage of paper **X** if **any one** of the following is true:

### L1 — Direct identifier link
The article contains a hyperlink to:
- The paper's DOI (e.g., `https://doi.org/10.1186/s12889-024-20102-x`)
- The paper's journal article URL (publisher landing page or PDF)
- An article identifier that uniquely resolves to paper X (PubMed PMID, PMC ID, etc.)

### L2 — Author + journal naming
The article body contains **both**:
- The paper's lead-author surname, **and**
- The journal name (e.g., "BMC Public Health", "JAMA Pediatrics")

### L3 — Distinctive paraphrase
The article paraphrases a finding that **uniquely maps** to paper X. Sufficient if the article includes any **two** of the following with values consistent with paper X:
- Sample size (n)
- Outcome variable
- Effect direction (positive/negative association, dose-response pattern)
- Specific exposure modality (e.g., "texting," "video chatting")
- Effect magnitude (β, OR, RR, % change)
- Subgroup specifications (e.g., "in females only")

The paraphrase must be specific enough that it could not equally describe another paper in the corpus.

### L4 — Institution + topic + ABCD configuration
The article names the paper's lead-author institution (or affiliated institution) **and** the study topic **and** identifies the ABCD Study by name, in a configuration uniquely consistent with paper X (e.g., "researchers at UC San Francisco analyzed data from the ABCD Study to examine social media use and depression in adolescents" — uniquely matches the Nagata depression paper if the timing aligns).

---

## Multi-mapping

If the article qualifies for inclusion under L1–L4 for **more than one** paper in the corpus (e.g., a generic "screen time and depression" article that could trace to multiple Nagata papers), the article is coded as **multi-mapped** and tagged with all matching `paper_id`s. Multi-mapping is not an exclusion — it is an analytic finding that journalism conflates studies.

## Exclusion at N1

An article is excluded at N1 if **none** of L1–L4 are met. Common exclusion reasons:
- Article is about ABCD generally (e.g., overview piece) without referencing a specific paper from the corpus
- Article is about a different ABCD topic (e.g., substance use without phone/social media variable)
- Article is about smartphone/social media research from a non-ABCD cohort (e.g., NHANES, MTF) but indexed by the search query because of overlapping keywords
- Article is a syndicated republication of an article already counted (deduplicate to canonical)

## Operationalization

The N1 screening is run by a single AI coder with confidence threshold ≥ 0.7. Articles with confidence < 0.7 or evidence of multi-mapping are flagged for human spot-check. The full article text is fetched (where accessible) for the linkage check; where the article is paywalled, the headline + lead paragraph + visible snippets from search results are used.

Output: `N1-scoring.csv` with columns:
- `article_id` (canonical URL hash)
- `paper_id_matched` (comma-separated list)
- `linkage_test` (L1 / L2 / L3 / L4 / multi)
- `confidence` (0–1)
- `excluded` (Y/N)
- `exclusion_reason` (if Y)
- `evidence` (specific text or link confirming the match)
