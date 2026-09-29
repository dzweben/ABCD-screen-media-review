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
    // Seed papers on first ever load
    const snap = await fbDb.collection("papers").limit(1).get();
    if (snap.empty) {
      console.log("[storage] Firestore is empty — seeding from papers-seed.json …");
      const batch = fbDb.batch();
      seed.papers.forEach((p) => {
        const ref = fbDb.collection("papers").doc(p.paper_id);
        batch.set(ref, sanitizeForFirestore({ ...p, last_edited_by: "seed" }));
      });
      await batch.commit();
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
    // Seed coders on first ever load
    const coderSnap = await fbDb.collection("coders").limit(1).get();
    if (coderSnap.empty) {
      console.log("[storage] Seeding coders collection …");
      const batch = fbDb.batch();
      seed.coders.forEach((c) => {
        batch.set(fbDb.collection("coders").doc(c.id), {
          name: c.name,
          role: c.role || "coder",
          added_at: new Date().toISOString(),
        });
      });
      await batch.commit();
    }
    await refreshCoders();
  }

  async function refreshCoders() {
    if (mode !== "remote") { coders = seed.coders; return; }
    const snap = await fbDb.collection("coders").get();
    coders = snap.docs.map((d) => ({ id: d.id, ...d.data() }));
    // Stable order: seeded ids first (by their seed order), then any added coders alphabetically.
    const seedOrder = new Map(seed.coders.map((c, i) => [c.id, i]));
    coders.sort((a, b) => {
      const ai = seedOrder.has(a.id) ? seedOrder.get(a.id) : Infinity;
      const bi = seedOrder.has(b.id) ? seedOrder.get(b.id) : Infinity;
      if (ai !== bi) return ai - bi;
      return a.name.localeCompare(b.name);
    });
  }

  async function addCoder({ name, role }) {
    const displayName = (name || "").trim();
    if (!displayName) throw new Error("Name is required");
    if (displayName.length > 59) throw new Error("Name too long (max 59 chars)");
    const id = displayName
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "")
      .slice(0, 40) || "coder-" + Date.now();
    if (mode === "remote") {
      // Only create if not present (so we don't overwrite an existing coder's role).
      const existing = await fbDb.collection("coders").doc(id).get();
      if (existing.exists) {
        throw new Error(`Coder id "${id}" already exists (${existing.data().name}). Pick a different name.`);
      }
      await fbDb.collection("coders").doc(id).set({
        name: displayName,
        role: role || "coder",
        added_at: new Date().toISOString(),
      });
      await refreshCoders();
    } else {
      if (coders.find((c) => c.id === id)) {
        throw new Error(`Coder id "${id}" already exists locally`);
      }
      coders.push({ id, name: displayName, role: role || "coder" });
    }
    return id;
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
    addCoder,
    refreshCoders,
    listPapers,
    getPaper,
    savePaper,
    appendLog,
    clearOverride,
    get mode() { return mode; },
    refreshIndex,
  };
})();
