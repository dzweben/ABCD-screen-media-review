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
node export_firestore.mjs                                  # snapshot live site state (incl. coder edits) -> docs/data/firestore-export.json
```
