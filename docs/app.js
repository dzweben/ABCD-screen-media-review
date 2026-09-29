/*
 * Main app — sidebar list, paper view/editor, coder attribution.
 *
 * Every value edit fires an autosave after a short debounce. Every save
 * appends a coder-log entry unless the write is itself a coder-log push
 * (avoid double-logging).
 */

const STATUS_LABELS = {
  empty: "Empty",
  ai_draft: "AI Draft",
  human_reviewed: "Reviewed",
  disputed: "Disputed",
  complete: "Complete",
};

const AppState = {
  currentPaperId: null,
  currentCoder: null,
  paperListCache: [],
  activeFilters: new Set(["empty", "ai_draft", "human_reviewed", "disputed", "complete"]),
  searchQuery: "",
  saveTimers: {},
};

function $(sel, root = document) { return root.querySelector(sel); }
function $$(sel, root = document) { return Array.from(root.querySelectorAll(sel)); }

async function main() {
  const mode = await Storage.init();
  const syncEl = document.getElementById("sync-status");
  if (mode === "remote") {
    syncEl.textContent = "Live · Firestore";
    syncEl.classList.add("remote");
    syncEl.title = "Every edit is shared with all viewers in real time";
  } else {
    syncEl.textContent = "Local storage";
    syncEl.title = "Firestore not connected — edits stay in this browser only";
  }
  initCoderPicker();
  wireSidebarControls();
  refreshSidebar();
}

function initCoderPicker() {
  const picker = $("#coder-picker");
  const coders = Storage.getCoders();
  picker.innerHTML = coders
    .map((c) => `<option value="${c.id}">${c.name}${c.role === "ai" ? " (AI)" : ""}</option>`)
    .join("");
  const remembered = localStorage.getItem("abcd-review-current-coder");
  if (remembered && coders.find((c) => c.id === remembered)) {
    picker.value = remembered;
  }
  AppState.currentCoder = picker.value;
  picker.addEventListener("change", () => {
    AppState.currentCoder = picker.value;
    localStorage.setItem("abcd-review-current-coder", picker.value);
  });
}

function wireSidebarControls() {
  const search = $("#search");
  search.addEventListener("input", () => {
    AppState.searchQuery = search.value.trim().toLowerCase();
    refreshSidebar();
  });
  $$(".status-filter").forEach((cb) => {
    cb.addEventListener("change", () => {
      if (cb.checked) AppState.activeFilters.add(cb.value);
      else AppState.activeFilters.delete(cb.value);
      refreshSidebar();
    });
  });
}

function refreshSidebar() {
  AppState.paperListCache = Storage.listPapers();
  const list = $("#paper-list");
  const q = AppState.searchQuery;
  const filtered = AppState.paperListCache.filter((p) => {
    if (!AppState.activeFilters.has(p.extraction_status)) return false;
    if (!q) return true;
    return (
      p.title.toLowerCase().includes(q) ||
      p.doi.toLowerCase().includes(q) ||
      p.paper_id.toLowerCase().includes(q)
    );
  });
  list.innerHTML = filtered
    .map(
      (p) => `
      <li data-pid="${p.paper_id}" class="${p.paper_id === AppState.currentPaperId ? "active" : ""}">
        <span class="pid">#${p.paper_id}</span>
        <span class="pt">${escapeHtml(p.title)}</span>
        <span class="badge badge-${p.extraction_status}">${STATUS_LABELS[p.extraction_status] || p.extraction_status}</span>
      </li>`
    )
    .join("");
  list.querySelectorAll("li").forEach((li) => {
    li.addEventListener("click", () => loadPaper(li.dataset.pid));
  });

  // progress summary
  const total = AppState.paperListCache.length;
  const byStatus = {};
  AppState.paperListCache.forEach((p) => {
    byStatus[p.extraction_status] = (byStatus[p.extraction_status] || 0) + 1;
  });
  $("#progress-summary").textContent = Object.entries(byStatus)
    .map(([s, n]) => `${STATUS_LABELS[s] || s}: ${n}`)
    .join(" · ") + ` / ${total} total`;
}

async function loadPaper(pid) {
  AppState.currentPaperId = pid;
  refreshSidebar(); // for active highlight
  const paper = await Storage.getPaper(pid);
  renderPaper(paper);
}

function renderPaper(paper) {
  $("#paper-pane-empty").hidden = true;
  const view = $("#paper-view");
  view.hidden = false;
  const tpl = $("#tpl-paper-view").content.cloneNode(true);
  view.innerHTML = "";
  view.appendChild(tpl);

  // Top-level scalar fields
  wireTextField(view, paper, "title");
  wireTextField(view, paper, "authors", "Authors — Last, First; Last, First; ...");
  wireTextField(view, paper, "year", "");
  wireTextField(view, paper, "journal", "");
  wireTextField(view, paper, "doi", "");
  wireTextField(view, paper, "lead_coder", "");
  wireCsvField(view, paper, "contributors", "Comma-separated coder ids");

  const linkEl = view.querySelector("a.doi-link");
  linkEl.href = paper.doi ? `https://doi.org/${paper.doi}` : "#";
  const lastEl = view.querySelector('[data-field="last_updated"]');
  lastEl.textContent = paper.last_updated ? new Date(paper.last_updated).toLocaleString() : "(never)";

  wireStatusBadge(view, paper);
  wireDottedFields(view, paper);
  wirePrimaryModels(view, paper);
  wireExcludedModels(view, paper);
  wireCoderLog(view, paper);
  wireResetButton(view, paper);
}

/* ── text field wiring ──────────────────────────────── */
function wireTextField(root, paper, field, placeholder) {
  const el = root.querySelector(`[data-field="${field}"][data-edit]`);
  if (!el) return;
  el.contentEditable = "true";
  if (placeholder !== undefined) el.dataset.placeholder = placeholder;
  el.textContent = paper[field] || "";
  el.addEventListener("blur", () => {
    const newVal = el.textContent.trim();
    if (newVal === (paper[field] || "")) return;
    paper[field] = newVal;
    autoSave(paper, `Edited ${field}`);
    flash(el);
  });
}

function wireCsvField(root, paper, field, placeholder) {
  const el = root.querySelector(`[data-field="${field}"][data-edit]`);
  if (!el) return;
  el.contentEditable = "true";
  el.dataset.placeholder = placeholder;
  el.textContent = (paper[field] || []).join(", ");
  el.addEventListener("blur", () => {
    const arr = el.textContent.split(",").map((s) => s.trim()).filter(Boolean);
    if (JSON.stringify(arr) === JSON.stringify(paper[field] || [])) return;
    paper[field] = arr;
    autoSave(paper, `Edited ${field}`);
    flash(el);
  });
}

function wireStatusBadge(root, paper) {
  const badge = root.querySelector(".status-badge");
  badge.textContent = STATUS_LABELS[paper.extraction_status] || paper.extraction_status;
  badge.className = `status-badge badge-${paper.extraction_status}`;
  badge.title = "Click to change status";
  badge.addEventListener("click", () => {
    const opts = Object.keys(STATUS_LABELS);
    const idx = opts.indexOf(paper.extraction_status);
    const next = opts[(idx + 1) % opts.length];
    paper.extraction_status = next;
    badge.textContent = STATUS_LABELS[next];
    badge.className = `status-badge badge-${next}`;
    autoSave(paper, `Changed status → ${STATUS_LABELS[next]}`);
    refreshSidebar();
  });
}

function wireDottedFields(root, paper) {
  root.querySelectorAll('[data-field*="."][data-edit]').forEach((el) => {
    const [outer, inner] = el.dataset.field.split(".");
    if (!paper[outer]) paper[outer] = {};
    el.contentEditable = "true";
    const edit = el.dataset.edit;

    if (edit === "tribool") {
      el.textContent = paper[outer][inner] === true ? "Yes"
                     : paper[outer][inner] === false ? "No"
                     : paper[outer][inner] === "partial" ? "Partial" : "";
      el.dataset.placeholder = "yes / no / partial";
      el.addEventListener("blur", () => {
        const v = el.textContent.trim().toLowerCase();
        const parsed = v === "yes" || v === "true" ? true
                     : v === "no" || v === "false" ? false
                     : v === "partial" ? "partial" : null;
        if (parsed === paper[outer][inner]) return;
        paper[outer][inner] = parsed;
        el.textContent = parsed === true ? "Yes" : parsed === false ? "No" : parsed === "partial" ? "Partial" : "";
        autoSave(paper, `Set ${outer}.${inner} = ${parsed}`);
      });
    } else {
      el.textContent = paper[outer][inner] || "";
      el.addEventListener("blur", () => {
        const v = el.textContent.trim();
        if (v === (paper[outer][inner] || "")) return;
        paper[outer][inner] = v;
        autoSave(paper, `Edited ${outer}.${inner}`);
        flash(el);
      });
    }
  });
}

/* ── primary models ─────────────────────────────────── */
function wirePrimaryModels(root, paper) {
  const list = root.querySelector('.section[data-section="primary-models"] .model-list');
  list.innerHTML = "";
  (paper.primary_models || []).forEach((model, idx) => {
    list.appendChild(buildModelCard(paper, model, idx));
  });
  root.querySelector('button[data-add="primary_model"]').addEventListener("click", () => {
    paper.primary_models = paper.primary_models || [];
    const newIdx = paper.primary_models.length + 1;
    paper.primary_models.push({
      model_id: `M${newIdx}`,
      name: "",
      location_in_paper: "",
      design: "",
      sample: "",
      iv: "",
      dv: "",
      covariates: [],
      equation: "",
      estimation: "",
      native_metric: "",
      estimates: [],
      iv_axis: [],
      dv_axis: [],
    });
    autoSave(paper, `Added primary model M${newIdx}`);
    wirePrimaryModels(root, paper);
  });
}

function buildModelCard(paper, model, idx) {
  const frag = $("#tpl-model-card").content.cloneNode(true);
  const card = frag.querySelector(".model-card");
  card.dataset.modelIdx = idx;

  const nameInput = card.querySelector(".model-name");
  nameInput.value = model.name || "";
  nameInput.addEventListener("change", () => {
    model.name = nameInput.value.trim();
    autoSave(paper, `Edited model M${idx + 1} name`);
  });

  card.querySelector('button[data-action="delete-model"]').addEventListener("click", () => {
    if (!confirm(`Delete model "${model.name || model.model_id}"?`)) return;
    paper.primary_models.splice(idx, 1);
    autoSave(paper, `Deleted model ${model.model_id}`);
    wirePrimaryModels(document.querySelector("#paper-view"), paper);
  });

  // wire text/textarea fields on the card
  card.querySelectorAll('[data-field]').forEach((el) => {
    const f = el.dataset.field;
    if (f === "covariates_text") {
      // Present covariates as "Name — detail" lines
      const covs = model.covariates || [];
      el.value = covs.map((c) => `${c.name || ""}${c.detail ? " — " + c.detail : ""}`).join("\n");
      el.addEventListener("change", () => {
        model.covariates = el.value
          .split("\n")
          .map((s) => s.trim())
          .filter(Boolean)
          .map((line) => {
            const [name, ...rest] = line.split(/\s*—\s*|\s*--\s*|:\s*/);
            return { name: name.trim(), detail: rest.join(" ").trim() };
          });
        autoSave(paper, `Edited covariates for ${model.model_id}`);
      });
    } else if (["iv", "dv"].includes(f)) {
      // These may be strings (paper 394) or objects (older shape); normalize to string display
      const v = model[f];
      el.value = typeof v === "string" ? v : v ? JSON.stringify(v, null, 2) : "";
      el.addEventListener("change", () => {
        model[f] = el.value.trim();
        autoSave(paper, `Edited ${f} for ${model.model_id}`);
      });
    } else {
      el.value = model[f] || "";
      el.addEventListener("change", () => {
        model[f] = el.value.trim();
        autoSave(paper, `Edited ${f} for ${model.model_id}`);
      });
    }
  });

  // estimates preview
  const prev = card.querySelector(".estimates-preview");
  prev.innerHTML = renderEstimatesTable(model);

  return card;
}

function renderEstimatesTable(model) {
  const ests = model.estimates || [];
  if (!ests.length) {
    return `<em style="color:var(--muted);">No estimates yet. Edit the underlying JSON to add them (a results-table editor is coming).</em>`;
  }
  const nm = model.native_metric || "?";
  const keys = new Set();
  ests.forEach((e) => Object.keys(e).forEach((k) => keys.add(k)));
  const cols = ["iv", "dv", nm, `${nm}_lo`, `${nm}_hi`, "p", "sig"].filter((c) => keys.has(c) || c === nm);
  const rows = ests.map((e) => {
    const cells = cols.map((c) => `<td>${formatCell(e[c])}</td>`).join("");
    return `<tr class="${e.sig ? "sig" : ""}">${cells}</tr>`;
  }).join("");
  return `<table><thead><tr>${cols.map((c) => `<th>${c}</th>`).join("")}</tr></thead><tbody>${rows}</tbody></table>`;
}
function formatCell(v) {
  if (v === null || v === undefined) return "";
  if (v === true) return "✓";
  if (v === false) return "";
  if (typeof v === "number") return Number.isInteger(v) ? String(v) : v.toFixed(3);
  return escapeHtml(String(v));
}

/* ── excluded models ────────────────────────────────── */
function wireExcludedModels(root, paper) {
  const tbody = root.querySelector(".ex-table tbody");
  tbody.innerHTML = "";
  (paper.excluded_models || []).forEach((row, idx) => {
    tbody.appendChild(buildExcludedRow(paper, row, idx));
  });
  root.querySelector('button[data-add="excluded_model"]').addEventListener("click", () => {
    paper.excluded_models = paper.excluded_models || [];
    paper.excluded_models.push({ model: "", location: "", why: "" });
    autoSave(paper, "Added excluded model row");
    wireExcludedModels(root, paper);
  });
}
function buildExcludedRow(paper, row, idx) {
  const tr = document.createElement("tr");
  tr.innerHTML = `
    <td><input type="text" data-field="model"></td>
    <td><input type="text" data-field="location"></td>
    <td><textarea rows="2" data-field="why"></textarea></td>
    <td><button class="delete-btn" data-action="delete-row">×</button></td>
  `;
  tr.querySelectorAll("[data-field]").forEach((el) => {
    const f = el.dataset.field;
    el.value = row[f] || "";
    el.addEventListener("change", () => {
      row[f] = el.value.trim();
      autoSave(paper, `Edited excluded model row ${idx + 1} (${f})`);
    });
  });
  tr.querySelector('button[data-action="delete-row"]').addEventListener("click", () => {
    paper.excluded_models.splice(idx, 1);
    autoSave(paper, `Deleted excluded model row ${idx + 1}`);
    wireExcludedModels(document.querySelector("#paper-view"), paper);
  });
  return tr;
}

/* ── coder log ──────────────────────────────────────── */
function wireCoderLog(root, paper) {
  const ul = root.querySelector(".coder-log");
  const entries = (paper.coder_log || []).slice().reverse();
  ul.innerHTML = entries
    .map((e) => `
      <li>
        <span class="ts">${new Date(e.timestamp).toLocaleString()}</span>
        <span class="who who-${e.coder}">${escapeHtml(e.coder || "?")}</span>
        <span class="change">${escapeHtml(e.change || "")}</span>
      </li>`
    ).join("") || `<li style="color:var(--muted);"><em>No coder activity yet.</em></li>`;

  const form = root.querySelector(".log-form");
  form.addEventListener("submit", async (ev) => {
    ev.preventDefault();
    const input = form.querySelector(".log-input");
    const change = input.value.trim();
    if (!change) return;
    if (!AppState.currentCoder) { alert("Select a coder at the top first."); return; }
    input.value = "";
    await Storage.appendLog(paper.paper_id, { coder: AppState.currentCoder, change });
    loadPaper(paper.paper_id); // re-render
  });
}

function wireResetButton(root, paper) {
  const btn = root.querySelector('button[data-action="reset-empty"]');
  btn.addEventListener("click", async () => {
    if (!confirm(`Reset paper #${paper.paper_id} to empty stub?\n\nThis clears everything you've edited locally on this paper.`)) return;
    Storage.clearOverride(paper.paper_id);
    await loadPaper(paper.paper_id);
    refreshSidebar();
  });
}

/* ── autosave helpers ───────────────────────────────── */
function autoSave(paper, changeLabel) {
  if (!AppState.currentCoder) {
    console.warn("Save aborted: no coder selected");
    return;
  }
  clearTimeout(AppState.saveTimers[paper.paper_id]);
  AppState.saveTimers[paper.paper_id] = setTimeout(async () => {
    paper.coder_log = paper.coder_log || [];
    paper.coder_log.push({
      timestamp: new Date().toISOString(),
      coder: AppState.currentCoder,
      change: changeLabel,
    });
    if (!paper.contributors) paper.contributors = [];
    if (!paper.contributors.includes(AppState.currentCoder)) {
      paper.contributors.push(AppState.currentCoder);
    }
    await Storage.savePaper(paper);
    refreshSidebar();
    // re-render coder log without full reload
    const logRoot = document.querySelector('#paper-view .section[data-section="coder-log"]');
    if (logRoot) wireCoderLog(logRoot.parentElement, paper);
  }, 400);
}

function flash(el) {
  el.classList.remove("saving-flash");
  void el.offsetWidth;
  el.classList.add("saving-flash");
}

function escapeHtml(s) {
  return String(s || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

main().catch((err) => {
  console.error(err);
  alert("Failed to load: " + err.message);
});
