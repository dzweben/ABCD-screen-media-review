/*
 * Storage adapter.
 *
 * Two modes:
 *   - LOCAL  (default): loads papers-seed.json, saves overrides to browser localStorage.
 *                       Good for single-viewer testing before Firebase is wired.
 *   - REMOTE (Firestore): plugged in once the user pastes their Firebase config into
 *                         `docs/firebase-config.js`. Every viewer sees every edit.
 *
 * The app.js code doesn't care which mode is active — it calls the same API:
 *
 *   await Storage.init()
 *   Storage.getCoders() -> [{id, name, role}, …]
 *   Storage.listPapers() -> [{paper_id, title, extraction_status, …}, …]  (index only)
 *   await Storage.getPaper(id) -> full paper object
 *   await Storage.savePaper(paperObj) -> persists and returns it
 *   await Storage.appendLog(paperId, {coder, change}) -> pushes a coder-log entry
 *   Storage.mode -> 'local' | 'remote'
 */

const Storage = (() => {
  const LOCAL_OVERRIDES_KEY = "abcd-review-overrides-v1";
  let seed = null;         // parsed papers-seed.json
  let overrides = {};       // { paper_id: fullPaperObject }
  let coders = [];
  let mode = "local";

  function loadOverrides() {
    try {
      const raw = localStorage.getItem(LOCAL_OVERRIDES_KEY);
      overrides = raw ? JSON.parse(raw) : {};
    } catch (e) {
      console.warn("Could not read localStorage overrides", e);
      overrides = {};
    }
  }

  function saveOverrides() {
    try {
      localStorage.setItem(LOCAL_OVERRIDES_KEY, JSON.stringify(overrides));
    } catch (e) {
      console.warn("Could not write localStorage overrides", e);
    }
  }

  function mergePaper(pid) {
    if (overrides[pid]) return structuredClone(overrides[pid]);
    const base = seed.papers.find((p) => p.paper_id === pid);
    return base ? structuredClone(base) : null;
  }

  async function init() {
    // Try to load Firebase config; if absent, we stay in local mode.
    // (Firebase adapter to be added when config is ready — see comment at bottom.)
    const seedResp = await fetch("data/papers-seed.json", { cache: "no-cache" });
    if (!seedResp.ok) throw new Error(`Seed fetch failed: HTTP ${seedResp.status}`);
    seed = await seedResp.json();
    coders = seed.coders;
    loadOverrides();
    mode = "local";
    return mode;
  }

  function getCoders() {
    return coders.slice();
  }

  function listPapers() {
    return seed.papers.map((p) => {
      const merged = mergePaper(p.paper_id);
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

  async function getPaper(pid) {
    return mergePaper(pid);
  }

  async function savePaper(paperObj) {
    paperObj.last_updated = new Date().toISOString();
    overrides[paperObj.paper_id] = structuredClone(paperObj);
    saveOverrides();
    return structuredClone(paperObj);
  }

  async function appendLog(pid, entry) {
    const paper = mergePaper(pid);
    if (!paper) throw new Error(`Unknown paper ${pid}`);
    paper.coder_log = paper.coder_log || [];
    paper.coder_log.push({
      timestamp: new Date().toISOString(),
      coder: entry.coder,
      change: entry.change,
    });
    if (entry.coder && paper.contributors && !paper.contributors.includes(entry.coder)) {
      paper.contributors.push(entry.coder);
    }
    return savePaper(paper);
  }

  function clearOverride(pid) {
    delete overrides[pid];
    saveOverrides();
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
  };
})();

/*
 * REMOTE-MODE STUB — TO WIRE UP WHEN FIREBASE PROJECT IS READY
 *
 * Once you have a Firebase project:
 *   1. Enable Firestore in test mode.
 *   2. Copy your web config into `docs/firebase-config.js`:
 *
 *        window.FIREBASE_CONFIG = {
 *          apiKey: "...",
 *          authDomain: "...",
 *          projectId: "...",
 *          ...
 *        };
 *
 *   3. Include the Firebase SDK before storage.js in index.html:
 *        <script type="module" src="firebase-adapter.js"></script>
 *
 *   4. That adapter file will override Storage.getPaper / savePaper / appendLog
 *      to write to Firestore instead of localStorage. Same API surface.
 *
 * Every write carries `edited_by: <selected coder>` and `edited_at: server timestamp`,
 * so any viewer on the URL sees the live coder log.
 */
