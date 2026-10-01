// Patch ONLY the computed Cohen's d fields (derived_*) into live Firestore papers,
// leaving every coder edit (text, agreements, strikes, notes) untouched.
// Matches estimates by (model_id, iv, dv). Use this instead of upload_to_firestore.mjs
// once coders have started reviewing.
// Usage (from docs/scripts/):  node patch_derived.mjs [paper_id ...]   (default: all)
import { initializeApp } from "firebase/app";
import { getFirestore, doc, getDoc, updateDoc } from "firebase/firestore";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const ingested = path.join(here, "..", "data", "ingested");
const cfgSrc = fs.readFileSync(path.join(here, "..", "firebase-config.js"), "utf8");
const config = new Function("window", cfgSrc + "; return window.FIREBASE_CONFIG;")({});
const db = getFirestore(initializeApp(config));
const FIELDS = ["derived_d", "derived_d_lo", "derived_d_hi", "derived_d_method", "derived_d_formula", "derived_d_calc"];

const ids = process.argv.slice(2);
const files = ids.length ? ids.map((i) => `paper_${i}.json`) : fs.readdirSync(ingested).filter((f) => /^paper_.*\.json$/.test(f));
let patched = 0;
for (const f of files) {
  const src = JSON.parse(fs.readFileSync(path.join(ingested, f), "utf8"));
  const ref = doc(db, "papers", String(src.paper_id));
  const live = (await getDoc(ref)).data();
  if (!live) { console.log(`missing #${src.paper_id}`); continue; }
  const idx = new Map();
  for (const m of src.primary_models || []) for (const e of m.estimates || []) idx.set(`${m.model_id}|${e.iv}|${e.dv}`, e);
  let n = 0;
  for (const m of live.primary_models || []) for (const e of m.estimates || []) {
    const s = idx.get(`${m.model_id}|${e.iv}|${e.dv}`);
    if (!s) continue;
    for (const k of FIELDS) e[k] = s[k] ?? null;
    n++;
  }
  await updateDoc(ref, { primary_models: JSON.parse(JSON.stringify(live.primary_models)), last_edited_by: live.last_edited_by || "danny" });
  patched++;
  console.log(`patched #${src.paper_id} (${n} estimates)`);
}
console.log(`\npatched ${patched} papers`);
process.exit(0);
