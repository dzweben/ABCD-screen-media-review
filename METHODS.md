# Methods

## Search Strategy

A systematic literature search was conducted in accordance with PRISMA 2020 guidelines. Three electronic databases and one supplementary source were searched for studies using data from the Adolescent Brain Cognitive Development (ABCD) Study that included a screen or digital media variable.

### Databases and Search Dates

| Source | Interface | Date Searched | Records |
|--------|-----------|---------------|---------|
| PubMed/MEDLINE | NCBI E-utilities API | 2026-04-06 | 171 |
| OpenAlex | OpenAlex REST API v1 | 2026-04-06 | 450 |
| Google Scholar | SerpAPI | 2026-04-07 | 443 |
| abcdstudy.org/publications | Programmatic scrape | 2026-03-25 | 101 |

No date, language, or publication type restrictions were applied at the search stage.

### Search Terms

All searches combined two concept blocks:

**Block 1 — ABCD Study identification:**
Adolescent Brain Cognitive Development, ABCD Study, ABCD cohort, ABCD sample, ABCD dataset, ABCD participants

**Block 2 — Screen and digital media:**
screen time, social media, smartphone, smart phone, mobile phone, cell phone, internet use, internet addiction, texting, text messaging, digital media, screen media, media use, phone use, screen use, video game, gaming, television, social networking, online, mobile device, problematic phone, problematic smartphone, problematic social media, problematic internet, Instagram, TikTok, Snapchat, Facebook, YouTube, Twitter, cyberbullying

### Database-Specific Implementation

**PubMed/MEDLINE.** Block 1 and Block 2 were combined with AND using title/abstract field tags ([tiab]) and MeSH terms ([mh]). The full Boolean string is reproduced in `search/search_strings.md`. Search was executed via the NCBI E-utilities API (`esearch` + `efetch`). Script: `search/01_pubmed_search.py`.

**OpenAlex.** All works containing Block 1 terms in the title or abstract were retrieved via the `title_and_abstract.search` API filter (5,301 unique ABCD papers). These were post-filtered for Block 2 keyword matches in the title or abstract, restricted to publications from 2015 onward. Script: `search/02_openalex_search.py`.

**Google Scholar.** Because Google Scholar does not support full Boolean syntax, 18 targeted phrase-combination queries were executed via the SerpAPI Google Scholar endpoint, each pairing a Block 1 phrase with a Block 2 term, filtered to 2015+. Script: `search/03_google_scholar_search.py`.

**ABCD Study Website.** The consortium publications page (https://abcdstudy.org/publications/) was scraped programmatically. The page contains a JSON-LD structured data element listing all ~1,443 consortium-tracked publications. Titles and PubMed-retrieved abstracts were screened against the same Block 2 keyword set. This source is classified as "other methods" in the PRISMA flow. Script: `search/01_scrape_publications.py`.

---

## Deduplication

Records were merged across all four sources by normalized DOI (lowercased, prefix-stripped). **1,165 total records** were reduced to **620 unique records** after removing 545 duplicates.

---

## Inclusion and Exclusion Criteria

### Inclusion (all required)

| Code | Criterion |
|------|-----------|
| **IC1** | Uses data from the U.S. Adolescent Brain Cognitive Development (ABCD) Study. Papers using the Amsterdam Born Children and their Development (ABCD) cohort do not qualify. |
| **IC2** | Includes a screen or digital media variable in any analytic role (exposure, outcome, mediator, moderator, or covariate). All modalities eligible: screen time, social media, smartphone, internet, texting, video gaming, television, digital media, passive sensing, or problematic use scales. |
| **IC3** | Reports original empirical findings with quantitative analysis of ABCD data. |
| **IC4** | Published in a peer-reviewed journal. |

### Exclusion (any sufficient)

| Code | Criterion |
|------|-----------|
| **EC1** | Does not use ABCD Study data, or does not include a screen/digital media variable. |
| **EC3** | No original empirical analysis: reviews, editorials, commentaries, letters, study protocols, meta-analyses, book chapters, news summaries, or policy briefs. |
| **EC4** | Conference abstract without a corresponding peer-reviewed full-text publication. |
| **EC5** | Duplicate: preprints where the peer-reviewed version is included; supplementary data deposits (Figshare, Zenodo); or identical analyses in multiple venues. The peer-reviewed version is retained. |

### Notes on Scope

- **No modality-based exclusion.** Papers examining any screen media modality (television, gaming, social media, aggregate screen time) are eligible. Modality is coded during full-text data extraction.
- **Screen time as outcome.** Papers in which screen time is the dependent variable are included. Directionality is coded during data extraction.
- **Aggregate screen time.** Papers reporting only total screen time without modality breakdown are included.

---

## Screening

Title and abstract screening was performed on all 620 unique records. Two coders independently reviewed each record against the inclusion and exclusion criteria. Disagreements were resolved by consensus. The complete screening record is in `screening/results/screening-all.csv`.

AI-assisted screening was conducted as a supplementary validation and is documented in `screening/ai_validation/`.

---

## PRISMA Flow

### Identification
| Source | Records |
|--------|---------|
| PubMed | 171 |
| OpenAlex | 450 |
| Google Scholar | 443 |
| ABCD website (other methods) | 101 |
| **Total** | **1,165** |

### Deduplication
- Duplicates removed: 545
- **Unique records screened:** 620

### Screening (Title/Abstract)
- Included: [per screening-all.csv]
- Excluded: [per screening-all.csv]

### Full-Text Review
- Sought for retrieval: [pending]
- Not retrieved: [pending]

### Included
- Studies included in review: [pending]

---

## Reproducibility

All search scripts are in `search/` and can be re-executed to reproduce the database queries:

```bash
python3 search/01_pubmed_search.py
python3 search/02_openalex_search.py
python3 search/03_google_scholar_search.py SERPAPI_KEY
```

Search logs with exact timestamps and hit counts are in `search/results/`. Result counts may differ on subsequent dates due to newly indexed publications.

| Tool | Purpose |
|------|---------|
| Python 3.9+ | All scripts |
| NCBI E-utilities API | PubMed search and abstract retrieval |
| OpenAlex REST API | OpenAlex search |
| SerpAPI | Google Scholar search |
