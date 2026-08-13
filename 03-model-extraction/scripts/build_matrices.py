"""
Generate HTML matrix snippets for each paper's results table in 3L-models.html.

Reads paper_XXX.json files in this directory, computes a derived Cohen's d
for every cell (using effect_sizes.to_d), and writes the matrix table HTML
to ./out/<paper_id>__<model_id>.html.

Run from this directory:
    python3 build_matrices.py

The output snippets are designed to be pasted in as-is, replacing the
existing <table class="matrix"> ... </table> blocks in 3L-models.html.
"""

import json
import os
import sys

from effect_sizes import to_d


def _smart_decimals(*vals):
    """Use 3 decimals if any value would round to 0.00 at 2 decimals, else 2."""
    return 3 if any(abs(round(v, 2)) < 0.005 for v in vals) else 2


def fmt_b(x):
    return f"{x:.{_smart_decimals(x)}f}"


def fmt_b_ci(lo, hi):
    p = _smart_decimals(lo, hi)
    return f"[{lo:.{p}f}, {hi:.{p}f}]"


def _norm_zero(x, places):
    """Round and zero-out negative-zero artifacts so we don't display '-0.000'."""
    r = round(x, places)
    return 0.0 if r == 0 else r


def fmt_d_main(d):
    return f"{_norm_zero(d, 3):.3f}"


def fmt_d_ci(lo, hi):
    return f"[{_norm_zero(lo, 3):.3f}, {_norm_zero(hi, 3):.3f}]"


def fmt_p(est):
    p = est.get("p")
    if p is None:
        return None
    if p < 0.001:
        return "p &lt; .001"
    s = f"{p:.3f}"  # "0.005", "0.080", "0.231"
    return f"p = {s[1:]}"  # strip leading "0" -> ".005", ".080", ".231"


def build_native_html(est, native_metric):
    """Inner HTML for the 'native metric' line of a cell."""
    if native_metric == "B":
        b = f'<span class="b">B = {fmt_b(est["B"])}</span>'
        ci = f'<span class="ci">{fmt_b_ci(est["B_lo"], est["B_hi"])}</span>'
        p = fmt_p(est)
        p_html = f'<span class="p">{p}</span>' if p else ""
        return b + ci + p_html
    if native_metric == "d":
        b = f'<span class="b">d = {est["d"]:.2f}</span>'
        p = "p &lt; .001" if est.get("sig") else None
        p_html = f'<span class="p">{p}</span>' if p else ""
        return b + p_html
    if native_metric == "RR":
        b = f'<span class="b">RR = {est["RR"]:.2f}</span>'
        p = "p &lt; .001" if est.get("sig") else "p &ge; .001"
        return b + f'<span class="p">{p}</span>'
    raise ValueError(f"Unknown native_metric: {native_metric}")


def build_derived_html(d_out, native_metric):
    """Inner HTML for the 'derived d' line of a cell. None if native already is d."""
    if native_metric == "d":
        return None  # no separate derived line; native IS d
    main = f'<span class="d-val">d &asymp; {fmt_d_main(d_out["d"])}</span>'
    if "d_lo" in d_out and "d_hi" in d_out:
        ci = f'<span class="d-ci">{fmt_d_ci(d_out["d_lo"], d_out["d_hi"])}</span>'
        return main + ci
    return main


def build_estimate_lookup(model):
    return {(e["iv"], e["dv"]): e for e in model["estimates"]}


def build_input_spec(est, iv_meta, dv_meta, native_metric):
    """Translate a paper-data estimate into an effect_sizes.to_d() spec."""
    if native_metric == "B":
        return {
            "kind": "linear_continuous",
            "B": est["B"], "B_lo": est["B_lo"], "B_hi": est["B_hi"],
            "sd_iv": iv_meta["sd_iv"], "sd_dv": dv_meta["sd_dv"],
        }
    if native_metric == "d":
        return {"kind": "d_passthrough", "d": est["d"]}
    if native_metric == "RR":
        return {"kind": "rr", "RR": est["RR"], "p0": dv_meta["p0"]}
    raise ValueError(f"Unknown native_metric: {native_metric}")


def build_table(model, paper_id, compact=False):
    iv_axis = model["iv_axis"]
    dv_axis = model["dv_axis"]
    native_metric = model["native_metric"]
    lookup = build_estimate_lookup(model)
    iv_meta_lookup = {iv["id"]: iv for iv in iv_axis}
    dv_meta_lookup = {dv["id"]: dv for dv in dv_axis}

    cls = "matrix compact" if compact else "matrix"
    out = [f'<table class="{cls}">']

    # Header row
    out.append("  <thead><tr>")
    out.append("    <th></th>")
    for dv in dv_axis:
        out.append(f'    <th class="col-head">{dv["label"]}</th>')
    out.append("  </tr></thead>")

    # Body rows
    out.append("  <tbody>")
    for iv in iv_axis:
        out.append("    <tr>")
        meta_html = (
            f'<div class="iv-meta">{iv["meta"]}</div>' if "meta" in iv else ""
        )
        out.append(f'      <td class="row-head">{iv["label"]}{meta_html}</td>')
        for dv in dv_axis:
            est = lookup.get((iv["id"], dv["id"]))
            if est is None:
                out.append('      <td class="cell">—</td>')
                continue
            spec = build_input_spec(est, iv_meta_lookup[iv["id"]], dv_meta_lookup[dv["id"]], native_metric)
            d_out = to_d(spec)
            sig_class = " sig" if est.get("sig") else ""
            native_html = build_native_html(est, native_metric)
            derived_html = build_derived_html(d_out, native_metric)
            cell_inner = f'<div class="native">{native_html}</div>'
            if derived_html is not None:
                cell_inner += f'<div class="derived">{derived_html}</div>'
            out.append(f'      <td class="cell{sig_class}">{cell_inner}</td>')
        out.append("    </tr>")
    out.append("  </tbody>")
    out.append("</table>")
    return "\n".join(out)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(here, "out")
    os.makedirs(out_dir, exist_ok=True)

    json_files = sorted(
        f for f in os.listdir(here) if f.startswith("paper_") and f.endswith(".json")
    )
    if not json_files:
        print("No paper_*.json files found", file=sys.stderr)
        sys.exit(1)

    for fname in json_files:
        with open(os.path.join(here, fname)) as fh:
            paper = json.load(fh)
        for model in paper["models"]:
            # paper 156 has more DVs than 394, mark it compact
            compact = len(model["dv_axis"]) >= 5
            html = build_table(model, paper["paper_id"], compact=compact)
            out_path = os.path.join(
                out_dir, f"paper_{paper['paper_id']}__{model['model_id']}.html"
            )
            with open(out_path, "w") as oh:
                oh.write(html + "\n")
            n = len(model["estimates"])
            print(f"  paper {paper['paper_id']} {model['model_id']}: {n} cells -> {out_path}")

    print("\nDone.")


if __name__ == "__main__":
    main()
