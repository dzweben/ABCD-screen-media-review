"""
Build docs/data/papers-seed.json from:
  - 02-L2/2L-scoring.csv           (69 INCLUDE papers)
  - 03-model-extraction/scripts/paper_394.json + paper_156.json  (extracted data)

Every paper gets a stub. Papers 394 and 156 get their full extracted structure.

Run from repo root:  python3 docs/scripts/build_seed.py
"""

import csv
import json
import os
import sys
from datetime import datetime

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_include_papers():
    path = os.path.join(REPO, "02-L2", "2L-scoring.csv")
    with open(path, "r", encoding="utf-8-sig") as f:
        return [r for r in csv.DictReader(f) if r["C1_decision"] == "INCLUDE"]


def load_extracted(paper_id):
    """Load a paper_<id>.json extraction (from scripts/ pipeline)."""
    path = os.path.join(REPO, "03-model-extraction", "scripts", f"paper_{paper_id}.json")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def stub_paper(row):
    """Empty stub for a paper we haven't extracted yet."""
    return {
        "paper_id": row["paper_id"],
        "title": row["title"].strip().rstrip("."),
        "doi": row["doi"].strip(),
        "year": row["year"].strip(),
        "authors": "",
        "journal": "",
        "extraction_status": "empty",
        "d_transformable": None,
        "lead_coder": None,
        "contributors": [],
        "last_updated": None,
        "primary_models": [],
        "excluded_models": [],
        "d_transformation": {
            "native_metric": "",
            "conversion_formula": "",
            "contrast_type": "",
            "transformable": None,
            "notes": "",
        },
        "coder_log": [],
    }


def paper_394():
    ext = load_extracted("394")
    if not ext:
        return None
    model = ext["models"][0]
    p = {
        "paper_id": "394",
        "title": "Screen time and mental health: a prospective analysis of the Adolescent Brain Cognitive Development (ABCD) Study",
        "doi": "10.1186/s12889-024-20102-x",
        "year": "2024",
        "authors": "Nagata JM, Al-Shoaibi AAA, Leong AW, Zamora G, Testa A, Ganson KT, Baker FC",
        "journal": "BMC Public Health",
        "extraction_status": "human_reviewed",
        "d_transformable": True,
        "lead_coder": "danny",
        "contributors": ["danny"],
        "last_updated": "2026-05-08T00:00:00Z",
        "primary_models": [{
            "model_id": "M1",
            "name": "Mixed-effects linear regression of CBCL DSM-oriented symptom t-scores on baseline phone/SM modalities",
            "location_in_paper": "Table 2, fully adjusted Model 2 (pp 5-7); discussion pp 8-9. Sensitivity analyses in Appendix B.",
            "design": "Prospective longitudinal cohort with repeated outcome measurement. Baseline phone/SM exposure (and baseline CBCL t-score for the DV scale) predicts follow-up CBCL at Y1 and Y2 (2018-2020, overlapping COVID). Both follow-up scores enter long-format as separate rows; the model treats them as repeated measures. No wave-by-IV interaction, so beta_1 pools across the two-year follow-up window.",
            "sample": "ABCD Release 4.0. Baseline 2016-2018, 21 U.S. sites. N=9,538 with complete data on baseline screen time, baseline covariates, and Y1+Y2 CBCL. Excluded N=2,337 (19.7%) for missing data. Same N for all 18 IV x DV estimates. Mean age 9.9 (SD 0.6); 48.8% female; 52.4% NH White, 20.1% Latino, 17.3% NH Black, 5.5% NH Asian, 3.2% Native American, 1.5% Other.",
            "iv": "Baseline phone/SM hours per day, one modality per estimate (texting, video chat, social media). ABCD Youth Screen Time Survey, weighted daily hours = (weekday x 5 + weekend x 2) / 7. Baseline distribution (M +/- SD): texting 0.2 +/- 0.6; video chat 0.3 +/- 0.7; social media 0.1 +/- 0.1 h/day. Floor effects: most 9-10 year olds are below the 13+ min age for major SM platforms.",
            "dv": "CBCL DSM-oriented t-score, parent-report, repeated measures Y1 and Y2. Six scales run separately: depressive, anxiety, somatic, ADHD, ODD, conduct. Raw scores -> t-scores (mean 50, SD 10 by construction). Baseline (Y0) t-score on the same scale enters as covariate.",
            "covariates": [
                {"name": "Baseline value of outcome scale", "detail": "Autoregressive; beta_1 becomes association with change-style follow-up net of baseline symptoms"},
                {"name": "Age", "detail": "Years at baseline (continuous)"},
                {"name": "Sex", "detail": "Binary female/male"},
                {"name": "Race/ethnicity", "detail": "5 categories; NH White reference; 4 dummies"},
                {"name": "Household income", "detail": "6 brackets <$25K to >=$200K; 5 dummies"},
                {"name": "Parent education", "detail": "Binary HS-or-less vs. college+"},
                {"name": "COVID period", "detail": "Binary pre/during (March 13, 2020 cutoff)"},
                {"name": "Study site", "detail": "Random intercept (21 sites)"}
            ],
            "equation": "CBCL_DV[i,wave] = b0 + b1*phoneSM_IV[i] + b2*CBCL_baseline[i] + b3*age + b4*sex + b5..b8*race + b9..b13*income + b14*parent_ed + b15*covid_period + u_site(i) + e[i,wave]",
            "estimation": "Software: Stata 18.0 mixed procedure. Estimation: maximum likelihood. Weights: ACS propensity weights (nationwide-representative). Random intercept for study site. alpha = 0.05. Multiple-comparison correction: NONE reported (with 18 tests, ~1 false positive expected). Sex interactions all p > 0.05. Race/ethnicity interactions significant for some outcomes but stratified estimates in Table 3 are total-screen-time only. Sensitivity in Appendix B refits adding sleep and physical activity; per-modality numbers not printed.",
            "native_metric": "B",
            "iv_axis": model["iv_axis"],
            "dv_axis": model["dv_axis"],
            "estimates": model["estimates"],
        }],
        "excluded_models": [
            {"model": "Model 1 (unadjusted)", "location": "Table 2 left columns", "why": "Reported for transparency to demonstrate covariate-driven attenuation; the paper anchors no claim to it. Adds no new information about the phone/SM-trait relationship."},
            {"model": "Race-stratified Model 2", "location": "Table 3", "why": "Reports stratified estimates for total screen time only, not per modality. No phone/SM-specific stratified estimates exist."},
            {"model": "Sensitivity adding sleep + physical activity", "location": "Appendix B", "why": "Per-modality estimates were not printed."},
            {"model": "Interaction tests", "location": "In-text", "why": "Tests of whether the slope differs across subgroups; produce interaction p-values, not new phone/SM estimates."}
        ],
        "d_transformation": {
            "native_metric": "B (unstandardized)",
            "conversion_formula": "beta_std = B * SD_IV / SD_DV; d = 2 * beta_std / sqrt(1 - beta_std^2) (Borenstein et al. 2009 eq 7.1)",
            "contrast_type": "per 1-SD change in the IV",
            "transformable": True,
            "notes": "SD_DV = 10 by construction (CBCL t-score is normed mean=50 SD=10). SD_IV per modality is reported in Table 1 (texting 0.6; video chat 0.7; social media 0.1). Not directly comparable to per-1-SD d's from papers using a different contrast (e.g., paper 156's high vs. low group difference)."
        },
        "coder_log": [
            {"timestamp": "2026-05-08T00:00:00Z", "coder": "danny", "change": "Initial extraction. Model 1 unadjusted excluded per §2 guideline (paper anchors claims to Model 2)."}
        ]
    }
    return p


def paper_156():
    ext = load_extracted("156")
    if not ext:
        return None
    m1 = ext["models"][0]
    m2 = ext["models"][1]
    p = {
        "paper_id": "156",
        "title": "Screen media use and sleep disturbance symptom severity in children",
        "doi": "10.1016/j.sleh.2020.07.002",
        "year": "2020",
        "authors": "Hisler GC, Hasler BP, Franzen PL, Clark DB, Twenge JM",
        "journal": "Sleep Health",
        "extraction_status": "human_reviewed",
        "d_transformable": True,
        "lead_coder": "danny",
        "contributors": ["danny"],
        "last_updated": "2026-05-09T00:00:00Z",
        "primary_models": [
            {
                "model_id": "M1",
                "name": "Linear regression of continuous sleep DVs on dichotomized phone/SM use (Cohen's d effect size)",
                "location_in_paper": "Tables 2 (weekday IVs) and 3 (weekend IVs). Pre-registered on OSF (deviation: IVs dichotomized post-hoc due to skew).",
                "design": "Cross-sectional analysis of a single ABCD timepoint (baseline, Release 2.0). Both IV and DVs measured at same visit. One observation per child. Pre-registered hypotheses H1-H7; IVs were pre-registered as continuous but data skew forced dichotomization at the AAP <2 vs >=2 hr threshold.",
                "sample": "ABCD Release 2.0 baseline (2016-2018), 21 U.S. sites. Analytic N varies 10,666-10,676 across cells (listwise). >=2 hr groups small (1.5-3.8% of sample): weekday texting 2.8%; weekend texting 3.8%; weekday SM 1.5%; weekend SM 2.2%; weekday video chat 2.1%; weekend video chat 3.2%. Mean age 9.91 (SD 0.62); 52% female; 53% White, 20% Hispanic/Latinx, 18% Black, 5% Asian, 2% Indigenous. Middle-upper class (mean parent ed 16.61 yr; mean income $103,309).",
                "iv": "Six binary IVs (3 modalities x 2 day-types), each 0 (<2 hr) or 1 (>=2 hr). Instrument: 12-item ABCD screen-time questionnaire with continuous response options (none/<30m/30m/1h/2h/3h/4+h). Dichotomization at AAP <=2 hr recommendation; deviates from pre-reg (right-skew). beta_1 is a group difference, not per-hour slope. Cohen's d from adjusted group means and pooled SD.",
                "dv": "Nine continuous sleep variables: sleep duration (hours, SDSC item), sleep onset latency (SDSC 5-pt), insomnia symptoms (7-item SDSC subscale, alpha=0.73), disordered breathing (3-item, alpha=0.37), arousal disturbances (3-item, alpha=0.56), sleep-wake transition disturbances (6-item, alpha=0.59), excessive sleepiness (5-item, alpha=0.72), sleep hyperhidrosis (2-item, alpha=0.81), total sleep-wake disturbance score (26 items, alpha=0.65).",
                "covariates": [
                    {"name": "Age", "detail": "Continuous, years at baseline"},
                    {"name": "Gender", "detail": "Binary male/trans-male=0, female/trans-female=1"},
                    {"name": "Race", "detail": "Binary White=0 vs. non-White=1 (coarser than paper 394)"},
                    {"name": "Ethnicity", "detail": "Binary Hispanic/Latinx=0 vs. non-Hispanic/non-Latinx=1"},
                    {"name": "Family income", "detail": "Continuous 1-10 ordinal (1 = <$5K, 10 = >=$200K)"},
                    {"name": "Parent education", "detail": "Continuous 0-21 ordinal"},
                    {"name": "Parent employment", "detail": "Binary currently-working=1 vs. not=0"}
                ],
                "equation": "sleep_DV[i] = b0 + b1*phoneSM_IV[i] + b2*age + b3*gender + b4*race + b5*ethnicity + b6*income + b7*parent_ed + b8*parent_emp + e[i]. Cohen's d computed from adjusted means at IV=0 and IV=1 and pooled SD (not directly returned by the regression).",
                "estimation": "OLS. Software not specified; analyses pre-registered on OSF. No survey weights. No random intercept for family despite siblings/twins in sample; sensitivity check with vs. without them yielded similar findings. alpha = 0.001 (paper's MC correction). Race and ethnicity interactions with IV all p > 0.001; no stratified per-modality estimates reported.",
                "native_metric": "d",
                "iv_axis": m1["iv_axis"],
                "dv_axis": m1["dv_axis"],
                "estimates": m1["estimates"],
            },
            {
                "model_id": "M2",
                "name": "Logistic regression of binary clinical-threshold sleep outcomes on dichotomized phone/SM use (relative risk)",
                "location_in_paper": "Tables 4 (insufficient sleep) and 5 (disturbed sleep).",
                "design": "Same cross-sectional ABCD baseline analysis as M1, same IV coding and same 7 covariates. Difference from M1 is the DV: dichotomized clinical-threshold outcomes instead of continuous.",
                "sample": "Same as M1: N 10,666-10,676 across cells, ages 9-10, same demographic profile and per-IV >=2 hr group sizes.",
                "iv": "Identical to M1: six binary IVs.",
                "dv": "Two binary clinical-threshold outcomes: (1) Insufficient sleep = 7-8 hr or fewer per SDSC duration item (NSF recommends 9-11 hr for 9-11 year olds); sample base rate ~14-17% depending on day type. (2) Disturbed sleep = SDSC total sum >= 39 (clinical threshold for likely clinically significant sleep-wake disturbance; sample M=36.54); sample base rate ~25-30%.",
                "covariates": [
                    {"name": "(same 7 as M1)", "detail": "Age, gender, race, ethnicity, family income, parent education, parent employment"}
                ],
                "equation": "logit(P(bad_sleep_DV[i]=1)) = b0 + b1*phoneSM_IV[i] + b2..b8*controls. Estimator returns log-odds-ratio; paper converts to relative risk for Tables 4-5.",
                "estimation": "Logistic regression. Converts OR to RR for reporting. No survey weights. No family random intercept. alpha = 0.001. Race and ethnicity interactions with IV all non-significant.",
                "native_metric": "RR",
                "iv_axis": m2["iv_axis"],
                "dv_axis": m2["dv_axis"],
                "estimates": m2["estimates"],
            }
        ],
        "excluded_models": [
            {"model": "TV, videos, video-games IVs alone", "location": "Tables 2-5 rows for those modalities", "why": "Non-phone/non-SM modalities. Fail IC2."},
            {"model": "Non-TV screen media composite IV", "location": "Tables 2-5 rows", "why": "Bundles texting + SM + video chat + video games + YouTube. Includes non-phone (gaming, video) ingredients without per-modality breakout. Fails IC2 Step 2."},
            {"model": "Total screen media composite IV", "location": "Tables 2-5 rows", "why": "Bundles all 6 modalities including TV. Includes non-phone ingredients. Fails IC2 Step 2."},
            {"model": "Continuous-IV logistic regressions", "location": "In-text", "why": "Paper reports continuous-IV ORs only for non-TV and total composites, not per phone/SM modality. No phone/SM-specific continuous estimates extractable."},
            {"model": "Sibling/twin-excluded sensitivity", "location": "In-text", "why": "'Findings did not differ'; per-modality numbers in the sibling-excluded version not printed."},
            {"model": "Race x IV and ethnicity x IV interactions", "location": "In-text", "why": "All non-significant at p > 0.001; no stratified per-modality estimates reported."},
            {"model": "Pre-registered continuous-IV linear regressions", "location": "Pre-registration / supplemental Table 1", "why": "Switched to dichotomized IVs in body due to right-skew. Continuous-IV phone/SM estimates not reported in the paper body."}
        ],
        "d_transformation": {
            "native_metric": "Cohen's d (M1) + Relative risk (M2)",
            "conversion_formula": "M1: passthrough (native is already d). M2: OR = RR * (1-p0) / (1 - RR*p0); d = ln(OR) * sqrt(3)/pi (Chinn 2000). p0 = 0.155 (insufficient sleep marginal base rate); 0.275 (disturbed sleep).",
            "contrast_type": "M1: >=2 hr group vs. <2 hr group difference / pooled SD. M2: log-OR scale via Chinn.",
            "transformable": True,
            "notes": "For M2, marginal sample rate approximates unexposed-group rate to within ~1% since exposure prevalence is 1.5-3.8%. Not directly comparable to per-1-SD-of-IV d's from papers like 394."
        },
        "coder_log": [
            {"timestamp": "2026-05-09T00:00:00Z", "coder": "danny", "change": "Initial extraction. Two models (linear/d and logistic/RR). Migrated 66 estimates."}
        ]
    }
    return p


def main():
    rows = load_include_papers()
    special = {"394": paper_394(), "156": paper_156()}

    papers = []
    for r in rows:
        pid = r["paper_id"]
        if pid in special and special[pid] is not None:
            papers.append(special[pid])
        else:
            papers.append(stub_paper(r))

    coders = [
        {"id": "danny",  "name": "Danny",  "role": "PI"},
        {"id": "cooper", "name": "Cooper", "role": "coder"},
    ]

    out = {"coders": coders, "papers": papers, "generated_at": datetime.utcnow().isoformat() + "Z"}
    out_path = os.path.join(REPO, "docs", "data", "papers-seed.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    n_stub = sum(1 for p in papers if p["extraction_status"] == "empty")
    n_done = len(papers) - n_stub
    print(f"Wrote {out_path}")
    print(f"  {len(papers)} papers total: {n_done} extracted, {n_stub} stubbed")


if __name__ == "__main__":
    main()
