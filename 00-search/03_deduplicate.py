#!/usr/bin/env python3
"""
Deduplicate search results across PubMed, OpenAlex, and ABCD website.

Merges by normalized DOI. Outputs:
- screening/results/deduplicated.csv
- screening/results/prisma_counts.json
"""

import csv, json
from pathlib import Path
from datetime import date

BASE = Path(__file__).parent.parent
SEARCH_DIR = BASE / "search" / "results"
SCREEN_DIR = Path(__file__).parent / "results"
SCREEN_DIR.mkdir(parents=True, exist_ok=True)


def norm_doi(d):
    if not d:
        return ""
    d = d.lower().strip()
    for prefix in ["https://doi.org/", "http://doi.org/", "doi:"]:
        if d.startswith(prefix):
            d = d[len(prefix):]
    return d.rstrip("/. ")


def main():
    # Load sources
    pm = list(csv.DictReader(open(SEARCH_DIR / "pubmed_results.csv")))
    oa = list(csv.DictReader(open(SEARCH_DIR / "openalex_results.csv")))

    abcd_path = BASE / "data" / "raw" / "candidate_list.csv"
    abcd = list(csv.DictReader(open(abcd_path))) if abcd_path.exists() else []

    print(f"PubMed: {len(pm)}, OpenAlex: {len(oa)}, ABCD website: {len(abcd)}")

    # Build master by DOI
    master = {}

    for p in pm:
        doi = norm_doi(p.get("doi", ""))
        if not doi:
            continue
        if doi not in master:
            master[doi] = {
                "doi": doi, "title": p["title"], "authors": p.get("authors", ""),
                "first_author": p.get("first_author", ""), "year": p.get("year", ""),
                "journal": p.get("journal", ""), "abstract": p.get("abstract", ""),
                "pmid": p.get("pmid", ""),
                "in_pubmed": 1, "in_openalex": 0, "in_abcd_website": 0,
            }
        else:
            master[doi]["in_pubmed"] = 1
            master[doi]["pmid"] = p.get("pmid", "")

    for o in oa:
        doi = norm_doi(o.get("doi", ""))
        if not doi:
            continue
        if doi not in master:
            master[doi] = {
                "doi": doi, "title": o["title"], "authors": o.get("authors", ""),
                "first_author": o.get("first_author", ""), "year": o.get("year", ""),
                "journal": o.get("journal", ""), "abstract": o.get("abstract", ""),
                "pmid": "",
                "in_pubmed": 0, "in_openalex": 1, "in_abcd_website": 0,
            }
        else:
            master[doi]["in_openalex"] = 1
            if not master[doi]["abstract"] and o.get("abstract"):
                master[doi]["abstract"] = o["abstract"]

    for a in abcd:
        doi = norm_doi(a.get("doi", ""))
        if not doi:
            continue
        if doi in master:
            master[doi]["in_abcd_website"] = 1
        else:
            master[doi] = {
                "doi": doi, "title": a.get("title", ""), "authors": a.get("first_author", ""),
                "first_author": a.get("first_author", ""), "year": a.get("year", ""),
                "journal": a.get("journal", ""), "abstract": "",
                "pmid": "",
                "in_pubmed": 0, "in_openalex": 0, "in_abcd_website": 1,
            }

    for doi, m in master.items():
        m["source_count"] = m["in_pubmed"] + m["in_openalex"] + m["in_abcd_website"]

    records = sorted(master.values(), key=lambda x: (x["year"], x["first_author"]), reverse=True)

    # Write CSV
    fields = ["doi", "title", "authors", "first_author", "year", "journal", "abstract",
              "pmid", "in_pubmed", "in_openalex", "in_abcd_website", "source_count"]
    with open(SCREEN_DIR / "deduplicated.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in records:
            w.writerow({k: r.get(k, "") for k in fields})

    # PRISMA counts
    total_raw = len(pm) + len(oa) + len(abcd)
    prisma = {
        "search_date": str(date.today()),
        "identification": {
            "pubmed": len(pm), "openalex": len(oa), "abcd_website": len(abcd),
            "total_before_dedup": total_raw,
        },
        "deduplication": {
            "duplicates_removed": total_raw - len(records),
            "unique_records": len(records),
        },
    }
    with open(SCREEN_DIR / "prisma_counts.json", "w") as f:
        json.dump(prisma, f, indent=2)

    print(f"\nUnique: {len(records)} (removed {total_raw - len(records)} dupes)")
    print(f"PubMed only: {sum(1 for r in records if r['in_pubmed'] and not r['in_openalex'] and not r['in_abcd_website'])}")
    print(f"OpenAlex only: {sum(1 for r in records if r['in_openalex'] and not r['in_pubmed'] and not r['in_abcd_website'])}")
    print(f"ABCD website only: {sum(1 for r in records if r['in_abcd_website'] and not r['in_pubmed'] and not r['in_openalex'])}")
    print(f"In all 3: {sum(1 for r in records if r['in_pubmed'] and r['in_openalex'] and r['in_abcd_website'])}")


if __name__ == "__main__":
    main()
