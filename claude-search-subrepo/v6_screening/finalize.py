"""
Build the final 2L-scoring.csv (and slim INCLUDE / EXCLUDE / UNSURE / NA-FOR-NOW CSVs).

For each of the 171 Stage-1 includes:
  - C1 status per criterion (with evidence)
  - C2 status per criterion (blinded; with evidence)
  - Resolver status per criterion (only on disagreed criteria)
  - FINAL status per criterion = resolver if exists else C1==C2 else UNKNOWN
  - FINAL paper-level decision via algorithmic aggregation:
      INCLUDE      = all FT_IC1..FT_IC6 == MET AND FT_EC7_applies != TRUE
      EXCLUDE      = any FT_IC1..FT_IC6 == NOT_MET, OR FT_EC7_applies == TRUE
                     → FT_EC code based on first failure (FT_IC1→FT-EC1, IC2→FT-EC2,
                       IC3→FT-EC4, IC4→FT-EC4, IC5→FT-EC3, IC6→FT-EC5, EC7→FT-EC7)
      UNSURE       = at least one criterion UNKNOWN with PDF available
      NA_FOR_NOW   = at least one criterion UNKNOWN with no PDF
"""
import json, os, glob, csv

V5 = "/Users/dannyzweben/Desktop/ABCD-smartphon-socialmedia-review/claude-search-subrepo/v6_screening"
L2 = "/Users/dannyzweben/Desktop/ABCD-smartphon-socialmedia-review/02-L2"
CRITERIA = ["FT_IC1","FT_IC5","FT_IC6","FT_IC2","FT_IC3","FT_IC4","FT_EC7_applies"]
DEFER = {"NOT_REACHED","NOT_APPLICABLE","N/A","NA","NOT-EVALUATED","NOT_EVALUATED"}

def load_records(pattern):
    out = {}
    for f in sorted(glob.glob(os.path.join(V5,pattern))):
        if any(s in os.path.basename(f) for s in ["c1_all","c2_all"]): continue
        try: d = json.load(open(f))
        except: continue
        if isinstance(d, dict) and "paper_id" in d: d=[d]
        if not isinstance(d, list): continue
        for rec in d:
            pid = str(rec.get("paper_id"))
            if pid not in out: out[pid] = rec
    return out

def status(rec, crit):
    if rec is None: return "MISSING"
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
    s = (s or "UNKNOWN").upper()
    if s in DEFER: return "DEFERRED"
    return s

def evidence(rec, crit):
    if crit == "FT_EC7_applies":
        return rec.get("FT_EC7_reason","") if rec else ""
    cell = rec.get(crit) if rec else None
    if isinstance(cell, dict): return cell.get("evidence","")
    return ""

def load_resolver():
    """resolver[pid][crit] = {status, evidence, binding_rules_cited, rationale}"""
    out = {}
    for f in sorted(glob.glob(os.path.join(V5,"r_*.json"))):
        try: d = json.load(open(f))
        except Exception as e:
            print(f"ERR {f}: {e}"); continue
        if isinstance(d, dict): d=[d]
        for rec in d:
            pid = str(rec.get("paper_id"))
            decisions = rec.get("resolver_decisions",[])
            out.setdefault(pid,{})
            for dec in decisions:
                crit = dec.get("crit")
                s = dec.get("status")
                if crit == "FT_EC7_applies":
                    if s is True or str(s).lower()=="true": s = "TRUE"
                    elif s is False or str(s).lower()=="false": s = "FALSE"
                    else: s = str(s).upper() if s else "UNKNOWN"
                else:
                    s = (str(s) or "UNKNOWN").upper()
                    if s in DEFER: s = "UNKNOWN"
                out[pid][crit] = {
                    "status": s,
                    "evidence": dec.get("evidence",""),
                    "binding_rules_cited": dec.get("binding_rules_cited",[]),
                    "rationale": dec.get("rationale","")
                }
    return out

def load_papers_meta():
    meta = {}
    for f in sorted(glob.glob(os.path.join(V5,"batches","batch_*.json"))):
        for p in json.load(open(f)):
            meta[str(p.get("paper_id"))] = p
    return meta

# Code map: which FT-EC code to attach to each criterion failure
EC_CODE = {
    "FT_IC1": "FT-EC1",
    "FT_IC5": "FT-EC3",
    "FT_IC6": "FT-EC6",
    "FT_IC2": "FT-EC2",
    "FT_IC3": "FT-EC4",
    "FT_IC4": "FT-EC4",
    "FT_EC7_applies": "FT-EC7",
}

def aggregate_paper(c1, c2, res, has_pdf):
    """Return (final_per_crit, paper_decision, ec_code, reason)."""
    final = {}
    any_unknown = False
    first_fail = None
    for crit in CRITERIA:
        if res and crit in res:
            s = res[crit]["status"]
        else:
            s1 = status(c1, crit); s2 = status(c2, crit)
            # If either is DEFERRED, use the other
            if s1 == "DEFERRED" and s2 != "DEFERRED": s = s2
            elif s2 == "DEFERRED" and s1 != "DEFERRED": s = s1
            elif s1 == s2: s = s1
            else: s = "UNKNOWN"  # conflict not resolved (shouldn't happen)
        final[crit] = s
        # Determine if this is a fail
        is_fail = False
        if crit == "FT_EC7_applies":
            if s == "TRUE": is_fail = True
        else:
            if s == "NOT_MET": is_fail = True
        if is_fail and first_fail is None:
            first_fail = crit
        if s == "UNKNOWN":
            any_unknown = True

    if first_fail:
        return final, "EXCLUDE", EC_CODE[first_fail], f"{first_fail} = {final[first_fail]}"
    if any_unknown:
        if has_pdf:
            return final, "UNSURE", "", "at least one criterion UNKNOWN with PDF"
        else:
            return final, "NA_FOR_NOW", "", "at least one criterion UNKNOWN with no PDF"
    return final, "INCLUDE", "", "all criteria MET; FT-EC7 not applicable"

def main():
    c1 = load_records("c1_*.json")
    c2 = load_records("c2_*.json")
    res = load_resolver()
    meta = load_papers_meta()

    pids = sorted(meta, key=lambda x: int(x) if x.isdigit() else 999999)
    print(f"Total Stage-1 includes: {len(pids)}")

    rows = []
    counts = {"INCLUDE":0,"EXCLUDE":0,"UNSURE":0,"NA_FOR_NOW":0}
    ec_counts = {}
    for pid in pids:
        m = meta[pid]
        c1r = c1.get(pid); c2r = c2.get(pid); rr = res.get(pid)
        has_pdf = bool(m.get("has_pdf"))
        final, decision, ec, reason = aggregate_paper(c1r, c2r, rr, has_pdf)
        counts[decision]+=1
        if decision=="EXCLUDE":
            ec_counts[ec] = ec_counts.get(ec,0)+1
        row = {
            "paper_id": pid,
            "title": m.get("title",""),
            "authors": m.get("authors",""),
            "year": m.get("year",""),
            "doi": m.get("doi",""),
            "has_pdf": has_pdf,
            "FINAL_decision": decision,
            "FINAL_EC_code": ec,
            "FINAL_reason": reason,
        }
        for crit in CRITERIA:
            row[f"{crit}_C1"] = status(c1r, crit)
            row[f"{crit}_C2"] = status(c2r, crit)
            row[f"{crit}_Resolver"] = (res[pid][crit]["status"] if (rr and crit in rr) else "")
            row[f"{crit}_FINAL"] = final[crit]
            row[f"{crit}_C1_evidence"] = evidence(c1r, crit)
            row[f"{crit}_C2_evidence"] = evidence(c2r, crit)
            row[f"{crit}_Resolver_rationale"] = (res[pid][crit]["rationale"] if (rr and crit in rr) else "")
        rows.append(row)

    # Write 2L-scoring.csv
    fieldnames = ["paper_id","title","authors","year","doi","has_pdf",
                  "FINAL_decision","FINAL_EC_code","FINAL_reason"]
    for crit in CRITERIA:
        fieldnames += [f"{crit}_C1",f"{crit}_C2",f"{crit}_Resolver",f"{crit}_FINAL",
                       f"{crit}_C1_evidence",f"{crit}_C2_evidence",f"{crit}_Resolver_rationale"]
    out_csv = os.path.join(L2,"2L-scoring.csv")
    with open(out_csv,"w",newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in rows: w.writerow(r)
    print(f"Wrote {out_csv}")

    # Slim CSVs
    slim_fields_inc = ["paper_id","title","authors","year","doi","FINAL_reason"]
    slim_fields_exc = ["paper_id","title","authors","year","doi","FINAL_EC_code","FINAL_reason"]
    slim_fields_uns = ["paper_id","title","authors","year","doi","has_pdf","FINAL_reason"]

    def write_slim(rows, fn, fields):
        with open(os.path.join(L2,fn),"w",newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            w.writeheader()
            for r in rows: w.writerow(r)

    write_slim([r for r in rows if r["FINAL_decision"]=="INCLUDE"], "2L-INCLUDE.csv", slim_fields_inc)
    write_slim([r for r in rows if r["FINAL_decision"]=="EXCLUDE"], "2L-EXCLUDE.csv", slim_fields_exc)
    write_slim([r for r in rows if r["FINAL_decision"]=="UNSURE"], "2L-UNSURE.csv", slim_fields_uns)
    write_slim([r for r in rows if r["FINAL_decision"]=="NA_FOR_NOW"], "2L-NA-FOR-NOW.csv", slim_fields_uns)

    # Summary print
    print("\n=== Final v5 PRISMA flow ===")
    print(f"INCLUDE      : {counts['INCLUDE']}")
    print(f"EXCLUDE      : {counts['EXCLUDE']}")
    for ec,n in sorted(ec_counts.items()):
        print(f"   {ec}: {n}")
    print(f"UNSURE (PDF): {counts['UNSURE']}")
    print(f"NA_FOR_NOW  : {counts['NA_FOR_NOW']}")
    print(f"TOTAL       : {sum(counts.values())}")

    # Persist summary
    json.dump({
        "counts": counts,
        "exclusion_codes": ec_counts,
        "n_total_stage1": len(pids),
        "n_with_resolver": len(res),
    }, open(os.path.join(V5,"final_summary.json"),"w"), indent=2)

if __name__=="__main__":
    main()
