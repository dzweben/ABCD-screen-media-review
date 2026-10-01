export const meta = {
  name: 'abcd-stage3-complete-and-audit',
  description: 'For all 67 papers: complete every gap (values, CIs, SE/p, SDs, IV type) then independently audit every number against the PDF',
  phases: [
    { title: 'Complete', detail: 'fill every missing value, CI input, SD and IV type from the PDF' },
    { title: 'Audit', detail: 'independent agent checks every number in the draft against the PDF and fixes errors' },
  ],
}

const REPO = '/Users/dannyzweben/Desktop/ABCD-smartphon-socialmedia-review'

const COMPLETE_OUT = {
  type: 'object',
  properties: {
    paper_id: { type: 'string' },
    values_filled: { type: 'integer' },
    ci_inputs_filled: { type: 'integer', description: 'CIs, SEs, exact p, t/z or group sizes added' },
    sds_filled: { type: 'integer' },
    iv_types_set: { type: 'integer' },
    confirmed_missing: { type: 'integer' },
    summary: { type: 'string' },
  },
  required: ['paper_id', 'values_filled', 'ci_inputs_filled', 'sds_filled', 'iv_types_set', 'confirmed_missing', 'summary'],
}
const AUDIT_OUT = {
  type: 'object',
  properties: {
    paper_id: { type: 'string' },
    numbers_checked: { type: 'integer' },
    errors_fixed: { type: 'integer' },
    error_examples: { type: 'array', items: { type: 'string' }, description: 'each fix as "item: was X, now Y (Table n p.m)"' },
    still_missing: { type: 'integer' },
    summary: { type: 'string' },
  },
  required: ['paper_id', 'numbers_checked', 'errors_fixed', 'error_examples', 'still_missing', 'summary'],
}

const SOURCES = (pid) => `FILES
- Draft (edit in place): ${REPO}/docs/data/drafts/paper_${pid}.json
- PDF: ${REPO}/docs/pdfs/<doi with "/" replaced by "_">.pdf (doi is in the draft). ALSO read every file in ${REPO}/docs/pdfs/ whose name starts with that same stem followed by "_supplement" (PDF: Read tool; .docx: convert with  textutil -convert txt -stdout <file>  via Bash). For paper 215 a text copy of the appendix is at ${REPO}/03-model-extraction/agent-extraction/215_supplement.txt.
- Conversion rules: ${REPO}/03-model-extraction/3L-extraction-guidelines.md §4a.
Read the ENTIRE PDF with the Read tool (pages param, max 20 pages per call): every table, figure label, footnote, appendix page. Do not stop early.`

const SCHEMA_NOTES = `Field conventions on each estimate (keep existing ones; add what is missing):
- native value + CI: B/B_lo/B_hi | beta/beta_lo/beta_hi | OR/OR_lo/OR_hi | RR/RR_lo/RR_hi | IRR/IRR_lo/IRR_hi | d/d_lo/d_hi | r/r_lo/r_hi | value/value_lo/value_hi (for "other:..." metrics)
- "se": the printed standard error of the estimate (number). If the estimate is an OR/RR/IRR or a logit coefficient, say on the estimate "se_scale": "log" when the SE is for the log/logit coefficient, "raw" otherwise.
- "p": exact p as a number when printed exactly (e.g. 0.034); when printed as an inequality keep p null and put the text in "p_label" (e.g. "<.001").
- "t" or "z": test statistic if printed. "df": error df for t/F if printed.
- For native d: "n1" and "n0" = the two group sizes behind that d, if printed.
- "sd_iv"/"sd_dv"/"p0" may be put on an individual estimate when they differ by cell; otherwise on iv_axis / dv_axis entries.
- On each MODEL: "iv_type": "continuous" | "binary" | "categorical". Continuous B uses β = B·SD_IV/SD_DV; binary/categorical B is a group mean difference (d = B/SD_DV, no SD_IV needed).
- F with 1 numerator df: native_metric "other:F(1,df)", F in "value", error df in "df", direction in "sign" (1 or -1). χ² with 1 df: native_metric "other:chi2", χ² in "value", "chi2_df": 1, test N in "n", "sign".
- "location": exact table/figure/page for every number.`

function completePrompt(pid) {
  return `You are COMPLETING an extraction draft for paper_id "${pid}" in a PRISMA systematic review of ABCD Study smartphone/social-media papers. The lead reviewer is unhappy that many cells were left blank (missing estimates, missing confidence intervals, missing SDs) when the information is actually in the paper. Your job: find and fill EVERYTHING that is printed. Never invent, never read values off unlabelled plots, never guess.

${SOURCES(pid)}

${SCHEMA_NOTES}

DO, for every model and every estimate in primary_models:
1. Set the model's "iv_type".
2. If the native value or its CI is null: search the whole paper (all tables, text, figure labels with printed numbers, footnotes, bundled supplements). Fill exactly what is printed.
3. If the CI is not printed anywhere, record whatever lets a CI be computed: the SE ("se" + "se_scale"), the exact p, t/z with df, or for d the group sizes n1/n0. Many papers print SE or exact p in tables even when they print no CI — find them.
4. Standard deviations for d: continuous-IV B needs sd_iv and sd_dv; binary/categorical-IV B needs sd_dv; RR/PR needs p0 (baseline/reference-group event rate) for binary outcomes. Look in descriptive tables (Table 1 etc.) for the ANALYTIC sample at the wave the variable enters the model. SD = SE·√N is allowed if both printed (write the arithmetic in "note"). T-scores: SD 10. Match units (per hour vs per minute) and note any conversion.
5. If something truly is not printed, keep it null and write in that estimate's "note" exactly where you looked and where the value lives (e.g. "Checked Tables 1-3, Fig 2 (bars unlabelled), text pp.5-8; only in online eTable 4, not in this PDF").
6. Do not delete models/estimates or rewrite prose fields. You may append to d_transformation.notes.
7. Append each action to a top-level array "verification_log": {"stage": "complete", "item": "M1 texting x depressive", "action": "filled_value|filled_ci_input|filled_sd|set_iv_type|confirmed_missing", "value": ..., "where": "Table 2 p.5"}.
8. Write the file, then validate: python3 -c "import json;json.load(open('${REPO}/docs/data/drafts/paper_${pid}.json'))"

Return the summary object.`
}

function auditPrompt(pid, flags) {
  return `You are an INDEPENDENT AUDITOR for paper_id "${pid}" in a PRISMA systematic review of ABCD Study smartphone/social-media papers. Another agent extracted and completed this draft. Assume it contains mistakes. Your job: check EVERY number in the draft against the paper and fix any that are wrong. Precision is everything.

${SOURCES(pid)}

${SCHEMA_NOTES}

AUDIT, for every model and every estimate:
- The native value, both CI bounds, se, p / p_label, t/z, sig, and location: open the cited table/page and confirm each matches exactly (right row, right column, right model — e.g. the fully adjusted model the authors interpret, not the unadjusted one; right sign; right decimal). Fix anything wrong and update location.
- sig: must match the paper's own α / correction (e.g. FDR-adjusted, Bonferroni, α = .001). A cell whose CI includes the null should not be sig unless the paper's own test says otherwise — check.
- sd_iv / sd_dv / p0: confirm against the descriptive table for the analytic sample, correct units.
- iv_type on each model: confirm continuous vs binary vs categorical against how the IV enters the model.
- Any value still null: do one more full search of the paper and supplements; fill if printed, otherwise make sure the estimate's "note" says where you looked.
- Also confirm the estimates set is complete: if the paper prints phone/SM estimates for this same model specification that are missing from the draft (a missing IV × DV cell), add them.
${flags.length ? `- AUTOMATED CONSISTENCY FLAGS raised on this draft (estimate vs CI vs p disagree — almost always an extraction error):\n${flags.map((f) => '  * ' + f).join('\n')}\n  Resolve each one against the paper.` : ''}

Rules: never invent; never read numbers off unlabelled plots; do not delete models or rewrite prose fields. Append every change to "verification_log" with "stage": "audit", "action": "corrected|added|confirmed_missing", "was": old, "value": new, "where": location.
Write the file, then validate: python3 -c "import json;json.load(open('${REPO}/docs/data/drafts/paper_${pid}.json'))"

Return the summary object. In error_examples list every correction you made.`
}

const FLAGS = args.flags || {}
const res = await pipeline(
  args.ids,
  (pid) => agent(completePrompt(pid), { label: `complete ${pid}`, phase: 'Complete', schema: COMPLETE_OUT }),
  (c, pid) => agent(auditPrompt(pid, FLAGS[pid] || []), { label: `audit ${pid}`, phase: 'Audit', schema: AUDIT_OUT })
    .then((a) => ({ complete: c, audit: a })),
)
const ok = res.filter(Boolean)
const sum = (f) => ok.reduce((s, r) => s + (f(r) || 0), 0)
log(`${ok.length}/${args.ids.length} papers done · filled values ${sum((r) => r.complete && r.complete.values_filled)} · CI inputs ${sum((r) => r.complete && r.complete.ci_inputs_filled)} · SDs ${sum((r) => r.complete && r.complete.sds_filled)} · audit fixes ${sum((r) => r.audit && r.audit.errors_fixed)}`)
return ok
