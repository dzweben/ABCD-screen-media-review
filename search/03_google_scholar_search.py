#!/usr/bin/env python3
"""
Google Scholar search via SerpAPI.

Searches for ABCD Study papers with screen/digital media exposures.
Requires a SerpAPI key (free tier: 250 searches/month).

Usage:
    python3 search/03_google_scholar_search.py YOUR_API_KEY

Output: search/results/google_scholar_results.csv + google_scholar_search_log.json
"""

import sys, json, csv, time
from urllib.request import urlopen, Request
from urllib.parse import urlencode, quote_plus
from pathlib import Path
from datetime import date

if len(sys.argv) < 2:
    print("Usage: python3 03_google_scholar_search.py YOUR_SERPAPI_KEY")
    sys.exit(1)

API_KEY = sys.argv[1]
OUT_DIR = Path(__file__).parent / "results"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Google Scholar queries — combine ABCD Study + screen/media terms
# GS doesn't support complex Boolean well, so we do multiple targeted queries
QUERIES = [
    '"Adolescent Brain Cognitive Development" "screen time"',
    '"Adolescent Brain Cognitive Development" "social media"',
    '"Adolescent Brain Cognitive Development" smartphone',
    '"Adolescent Brain Cognitive Development" "internet use"',
    '"Adolescent Brain Cognitive Development" "digital media"',
    '"Adolescent Brain Cognitive Development" texting',
    '"Adolescent Brain Cognitive Development" "media use"',
    '"Adolescent Brain Cognitive Development" "phone use"',
    '"ABCD Study" "screen time" adolescent',
    '"ABCD Study" "social media" adolescent',
    '"ABCD Study" smartphone adolescent',
    '"ABCD Study" "internet use" adolescent',
    '"ABCD Study" "digital media" adolescent',
    '"ABCD Study" "media use" adolescent',
    '"ABCD Study" "screen media" adolescent',
    '"ABCD Study" gaming adolescent',
    '"ABCD Study" television adolescent',
    '"ABCD Study" "problematic phone" OR "problematic social media"',
]

BASE_URL = "https://serpapi.com/search.json"


def search_scholar(query, start=0):
    """Search Google Scholar via SerpAPI."""
    params = {
        "engine": "google_scholar",
        "q": query,
        "api_key": API_KEY,
        "start": start,
        "num": 20,  # max per page
        "as_ylo": 2015,  # ABCD Study started 2015
    }
    url = f"{BASE_URL}?{urlencode(params)}"
    resp = json.loads(urlopen(Request(url), timeout=30).read())
    return resp


def main():
    all_papers = []
    seen_titles = set()  # Dedup by normalized title
    total_api_calls = 0

    for qi, query in enumerate(QUERIES):
        print(f"\n[{qi+1}/{len(QUERIES)}] {query[:60]}...")
        start = 0
        query_new = 0

        while start < 100:  # Max 5 pages per query
            try:
                resp = search_scholar(query, start)
                total_api_calls += 1
            except Exception as e:
                print(f"  Error at start={start}: {e}")
                break

            results = resp.get("organic_results", [])
            if not results:
                break

            for r in results:
                title = (r.get("title") or "").strip()
                title_norm = title.lower().replace(" ", "")

                if title_norm in seen_titles:
                    continue
                seen_titles.add(title_norm)

                # Extract info
                pub_info = r.get("publication_info", {})
                authors = pub_info.get("summary", "").split(" - ")[0] if pub_info.get("summary") else ""
                source = pub_info.get("summary", "").split(" - ")[-1] if pub_info.get("summary") else ""

                # Try to get year from snippet or source
                year = ""
                for field in [source, r.get("snippet", "")]:
                    import re
                    years = re.findall(r'20[12]\d', field)
                    if years:
                        year = years[-1]
                        break

                # Resources (PDF links, etc.)
                resources = r.get("resources", [])
                pdf_link = ""
                for res in resources:
                    if "pdf" in (res.get("file_format", "") or "").lower():
                        pdf_link = res.get("link", "")
                        break

                # Inline links
                link = r.get("link", "")

                all_papers.append({
                    "title": title,
                    "authors": authors,
                    "year": year,
                    "source": source,
                    "link": link,
                    "snippet": (r.get("snippet") or "")[:500],
                    "cited_by": r.get("inline_links", {}).get("cited_by", {}).get("total", ""),
                    "pdf_link": pdf_link,
                    "gs_position": r.get("position", ""),
                    "query": query[:60],
                })
                query_new += 1

            print(f"  start={start}: {len(results)} results, {query_new} new (total unique: {len(all_papers)})")

            # Check if more pages
            if len(results) < 20:
                break
            start += 20
            time.sleep(1)  # Rate limit

        time.sleep(0.5)

    # Sort by year
    all_papers.sort(key=lambda x: x.get("year", ""), reverse=True)

    # Write CSV
    csv_path = OUT_DIR / "google_scholar_results.csv"
    if all_papers:
        with open(csv_path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=all_papers[0].keys())
            w.writeheader()
            w.writerows(all_papers)

    # Write log
    log = {
        "database": "Google Scholar (via SerpAPI)",
        "search_date": str(date.today()),
        "queries": QUERIES,
        "total_api_calls": total_api_calls,
        "total_unique_results": len(all_papers),
        "year_filter": "2015+",
        "api": "SerpAPI free tier",
    }
    with open(OUT_DIR / "google_scholar_search_log.json", "w") as f:
        json.dump(log, f, indent=2)

    print(f"\n{'='*50}")
    print(f"Total unique papers: {len(all_papers)}")
    print(f"API calls used: {total_api_calls}/250 (monthly free tier)")
    print(f"Saved to: {csv_path}")


if __name__ == "__main__":
    main()
