/*
 * Storage adapter.
 *
 * Two modes, picked at init() based on whether window.FIREBASE_CONFIG is present:
 *
 *   - REMOTE (Firestore): every viewer sees every edit. Public honor-system
 *     attribution enforced by firestore.rules (see .firebase/firestore.rules).
 *     Documents live in the `papers` collection with paper_id as doc id.
 *     Log entries live in the `papers/{paperId}/log` subcollection, append-only.
 *
 *   - LOCAL (fallback): loads papers-seed.json, saves overrides to browser
 *     localStorage. Single-viewer testing only.
 *
 * Public API — same in both modes:
 *   await Storage.init()
 *   Storage.getCoders()             -> [{id, name, role}, ...]
 *   Storage.listPapers()            -> [{paper_id, title, extraction_status, ...}]  (index)
 *   await Storage.getPaper(id)      -> full paper object
 *   await Storage.savePaper(paper)  -> persists and returns
 *   await Storage.appendLog(id, {coder, change}) -> pushes a log entry
 *   Storage.clearOverride(id)       -> revert local edits (local mode only)
 *   Storage.mode                    -> 'local' | 'remote'
 */

const Storage = (() => {
  const LOCAL_OVERRIDES_KEY = "abcd-review-overrides-v1";

  let seed = null;
  let coders = [];
  let mode = "local";
  let indexCache = [];   // list-view rows, refreshed after every write
  let indexReady = false;

  // Remote-mode Firebase handles
  let fbApp = null;
  let fbDb = null;

  /* ── init ─────────────────────────────────────────── */
  async function init() {
    const seedResp = await fetch("data/papers-seed.json", { cache: "no-cache" });
    if (!seedResp.ok) throw new Error(`Seed fetch failed: HTTP ${seedResp.status}`);
    seed = await seedResp.json();
    coders = seed.coders;

    if (window.FIREBASE_CONFIG && window.firebase) {
      try {
        await initRemote();
        mode = "remote";
      } catch (err) {
        console.error("Firestore init failed, falling back to localStorage:", err);
        mode = "local";
      }
    }
    await refreshIndex();
    return mode;
  }

  async function initRemote() {
    fbApp = firebase.initializeApp(window.FIREBASE_CONFIG);
    fbDb = firebase.firestore();
    // On first ever load, seed Firestore from the JSON file if empty.
    const snap = await fbDb.collection("papers").limit(1).get();
    if (snap.empty) {
      console.log("[storage] Firestore is empty — seeding from papers-seed.json …");
      const batch = fbDb.batch();
      seed.papers.forEach((p) => {
        const ref = fbDb.collection("papers").doc(p.paper_id);
        batch.set(ref, sanitizeForFirestore({ ...p, last_edited_by: "seed" }));
      });
      await batch.commit();
      // Seed initial coder-log entries as subcollection docs
      for (const p of seed.papers) {
        for (const e of p.coder_log || []) {
          await fbDb
            .collection("papers")
            .doc(p.paper_id)
            .collection("log")
            .add({
              timestamp: e.timestamp || new Date().toISOString(),
              coder: e.coder || "seed",
              change: e.change || "",
            });
        }
      }
      console.log("[storage] Seeded", seed.papers.length, "papers.");
    }
  }

  /* ── index / list ─────────────────────────────────── */
  async function refreshIndex() {
    if (mode === "remote") {
      const snap = await fbDb.collection("papers").get();
      indexCache = snap.docs.map((doc) => {
        const p = doc.data();
        return {
          paper_id: p.paper_id,
          title: p.title || "",
          year: p.year || "",
          doi: p.doi || "",
          extraction_status: p.extraction_status || "empty",
          d_transformable: p.d_transformable ?? null,
          n_primary_models: (p.primary_models || []).length,
          n_excluded_models: (p.excluded_models || []).length,
        };
      });
      // Sort by numeric paper_id to preserve consistent order
      indexCache.sort((a, b) => Number(a.paper_id) - Number(b.paper_id));
    } else {
      const overrides = loadOverrides();
      indexCache = seed.papers.map((base) => {
        const merged = overrides[base.paper_id] || base;
        return {
          paper_id: merged.paper_id,
          title: merged.title,
          year: merged.year,
          doi: merged.doi,
          extraction_status: merged.extraction_status,
          d_transformable: merged.d_transformable,
          n_primary_models: (merged.primary_models || []).length,
          n_excluded_models: (merged.excluded_models || []).length,
        };
      });
    }
    indexReady = true;
  }

  function listPapers() {
    return indexReady ? indexCache.slice() : [];
  }
  function getCoders() { return coders.slice(); }

  /* ── read ─────────────────────────────────────────── */
  async function getPaper(pid) {
    if (mode === "remote") {
      const doc = await fbDb.collection("papers").doc(pid).get();
      if (!doc.exists) return null;
      const paper = doc.data();
      const logSnap = await fbDb
        .collection("papers")
        .doc(pid)
        .collection("log")
        .orderBy("timestamp", "asc")
        .get();
      paper.coder_log = logSnap.docs.map((d) => d.data());
      return paper;
    }
    const overrides = loadOverrides();
    if (overrides[pid]) return structuredClone(overrides[pid]);
    const base = seed.papers.find((p) => p.paper_id === pid);
    return base ? structuredClone(base) : null;
  }

  /* ── write ────────────────────────────────────────── */
  async function savePaper(paperObj) {
    const now = new Date().toISOString();
    paperObj.last_updated = now;
    if (mode === "remote") {
      // Log entries live in subcollection, not on the doc.
      const { coder_log, ...body } = paperObj;
      body.last_edited_by = body.last_edited_by || "unknown";
      await fbDb
        .collection("papers")
        .doc(paperObj.paper_id)
        .set(sanitizeForFirestore(body), { merge: false });
    } else {
      const overrides = loadOverrides();
      overrides[paperObj.paper_id] = structuredClone(paperObj);
      saveOverrides(overrides);
    }
    await refreshIndex();
    return paperObj;
  }

  async function appendLog(pid, entry) {
    const now = new Date().toISOString();
    const logEntry = {
      timestamp: now,
      coder: entry.coder,
      change: entry.change,
    };
    if (mode === "remote") {
      await fbDb
        .collection("papers")
        .doc(pid)
        .collection("log")
        .add(logEntry);
      // Also update contributors + last_edited_by on the doc
      const docRef = fbDb.collection("papers").doc(pid);
      const doc = await docRef.get();
      if (doc.exists) {
        const p = doc.data();
        const contribs = new Set(p.contributors || []);
        contribs.add(entry.coder);
        await docRef.update({
          contributors: [...contribs],
          last_edited_by: entry.coder,
          last_updated: now,
        });
      }
      return await getPaper(pid);
    }
    // local
    const paper = (await getPaper(pid)) || {};
    paper.coder_log = paper.coder_log || [];
    paper.coder_log.push(logEntry);
    if (entry.coder && paper.contributors && !paper.contributors.includes(entry.coder)) {
      paper.contributors.push(entry.coder);
    }
    paper.last_edited_by = entry.coder;
    return savePaper(paper);
  }

  function clearOverride(pid) {
    if (mode === "remote") {
      console.warn("[storage] Reset-to-seed is not supported in remote mode from the UI (would require rewriting the doc). Skipping.");
      return;
    }
    const overrides = loadOverrides();
    delete overrides[pid];
    saveOverrides(overrides);
  }

  /* ── helpers ──────────────────────────────────────── */
  function loadOverrides() {
    try {
      const raw = localStorage.getItem(LOCAL_OVERRIDES_KEY);
      return raw ? JSON.parse(raw) : {};
    } catch (e) {
      return {};
    }
  }
  function saveOverrides(obj) {
    try { localStorage.setItem(LOCAL_OVERRIDES_KEY, JSON.stringify(obj)); }
    catch (e) { console.warn(e); }
  }
  // Firestore rejects undefined values; convert to null recursively.
  function sanitizeForFirestore(o) {
    if (o === undefined) return null;
    if (o === null) return null;
    if (Array.isArray(o)) return o.map(sanitizeForFirestore);
    if (typeof o === "object") {
      const out = {};
      for (const [k, v] of Object.entries(o)) out[k] = sanitizeForFirestore(v);
      return out;
    }
    return o;
  }

  return {
    init,
    getCoders,
    listPapers,
    getPaper,
    savePaper,
    appendLog,
    clearOverride,
    get mode() { return mode; },
    refreshIndex,
  };
})();
