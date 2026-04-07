# Search Strategy and Methods

## Overview

This systematic review follows PRISMA 2020 guidelines. Two electronic databases were searched, supplemented by a hand search of the ABCD Study publications page.

## Databases Searched

| Database | Interface | Search Date | Records |
|----------|-----------|-------------|---------|
| PubMed/MEDLINE | NCBI E-utilities API | 2026-04-06 | 171 |
| OpenAlex | REST API v1 | 2026-04-06 | 450 |
| abcdstudy.org | Hand-searched publications page | 2026-03-25 | 101 |

### Why OpenAlex Instead of PsycINFO/Web of Science

OpenAlex was selected as the second database because:
1. It indexes 250M+ academic works including journals covered by PsycINFO, Web of Science, and Scopus
2. A 2025 validation study found OpenAlex captures 98% of records from traditional systematic reviews (PMC12302543)
3. It provides 28-29% more coverage than Web of Science or Scopus alone
4. It offers a free, unrestricted REST API enabling fully reproducible programmatic searches
5. PsycINFO and Web of Science require institutional browser authentication (Duo MFA) incompatible with automated reproducible search pipelines

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

**Result:** 545 unique records (177 duplicates removed from 722 total)

## PRISMA Flow

### Identification
- Records from PubMed: 171
- Records from OpenAlex: 450
- Records from other sources (abcdstudy.org): 101
- **Total:** 722

### Before Screening
- Duplicate records removed: 177
- **Records after dedup:** 545

### Screening
- Records screened (title/abstract): 545
- Records excluded: [pending]
- Records included for full-text review: [pending]

### Included
- Studies included in review: [pending]
- Previously coded from pilot analysis: 94

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
