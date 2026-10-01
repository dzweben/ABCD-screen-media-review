// Upload ingested paper JSON (docs/data/ingested/paper_*.json) to Firestore /papers/<id>.
// Usage (from docs/scripts/):  npm install && node upload_to_firestore.mjs [paper_id ...]
// With no ids, uploads every file in docs/data/ingested/.
// Overwrites the whole doc — only run on papers no human has started editing,
// unless you pass --force. Refuses by default if the existing doc has
// agreements/strikes/notes or contributors beyond "danny".
import { initializeApp } from "firebase/app";
import { getFirestore, doc, getDoc, setDoc } from "firebase/firestore";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const ingested = path.join(here, "..", "data", "ingested");
const cfgSrc = fs.readFileSync(path.join(here, "..", "firebase-config.js"), "utf8");
const config = new Function("window", cfgSrc + "; return window.FIREBASE_CONFIG;")({});

const args = process.argv.slice(2);
const force = args.includes("--force");
const ids = args.filter((a) => a !== "--force");
const files = (ids.length ? ids.map((id) => `paper_${id}.json`) : fs.readdirSync(ingested).filter((f) => /^paper_.*\.json$/.test(f)));

const db = getFirestore(initializeApp(config));
const clean = (o) => JSON.parse(JSON.stringify(o, (k, v) => (v === undefined ? null : v)));

function humanTouched(d) {
  if (!d) return false;
  const nonEmpty = (o) => o && Object.values(o).some((v) => v && (typeof v !== "object" || Object.keys(v).length));
  return nonEmpty(d.agreements) || nonEmpty(d.strikes) || nonEmpty(d.notes) ||
    (d.contributors || []).some((c) => c !== "danny");
}

let up = 0, skipped = 0;
for (const f of files) {
  const paper = JSON.parse(fs.readFileSync(path.join(ingested, f), "utf8"));
  const ref = doc(db, "papers", String(paper.paper_id));
  const existing = (await getDoc(ref)).data();
  if (!force && humanTouched(existing)) {
    console.log(`SKIP #${paper.paper_id} — already has human review activity (use --force)`);
    skipped++;
    continue;
  }
  paper.last_edited_by = "danny";
  paper.last_updated = new Date().toISOString();
  paper.agreements = {}; paper.strikes = {}; paper.notes = {};
  await setDoc(ref, clean(paper));
  up++;
  console.log(`up  #${paper.paper_id}`);
}
console.log(`\nuploaded ${up}, skipped ${skipped}`);
process.exit(0);
