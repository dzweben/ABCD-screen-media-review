"""
Audit the 52 disagreement papers to identify ROOT-CAUSE criteria gaps.
For every disagreement, extract:
  - which criterion
  - what each coder said (status + evidence + binding rules cited)
  - what type of judgment call drove the split

Then cluster by pattern and surface the gaps so we can write tighter rules
(rather than escalating to a resolver).
"""
import json, os
from collections import Counter, defaultdict

V5 = "/Users/dannyzweben/Desktop/ABCD-smartphon-socialmedia-review/claude-search-subrepo/v5_screening"

c1 = json.load(open(os.path.join(V5,"c1_all.json")))
c2 = json.load(open(os.path.join(V5,"c2_all.json")))
dis = json.load(open(os.path.join(V5,"disagreements.json")))

import glob
papers = {}
for f in sorted(glob.glob(os.path.join(V5,"batches","batch_*.json"))):
    for p in json.load(open(f)):
        papers[str(p.get("paper_id"))] = p

def evidence(rec, crit):
    if crit == "FT_EC7_applies":
        return rec.get("FT_EC7_reason","")
    cell = rec.get(crit)
    if isinstance(cell, dict):
        return cell.get("evidence","")
    return ""

def rules(rec):
    return rec.get("binding_rules_applied",[]) if rec else []

# Group disagreements by criterion
by_crit = defaultdict(list)
for d in dis:
    pid = d["paper_id"]
    title = papers.get(pid,{}).get("title","")[:80]
    for c in d["criteria"]:
        by_crit[c["crit"]].append({
            "pid": pid,
            "title": title,
            "c1": c["c1"],
            "c2": c["c2"],
            "c1_evidence": evidence(c1[pid], c["crit"]),
            "c2_evidence": evidence(c2[pid], c["crit"]),
            "c1_rules": rules(c1[pid]),
            "c2_rules": rules(c2[pid]),
        })

print(f"=== Disagreement counts by criterion ===")
for crit, items in sorted(by_crit.items(), key=lambda x: -len(x[1])):
    print(f"  {crit}: {len(items)} disagreements")

# Output detailed dump for analysis
out = {crit: items for crit, items in by_crit.items()}
json.dump(out, open(os.path.join(V5,"disagreement_audit.json"),"w"), indent=2)
print(f"\nWrote {os.path.join(V5,'disagreement_audit.json')}")
