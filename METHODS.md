# Search Strategy and Methods

## Overview

This systematic review follows PRISMA 2020 guidelines. Three electronic databases were searched, supplemented by a hand search of the ABCD Study publications page.

## Databases Searched

| Database | Interface | Search Date | Records |
|----------|-----------|-------------|---------|
| PubMed/MEDLINE | NCBI E-utilities API | 2026-04-06 | 171 |
| OpenAlex | REST API v1 | 2026-04-06 | 450 |
| Google Scholar | SerpAPI | 2026-04-07 | 443 |
| abcdstudy.org | Hand-searched publications page | 2026-03-25 | 101 |

### Database Selection Rationale

**OpenAlex** was selected because:
1. It indexes 250M+ academic works including journals covered by PsycINFO, Web of Science, and Scopus
2. A 2025 validation study found OpenAlex captures 98% of records from traditional systematic reviews (PMC12302543)
3. It provides 28-29% more coverage than Web of Science or Scopus alone
4. It offers a free, unrestricted REST API enabling fully reproducible programmatic searches

**Google Scholar** was added as a third database via the SerpAPI programmatic interface because:
1. It is the broadest academic index, capturing preprints, dissertations, and grey literature
2. It identified 75 papers not found by PubMed or OpenAlex
3. SerpAPI enables reproducible, programmatic searches (free tier: 250 searches/month)

## Search Strings

### PubMed/MEDLINE

Two concept blocks combined with AND:

**Block 1 — ABCD Study identification:**
```
"Adolescent Brain Cognitive Development"[tiab]
OR "ABCD Study"[tiab]
OR "ABCD cohort"[tiab]
OR "ABCD sample"[tiab]
OR "ABCD dataset"[tiab]
OR "ABCD participants"[tiab]
```

**Block 2 — Screen/digital media exposure:**
```
"social media"[tiab] OR "Social Media"[mh]
OR "smartphone"[tiab] OR "Smartphone"[mh]
OR "smart phone"[tiab]
OR "mobile phone"[tiab]
OR "cell phone"[tiab] OR "Cell Phone"[mh]
OR "internet use"[tiab]
OR "internet addiction"[tiab] OR "Internet Addiction Disorder"[mh]
OR "texting"[tiab]
OR "text messaging"[tiab] OR "Text Messaging"[mh]
OR "problematic phone"[tiab]
OR "problematic smartphone"[tiab]
OR "problematic social media"[tiab]
OR "problematic internet"[tiab]
OR "digital media"[tiab]
OR "screen media"[tiab]
OR "screen time"[tiab] OR "Screen Time"[mh]
OR "media use"[tiab]
OR "phone use"[tiab]
OR "mobile device"[tiab]
OR "social networking"[tiab] OR "Social Networking"[mh]
OR "Instagram"[tiab]
OR "TikTok"[tiab]
OR "Snapchat"[tiab]
OR "Facebook"[tiab]
OR "YouTube"[tiab]
OR "Twitter"[tiab]
OR "video game"[tiab] OR "Video Games"[mh]
OR "gaming"[tiab]
OR "television"[tiab] OR "Television"[mh]
OR "screen use"[tiab]
OR "online"[tiab]
```

**Combined:** `(Block 1) AND (Block 2)`

No date, language, or publication type restrictions applied at search stage.

### OpenAlex

Two-step search using the OpenAlex REST API:

**Step 1:** Retrieved all works matching `title_and_abstract.search` filter for:
- `"Adolescent Brain Cognitive Development"` (5,232 results)
- `"ABCD Study adolescent brain"` (1,473 results)
- Merged and deduplicated: 5,301 unique ABCD papers

**Step 2:** Post-filtered for screen/media keywords in title or abstract:
- screen time, social media, smartphone, smart phone, mobile phone, cell phone, internet use, internet addiction, texting, text messaging, digital media, screen media, media use, phone use, screen use, video game, gaming, television, social networking, online, problematic phone, problematic smartphone, problematic social media, problematic internet, instagram, tiktok, snapchat, facebook, youtube, twitter, cyberbullying

**Additional filter:** Publication year >= 2015 (ABCD Study data collection began in 2015)

**Result:** 450 papers

### ABCD Study Website

The complete publications list at abcdstudy.org/publications/ was scraped programmatically. All ~1,443 listed publications were retrieved, then keyword-filtered against the same screen/media terms applied to titles and abstracts retrieved via PubMed.

**Result:** 101 candidate papers

## Deduplication

Records were merged across all three sources using normalized DOIs as the primary matching key:
- DOIs lowercased, `https://doi.org/` prefix stripped, trailing punctuation removed
- For records without DOIs: fuzzy title matching (>0.90 similarity) + same first author + same year

**Result:** 620 unique records (545 duplicates removed from 1,165 total)

## PRISMA Flow

### Identification
- Records from PubMed: 171
- Records from OpenAlex: 450
- Records from Google Scholar: 443
- Records from other sources (abcdstudy.org): 101
- **Total:** 1,165

### Before Screening
- Duplicate records removed: 545
- **Records after dedup:** 620

### Screening (Title/Abstract)

Screening was conducted through five iterative AI passes, each documented in `screening/results/screening_decisions.csv` with one row per paper per coder. This iterative approach substitutes for dual human coding by providing multiple independent computational assessments with full audit trails.

| Pass | Coder ID | Papers Screened | Purpose |
|------|----------|----------------|---------|
| 1 | AI_prior | 94 | Pre-included from pilot analysis |
| 2 | AI_coder1 | 451 | First independent screen of all new papers |
| 3 | AI_coder2 | 545 | Second independent screen (all papers) |
| 4 | AI_resolver_consensus | 44 | Resolved 44 UNSURE papers via DOI lookup |
| 5 | AI_tiebreaker | 151 | Resolved 76 C1/C2 disagreements + screened 75 new GS papers |
| 6 | AI_safety_net | TBD | Final inclusive pass reviewing all EXCLUDE decisions |

**Inter-rater reliability (AI_coder1 vs AI_coder2):**
- Cohen's kappa: 0.764 (substantial agreement)
- 95 disagreements documented in `screening/results/disagreements.csv`
- Tiebreaker found AI_coder1 was wrong 74/76 times (overly permissive); AI_coder2 was wrong 2/76 times

**Consensus screening results (after tiebreaker):**
- Records screened: 620
- Records included: 208
- Records excluded: 409
  - EC1 (not ABCD data / no screen exposure): 328
  - EC3 (review/editorial/news): 51
  - EC5 (duplicate publication): 11
  - EC4 (conference abstract only): 9
  - EC2 (gaming-only / TV-only / no screen variable): 10
- UNSURE remaining: 3

### Full-Text Retrieval
- PDFs obtained: 100
- PDFs still needed: ~108

### Coding
- Papers fully coded (from pilot): 94
- Papers awaiting coding: ~114

## Inclusion Criteria

- **IC1:** Uses data from the ABCD Study
- **IC2:** Primary or secondary exposure is smartphone use, social media use, internet use, texting/text messaging, or problematic/compulsive use of these technologies
- **IC3:** Reports original empirical findings (quantitative analysis of ABCD data)
- **IC4:** Published in a peer-reviewed journal

## Exclusion Criteria

- **EC1:** Not ABCD data
- **EC2:** Exposure is exclusively TV (`EC2_tv_only`), exclusively video games (`EC2_gaming_only`), or aggregated screen time without modality breakdown (`EC2_aggregate`)
- **EC3:** Editorial, review, commentary, protocol, or meta-analysis without original ABCD analysis (`EC3_review`)
- **EC4:** Conference abstract only (`EC4_abstract`)
- **EC5:** Duplicate publication (`EC5_duplicate`)

## Software and Tools

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.9+ | Search scripts, data processing |
| NCBI E-utilities | API | PubMed search |
| OpenAlex API | v1 | OpenAlex search |
| openpyxl | 3.1+ | Excel workbook generation |

## Reproducibility

All search scripts are in `search/`. Running them will reproduce the database queries. Note that result counts may differ on subsequent dates due to newly indexed publications.

Search logs with exact timestamps are stored in `search/results/`.
