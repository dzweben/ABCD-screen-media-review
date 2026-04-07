# Exact Search Strings

Copy-paste ready for each database. Last executed: 2026-04-06.

## PubMed/MEDLINE

Paste into PubMed Advanced Search or use with E-utilities API:

```
("Adolescent Brain Cognitive Development"[tiab] OR "ABCD Study"[tiab] OR "ABCD cohort"[tiab] OR "ABCD sample"[tiab] OR "ABCD dataset"[tiab] OR "ABCD participants"[tiab]) AND ("social media"[tiab] OR "Social Media"[mh] OR "smartphone"[tiab] OR "Smartphone"[mh] OR "smart phone"[tiab] OR "mobile phone"[tiab] OR "cell phone"[tiab] OR "Cell Phone"[mh] OR "internet use"[tiab] OR "internet addiction"[tiab] OR "Internet Addiction Disorder"[mh] OR "texting"[tiab] OR "text messaging"[tiab] OR "Text Messaging"[mh] OR "problematic phone"[tiab] OR "problematic smartphone"[tiab] OR "problematic social media"[tiab] OR "problematic internet"[tiab] OR "digital media"[tiab] OR "screen media"[tiab] OR "screen time"[tiab] OR "Screen Time"[mh] OR "media use"[tiab] OR "phone use"[tiab] OR "mobile device"[tiab] OR "social networking"[tiab] OR "Social Networking"[mh] OR "Instagram"[tiab] OR "TikTok"[tiab] OR "Snapchat"[tiab] OR "Facebook"[tiab] OR "YouTube"[tiab] OR "Twitter"[tiab] OR "video game"[tiab] OR "Video Games"[mh] OR "gaming"[tiab] OR "television"[tiab] OR "Television"[mh] OR "screen use"[tiab] OR "online"[tiab])
```

**Result:** 171 records

## OpenAlex API

Two-step programmatic search:

**Step 1 — Retrieve all ABCD Study papers:**
```
GET https://api.openalex.org/works?filter=title_and_abstract.search:Adolescent%20Brain%20Cognitive%20Development&per_page=200&cursor=*

GET https://api.openalex.org/works?filter=title_and_abstract.search:ABCD%20Study%20adolescent%20brain&per_page=200&cursor=*
```

**Step 2 — Post-filter for screen/media keywords in title+abstract:**

Keywords: screen time, social media, smartphone, smart phone, mobile phone, cell phone, internet use, internet addiction, texting, text messaging, digital media, screen media, media use, phone use, screen use, video game, gaming, television, social networking, online, problematic phone, problematic smartphone, problematic social media, problematic internet, instagram, tiktok, snapchat, facebook, youtube, twitter, cyberbullying

**Additional filter:** Year >= 2015

**Result:** 450 records

## ABCD Study Website (Supplementary Hand Search)

**Source:** https://abcdstudy.org/publications/

**Date accessed:** 2026-03-25

**Method:**
1. The ABCD Study publications page contains an embedded JSON-LD `<script type="application/ld+json">` element with an `ItemList` of all consortium-tracked publications (~1,443 at time of access).
2. The page was fetched via Python `requests` and parsed with BeautifulSoup. Each `itemListElement` yielded: title, authors, year, DOI or URL, and journal.
3. DOIs were resolved to PubMed IDs (PMIDs) via NCBI E-utilities `esearch`, and abstracts were batch-retrieved via `efetch` (200 PMIDs per request).
4. All 1,443 publications were screened against the same keyword set used in the database searches (applied to title and abstract): screen time, social media, smartphone, smart phone, mobile phone, cell phone, internet use, internet addiction, texting, text messaging, problematic phone, problematic smartphone, problematic social media, problematic internet, digital media, screen media, media use, phone use, screen use, video game, gaming, television, social networking, online, mobile device, Instagram, TikTok, Snapchat, Facebook, YouTube, Twitter, cyberbullying.
5. Papers with any keyword match in title or abstract were retained as candidates.

**Script:** `search/01_scrape_publications.py`

**Result:** 101 candidate records from ~1,443 total publications
