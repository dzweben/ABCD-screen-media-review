"""
Validate per-paper draft extractions and attach derived Cohen's d to every estimate.

Reads   docs/data/drafts/paper_<id>.json   (written by the extraction agents)
Writes  docs/data/ingested/paper_<id>.json (same object + d / d_lo / d_hi / d_method per estimate)
Prints  a validation report.

Duplicates in the INCLUDE set (same paper, two IDs) are mirrored from the canonical id.

Run from repo root:  python3 docs/scripts/ingest_drafts.py
"""

import glob
import json
import math
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "03-model-extraction", "scripts"))
from effect_sizes import to_d  # noqa: E402

DRAFTS = os.path.join(REPO, "docs", "data", "drafts")
OUT = os.path.join(REPO, "docs", "data", "ingested")
DUPLICATES = {"393": "394", "436": "435"}

REQUIRED_TOP = ["paper_id", "title", "doi", "primary_models", "excluded_models", "d_transformation"]
REQUIRED_MODEL = ["model_id", "name", "location_in_paper", "design", "sample", "iv", "dv",
                  "covariates", "equation", "estimation", "native_metric", "iv_axis", "dv_axis", "estimates"]


def spec_for(est, metric, iv_meta, dv_meta):
    """Translate one estimate into an effect_sizes.to_d spec, or (None, reason)."""
    m = (metric or "").strip()
    if m == "B":
        if est.get("B") is None:
            return None, "B missing"
        sd_iv = est.get("sd_iv") or iv_meta.get("sd_iv")
        sd_dv = est.get("sd_dv") or dv_meta.get("sd_dv")
        if not sd_iv or not sd_dv:
            return None, "SD_IV or SD_DV not reported"
        s = {"kind": "linear_continuous", "B": est["B"], "sd_iv": sd_iv, "sd_dv": sd_dv}
        if est.get("B_lo") is not None and est.get("B_hi") is not None:
            s.update(B_lo=est["B_lo"], B_hi=est["B_hi"])
        return s, None
    if m == "beta_std":
        if est.get("beta") is None:
            return None, "beta missing"
        s = {"kind": "standardized_beta", "beta": est["beta"]}
        if est.get("beta_lo") is not None and est.get("beta_hi") is not None:
            s.update(beta_lo=est["beta_lo"], beta_hi=est["beta_hi"])
        return s, None
    if m == "OR":
        if not est.get("OR"):
            return None, "OR missing"
        s = {"kind": "or", "OR": est["OR"]}
        if est.get("OR_lo") and est.get("OR_hi"):
            s.update(OR_lo=est["OR_lo"], OR_hi=est["OR_hi"])
        return s, None
    if m == "RR":
        if not est.get("RR"):
            return None, "RR missing"
        p0 = est.get("p0") or dv_meta.get("p0")
        if not p0:
            return None, "p0 (baseline rate) not reported"
        s = {"kind": "rr", "RR": est["RR"], "p0": p0}
        if est.get("RR_lo") and est.get("RR_hi"):
            s.update(RR_lo=est["RR_lo"], RR_hi=est["RR_hi"])
        return s, None
    if m == "IRR":
        if not est.get("IRR"):
            return None, "IRR missing"
        s = {"kind": "irr", "IRR": est["IRR"]}
        if est.get("IRR_lo") and est.get("IRR_hi"):
            s.update(IRR_lo=est["IRR_lo"], IRR_hi=est["IRR_hi"])
        return s, None
    if m == "d":
        if est.get("d") is None:
            return None, "d missing"
        return {"kind": "d_passthrough", "d": est["d"]}, None
    if m == "r":
        if est.get("r") is None:
            return None, "r missing"
        s = {"kind": "r", "r": est["r"]}
        if est.get("r_lo") is not None and est.get("r_hi") is not None:
            s.update(r_lo=est["r_lo"], r_hi=est["r_hi"])
        return s, None
    # 'other:' metrics with a legitimate closed-form conversion
    v, lo, hi = est.get("value"), est.get("value_lo"), est.get("value_hi")
    has_ci = lo is not None and hi is not None
    if m == "other:standardized_beta_x100":
        if v is None:
            return None, "value missing"
        s = {"kind": "standardized_beta", "beta": v / 100}
        if has_ci:
            s.update(beta_lo=lo / 100, beta_hi=hi / 100)
        return s, None
    if m in ("other:logit_B", "other:ordered_logit_coefficient"):
        # coefficient is a log-odds ratio: OR = exp(b), then Chinn
        if v is None:
            return None, "value missing"
        s = {"kind": "or", "OR": math.exp(v)}
        if has_ci:
            s.update(OR_lo=math.exp(lo), OR_hi=math.exp(hi))
        return s, None
    if m == "other:PR":
        # prevalence ratio: same algebra as RR
        if not v:
            return None, "value missing"
        p0 = est.get("p0") or dv_meta.get("p0")
        if not p0:
            return None, "p0 (baseline rate) not reported"
        s = {"kind": "rr", "RR": v, "p0": p0}
        if has_ci:
            s.update(RR_lo=lo, RR_hi=hi)
        return s, None
    return None, f"no Cohen's d conversion for '{m}' (flagged for later review level)"


def process(paper):
    issues = []
    for k in REQUIRED_TOP:
        if k not in paper:
            issues.append(f"missing top-level '{k}'")
    n_est = n_d = 0
    for mi, model in enumerate(paper.get("primary_models") or []):
        for k in REQUIRED_MODEL:
            if k not in model:
                issues.append(f"M{mi+1}: missing '{k}'")
        ivs = {x.get("id"): x for x in model.get("iv_axis") or []}
        dvs = {x.get("id"): x for x in model.get("dv_axis") or []}
        for est in model.get("estimates") or []:
            n_est += 1
            if est.get("iv") not in ivs:
                issues.append(f"M{mi+1}: estimate iv '{est.get('iv')}' not in iv_axis")
            if est.get("dv") not in dvs:
                issues.append(f"M{mi+1}: estimate dv '{est.get('dv')}' not in dv_axis")
            if model.get("d_kind") == "beta_is_y_standardized_group_difference" and est.get("beta") is not None:
                spec, why = {"kind": "d_passthrough", "d": est["beta"]}, None
            else:
                spec, why = spec_for(est, model.get("native_metric"), ivs.get(est.get("iv"), {}), dvs.get(est.get("dv"), {}))
            for k in ("d", "d_lo", "d_hi") if model.get("native_metric") != "d" else ():
                est.pop("derived_" + k, None)
            if spec is None:
                est["derived_d"] = None
                est["derived_d_method"] = why
                continue
            try:
                out = to_d(spec)
                est["derived_d"] = round(out["d"], 4)
                est["derived_d_lo"] = round(out["d_lo"], 4) if "d_lo" in out else None
                est["derived_d_hi"] = round(out["d_hi"], 4) if "d_hi" in out else None
                est["derived_d_method"] = out["method"]
                n_d += 1
            except Exception as e:  # bad inputs (e.g. |r|>=1, RR*p0>=1)
                est["derived_d"] = None
                est["derived_d_method"] = f"conversion failed: {e}"
                issues.append(f"M{mi+1} {est.get('iv')}x{est.get('dv')}: {e}")
    # Link any supplement files saved next to the PDF as <doi>_supplement*.*
    stem = (paper.get("doi") or "").strip().replace("/", "_")
    pdf_dir = os.path.join(REPO, "docs", "pdfs")
    paper["supplements"] = sorted(
        "pdfs/" + f for f in os.listdir(pdf_dir) if stem and f.startswith(stem + "_supplement")
    )
    paper.setdefault("extraction_status", "ai_draft")
    paper.setdefault("lead_coder", "danny")
    paper.setdefault("contributors", ["danny"])
    paper["last_edited_by"] = "danny"
    return n_est, n_d, issues


def main():
    os.makedirs(OUT, exist_ok=True)
    files = sorted(glob.glob(os.path.join(DRAFTS, "paper_*.json")))
    total_est = total_d = 0
    bad = []
    by_id = {}
    for f in files:
        try:
            paper = json.load(open(f))
        except Exception as e:
            bad.append((os.path.basename(f), f"invalid JSON: {e}"))
            continue
        pid = str(paper.get("paper_id"))
        n_est, n_d, issues = process(paper)
        total_est += n_est
        total_d += n_d
        by_id[pid] = paper
        json.dump(paper, open(os.path.join(OUT, f"paper_{pid}.json"), "w"), indent=1)
        flag = "OK " if not issues else "!! "
        print(f"{flag}#{pid:>4}  models={len(paper.get('primary_models') or []):>2}  est={n_est:>3}  d={n_d:>3}"
              + (f"  issues: {'; '.join(issues[:4])}" if issues else ""))
    # Duplicates
    for dup, canon in DUPLICATES.items():
        if canon in by_id:
            p = json.loads(json.dumps(by_id[canon]))
            p["paper_id"] = dup
            p["duplicate_of"] = canon
            json.dump(p, open(os.path.join(OUT, f"paper_{dup}.json"), "w"), indent=1)
            print(f"DUP #{dup} mirrored from #{canon}")
    print(f"\n{len(files)} drafts, {total_est} estimates, {total_d} with derived d")
    for b in bad:
        print("BAD", *b)


if __name__ == "__main__":
    main()
