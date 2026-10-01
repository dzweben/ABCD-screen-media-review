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
from statistics import NormalDist
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


def spec_for(est, metric, iv_meta, dv_meta, iv_type=None):
    """Translate one estimate into an effect_sizes.to_d spec, or (None, reason)."""
    m = (metric or "").strip()
    if m == "B" and iv_type in ("binary", "categorical"):
        # B is an adjusted group mean difference vs the reference group: d = B / SD_DV
        if est.get("B") is None:
            return None, "B missing"
        sd_dv = est.get("sd_dv") or dv_meta.get("sd_dv")
        if not sd_dv:
            return None, "SD_DV not reported (group-contrast IV, so SD_IV not needed)"
        s = {"kind": "group_diff", "B": est["B"], "sd_dv": sd_dv}
        if est.get("B_lo") is not None and est.get("B_hi") is not None:
            s.update(B_lo=est["B_lo"], B_hi=est["B_hi"])
        return s, None
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
    if m in ("other:F(1,df)", "F1"):
        F, df = est.get("value"), est.get("df")
        if F is None or not df:
            return None, "F or its error df not reported"
        return {"kind": "F1", "F": F, "df": df, "sign": est.get("sign") or 1}, None
    if m in ("other:chi2", "chi2_1"):
        X, N = est.get("value"), est.get("n")
        if X is None or not N or (est.get("chi2_df") not in (None, 1)):
            return None, "χ² needs 1 df and its N to convert"
        return {"kind": "chi2_1", "chi2": X, "N": N, "sign": est.get("sign") or 1}, None
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


CHINN = math.sqrt(3) / math.pi


def g(x, n=4):
    """Compact number formatting for worked calculations."""
    return f"{x:.{n}g}" if abs(x) < 1e-3 and x != 0 else f"{round(x, n):g}"


def sq(x):
    return f"({g(x)})²" if x < 0 else f"{g(x)}²"


def worked(spec, metric, est):
    """Return (formula, worked calculation) strings for one conversion."""
    k = spec["kind"]
    if k == "d_passthrough":
        if metric == "d":
            return "d reported by the paper", f"d = {g(spec['d'])} (no conversion)"
        return ("d = β (β is a Y-standardized mean difference for a binary IV)",
                f"d = β = {g(spec['d'])}")
    if k == "group_diff":
        B, b = spec["B"], spec["sd_dv"]
        return ("d = B / SD_DV  (B = adjusted mean difference vs reference group)",
                f"d = {g(B)} / {g(b)} = {g(B / b)}")
    if k == "F1":
        F, df = spec["F"], spec["df"]
        r = math.sqrt(F / (F + df))
        d = 2 * r / math.sqrt(1 - r ** 2)
        return ("r = √(F / (F + df_error));  d = 2r / √(1 − r²)  (F with 1 numerator df)",
                f"r = √({g(F)} / ({g(F)} + {g(df)})) = {g(r)};  d = 2({g(r)}) / √(1 − {sq(r)}) = {g(d)}")
    if k == "chi2_1":
        X, N = spec["chi2"], spec["N"]
        r = math.sqrt(X / N)
        d = 2 * r / math.sqrt(1 - r ** 2)
        return ("r = √(χ² / N);  d = 2r / √(1 − r²)  (χ² with 1 df; sign from direction of effect)",
                f"r = √({g(X)} / {g(N)}) = {g(r)};  d = 2({g(r)}) / √(1 − {sq(r)}) = {g(d)}")
    if k == "linear_continuous":
        B, a, b = spec["B"], spec["sd_iv"], spec["sd_dv"]
        beta = B * a / b
        d = 2 * beta / math.sqrt(1 - beta ** 2)
        return ("β_std = B × SD_IV / SD_DV;  d = 2β_std / √(1 − β_std²)",
                f"β_std = {g(B)} × {g(a)} / {g(b)} = {g(beta)};  d = 2({g(beta)}) / √(1 − {sq(beta)}) = {g(d)}")
    if k in ("standardized_beta", "r"):
        r = spec["beta"] if k == "standardized_beta" else spec["r"]
        d = 2 * r / math.sqrt(1 - r ** 2)
        sym = "β" if k == "standardized_beta" else "r"
        pre = ""
        if metric == "other:standardized_beta_x100":
            pre = f"β = {g(est.get('value'))} / 100 = {g(r)};  "
        return (f"d = 2{sym} / √(1 − {sym}²)" + ("  (β reported ×100 by the paper)" if pre else ""),
                pre + f"d = 2({g(r)}) / √(1 − {sq(r)}) = {g(d)}")
    if k in ("or", "irr"):
        OR = spec["OR"] if k == "or" else spec["IRR"]
        d = math.log(OR) * CHINN
        name = "IRR (treated as OR)" if k == "irr" else "OR"
        pre = ""
        if metric in ("other:logit_B", "other:ordered_logit_coefficient"):
            pre = f"OR = e^b = e^{g(est.get('value'))} = {g(OR)};  "
            return ("OR = e^b;  d = ln(OR) × √3/π  (Chinn 2000)",
                    pre + f"d = {g(est.get('value'))} × 0.5513 = {g(d)}")
        return (f"d = ln({name}) × √3/π  (Chinn 2000)",
                f"d = ln({g(OR)}) × 0.5513 = {g(math.log(OR))} × 0.5513 = {g(d)}")
    if k == "rr":
        RR, p0 = spec["RR"], spec["p0"]
        OR = RR * (1 - p0) / (1 - RR * p0)
        d = math.log(OR) * CHINN
        lab = "PR" if metric == "other:PR" else "RR"
        return (f"OR = {lab}(1 − p0) / (1 − {lab}·p0);  d = ln(OR) × √3/π  (Chinn 2000)",
                f"OR = {g(RR)}(1 − {g(p0)}) / (1 − {g(RR)}×{g(p0)}) = {g(OR)};  d = ln({g(OR)}) × 0.5513 = {g(d)}")
    return "", ""


RATIO = {"OR", "RR", "IRR", "other:PR", "other:ratio_of_means"}
# Metrics where a Wald CI from SE / exact p is valid
WALD_OK = {"B", "beta_std", "OR", "RR", "IRR", "d", "other:PR", "other:ratio_of_means", "other:logit_B",
           "other:ordered_logit_coefficient", "other:standardized_beta_x100"}
NATIVE_KEY = {"B": "B", "beta_std": "beta", "OR": "OR", "RR": "RR", "IRR": "IRR", "d": "d", "r": "r"}


def fill_ci(est, metric):
    """Fill a missing 95% CI on the native estimate from what the paper prints.

    Order: (1) printed SE -> estimate ± 1.96·SE (log scale for ratios);
           (2) exact p -> z = Φ⁻¹(1 − p/2), SE = |θ|/z (Altman & Bland 2011);
           (3) Cohen's d with group sizes -> SE(d) = √((n1+n0)/(n1·n0) + d²/(2(n1+n0))).
    Records how the CI was obtained in est["ci_source"]. Never overwrites a printed CI.
    """
    if metric not in WALD_OK:
        return
    k = NATIVE_KEY.get(metric, "value")
    v = est.get(k)
    if v is None or (est.get(k + "_lo") is not None and est.get(k + "_hi") is not None):
        return
    ratio = metric in RATIO or est.get("se_scale") == "log"
    if ratio and v <= 0:
        return
    theta = math.log(v) if ratio else v
    se = est.get("se")
    src = None
    if isinstance(se, (int, float)) and se > 0:
        src = "computed: estimate ± 1.96 × SE" + (" (log scale)" if ratio else "")
    elif isinstance(est.get("t") or est.get("z"), (int, float)) and (est.get("t") or est.get("z")) != 0 and theta != 0:
        stat = est.get("t") or est.get("z")
        se = abs(theta) / abs(stat)
        src = f"computed: SE = |estimate| / |{'t' if est.get('t') else 'z'}| = {abs(theta):.4g} / {abs(stat):.4g}" + (" (log scale)" if ratio else "")
    elif metric == "d" and est.get("n1") and est.get("n0"):
        n1, n0 = est["n1"], est["n0"]
        se = math.sqrt((n1 + n0) / (n1 * n0) + v ** 2 / (2 * (n1 + n0)))
        src = f"computed: SE(d) from group sizes n1={n1}, n0={n0}"
    else:
        p = est.get("p")
        lab = str(est.get("p_label") or "")
        exact = isinstance(p, (int, float)) and 0 < p < 1 and not lab.strip().startswith(("<", ">", "≤", "≥"))
        if exact and theta != 0:
            z = NormalDist().inv_cdf(1 - p / 2)
            if z > 0:
                se = abs(theta) / z
                src = f"computed from exact p = {p} (Altman & Bland 2011)" + (" on log scale" if ratio else "")
    if not src:
        return
    lo, hi = theta - 1.959964 * se, theta + 1.959964 * se
    if ratio:
        lo, hi = math.exp(lo), math.exp(hi)
    est[k + "_lo"], est[k + "_hi"] = round(lo, 4), round(hi, 4)
    est["ci_source"] = src


def consistency(est, metric):
    """Flag internally inconsistent numbers (likely extraction errors)."""
    k = NATIVE_KEY.get(metric, "value")
    v, lo, hi = est.get(k), est.get(k + "_lo"), est.get(k + "_hi")
    flags = []
    if None not in (v, lo, hi) and not est.get("ci_source"):
        if lo > hi:
            flags.append("CI lower bound > upper bound")
        elif not (lo - 1e-9 <= v <= hi + 1e-9):
            flags.append("estimate lies outside its own CI")
        p, lab = est.get("p"), str(est.get("p_label") or "")
        if metric in WALD_OK and isinstance(p, (int, float)) and 0 < p < 1 and not lab.strip().startswith("<"):
            ratio = metric in RATIO
            if (not ratio or (v > 0 and lo > 0 and hi > 0)):
                th = math.log(v) if ratio else v
                w = (math.log(hi) - math.log(lo)) if ratio else (hi - lo)
                z = NormalDist().inv_cdf(1 - p / 2)
                if th != 0 and w > 0 and z > 0:
                    implied = 2 * 1.959964 * abs(th) / z
                    if abs(implied - w) / w > 0.5:
                        flags.append(f"p = {p} implies a CI width of {implied:.3g}, printed width is {w:.3g}")
        excl = (1 if metric in RATIO else 0)
        crosses = lo < excl < hi
        if est.get("sig") is True and crosses:
            flags.append("marked significant but CI includes the null")
    if flags:
        est["consistency_flags"] = flags
    else:
        est.pop("consistency_flags", None)


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
            consistency(est, model.get("native_metric"))
            if not est.get("ci_source"):
                fill_ci(est, model.get("native_metric"))
            if est.get("iv") not in ivs:
                issues.append(f"M{mi+1}: estimate iv '{est.get('iv')}' not in iv_axis")
            if est.get("dv") not in dvs:
                issues.append(f"M{mi+1}: estimate dv '{est.get('dv')}' not in dv_axis")
            if model.get("d_kind") == "beta_is_y_standardized_group_difference" and est.get("beta") is not None:
                spec, why = {"kind": "d_passthrough", "d": est["beta"]}, None
            else:
                spec, why = spec_for(est, model.get("native_metric"), ivs.get(est.get("iv"), {}), dvs.get(est.get("dv"), {}),
                                     iv_type=model.get("iv_type"))
            for k in ("d", "d_lo", "d_hi") if model.get("native_metric") != "d" else ():
                est.pop("derived_" + k, None)
            est.pop("derived_d_formula", None)
            est.pop("derived_d_calc", None)
            if spec is None:
                est["derived_d"] = None
                est["derived_d_method"] = why
                continue
            try:
                out = to_d(spec)
                est["derived_d_formula"], est["derived_d_calc"] = worked(spec, model.get("native_metric"), est)
                if spec.get("kind") in ("F1", "chi2_1") and est.get("sign") is None:
                    est["derived_d_calc"] += "  (direction not reported: sign assumed positive, treat as |d|)"
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
