// Snapshot the live site's Firestore state into the repo:
//   docs/data/firestore-export.json  { exported_at, coders: [...], papers: [...] }
// Includes every coder edit, agreement, strike and note, so the repo holds a
// recoverable copy of the review. Run from docs/scripts/:  node export_firestore.mjs
import { initializeApp } from "firebase/app";
import { getFirestore, collection, getDocs } from "firebase/firestore";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const cfgSrc = fs.readFileSync(path.join(here, "..", "firebase-config.js"), "utf8");
const config = new Function("window", cfgSrc + "; return window.FIREBASE_CONFIG;")({});
const db = getFirestore(initializeApp(config));

const coders = (await getDocs(collection(db, "coders"))).docs.map((d) => ({ id: d.id, ...d.data() }));
const papers = [];
for (const d of (await getDocs(collection(db, "papers"))).docs) {
  const log = (await getDocs(collection(db, "papers", d.id, "log"))).docs.map((x) => x.data());
  papers.push({ ...d.data(), _log: log.sort((a, b) => String(a.timestamp).localeCompare(String(b.timestamp))) });
}
papers.sort((a, b) => Number(a.paper_id) - Number(b.paper_id));
const out = path.join(here, "..", "data", "firestore-export.json");
fs.writeFileSync(out, JSON.stringify({ exported_at: new Date().toISOString(), coders, papers }, null, 1));
console.log(`exported ${papers.length} papers, ${coders.length} coders -> ${out}`);
process.exit(0);
