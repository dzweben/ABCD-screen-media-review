"""
Aggregate v5 C1 + C2 atomic screenings, compute disagreements and Cohen's kappa.

Status normalization:
  Maps NOT_REACHED / NOT_APPLICABLE / N/A / NA / NOT-EVALUATED to "DEFERRED"
  (occurs when one coder stops scoring after a NOT_MET; the later criteria
  shouldn't count as disagreements against the other coder's substantive value).

True disagreement:
  Both coders gave a substantive status (MET / NOT_MET / UNKNOWN) AND they differ.
  DEFERRED on either side is not a disagreement (we use the substantive value).
"""
import json, os, glob
from collections import Counter

V5 = "/Users/dannyzweben/Desktop/ABCD-smartphon-socialmedia-review/claude-search-subrepo/v6_screening"
CRITERIA = ["FT_IC1","FT_IC2","FT_IC3","FT_IC4","FT_IC5","FT_IC6","FT_EC7_applies"]
DEFER = {"NOT_REACHED","NOT_APPLICABLE","N/A","NA","NOT-EVALUATED","NOT_EVALUATED"}

def load_records(pattern):
    out = {}
    for f in sorted(glob.glob(os.path.join(V5, pattern))):
        # skip aggregated files
        if f.endswith("c1_all.json") or f.endswith("c2_all.json"): continue
        try:
            d = json.load(open(f))
        except Exception as e:
            print(f"ERR {f}: {e}"); continue
        if isinstance(d, dict) and "paper_id" in d: d=[d]
        if not isinstance(d, list): continue
        for rec in d:
            pid = str(rec.get("paper_id"))
            if pid in out: continue
            out[pid] = rec
    return out

def status(rec, crit):
    if crit == "FT_EC7_applies":
        v = rec.get("FT_EC7_applies")
        if v is True: return "TRUE"
        if v is False: return "FALSE"
        if isinstance(v, str): return v.upper()
        return "UNKNOWN"
    cell = rec.get(crit)
    if isinstance(cell, dict):
        s = cell.get("status","UNKNOWN")
    elif isinstance(cell, str):
        s = cell
    else:
        s = "UNKNOWN"
    s = s.upper()
    if s in DEFER: return "DEFERRED"
    return s

def cohens_kappa(c1_list, c2_list):
    n = len(c1_list)
    if n==0: return None
    cats = sorted(set(c1_list)|set(c2_list))
    obs = sum(1 for a,b in zip(c1_list,c2_list) if a==b)/n
    p1 = Counter(c1_list); p2 = Counter(c2_list)
    exp = sum((p1[c]/n)*(p2[c]/n) for c in cats)
    if exp==1: return 1.0
    return (obs-exp)/(1-exp)

def main():
    c1 = load_records("c1_*.json")
    c2 = load_records("c2_*.json")
    print(f"C1: {len(c1)} unique papers; C2: {len(c2)} unique papers")
    json.dump(c1, open(os.path.join(V5,"c1_all.json"),"w"), indent=2)
    json.dump(c2, open(os.path.join(V5,"c2_all.json"),"w"), indent=2)

    common = sorted(set(c1)&set(c2), key=lambda x: int(x) if x.isdigit() else 999999)
    only_c1 = sorted(set(c1)-set(c2))
    only_c2 = sorted(set(c2)-set(c1))
    print(f"Common: {len(common)}; only_c1: {len(only_c1)}; only_c2: {len(only_c2)}")

    by_crit_inc_def = {}    # including DEFERRED
    by_crit_eff = {}        # excluding DEFERRED on either side
    disagreements = []
    for pid in common:
        crits_disagreed = []
        for crit in CRITERIA:
            s1 = status(c1[pid], crit)
            s2 = status(c2[pid], crit)
            by_crit_inc_def.setdefault(crit,([],[]))
            by_crit_inc_def[crit][0].append(s1); by_crit_inc_def[crit][1].append(s2)
            if s1=="DEFERRED" or s2=="DEFERRED":
                continue  # not a true disagreement
            by_crit_eff.setdefault(crit,([],[]))
            by_crit_eff[crit][0].append(s1); by_crit_eff[crit][1].append(s2)
            if s1 != s2:
                crits_disagreed.append({"crit":crit,"c1":s1,"c2":s2})
        if crits_disagreed:
            disagreements.append({"paper_id":pid,"criteria":crits_disagreed})

    kappas = {}
    for crit,(l1,l2) in by_crit_eff.items():
        kappas[crit] = {
            "n_substantive": len(l1),
            "agree": sum(1 for a,b in zip(l1,l2) if a==b),
            "kappa": cohens_kappa(l1,l2)
        }

    pooled1=[]; pooled2=[]
    for crit,(l1,l2) in by_crit_eff.items():
        pooled1+=l1; pooled2+=l2
    pooled_kappa = cohens_kappa(pooled1,pooled2)
    pooled_agree = sum(1 for a,b in zip(pooled1,pooled2) if a==b)/len(pooled1) if pooled1 else 0

    n_papers = len(common)
    n_disagree_papers = len(disagreements)
    summary = {
        "n_common_papers": n_papers,
        "n_papers_with_any_true_disagreement": n_disagree_papers,
        "n_papers_full_agreement_substantive": n_papers - n_disagree_papers,
        "pct_papers_full_agreement": round(100*(n_papers-n_disagree_papers)/n_papers,2) if n_papers else 0,
        "pooled_substantive_pct_agreement": round(100*pooled_agree,2),
        "pooled_substantive_kappa": round(pooled_kappa,3) if pooled_kappa is not None else None,
        "per_criterion_substantive": {k:{**v,"kappa":round(v["kappa"],3) if v["kappa"] is not None else None,
                                         "pct_agree":round(100*v["agree"]/v["n_substantive"],2) if v["n_substantive"] else 0}
                                      for k,v in kappas.items()},
        "only_c1": only_c1, "only_c2": only_c2,
    }
    json.dump(disagreements, open(os.path.join(V5,"disagreements.json"),"w"), indent=2)
    json.dump(summary, open(os.path.join(V5,"agreement_summary.json"),"w"), indent=2)
    print(json.dumps(summary, indent=2))

if __name__=="__main__":
    main()
