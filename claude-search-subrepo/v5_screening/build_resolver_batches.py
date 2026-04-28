"""Build resolver batches from disagreements + C1/C2 evidence + paper PDF/abstract paths.
Each resolver batch contains a single paper with the specific disagreed criteria + both coder
positions and evidence strings. The resolver agent re-reads the PDF (if any) and decides
each disagreed criterion independently.
"""
import json, os, glob

V5 = "/Users/dannyzweben/Desktop/ABCD-smartphon-socialmedia-review/claude-search-subrepo/v5_screening"
RES_DIR = os.path.join(V5, "resolver_batches")
os.makedirs(RES_DIR, exist_ok=True)

c1 = json.load(open(os.path.join(V5,"c1_all.json")))
c2 = json.load(open(os.path.join(V5,"c2_all.json")))
dis = json.load(open(os.path.join(V5,"disagreements.json")))

# Build paper_id -> {pdf_path, has_pdf, title, ...} from original batches
papers_meta = {}
for f in sorted(glob.glob(os.path.join(V5,"batches","batch_*.json"))):
    for p in json.load(open(f)):
        papers_meta[str(p.get("paper_id"))] = p

def get_evidence(rec, crit):
    if crit == "FT_EC7_applies":
        return rec.get("FT_EC7_reason","")
    cell = rec.get(crit)
    if isinstance(cell, dict):
        return cell.get("evidence","")
    return ""

n=0
batches_per_file = 3   # bundle 3 disagreement papers per resolver batch
buf = []
for d in dis:
    pid = d["paper_id"]
    meta = papers_meta.get(pid, {})
    item = {
        "paper_id": pid,
        "title": meta.get("title",""),
        "authors": meta.get("authors",""),
        "year": meta.get("year",""),
        "doi": meta.get("doi",""),
        "abstract": meta.get("abstract",""),
        "pdf_path": meta.get("pdf_path",""),
        "has_pdf": meta.get("has_pdf", False),
        "disagreed_criteria": [
            {
                "crit": c["crit"],
                "c1_status": c["c1"],
                "c1_evidence": get_evidence(c1[pid], c["crit"]),
                "c2_status": c["c2"],
                "c2_evidence": get_evidence(c2[pid], c["crit"]),
            } for c in d["criteria"]
        ]
    }
    buf.append(item)
    if len(buf)>=batches_per_file:
        json.dump(buf, open(os.path.join(RES_DIR, f"batch_{n}.json"),"w"), indent=2)
        n+=1; buf=[]
if buf:
    json.dump(buf, open(os.path.join(RES_DIR, f"batch_{n}.json"),"w"), indent=2)
    n+=1

print(f"Wrote {n} resolver batches across {len(dis)} disagreement papers")
