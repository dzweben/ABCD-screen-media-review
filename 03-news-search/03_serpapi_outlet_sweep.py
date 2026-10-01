"""
Layer S-O: Outlet-anchored sweep.

For each of N major news outlets, run a single SerpAPI Google search:

    site:{outlet} ("Adolescent Brain Cognitive Development" OR "ABCD Study")

Date range: 2018-01-01 to present. ABCD started yielding publications in ~2018,
so this captures the full historical span of mainstream coverage.

Rationale: news articles often do not name the lead author or paper title,
or do not co-occur all of {author, topic, ABCD} within search distance.
An outlet-anchored sweep catches every article in target outlets that
mentions ABCD by name, regardless of how the journalist framed authorship.
Papers are then linked back at the N1 stage based on article content.

Outputs:
  raw/serpapi_outlets_results.csv
  raw/serpapi_outlets_log.json
"""
import os, json, csv, time, urllib.request, urllib.parse, urllib.error
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT_CSV = os.path.join(ROOT, "raw/serpapi_outlets_results.csv")
LOG = os.path.join(ROOT, "raw/serpapi_outlets_log.json")

API_KEY = os.environ.get("SERPAPI_KEY")
if not API_KEY:
    raise SystemExit("Set SERPAPI_KEY")

# Tier-1 mainstream outlets (high-priority capture)
OUTLETS = [
    # General news
    "nytimes.com", "washingtonpost.com", "npr.org", "wsj.com",
    "nbcnews.com", "cbsnews.com", "abcnews.go.com", "cnn.com",
    "reuters.com", "apnews.com", "bloomberg.com", "usatoday.com",
    # Magazines / opinion
    "theatlantic.com", "wired.com", "vox.com", "time.com",
    "newsweek.com", "theguardian.com", "bbc.com", "bbc.co.uk",
    # Specialty health press
    "medpagetoday.com", "medscape.com", "sciencealert.com",
    "scientificamerican.com", "livescience.com", "healthday.com",
    "psychologytoday.com",
    # Tech / news
    "theverge.com", "axios.com", "businessinsider.com",
    # Public broadcasting + science press
    "pbs.org", "statnews.com", "kffhealthnews.org",
    # Local/regional with national reach
    "latimes.com", "chicagotribune.com",
]

QUERY_TEMPLATE = '("Adolescent Brain Cognitive Development" OR "ABCD Study")'
log = {"start": datetime.utcnow().isoformat()+"Z", "calls": [], "errors": []}
rows = []

for i, outlet in enumerate(OUTLETS, 1):
    q = f'site:{outlet} {QUERY_TEMPLATE}'
    params = {
        "engine":"google",
        "q": q,
        "gl":"us","hl":"en","num":100,
        "tbs":"cdr:1,cd_min:01/01/2018,cd_max:12/31/2026",
        "api_key": API_KEY,
    }
    url = "https://serpapi.com/search.json?" + urllib.parse.urlencode(params)
    retrieved = datetime.utcnow().isoformat() + "Z"
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"abcd-news-review/1.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read())
        organics = data.get("organic_results", [])
        for n in organics:
            rows.append({
                "paper_id": "",  # to be filled at N1 linkage
                "doi": "",
                "source": "serpapi_outlet_sweep",
                "query_id": "S-O",
                "query": q,
                "outlet": outlet,
                "url": n.get("link",""),
                "title": n.get("title","") or "",
                "summary": (n.get("snippet","") or "")[:1000],
                "published_date": n.get("date",""),
                "retrieved_on": retrieved,
            })
        log["calls"].append({"outlet": outlet, "n_results": len(organics), "retrieved_on": retrieved})
        print(f"[{i}/{len(OUTLETS)}] {outlet}: {len(organics)} hits")
    except urllib.error.HTTPError as e:
        log["errors"].append({"outlet": outlet, "error": f"HTTP {e.code}", "retrieved_on": retrieved})
        print(f"[{i}/{len(OUTLETS)}] {outlet}: HTTP {e.code}")
    except Exception as e:
        log["errors"].append({"outlet": outlet, "error": str(e), "retrieved_on": retrieved})
        print(f"[{i}/{len(OUTLETS)}] {outlet}: {e}")
    time.sleep(0.4)

log["end"] = datetime.utcnow().isoformat() + "Z"
log["total_calls"] = len(log["calls"])
log["total_results"] = len(rows)

with open(OUT_CSV, "w", newline="") as f:
    fields = ["paper_id","doi","source","query_id","query","outlet","url","title","summary","published_date","retrieved_on"]
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for r in rows: w.writerow(r)
with open(LOG, "w") as f:
    json.dump(log, f, indent=2)

print(f"\n=== Outlet sweep summary ===")
print(f"  outlets queried: {len(OUTLETS)}")
print(f"  total results: {len(rows)}")
print(f"  errors: {len(log['errors'])}")
print(f"  CSV: {OUT_CSV}")
