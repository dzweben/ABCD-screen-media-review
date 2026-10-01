"""C1 vs C2 inter-rater agreement for N1 linkage screening."""
import csv, json, os
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
c1 = {r["article_id"]: r for r in csv.DictReader(open(os.path.join(ROOT,"N1-scoring_c1.csv")))}
c2 = {r["article_id"]: r for r in csv.DictReader(open(os.path.join(ROOT,"N1-scoring_c2.csv")))}

common = sorted(set(c1) & set(c2))
print(f"Articles scored by both: {len(common)}")

# Decision-level agreement (INCLUDE vs EXCLUDE)
agree_dec = 0
disagree_dec = []
for aid in common:
    d1 = c1[aid]["n1_decision"]
    d2 = c2[aid]["n1_decision"]
    if d1 == d2:
        agree_dec += 1
    else:
        disagree_dec.append((aid, d1, d2))

# Cohen's kappa for INCLUDE/EXCLUDE
def kappa(a, b):
    n = len(a)
    po = sum(1 for x,y in zip(a,b) if x==y)/n
    ca = Counter(a); cb = Counter(b)
    pe = sum((ca[k]/n)*(cb[k]/n) for k in set(a)|set(b))
    return (po - pe) / (1 - pe) if pe < 1 else 1.0

c1_decs = [c1[a]["n1_decision"] for a in common]
c2_decs = [c2[a]["n1_decision"] for a in common]
k = kappa(c1_decs, c2_decs)

print(f"\n=== INCLUDE/EXCLUDE agreement ===")
print(f"  Agree: {agree_dec}/{len(common)} = {100*agree_dec/len(common):.1f}%")
print(f"  Disagree: {len(disagree_dec)}")
print(f"  Cohen's κ: {k:.3f}")
print(f"\n  Confusion matrix:")
mat = Counter()
for aid in common:
    mat[(c1[aid]["n1_decision"], c2[aid]["n1_decision"])] += 1
labels = sorted(set(c1_decs) | set(c2_decs))
print(f"            C2: {'  '.join(labels)}")
for r in labels:
    row = [f"{mat[(r,c)]:>7}" for c in labels]
    print(f"   C1: {r:<10s} {' '.join(row)}")

# Paper-id matching agreement (among articles BOTH coders INCLUDED)
both_inc = [a for a in common if c1[a]["n1_decision"]=="INCLUDE" and c2[a]["n1_decision"]=="INCLUDE"]
exact_pid = 0
overlap_pid = 0
disjoint_pid = 0
disjoint_examples = []
for aid in both_inc:
    p1 = set(p for p in c1[aid]["matched_paper_ids"].split(",") if p)
    p2 = set(p for p in c2[aid]["matched_paper_ids"].split(",") if p)
    if p1 == p2:
        exact_pid += 1
    elif p1 & p2:
        overlap_pid += 1
    else:
        disjoint_pid += 1
        disjoint_examples.append((aid, sorted(p1), sorted(p2)))

print(f"\n=== Paper-id matching among both-INCLUDE articles ===")
print(f"  Both INCLUDE: {len(both_inc)}")
print(f"    exact paper-id match:  {exact_pid} ({100*exact_pid/len(both_inc):.1f}%)")
print(f"    overlap (≥1 shared):   {overlap_pid} ({100*overlap_pid/len(both_inc):.1f}%)")
print(f"    disjoint (no overlap): {disjoint_pid} ({100*disjoint_pid/len(both_inc):.1f}%)")

# Save disagreements for resolution
out = []
for aid, d1, d2 in disagree_dec:
    out.append({
        "article_id": aid,
        "url": c1[aid]["url"],
        "outlet": c1[aid]["outlet"],
        "title": c1[aid]["title"],
        "c1_decision": d1, "c2_decision": d2,
        "c1_paper_ids": c1[aid]["matched_paper_ids"],
        "c2_paper_ids": c2[aid]["matched_paper_ids"],
        "c1_test": c1[aid]["linkage_test"], "c2_test": c2[aid]["linkage_test"],
        "c1_conf": c1[aid]["confidence"], "c2_conf": c2[aid]["confidence"],
        "c1_reason_or_evidence": c1[aid]["exclusion_reason"] or c1[aid]["evidence"],
        "c2_reason_or_evidence": c2[aid]["exclusion_reason"] or c2[aid]["evidence"],
        "type": "include_exclude_disagreement"
    })

# Also save paper-id disagreements among both-INCLUDE
for aid, p1, p2 in disjoint_examples:
    out.append({
        "article_id": aid,
        "url": c1[aid]["url"],
        "outlet": c1[aid]["outlet"],
        "title": c1[aid]["title"],
        "c1_decision": "INCLUDE", "c2_decision": "INCLUDE",
        "c1_paper_ids": ",".join(p1), "c2_paper_ids": ",".join(p2),
        "c1_test": c1[aid]["linkage_test"], "c2_test": c2[aid]["linkage_test"],
        "c1_conf": c1[aid]["confidence"], "c2_conf": c2[aid]["confidence"],
        "c1_reason_or_evidence": c1[aid]["evidence"],
        "c2_reason_or_evidence": c2[aid]["evidence"],
        "type": "paper_id_disjoint"
    })

with open(os.path.join(ROOT,"N1-disagreements.csv"),"w",newline="") as f:
    fields = ["article_id","outlet","title","c1_decision","c2_decision",
              "c1_paper_ids","c2_paper_ids","c1_test","c2_test","c1_conf","c2_conf",
              "c1_reason_or_evidence","c2_reason_or_evidence","type","url"]
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for r in out: w.writerow(r)

print(f"\nWrote N1-disagreements.csv: {len(out)} rows")
print(f"  include/exclude disagreements: {len(disagree_dec)}")
print(f"  paper-id disjoint among both-INCLUDE: {len(disjoint_examples)}")
print(f"  total needing resolution: {len(out)}")
