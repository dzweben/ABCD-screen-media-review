/*
 * Main app — sidebar list, paper view/editor, coder attribution.
 *
 * Every value edit fires an autosave after a short debounce. Every save
 * appends a coder-log entry unless the write is itself a coder-log push
 * (avoid double-logging).
 */

const STATUS_LABELS = {
  empty: "Empty",
  ai_draft: "Draft",
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

const SITE_PASSWORD = "ABCD";
const PW_OK_KEY = "abcd-review-pw-ok-v1";

async function main() {
  await requirePassword();
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

  await ensureCoderPicked();
  renderCoderChipRow();
  wireSidebarControls();
  refreshSidebar();
}

/* ── password gate ──────────────────────────────────── */
async function requirePassword() {
  if (sessionStorage.getItem(PW_OK_KEY) === "yes") return;
  const gate = document.getElementById("pw-gate");
  const form = document.getElementById("pw-form");
  const input = document.getElementById("pw-input");
  const err = document.getElementById("pw-err");
  gate.hidden = false;
  return new Promise((resolve) => {
    form.addEventListener("submit", (ev) => {
      ev.preventDefault();
      if (input.value === SITE_PASSWORD) {
        sessionStorage.setItem(PW_OK_KEY, "yes");
        gate.hidden = true;
        resolve();
      } else {
        err.hidden = false;
        input.value = "";
        input.focus();
      }
    });
  });
}

/* ── coder picking ──────────────────────────────────── */
async function ensureCoderPicked() {
  const remembered = localStorage.getItem("abcd-review-current-coder");
  const coders = Storage.getCoders();
  if (remembered && coders.find((c) => c.id === remembered)) {
    AppState.currentCoder = remembered;
    return;
  }
  await showWhoModal();
}

async function showWhoModal() {
  const modal = document.getElementById("who-modal");
  const chips = document.getElementById("who-chips");
  const addBtn = document.getElementById("who-add-btn");
  const addInput = document.getElementById("who-add-input");
  modal.hidden = false;
  const coders = Storage.getCoders();
  chips.innerHTML = coders
    .map((c) => `<button class="who-chip ${c.role === "ai" ? "ai" : ""}" data-id="${c.id}">${escapeHtml(c.name)}${c.role === "ai" ? " (AI)" : ""}</button>`)
    .join("");
  return new Promise((resolve) => {
    chips.querySelectorAll(".who-chip").forEach((btn) => {
      btn.addEventListener("click", () => {
        selectCoder(btn.dataset.id);
        modal.hidden = true;
        resolve();
      });
    });
    addBtn.addEventListener("click", async () => {
      const name = addInput.value.trim();
      if (!name) return;
      try {
        const id = await Storage.addCoder({ name, role: "coder" });
        selectCoder(id);
        modal.hidden = true;
        resolve();
      } catch (err) {
        alert("Could not add: " + err.message);
      }
    });
    addInput.addEventListener("keydown", (ev) => {
      if (ev.key === "Enter") { ev.preventDefault(); addBtn.click(); }
    });
  });
}

function selectCoder(id) {
  AppState.currentCoder = id;
  localStorage.setItem("abcd-review-current-coder", id);
  renderCoderChipRow();
  if (AppState.currentPaperId) loadPaper(AppState.currentPaperId);
}

function renderCoderChipRow() {
  const row = document.getElementById("coder-chip-row");
  if (!row) return;
  const coders = Storage.getCoders();
  const chips = coders
    .filter((c) => c.role !== "ai")
    .map((c) => `<button class="mini-chip ${c.id === AppState.currentCoder ? "active" : ""}" data-id="${c.id}" title="Switch identity to ${escapeHtml(c.name)}">${escapeHtml(c.name)}</button>`)
    .join("");
  row.innerHTML = chips + `<button class="mini-chip add" data-add="1" title="Add a new coder">+ Add</button>`;
  row.querySelectorAll("button.mini-chip").forEach((btn) => {
    btn.addEventListener("click", async () => {
      if (btn.dataset.add) {
        await showWhoModal();
      } else {
        selectCoder(btn.dataset.id);
      }
    });
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

  // Derive PDF url from DOI: pdfs/<doi with / -> _>.pdf
  const pdfUrl = paper.pdf_url
    || (paper.doi ? "pdfs/" + paper.doi.trim().replace(/\//g, "_") + ".pdf" : null);
  const pdfLink = view.querySelector(".pdf-link");
  const pdfDl = view.querySelector(".pdf-download");
  const pdfMissing = view.querySelector(".pdf-missing");
  if (pdfUrl) {
    pdfLink.href = pdfUrl;
    pdfLink.hidden = false;
    pdfDl.href = pdfUrl;
    pdfDl.setAttribute("download", `paper_${paper.paper_id}.pdf`);
    pdfDl.hidden = false;
    pdfMissing.hidden = true;
  } else {
    pdfLink.hidden = true;
    pdfDl.hidden = true;
    pdfMissing.hidden = false;
  }

  if (paper.duplicate_of) {
    const b = document.createElement("div");
    b.className = "dup-banner";
    b.innerHTML = `Duplicate record — same paper as <a href="#" data-goto="${escapeHtml(paper.duplicate_of)}">#${escapeHtml(paper.duplicate_of)}</a>. Review and edit there; this copy is kept only so the PRISMA counts reconcile.`;
    b.querySelector("a").onclick = (ev) => { ev.preventDefault(); loadPaper(paper.duplicate_of); };
    view.querySelector(".paper-head").prepend(b);
  }
  wireStatusBadge(view, paper);
  wireDottedFields(view, paper);
  wireReviewBar(view, paper);
  wirePrimaryModels(view, paper);
  wireExcludedModels(view, paper);
  wireSectionApprovals(view, paper);
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

  // Strike-through instead of delete — model stays visible with line-through
  const strikeKey = `primary_models.${idx}`;
  const strikeBtn = card.querySelector('button[data-action="strike-model"]');
  const strikeInfo = getStrike(paper, strikeKey);
  if (strikeInfo) {
    card.classList.add("struck");
    strikeBtn.textContent = "Un-strike";
    strikeBtn.title = `Struck by ${coderName(strikeInfo.coder)} · ${relTime(strikeInfo.ts)}`;
  }
  strikeBtn.addEventListener("click", () => {
    if (strikeInfo) {
      unstrike(paper, strikeKey);
      autoSave(paper, `Removed strike on model ${model.model_id}`);
    } else {
      if (!AppState.currentCoder) { alert("Pick a coder identity first."); return; }
      setStrike(paper, strikeKey, AppState.currentCoder);
      autoSave(paper, `Struck through model ${model.model_id}`);
    }
    wirePrimaryModels(document.querySelector("#paper-view"), paper);
  });

  // Notes block
  wireNotesBlock(card, paper, `primary_models.${idx}`);

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

const NATIVE_KEYS = { B: "B", beta_std: "beta", OR: "OR", RR: "RR", IRR: "IRR", d: "d", r: "r" };

function fmtNum(v, places) {
  if (v === null || v === undefined || v === "") return "";
  if (typeof v !== "number") return escapeHtml(String(v));
  const p = places ?? (Math.abs(v) < 0.1 && v !== 0 ? 3 : 2);
  return (Object.is(Math.round(v * 10 ** p), -0) ? 0 : v).toFixed(p);
}

function renderEstimatesTable(model) {
  const ests = model.estimates || [];
  if (!ests.length) {
    return `<em style="color:var(--muted);">No phone/SM estimates recorded for this model.</em>`;
  }
  const nm = model.native_metric || "?";
  const key = NATIVE_KEYS[nm] || "value";
  const label = nm.startsWith("other:") ? nm.slice(6) : nm;
  const ivs = (model.iv_axis && model.iv_axis.length) ? model.iv_axis : [...new Set(ests.map((e) => e.iv))].map((id) => ({ id, label: id }));
  const dvs = (model.dv_axis && model.dv_axis.length) ? model.dv_axis : [...new Set(ests.map((e) => e.dv))].map((id) => ({ id, label: id }));
  const lookup = new Map(ests.map((e) => [`${e.iv}||${e.dv}`, e]));

  const head = `<tr><th></th>${dvs.map((d) => `<th class="col-head">${d.label}</th>`).join("")}</tr>`;
  const body = ivs.map((iv) => {
    const cells = dvs.map((dv) => {
      const e = lookup.get(`${iv.id}||${dv.id}`);
      if (!e) return `<td class="mcell empty">—</td>`;
      const v = e[key];
      const lo = e[`${key}_lo`], hi = e[`${key}_hi`];
      const ci = (lo !== null && lo !== undefined && hi !== null && hi !== undefined) ? `<span class="ci">[${fmtNum(lo)}, ${fmtNum(hi)}]</span>` : "";
      const p = e.p_label ? `p ${escapeHtml(e.p_label.replace(/^p\s*/i, ""))}` : (e.p !== null && e.p !== undefined ? (e.p < 0.001 ? "p &lt; .001" : `p = ${e.p.toFixed(3).replace(/^0/, "")}`) : "");
      let dLine;
      if (nm === "d") {
        dLine = "";
      } else if (e.derived_d !== null && e.derived_d !== undefined) {
        const dci = (e.derived_d_lo !== null && e.derived_d_lo !== undefined) ? ` <span class="dci">[${fmtNum(e.derived_d_lo, 3)}, ${fmtNum(e.derived_d_hi, 3)}]</span>` : "";
        dLine = `<span class="dline" title="${escapeHtml(e.derived_d_method || "")}">d ≈ ${fmtNum(e.derived_d, 3)}${dci}</span>`;
      } else {
        dLine = `<span class="dline none" title="${escapeHtml(e.derived_d_method || "")}">d: n/a</span>`;
      }
      return `<td class="mcell ${e.sig ? "sig" : ""}" title="${escapeHtml(e.location || "")}${e.note ? " — " + escapeHtml(e.note) : ""}">
        <span class="nv">${escapeHtml(label)} = ${fmtNum(v)}</span>${ci}${p ? `<span class="pv">${p}</span>` : ""}${dLine}</td>`;
    }).join("");
    return `<tr><td class="row-head">${escapeHtml(iv.label)}${iv.meta ? `<div class="iv-meta">${escapeHtml(iv.meta)}</div>` : ""}</td>${cells}</tr>`;
  }).join("");

  const naReasons = [...new Set(ests.filter((e) => nm !== "d" && (e.derived_d === null || e.derived_d === undefined)).map((e) => e.derived_d_method).filter(Boolean))];
  const legend = nm === "d"
    ? `Native metric is already Cohen's d.`
    : `Top: native ${escapeHtml(label)} [95% CI], p. Purple: computed Cohen's d [95% CI].` + (naReasons.length ? ` d not computed where: ${naReasons.map(escapeHtml).join("; ")}.` : "");
  return `<table class="est-matrix"><thead>${head}</thead><tbody>${body}</tbody></table><div class="est-legend">${legend} Green = significant at the paper's α. Hover a cell for its table location.</div>`;
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
  const strikeKey = `excluded_models.${idx}`;
  const strikeInfo = getStrike(paper, strikeKey);
  const tr = document.createElement("tr");
  if (strikeInfo) tr.classList.add("struck");
  tr.innerHTML = `
    <td><input type="text" data-field="model"></td>
    <td><input type="text" data-field="location"></td>
    <td><textarea rows="2" data-field="why"></textarea></td>
    <td>
      <button class="strike-btn" data-action="strike-row" title="${strikeInfo ? "Struck by " + escapeHtml(coderName(strikeInfo.coder)) : "Cross this row out (kept for audit)"}">${strikeInfo ? "Un-strike" : "Strike"}</button>
    </td>
  `;
  tr.querySelectorAll("[data-field]").forEach((el) => {
    const f = el.dataset.field;
    el.value = row[f] || "";
    el.addEventListener("change", () => {
      row[f] = el.value.trim();
      autoSave(paper, `Edited excluded model row ${idx + 1} (${f})`);
    });
  });
  tr.querySelector('button[data-action="strike-row"]').addEventListener("click", () => {
    if (strikeInfo) {
      unstrike(paper, strikeKey);
      autoSave(paper, `Removed strike on excluded row ${idx + 1}`);
    } else {
      if (!AppState.currentCoder) { alert("Pick a coder identity first."); return; }
      setStrike(paper, strikeKey, AppState.currentCoder);
      autoSave(paper, `Struck through excluded row ${idx + 1}`);
    }
    wireExcludedModels(document.querySelector("#paper-view"), paper);
  });
  return tr;
}

/* ── review bar (paper-level agreement chips) ────────── */
function wireReviewBar(root, paper) {
  const chipsEl = root.querySelector(".agree-chips");
  const agreeBtn = root.querySelector(".agree-btn");
  const unagreeBtn = root.querySelector(".unagree-btn");
  const agreements = paper.agreements || {};
  const paperAgree = agreements.paper || {};
  const me = AppState.currentCoder;

  chipsEl.innerHTML = Object.entries(paperAgree)
    .map(([coder, info]) => `<span class="agree-chip" title="${escapeHtml(new Date(info.ts).toLocaleString())}">${escapeHtml(coderName(coder))}</span>`)
    .join("");
  if (!me) {
    agreeBtn.hidden = true;
    unagreeBtn.hidden = true;
  } else if (paperAgree[me]) {
    agreeBtn.hidden = true;
    unagreeBtn.hidden = false;
  } else {
    agreeBtn.hidden = false;
    unagreeBtn.hidden = true;
  }
  agreeBtn.onclick = () => {
    const me = AppState.currentCoder;
    if (!me) return;
    paper.agreements = paper.agreements || {};
    paper.agreements.paper = paper.agreements.paper || {};
    paper.agreements.paper[me] = { ts: new Date().toISOString() };
    autoSave(paper, `${coderName(me)} agreed with the extraction`);
    wireReviewBar(root, paper);
  };
  unagreeBtn.onclick = () => {
    const me = AppState.currentCoder;
    if (!me) return;
    if (paper.agreements?.paper) delete paper.agreements.paper[me];
    autoSave(paper, `${coderName(me)} retracted agreement`);
    wireReviewBar(root, paper);
  };
}

/* ── per-section approvals ──────────────────────────── */
function wireSectionApprovals(root, paper) {
  root.querySelectorAll(".section-approve").forEach((wrap) => {
    const btn = wrap.querySelector(".approve-btn");
    const key = btn.dataset.sectionKey;
    const chips = wrap.querySelector(".approve-chips");
    const agreements = (paper.agreements && paper.agreements[key]) || {};
    chips.innerHTML = Object.entries(agreements)
      .map(([coder, info]) => `<span class="agree-chip small" title="${escapeHtml(new Date(info.ts).toLocaleString())}">${escapeHtml(coderName(coder))}</span>`)
      .join("");
    const me = AppState.currentCoder;
    const iAgreed = me && agreements[me];
    btn.textContent = iAgreed ? "Retract ✓" : "✓ Looks right";
    btn.classList.toggle("done", !!iAgreed);
    btn.onclick = () => {
      const me = AppState.currentCoder;
      if (!me) { alert("Pick a coder identity first."); return; }
      paper.agreements = paper.agreements || {};
      paper.agreements[key] = paper.agreements[key] || {};
      if (paper.agreements[key][me]) {
        delete paper.agreements[key][me];
        autoSave(paper, `${coderName(me)} retracted approval of ${key}`);
      } else {
        paper.agreements[key][me] = { ts: new Date().toISOString() };
        autoSave(paper, `${coderName(me)} approved ${key}`);
      }
      wireSectionApprovals(root, paper);
    };
  });
}

/* ── notes on a model card ─────────────────────────── */
function wireNotesBlock(card, paper, keyPath) {
  const list = card.querySelector(".notes-list");
  const form = card.querySelector(".add-note-form");
  const input = form.querySelector(".add-note-input");
  const notes = (paper.notes && paper.notes[keyPath]) || [];
  list.innerHTML = notes.length
    ? notes
        .map(
          (n, i) => `
        <div class="note">
          <span class="note-who who-${n.coder}">${escapeHtml(coderName(n.coder))}</span>
          <span class="note-ts">${escapeHtml(relTime(n.ts))}</span>
          <div class="note-text">${escapeHtml(n.text)}</div>
        </div>`
        )
        .join("")
    : "";
  form.onsubmit = (ev) => {
    ev.preventDefault();
    const text = input.value.trim();
    if (!text) return;
    if (!AppState.currentCoder) { alert("Pick a coder identity first."); return; }
    paper.notes = paper.notes || {};
    paper.notes[keyPath] = paper.notes[keyPath] || [];
    paper.notes[keyPath].push({
      coder: AppState.currentCoder,
      ts: new Date().toISOString(),
      text,
    });
    input.value = "";
    autoSave(paper, `${coderName(AppState.currentCoder)} added a note`);
    wireNotesBlock(card, paper, keyPath);
  };
}

/* ── strike helpers ─────────────────────────────────── */
function getStrike(paper, keyPath) {
  return paper.strikes && paper.strikes[keyPath];
}
function setStrike(paper, keyPath, coder) {
  paper.strikes = paper.strikes || {};
  paper.strikes[keyPath] = { coder, ts: new Date().toISOString() };
}
function unstrike(paper, keyPath) {
  if (paper.strikes) delete paper.strikes[keyPath];
}
function coderName(id) {
  const c = Storage.getCoders().find((c) => c.id === id);
  return c ? c.name : id;
}
function relTime(iso) {
  if (!iso) return "";
  const d = new Date(iso);
  const secs = (Date.now() - d.getTime()) / 1000;
  if (secs < 60) return "just now";
  if (secs < 3600) return `${Math.floor(secs / 60)}m ago`;
  if (secs < 86400) return `${Math.floor(secs / 3600)}h ago`;
  return d.toLocaleDateString();
}

/* ── autosave helpers ───────────────────────────────── */
function autoSave(paper, changeLabel) {
  if (!AppState.currentCoder) {
    console.warn("Save aborted: no coder selected");
    return;
  }
  paper.last_edited_by = AppState.currentCoder;
  if (!paper.contributors) paper.contributors = [];
  if (!paper.contributors.includes(AppState.currentCoder)) {
    paper.contributors.push(AppState.currentCoder);
  }
  clearTimeout(AppState.saveTimers[paper.paper_id]);
  AppState.saveTimers[paper.paper_id] = setTimeout(async () => {
    await Storage.savePaper(paper);
    refreshSidebar();
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
