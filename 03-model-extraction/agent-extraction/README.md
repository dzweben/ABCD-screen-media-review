# Agent extraction harness (Stage 3 first pass)

How the first-pass ("Draft") extractions in `docs/data/drafts/` were produced.

- `extract_workflow.js`: the Claude Code workflow script. It runs one agent per paper. Each agent reads `3L-extraction-guidelines.md`, `02-L2/2L-criteria.md`, the two hand-finished reference extractions (`example_extractions.json`: papers 394 and 156) and the full PDF, then writes `docs/data/drafts/paper_<id>.json`.
- `items.json`: the work list (65 papers). It holds the PDF path, the output path, and the Stage 2 reason that pointed to the qualifying phone/SM analysis. Notes about supplements are appended for 215 and 431.
- `agent_summaries.json`: each agent's returned summary (models, estimates, metrics, and the "concerns" text). That text appears on the site as "Things to verify".
- `215_supplement.txt`: a text conversion of paper 215's supplementary appendix (.docx), so an agent could read Tables S6/S7.

Duplicates were not extracted. 393 is the same paper as 394, and 436 is the same paper as 435; `docs/scripts/ingest_drafts.py` mirrors them. 394 and 156 were done by hand before this run.

## Pipeline after extraction

```bash
python3 docs/scripts/ingest_drafts.py                      # validate + compute Cohen's d per estimate -> docs/data/ingested/
cd docs/scripts && npm install && node upload_to_firestore.mjs   # push to the live site (skips papers coders have touched)
node patch_derived.mjs                                     # once coders are reviewing: update only the computed-d fields, never their edits
node export_firestore.mjs                                  # snapshot live site state (incl. coder edits) -> docs/data/firestore-export.json
```

## Completion + audit pass

`complete_and_audit_workflow.js` runs two independent agents per paper (all 67 papers):
1. **Complete**: re-reads the PDF and supplements and fills every printed value, the CI inputs (SE, exact p, t/z, group sizes), the SDs, and `iv_type`. Anything not printed gets a note saying where the agent looked.
2. **Audit**: a separate agent checks every number against the PDF and fixes errors.

Per-paper results are in `complete_and_audit_summaries.json`. Every change is also stored in each draft's `verification_log` and shown on the site. In the first run, 5,519 numbers were checked and 76 errors fixed.
