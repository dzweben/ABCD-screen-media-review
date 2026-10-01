"""
Layer C: SerpAPI Google News + Google site-search across all 72 INCLUDE papers.

Reads queries from `papers_manifest.json` (generated deterministically from each
paper's metadata; see search-terms-platforms.md for construction rule).

Outputs:
  raw/serpapi_results.csv     — every result row with full provenance
  raw/serpapi_search_log.json — every API call (status, # results, timestamp)

Reproducibility: each row carries `paper_id`, `query_id`, `query`, `engine`, and
`retrieved_on`, sufficient for any researcher to re-run the exact query.
"""
import os, json, csv, time, urllib.request, urllib.parse, urllib.error
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(ROOT, "papers_manifest.json")
OUT_CSV = os.path.join(ROOT, "raw/serpapi_results.csv")
LOG = os.path.join(ROOT, "raw/serpapi_search_log.json")

API_KEY = os.environ.get("SERPAPI_KEY")
if not API_KEY:
    raise SystemExit("Set SERPAPI_KEY (e.g. `source .secrets/api_keys.env`)")

papers = json.load(open(MANIFEST))
log = {"start": datetime.utcnow().isoformat()+"Z", "calls": [], "errors": []}
rows = []

def call_serpapi(params):
    url = "https://serpapi.com/search.json?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent":"abcd-news-review/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())

def parse_news(data):
    out = []
    for n in data.get("news_results", []):
        src = n.get("source", {})
        if isinstance(src, dict): src = src.get("name", "")
        out.append({
            "outlet": src,
            "url": n.get("link",""),
            "title": n.get("title","") or "",
            "summary": (n.get("snippet","") or n.get("description","") or "")[:1000],
            "published_date": n.get("date","")
        })
    return out

def parse_organic(data):
    out = []
    for n in data.get("organic_results", []):
        out.append({
            "outlet": n.get("displayed_link", n.get("source","")),
            "url": n.get("link",""),
            "title": n.get("title","") or "",
            "summary": (n.get("snippet","") or "")[:1000],
            "published_date": n.get("date","")
        })
    return out

n_calls = 0
for i, p in enumerate(papers, 1):
    pid = p["paper_id"]
    queries = p.get("queries", [])
    if not queries:
        print(f"[{i}/{len(papers)}] paper {pid}: no queries (skipping)")
        continue
    paper_n_results = 0
    for q in queries:
        params = {k:v for k,v in q.items() if k != "id"}
        params["api_key"] = API_KEY
        retrieved = datetime.utcnow().isoformat() + "Z"
        try:
            data = call_serpapi(params)
            n_calls += 1
            if q["engine"] == "google_news":
                results = parse_news(data)
            else:
                results = parse_organic(data)
            for r in results:
                rows.append({
                    "paper_id": pid,
                    "doi": p["doi"],
                    "source": "serpapi_" + q["engine"],
                    "query_id": q["id"],
                    "query": q["q"],
                    "outlet": r["outlet"],
                    "url": r["url"],
                    "title": r["title"],
                    "summary": r["summary"],
                    "published_date": r["published_date"],
                    "retrieved_on": retrieved,
                })
            paper_n_results += len(results)
            log["calls"].append({
                "paper_id": pid, "query_id": q["id"], "q": q["q"],
                "engine": q["engine"], "n_results": len(results),
                "retrieved_on": retrieved
            })
        except urllib.error.HTTPError as e:
            log["errors"].append({"paper_id": pid, "query_id": q["id"], "error": f"HTTP {e.code}", "retrieved_on": retrieved})
            print(f"  [{i}/{len(papers)}] {pid}/{q['id']}: HTTP {e.code}")
        except Exception as e:
            log["errors"].append({"paper_id": pid, "query_id": q["id"], "error": str(e), "retrieved_on": retrieved})
            print(f"  [{i}/{len(papers)}] {pid}/{q['id']}: {e}")
        time.sleep(0.4)  # polite pacing
    print(f"[{i}/{len(papers)}] paper {pid}: {paper_n_results} results from {len(queries)} queries (calls used: {n_calls})")

log["end"] = datetime.utcnow().isoformat() + "Z"
log["total_calls"] = n_calls
log["total_results"] = len(rows)
log["papers_with_hits"] = len(set(r["paper_id"] for r in rows))

with open(OUT_CSV, "w", newline="") as f:
    fields = ["paper_id","doi","source","query_id","query","outlet","url","title","summary","published_date","retrieved_on"]
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for r in rows: w.writerow(r)
with open(LOG, "w") as f:
    json.dump(log, f, indent=2)

print(f"\n=== summary ===")
print(f"  API calls: {n_calls}")
print(f"  result rows: {len(rows)}")
print(f"  papers with ≥1 hit: {log['papers_with_hits']}/{len(papers)}")
print(f"  errors: {len(log['errors'])}")
print(f"  CSV: {OUT_CSV}")
print(f"  log: {LOG}")
