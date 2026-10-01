"""
Aggregate the 30 N1 batch outputs into a single N1-scoring.csv.

Reads:
  N1/results/n1_results_batch_*.json

Outputs:
  N1/N1-scoring.csv     — one row per article: article_id, decision, paper_ids,
                          linkage_test, confidence, evidence
  N1/N1-summary.json    — totals + flagged-for-review list

PRISMA flow numbers it produces:
  - candidates_screened     (input from news_deduplicated.csv)
  - included_after_n1
  - excluded_after_n1 + reason breakdown
  - flagged_for_human_review (confidence < 0.7)
  - multi_mapped_articles
  - papers_with_news_coverage_after_n1
"""
import json, glob, csv, os, sys
from collections import Counter

CODER = sys.argv[1] if len(sys.argv) > 1 else "c1"   # c1 | c2
ROOT = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(ROOT, f"results_{CODER}")
ARTICLES = os.path.join(ROOT, "articles.json")
OUT_CSV = os.path.join(ROOT, f"N1-scoring_{CODER}.csv")
SUMMARY = os.path.join(ROOT, f"N1-summary_{CODER}.json")

articles = {a["article_id"]: a for a in json.load(open(ARTICLES))}

# Load all batch results
all_results = {}
batch_files = sorted(glob.glob(os.path.join(RESULTS, "n1_results_batch_*.json")))
print(f"Loading {len(batch_files)} batch result files")
for bf in batch_files:
    try:
        d = json.load(open(bf))
        if isinstance(d, dict): d = [d]
        for r in d:
            aid = r.get("article_id")
            if aid: all_results[aid] = r
    except Exception as e:
        print(f"  ERR {bf}: {e}")

print(f"Articles with N1 result: {len(all_results)} / {len(articles)}")

# Build CSV
rows = []
for aid, art in articles.items():
    res = all_results.get(aid)
    if not res:
        rows.append({
            "article_id": aid,
            "url": art["url"],
            "outlet": art["outlet"],
            "title": art["title"],
            "summary": (art.get("summary","") or "")[:300],
            "published_date": art.get("published_date",""),
            "n1_decision": "NOT_SCORED",
            "matched_paper_ids": "",
            "linkage_test": "",
            "confidence": "",
            "exclusion_reason": "no result",
            "evidence": "",
            "provisional_paper_ids": ",".join(art.get("provisional_paper_ids",[])),
        })
        continue
    rows.append({
        "article_id": aid,
        "url": art["url"],
        "outlet": art["outlet"],
        "title": art["title"],
        "summary": (art.get("summary","") or "")[:300],
        "published_date": art.get("published_date",""),
        "n1_decision": "EXCLUDE" if res.get("excluded") else "INCLUDE",
        "matched_paper_ids": ",".join(map(str, res.get("matched_paper_ids", []))),
        "linkage_test": res.get("linkage_test", ""),
        "confidence": res.get("confidence", ""),
        "exclusion_reason": res.get("exclusion_reason", "") if res.get("excluded") else "",
        "evidence": res.get("evidence", ""),
        "provisional_paper_ids": ",".join(art.get("provisional_paper_ids",[])),
    })

fields = ["article_id","outlet","title","url","published_date",
          "n1_decision","matched_paper_ids","linkage_test","confidence",
          "exclusion_reason","evidence","provisional_paper_ids","summary"]
with open(OUT_CSV, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for r in rows: w.writerow(r)
print(f"\nWrote {OUT_CSV}: {len(rows)} rows")

# Summary stats
included = [r for r in rows if r["n1_decision"]=="INCLUDE"]
excluded = [r for r in rows if r["n1_decision"]=="EXCLUDE"]
not_scored = [r for r in rows if r["n1_decision"]=="NOT_SCORED"]
flagged = [r for r in included if r["confidence"] and float(r["confidence"])<0.7]
multi = [r for r in included if r["matched_paper_ids"] and "," in r["matched_paper_ids"]]
exc_reasons = Counter(r["exclusion_reason"] for r in excluded)

# Papers with coverage
paper_coverage = Counter()
for r in included:
    for pid in r["matched_paper_ids"].split(","):
        if pid: paper_coverage[pid] += 1

summary = {
    "total_articles": len(rows),
    "included_after_n1": len(included),
    "excluded_after_n1": len(excluded),
    "not_scored": len(not_scored),
    "flagged_for_human_review": len(flagged),
    "multi_mapped": len(multi),
    "papers_with_coverage": len(paper_coverage),
    "exclusion_reasons": dict(exc_reasons.most_common()),
    "papers_top10": dict(paper_coverage.most_common(10)),
}
with open(SUMMARY, "w") as f:
    json.dump(summary, f, indent=2)
print(f"Wrote {SUMMARY}")

print(f"\n=== N1 PRISMA flow ===")
print(f"  candidate articles screened: {len(rows)}")
print(f"  → INCLUDE: {len(included)}")
print(f"  → EXCLUDE: {len(excluded)}")
print(f"  → NOT_SCORED: {len(not_scored)}")
print(f"  flagged for human review (conf<0.7): {len(flagged)}")
print(f"  multi-mapped (>1 paper): {len(multi)}")
print(f"  papers with ≥1 confirmed news article: {len(paper_coverage)} / 69")
print(f"\nTop exclusion reasons:")
for reason, n in exc_reasons.most_common(8):
    print(f"  {n:>3} | {reason[:80]}")
