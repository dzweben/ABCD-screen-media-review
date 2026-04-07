#!/usr/bin/env python3
"""
OpenAlex search for ABCD Study screen/digital media papers.

Two-step approach:
1. Retrieve all ABCD Study papers via title_and_abstract.search filter
2. Post-filter for screen/media keywords in title + abstract

No API key required. Polite pool access with mailto parameter.

Output: search/results/openalex_results.csv + openalex_search_log.json
"""

import sys, json, csv, time
from urllib.request import urlopen, Request
from urllib.parse import quote
from pathlib import Path
from datetime import date

EMAIL = "daniel.zweben@temple.edu"
OUT_DIR = Path(__file__).parent / "results"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ABCD Study search terms for Step 1
ABCD_TERMS = [
    "Adolescent Brain Cognitive Development",
    "ABCD Study adolescent brain",
]

# Screen/media keywords for Step 2 post-filter
MEDIA_KEYWORDS = [
    "screen time", "social media", "smartphone", "smart phone", "mobile phone",
    "cell phone", "internet use", "internet addiction", "texting", "text messaging",
    "digital media", "screen media", "media use", "phone use", "screen use",
    "video game", "gaming", "television", "social networking", "online",
    "problematic phone", "problematic smartphone", "problematic social media",
    "problematic internet", "instagram", "tiktok", "snapchat", "facebook",
    "youtube", "twitter", "mobile device", "cyberbull",
]

MIN_YEAR = 2015  # ABCD data collection started 2015


def fetch_all_pages(search_term):
    """Fetch all works matching a title/abstract search term."""
    works = []
    cursor = "*"
    page = 0
    while cursor:
        url = (
            f"https://api.openalex.org/works?"
            f"filter=title_and_abstract.search:{quote(search_term)}"
            f"&per_page=200&cursor={cursor}"
            f"&mailto={EMAIL}"
            f"&select=id,doi,title,publication_year,authorships,"
            f"primary_location,abstract_inverted_index,type,cited_by_count"
        )
        resp = json.loads(urlopen(Request(url), timeout=30).read())
        batch = resp.get("results", [])
        works.extend(batch)
        page += 1
        meta = resp.get("meta", {})
        cursor = meta.get("next_cursor")
        total = meta.get("count", 0)
        if page <= 3 or page % 10 == 0:
            print(f"  '{search_term[:35]}' p{page}: {len(works)}/{total}")
        if not batch:
            break
        time.sleep(0.15)
    return works, total


def reconstruct_abstract(inverted_index):
    """Reconstruct abstract text from OpenAlex inverted index format."""
    if not inverted_index:
        return ""
    try:
        max_pos = max(max(p) for p in inverted_index.values())
        arr = [""] * (max_pos + 1)
        for word, positions in inverted_index.items():
            for pos in positions:
                if pos <= max_pos:
                    arr[pos] = word
        return " ".join(arr)
    except (ValueError, TypeError):
        return ""


def main():
    # Step 1: Get all ABCD papers
    print("Step 1: Retrieving all ABCD Study papers from OpenAlex...")
    all_works = []
    term_counts = {}
    for term in ABCD_TERMS:
        works, total = fetch_all_pages(term)
        all_works.extend(works)
        term_counts[term] = total
        print(f"  Done: {total} hits for '{term[:35]}'")

    # Deduplicate by OpenAlex ID
    seen = {}
    for w in all_works:
        oid = w.get("id", "")
        if oid not in seen:
            seen[oid] = w
    print(f"\nTotal unique ABCD papers: {len(seen)}")

    # Step 2: Filter for screen/media keywords
    print("Step 2: Filtering for screen/media keywords...")
    rows = []
    for oid, w in seen.items():
        year = w.get("publication_year") or 0
        if year < MIN_YEAR:
            continue

        title = w.get("title") or ""
        abstract = reconstruct_abstract(w.get("abstract_inverted_index"))
        combined = (title + " " + abstract).lower()

        matched = [kw for kw in MEDIA_KEYWORDS if kw in combined]
        if not matched:
            continue

        doi = (w.get("doi") or "").replace("https://doi.org/", "")
        authorships = w.get("authorships") or []
        authors = [(a.get("author") or {}).get("display_name", "") for a in authorships]
        authors = [a for a in authors if a]
        source = (w.get("primary_location") or {}).get("source") or {}

        rows.append({
            "openalex_id": oid,
            "doi": doi,
            "title": title,
            "authors": "; ".join(authors),
            "first_author": authors[0] if authors else "",
            "year": str(year),
            "journal": source.get("display_name", ""),
            "abstract": abstract[:5000],
            "doc_type": w.get("type", ""),
            "cited_by_count": w.get("cited_by_count", 0),
            "matched_keywords": "; ".join(matched),
        })

    rows.sort(key=lambda x: x["year"], reverse=True)
    print(f"After filter: {len(rows)} papers (>= {MIN_YEAR})")

    # Write CSV
    csv_path = OUT_DIR / "openalex_results.csv"
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)

    # Write log
    log = {
        "database": "OpenAlex",
        "search_date": str(date.today()),
        "method": "title_and_abstract.search filter then keyword post-filter",
        "abcd_search_terms": ABCD_TERMS,
        "abcd_term_counts": term_counts,
        "total_abcd_papers": len(seen),
        "media_keywords": MEDIA_KEYWORDS,
        "min_year": MIN_YEAR,
        "after_filter": len(rows),
    }
    with open(OUT_DIR / "openalex_search_log.json", "w") as f:
        json.dump(log, f, indent=2)

    print(f"\nDone! {len(rows)} papers -> {csv_path}")


if __name__ == "__main__":
    main()
