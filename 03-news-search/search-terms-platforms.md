# News-Coverage Search — Sources, Queries, and Parameters (PRISMA-S)

This document specifies the news-coverage search strategy a-priori. It defines the exact information source, query construction rule, parameters, and filters used. The corresponding scripts in this directory operationalize the rules so that the search is fully reproducible.

The 69 papers included at Stage 2 (full-text eligibility) are the targets. For each paper, deterministic queries are generated from paper metadata (lead author surname, paper-specific topic terms, study identifier, publication date). The query manifest (`papers_manifest.json`) records the exact strings used per paper.

---

## Information source

| Source | Endpoint | Coverage | Key required |
|---|---|---|---|
| **SerpAPI** | `https://serpapi.com/search.json` | Google News and Google search indices | Yes (researcher API key) |

SerpAPI is used in two modes:

- `engine=google_news` for per-paper keyword searches of Google News.
- `engine=google` with `site:` operator for outlet-anchored sweeps of pre-specified mainstream and specialty health press websites.

---

## Two-strategy search

### Strategy 1 — Paper-anchored Google News (per-paper queries)

For each of the 69 included papers, deterministic queries are generated from paper metadata using the rules below. Date restriction uses the paper's publication date ± 6 months.

**Q2 — Author + study-context (Google News)**
```
"{first_author_last_name}" "Adolescent Brain Cognitive Development" "{topic_term}"
```
Where `{topic_term}` is the paper-specific phone/SM modality extracted from the paper title (e.g., "social media", "screen time", "smartphone", "video chat", "texting", "cyberbullying", "digital media", "online dating", "screen use").

**Q3 — Distinctive title fragment (Google News)**
```
"{first_6_words_of_title}"
```
Where the title fragment is the first 6 words of the paper title with leading filler removed (e.g., "A study of", "The role of", "Examining the", "Exploring the", "Associations between").

**Q4 — Press release search (Google, site filter)**
```
"{first_author_last_name}" "{topic_term}" site:eurekalert.org
```
No date filter (press releases are easy to find by author + topic).

Per-paper queries total: 196 (varying 1–3 per paper depending on which fields were extractable).

### Strategy 2 — Outlet-anchored Google search (per-outlet queries)

For each of 35 pre-specified mainstream news and specialty health press outlets, one Google search:

```
site:{outlet} ("Adolescent Brain Cognitive Development" OR "ABCD Study")
```

Date range: 2018-01-01 through 2026-12-31. Captures any article on those outlets that mentions ABCD by name, regardless of how the journalist framed the lead author or paper title. Articles are linked back to specific papers at the N1 linkage stage based on article content.

**Outlet list:**

| Category | Outlets |
|---|---|
| General news | nytimes.com, washingtonpost.com, npr.org, wsj.com, nbcnews.com, cbsnews.com, abcnews.go.com, cnn.com, reuters.com, apnews.com, bloomberg.com, usatoday.com |
| Magazines / opinion | theatlantic.com, wired.com, vox.com, time.com, newsweek.com, theguardian.com, bbc.com, bbc.co.uk |
| Specialty health press | medpagetoday.com, medscape.com, sciencealert.com, scientificamerican.com, livescience.com, healthday.com, psychologytoday.com |
| Tech / news | theverge.com, axios.com, businessinsider.com |
| Public broadcasting + science press | pbs.org, statnews.com, kffhealthnews.org |
| Local/regional with national reach | latimes.com, chicagotribune.com |

Outlet-anchored queries total: 35.

**Combined total: 231 SerpAPI calls. 1,458 raw results.**

---

## SerpAPI parameters

### `engine=google_news` (paper-anchored)
- `q`: query string per Q2 / Q3 above
- `gl`: `us` (US English news priority)
- `hl`: `en`
- `tbs`: date range — `cdr:1,cd_min:MM/DD/YYYY,cd_max:MM/DD/YYYY` (paper publication date − 30 days through publication + 180 days)
- `num`: 100

### `engine=google` with site filter (outlet-anchored and press-release)
- `q`: query string per Q4 / outlet sweep above
- `gl`: `us`
- `hl`: `en`
- `tbs`: date range for outlet sweep — `cdr:1,cd_min:01/01/2018,cd_max:12/31/2026`
- `num`: 30 (Q4) or 100 (outlet sweep)

---

## Output schema

Each script produces a CSV with this schema:

| Column | Description |
|---|---|
| `paper_id` | The Stage-2-included paper this query targeted (blank for outlet-sweep rows, populated at N1 linkage) |
| `doi` | Paper DOI |
| `source` | `serpapi_google_news` (paper-anchored) or `serpapi_outlet_sweep` (outlet-anchored) |
| `query_id` | Q2 / Q3 / Q4 / S-O |
| `query` | The exact query string sent to SerpAPI |
| `outlet` | News outlet / domain |
| `url` | Article URL |
| `title` | Article title |
| `summary` | Lead paragraph or snippet returned by SerpAPI |
| `published_date` | Article publication date as reported by Google News/Search |
| `retrieved_on` | ISO-8601 timestamp of the API call |

Each script also produces a JSON log (`raw/*_log.json`) recording every API call: timestamp, endpoint, query parameters, number of results returned, and errors.

---

## Deduplication

`05_deduplicate.py` merges the per-paper and outlet-sweep CSVs into `news_deduplicated.csv` using these rules:

1. **URL canonicalization**: lowercase scheme + host, strip trailing slash, strip tracking params (`utm_*`, `fbclid`, `gclid`, etc.), strip URL fragments.
2. **Group by canonical URL**.
3. **Preserve all paper_ids** that mapped to the URL — `paper_ids` becomes a comma-separated list. Multi-mapped articles are kept; this is itself an analytic finding for the substantive coding stage.
4. **Title-fuzzy merge** within the same domain: if two URLs share a domain and have title similarity ≥ 90% (Levenshtein ratio on lowercased text), merge them with the older URL as canonical.

---

## Sources considered but not used

The following sources were attempted or considered but did not yield usable results within the project timeline. Documented here for transparency.

- **Altmetric public API** (`api.altmetric.com/v1/doi/{doi}`): returned HTTP 403 for all 72 attempted DOI lookups. The public endpoint has been gated since 2022. A formal researcher API application was submitted to Altmetric; access was not granted within the project timeline.
- **Crossref Event Data** (`api.eventdata.crossref.org`): returned HTTP 403. This product was discontinued by Crossref in 2022.
- **GDELT 2.0 DOC API** (`api.gdeltproject.org/api/v2/doc/doc`): returned persistent rate-limit messages even with 5-second spacing between requests; not productive without registered access.
- **EurekAlert direct scrape**: blocked by automated request filters.

Coverage of the outlets and articles these alternative sources would have surfaced is substantially achieved by the outlet-anchored Google search strategy (Strategy 2 above), which queries each major news and specialty health press domain directly for ABCD-named coverage.

---

## Eligibility for the news corpus (linkage criteria)

After deduplication, candidate articles enter the linkage screening (Stage N1). See `N1-linkage-criteria.md` for the four ways an article qualifies as "coverage of paper X" (L1 direct link, L2 author + journal, L3 distinctive paraphrase, L4 institution + topic + ABCD configuration), the multi-mapping rule, and the AI-coder operationalization.

---

## Provenance and reproducibility

Every news article in the final corpus carries the following provenance fields, sufficient for any researcher to re-run the exact query that retrieved it:

- `source` (paper-anchored or outlet-anchored)
- `query` (exact string sent)
- `parameters` (date range, language, num, site filter)
- `retrieved_on` (ISO-8601 timestamp)
- `paper_id(s)` it was provisionally mapped to (populated at N1 linkage)

Per-source scripts are versioned with the manifest they consumed; the manifest (`papers_manifest.json`) records the Crossref metadata-retrieval timestamp at the time queries were generated.
