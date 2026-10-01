"""
Cross-source deduplication for the news corpus.

Reads:
  raw/altmetric_results.csv
  raw/serpapi_results.csv
  raw/gdelt_results.csv

Produces:
  news_deduplicated.csv — one row per unique article, with all paper_ids it was
                          mapped to and all sources that returned it preserved.
  prisma_news_counts.json — Identification → Screening flow numbers for the
                          PRISMA-S diagram.

Dedup rules (see search-terms-platforms.md §Deduplication):
  1. URL-canonicalize: lowercase scheme + host, strip trailing /, strip
     tracking params (utm_*, fbclid, gclid, etc.), strip URL fragments.
  2. Group by canonical URL.
  3. Preserve all paper_ids and all sources (multi-mapped articles kept).
  4. Title-fuzzy merge within same domain (≥ 90% similarity).
"""
import csv, json, os, re
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from difflib import SequenceMatcher

ROOT = os.path.dirname(os.path.abspath(__file__))
SOURCES = [
    os.path.join(ROOT, "raw/serpapi_results.csv"),
    os.path.join(ROOT, "raw/serpapi_outlets_results.csv"),
]
OUT = os.path.join(ROOT, "news_deduplicated.csv")
COUNTS = os.path.join(ROOT, "prisma_news_counts.json")

TRACKING_PARAMS = {"utm_source","utm_medium","utm_campaign","utm_term","utm_content",
                   "fbclid","gclid","ref","ref_src","mc_cid","mc_eid","_hsenc","_hsmi"}

def canonicalize(url):
    if not url: return ""
    try:
        u = urlparse(url.strip())
    except Exception:
        return url
    netloc = u.netloc.lower().lstrip("www.")
    path = u.path.rstrip("/")
    query = "&".join(f"{k}={v}" for k,v in parse_qsl(u.query) if k.lower() not in TRACKING_PARAMS)
    return urlunparse((u.scheme.lower() or "https", netloc, path, "", query, ""))

def title_norm(t):
    t = (t or "").lower().strip()
    t = re.sub(r"[^a-z0-9 ]+", " ", t)
    return re.sub(r"\s+", " ", t)

# Load all source CSVs
all_rows = []
per_source_counts = {}
for path in SOURCES:
    if not os.path.exists(path):
        per_source_counts[os.path.basename(path)] = 0
        continue
    with open(path) as f:
        rows = list(csv.DictReader(f))
    per_source_counts[os.path.basename(path)] = len(rows)
    all_rows.extend(rows)
print(f"Loaded {len(all_rows)} total rows across {len(SOURCES)} sources")
for k,v in per_source_counts.items(): print(f"  {k}: {v}")

# Group by canonical URL
groups = {}
for r in all_rows:
    canon = canonicalize(r.get("url",""))
    if not canon: continue
    if canon not in groups:
        groups[canon] = {
            "canonical_url": canon,
            "url": r.get("url",""),
            "title": r.get("title",""),
            "outlet": r.get("outlet",""),
            "published_date": r.get("published_date",""),
            "summary": r.get("summary",""),
            "paper_ids": set(),
            "sources": set(),
            "queries": set(),
            "rows": []
        }
    g = groups[canon]
    g["paper_ids"].add(r.get("paper_id",""))
    g["sources"].add(r.get("source",""))
    g["queries"].add(f"{r.get('source','')}::{r.get('query_id','')}")
    g["rows"].append(r)
    if not g["title"] and r.get("title"): g["title"] = r["title"]
    if not g["summary"] and r.get("summary"): g["summary"] = r["summary"]

print(f"\nUnique URLs after canonicalization: {len(groups)}")

# Title-fuzzy merge within same domain
final = list(groups.values())
domain_buckets = {}
for g in final:
    d = urlparse(g["canonical_url"]).netloc
    domain_buckets.setdefault(d, []).append(g)

merged = []
for domain, arts in domain_buckets.items():
    used = set()
    for i, a in enumerate(arts):
        if i in used: continue
        cluster = [a]
        for j in range(i+1, len(arts)):
            if j in used: continue
            sim = SequenceMatcher(None, title_norm(a["title"]), title_norm(arts[j]["title"])).ratio()
            if sim >= 0.90 and a["title"] and arts[j]["title"]:
                cluster.append(arts[j]); used.add(j)
        # Merge cluster
        if len(cluster) == 1:
            merged.append(a)
        else:
            base = cluster[0]
            for x in cluster[1:]:
                base["paper_ids"] |= x["paper_ids"]
                base["sources"] |= x["sources"]
                base["queries"] |= x["queries"]
            merged.append(base)
print(f"After title-fuzzy merge: {len(merged)} unique articles")

# Write output
fields = ["canonical_url","url","title","outlet","published_date","summary",
          "paper_ids","n_paper_ids","sources","n_sources","queries","n_queries"]
with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for g in merged:
        w.writerow({
            "canonical_url": g["canonical_url"],
            "url": g["url"],
            "title": g["title"],
            "outlet": g["outlet"],
            "published_date": g["published_date"],
            "summary": g["summary"],
            "paper_ids": ",".join(sorted(g["paper_ids"]-{""})),
            "n_paper_ids": len(g["paper_ids"]-{""}),
            "sources": ",".join(sorted(g["sources"])),
            "n_sources": len(g["sources"]),
            "queries": ",".join(sorted(g["queries"])),
            "n_queries": len(g["queries"]),
        })
print(f"Wrote {OUT}")

# PRISMA flow counts
with open(COUNTS,"w") as f:
    multi_mapped = sum(1 for g in merged if len(g["paper_ids"]-{""}) > 1)
    by_n_sources = {}
    for g in merged:
        ns = len(g["sources"])
        by_n_sources[ns] = by_n_sources.get(ns,0)+1
    json.dump({
        "raw_per_source": per_source_counts,
        "raw_total_rows": len(all_rows),
        "after_url_canonicalize": len(groups),
        "after_fuzzy_merge": len(merged),
        "multi_mapped_articles": multi_mapped,
        "by_n_sources": by_n_sources,
        "papers_with_news_coverage": len(set().union(*[g["paper_ids"]-{""} for g in merged])),
    }, f, indent=2)
print(f"Wrote {COUNTS}")
