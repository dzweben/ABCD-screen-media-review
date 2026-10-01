export const meta = {
  name: 'abcd-stage3-extract',
  description: 'Draft Stage 3 model extractions for 65 ABCD phone/SM papers, one agent per PDF',
  phases: [{ title: 'Extract', detail: 'one agent per paper reads the full PDF and writes a structured draft JSON' }],
}

const SP = '/Users/dannyzweben/Desktop/ABCD-smartphon-socialmedia-review/03-model-extraction/agent-extraction'
const REPO = '/Users/dannyzweben/Desktop/ABCD-smartphon-socialmedia-review'

const SUMMARY = {
  type: 'object',
  properties: {
    paper_id: { type: 'string' },
    wrote_file: { type: 'boolean' },
    n_primary_models: { type: 'integer' },
    n_estimates: { type: 'integer' },
    native_metrics: { type: 'array', items: { type: 'string' } },
    d_transformable: { type: 'string', enum: ['yes', 'no', 'partial'] },
    concerns: { type: 'string', description: 'anything the human reviewer should double-check; empty string if none' },
  },
  required: ['paper_id', 'wrote_file', 'n_primary_models', 'n_estimates', 'native_metrics', 'd_transformable', 'concerns'],
}

function prompt(pid) {
  return `You are extracting statistical models from ONE published paper for a PRISMA systematic review of ABCD Study papers on youth SMARTPHONE / SOCIAL MEDIA use. Your output is the first-pass extraction that human coders will review, agree with, strike through, or annotate. Precision matters far more than speed: every number you write must be copied exactly from the paper. Never estimate, round differently, or invent a value — if something is not reported, write null and say so in a note.

YOUR PAPER: paper_id "${pid}". Look up its entry in ${SP}/items.json (fields: title, doi, year, pdf, out, stage2_reason; pdf/out paths are relative to the repo root ${REPO}). stage2_reason explains which phone/SM analysis got this paper included at Stage 2 — use it as a pointer, but verify against the PDF.

STEP 1 — Read the rules (both files, fully):
- ${REPO}/03-model-extraction/3L-extraction-guidelines.md  (what counts as a model, which spec to extract, per-model and per-estimate fields, composite handling, what NOT to extract, derived Cohen's d rules in §4a)
- ${REPO}/02-L2/2L-criteria.md  (especially FT-IC2: what counts as a qualifying smartphone/social-media variable, and the two-step composite isolation rule)

STEP 2 — Read the two finished reference extractions in ${SP}/example_extractions.json (papers 394 and 156). Your output must have exactly this shape and this level of detail and plain-prose style. Note how: one spec applied across many IV×DV combos = ONE model card with an estimates matrix; a genuinely different spec (e.g. logistic on binary DVs vs linear on continuous) = a second card; unadjusted models, non-phone modalities, mixed composites without phone/SM breakout, and narrative-only sensitivity analyses go in excluded_models with location + reason.

STEP 3 — Read the ENTIRE PDF at the "pdf" path with the Read tool (use the pages parameter, at most 20 pages per call, e.g. "1-10" then "11-20"; continue until you have every page, including any appendix/supplement bundled in the PDF). Read every table carefully.

STEP 4 — Decide the models. Qualifying IVs/DVs are phone/SM-specific: texting, video chat, social media time, smartphone/mobile phone ownership or age of acquisition, app use, problematic/addictive SM or phone use, dating apps, etc. (follow 2L-criteria FT-IC2 exactly). Phone/SM may be the IV or the DV — extract either way and say which. For each qualifying analysis, extract the specification the AUTHORS use to interpret that finding (usually the final fully-adjusted model). Every model and every excluded model needs an exact location (table number / figure / page / supplement table).

STEP 5 — Write the JSON file to the "out" path with the Write tool. Shape (one object, not an array):
{
  "paper_id": "${pid}", "title": ..., "doi": ..., "year": ...,
  "authors": "Last AB, Last CD, ...", "journal": "...",
  "extraction_status": "ai_draft", "lead_coder": "danny", "contributors": ["danny"], "last_edited_by": "danny",
  "d_transformable": true | false | "partial",
  "primary_models": [ {
     "model_id": "M1", "name": "<analytic class> of <DV> on <IV>, <key adjustment>",
     "location_in_paper": "Table 2, Model 3 (p. 6); interpreted in Discussion p. 8",
     "design": "<prose: cross-sectional/longitudinal, waves, which wave IV vs DV, repeated measures or not, interactions with time>",
     "sample": "<prose: ABCD release, N analytic, exclusions, age, sex, race/ethnicity breakdown as reported>",
     "iv": "<prose: what the IV is, instrument, units, coding, descriptive stats if reported>",
     "dv": "<prose: same for DV(s)>",
     "covariates": [ {"name": "...", "detail": "..."} ],
     "equation": "<plain-text equation with every term, e.g. Y = b0 + b1*SM + b2*age + ... + u_site + e>",
     "estimation": "<prose: software, estimator, weights, random effects/clustering, alpha, multiple-comparison correction, interaction/stratification tests, sensitivity analyses>",
     "native_metric": "B" | "beta_std" | "OR" | "RR" | "IRR" | "d" | "r" | "other:<name>",
     "iv_axis": [ {"id": "...", "label": "...", "meta": "short descriptive", "sd_iv": <number or null>} ],
     "dv_axis": [ {"id": "...", "label": "...", "sd_dv": <number or null>, "p0": <baseline event rate 0-1 for binary DV, or null>} ],
     "estimates": [ {"iv": "<iv id>", "dv": "<dv id>",
        <native fields, named by metric>: B/B_lo/B_hi | beta/beta_lo/beta_hi | OR/OR_lo/OR_hi | RR/RR_lo/RR_hi | IRR/IRR_lo/IRR_hi | d/d_lo/d_hi | r/r_lo/r_hi | value/value_lo/value_hi,
        "p": <number or null>, "p_label": "<exactly as printed, e.g. '<.001'>", "sig": true|false,
        "location": "Table 2 row 3", "note": "<optional>"} ]
  } ],
  "excluded_models": [ {"model": "...", "location": "...", "why": "..."} ],
  "d_transformation": {
     "native_metric": "...",
     "conversion_formula": "<exact formula used for this paper's metric per guidelines §4a>",
     "contrast_type": "<what one unit of the IV means: per 1 hour/day, per 1 SD, high vs low group, yes vs no ownership, ...>",
     "transformable": true | false | "partial",
     "notes": "<where SD_IV / SD_DV / p0 came from (table + page), or why conversion is impossible (e.g. SHAP values, network edge weights, factor loadings), and any caveats>"
  }
}
Rules for numbers: CI bounds go in *_lo / *_hi; if only SE is reported, compute nothing — put SE in "note" and leave CI null. sd_iv / sd_dv: take from the paper's descriptive table for the analytic sample (cite it in d_transformation.notes); if the DV is a CBCL/T-score, SD_DV=10 by construction; if not reported, null. For binary DVs give p0 when reported. If the model output is not convertible to Cohen's d (ML importance, SHAP, network edges, loadings, mediation indirect effects without SDs, etc.), still extract it fully with native_metric "other:<name>", set transformable false, and explain — those papers go to a later review level.
If the paper has NO qualifying phone/SM estimate at all after careful reading, write the file with primary_models: [] and explain thoroughly in excluded_models and d_transformation.notes, and say so in concerns.

Writing style: plain, specific prose like the reference extractions. No templated labels ("What it is:", "This paper:"). No editorializing.

STEP 6 — Validate: run  python3 -c "import json;json.load(open('<out path>'))"  via Bash and fix any error. Then re-open the PDF tables once more and spot-check at least 5 of your numbers against the table (or all of them if fewer than 5). Fix anything wrong.

Finally return the summary object. "concerns" should flag anything a human must verify (ambiguous which model the authors anchor on, unclear units, SDs missing, values read off a figure, possible phone/SM-eligibility doubts).`
}

phase('Extract')
const results = await parallel(args.map((pid) => () =>
  agent(prompt(pid), { label: `paper ${pid}`, phase: 'Extract', schema: SUMMARY })
))
const ok = results.filter(Boolean)
log(`${ok.length}/${args.length} agents returned; ${ok.filter(r => r.wrote_file).length} wrote files`)
return ok
