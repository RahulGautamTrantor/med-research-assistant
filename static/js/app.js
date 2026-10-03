/**
 * Medical Research Assistant - Main Application Controller.
 * Seamlessly interfaces with FastAPI backend or client-side Pyodide WebAssembly engine.
 */

// Application State
const state = {
  currentEngine: "detecting", // 'fastapi' | 'pyodide' | 'detecting'
  fastApiAvailable: false,
  activeTab: "case-processor",
  cases: window.SAMPLE_CASES || [],
  papers: window.SAMPLE_PAPERS || [],
  guidelines: window.SAMPLE_GUIDELINES || []
};

// DOM Elements
const engineBadge = document.getElementById("engine-badge");
const engineStatusText = document.getElementById("engine-status-text");
const engineStatusDot = document.getElementById("engine-status-dot");
const engineSwitchBtn = document.getElementById("engine-switch-btn");

// Initialization
document.addEventListener("DOMContentLoaded", async () => {
  setupTabs();
  setupSampleSelectors();
  setupActionButtons();
  await detectAndInitializeEngine();
  renderGuidelineList(state.guidelines);
});

/* ---------------- Engine Detection & Switching ---------------- */
async function detectAndInitializeEngine() {
  updateEngineUI("Checking API connection...", "loading");

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 2000);
    const response = await fetch("/api/health", { signal: controller.signal });
    clearTimeout(timeoutId);

    if (response.ok) {
      const data = await response.json();
      state.fastApiAvailable = true;
      state.currentEngine = "fastapi";
      updateEngineUI("FastAPI Python 3.14 (Local Server)", "ready");
      loadBackendSamples();
      return;
    }
  } catch (e) {
    // Backend API not reachable (running on GitHub Pages or static host)
    console.info("FastAPI backend not detected. Falling back to Pyodide WebAssembly.");
  }

  // Fallback to Pyodide WebAssembly for GitHub Pages
  state.fastApiAvailable = false;
  state.currentEngine = "pyodide";
  updateEngineUI("Initializing Pyodide Wasm...", "loading");

  try {
    await window.initPyodideEngine((msg, status) => {
      updateEngineUI(msg, status);
    });
    updateEngineUI("Python 3 Wasm (GitHub Pages Mode)", "ready");
  } catch (err) {
    console.error("Pyodide failed to load:", err);
    updateEngineUI("Pyodide Engine Error (Using Client Mock)", "error");
  }
}

function updateEngineUI(label, status) {
  if (engineStatusText) engineStatusText.textContent = label;
  if (engineStatusDot) {
    engineStatusDot.className = "engine-dot " + (status === "loading" ? "loading" : "");
    if (status === "error") {
      engineStatusDot.style.backgroundColor = "var(--accent-red)";
      engineStatusDot.style.boxShadow = "0 0 8px var(--accent-red)";
    } else if (status === "ready") {
      engineStatusDot.style.backgroundColor = "var(--accent-green)";
      engineStatusDot.style.boxShadow = "0 0 8px var(--accent-green)";
    }
  }
}

async function toggleEngine() {
  if (state.currentEngine === "fastapi") {
    state.currentEngine = "pyodide";
    updateEngineUI("Switching to Pyodide Wasm...", "loading");
    await window.initPyodideEngine();
    updateEngineUI("Python 3 Wasm (Client-Side)", "ready");
  } else if (state.fastApiAvailable) {
    state.currentEngine = "fastapi";
    updateEngineUI("FastAPI Python 3.14 (Local Server)", "ready");
  } else {
    alert("FastAPI backend server is not running on this host. Currently executing client-side WebAssembly Python.");
  }
}
if (engineSwitchBtn) engineSwitchBtn.addEventListener("click", toggleEngine);

async function loadBackendSamples() {
  try {
    const res = await fetch("/api/samples");
    if (res.ok) {
      const data = await res.json();
      if (data.cases) state.cases = data.cases;
      if (data.papers) state.papers = data.papers;
      if (data.guidelines) {
        state.guidelines = data.guidelines;
        renderGuidelineList(state.guidelines);
      }
    }
  } catch (err) {
    console.warn("Using bundled client samples:", err);
  }
}

/* ---------------- Tabs ---------------- */
function setupTabs() {
  const tabBtns = document.querySelectorAll(".tab-btn");
  tabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      tabBtns.forEach(b => b.classList.remove("active"));
      document.querySelectorAll(".tab-panel").forEach(p => p.classList.remove("active"));
      
      btn.classList.add("active");
      const targetId = btn.getAttribute("data-tab");
      const targetPanel = document.getElementById(targetId);
      if (targetPanel) targetPanel.classList.add("active");
      state.activeTab = targetId;
    });
  });
}

/* ---------------- Sample Selectors ---------------- */
function setupSampleSelectors() {
  // Case study presets
  const casePresetBtns = document.querySelectorAll(".case-preset-btn");
  casePresetBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      const caseId = btn.getAttribute("data-id");
      const found = state.cases.find(c => c.id === caseId);
      if (found) {
        document.getElementById("case-title").value = found.title;
        const fullCaseText = `DEMOGRAPHICS: ${found.demographics}\n\nHPI: ${found.hpi}\n\nVITALS: ${found.vitals}\n\nPHYSICAL EXAMINATION:\n${found.physical_exam}\n\nLABORATORY DATA:\n${found.labs}\n\nDIAGNOSTIC IMAGING:\n${found.imaging}`;
        document.getElementById("case-input").value = fullCaseText;
      }
    });
  });

  // Paper presets
  const paperPresetBtns = document.querySelectorAll(".paper-preset-btn");
  paperPresetBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      const paperId = btn.getAttribute("data-id");
      const found = state.papers.find(p => p.id === paperId);
      if (found) {
        document.getElementById("paper-title").value = found.title;
        document.getElementById("paper-input").value = found.abstract;
      }
    });
  });

  // Auto-load first sample for both case and paper
  if (casePresetBtns.length > 0) casePresetBtns[0].click();
  if (paperPresetBtns.length > 0) paperPresetBtns[0].click();
}

/* ---------------- Action Buttons ---------------- */
function setupActionButtons() {
  // Analyze Case
  const analyzeBtn = document.getElementById("analyze-case-btn");
  if (analyzeBtn) {
    analyzeBtn.addEventListener("click", handleCaseAnalysis);
  }

  // Summarize Paper
  const summarizeBtn = document.getElementById("summarize-paper-btn");
  if (summarizeBtn) {
    summarizeBtn.addEventListener("click", handlePaperSummarization);
  }

  // Guidelines Search & Filter
  const guidelineSearch = document.getElementById("guideline-search-input");
  const specialtyFilter = document.getElementById("specialty-filter-select");
  if (guidelineSearch) guidelineSearch.addEventListener("input", filterGuidelines);
  if (specialtyFilter) specialtyFilter.addEventListener("change", filterGuidelines);
}

/* ---------------- Case Study Analysis ---------------- */
async function handleCaseAnalysis() {
  const caseText = document.getElementById("case-input").value.trim();
  const caseTitle = document.getElementById("case-title").value.trim();
  const outputContainer = document.getElementById("case-output-container");
  const btn = document.getElementById("analyze-case-btn");

  if (!caseText) {
    alert("Please enter or select a patient clinical case vignette.");
    return;
  }

  btn.disabled = true;
  btn.innerHTML = `<span class="engine-dot loading"></span> Analyzing Case with Python Engine...`;
  outputContainer.innerHTML = `<div class="output-placeholder"><div class="engine-dot loading" style="width:24px;height:24px;margin-bottom:12px;"></div><p>Evaluating clinical features, vitals, biomarkers & differential tiers...</p></div>`;

  try {
    let result = null;
    if (state.currentEngine === "fastapi" && state.fastApiAvailable) {
      const response = await fetch("/api/case/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ case_text: caseText, title: caseTitle || undefined })
      });
      if (!response.ok) throw new Error(`FastAPI error: ${response.statusText}`);
      result = await response.json();
    } else {
      result = await window.pyodideAnalyzeCase(caseText, caseTitle);
    }
    renderCaseAnalysis(result);
  } catch (err) {
    console.error("Case Analysis Error:", err);
    outputContainer.innerHTML = `<div class="alert-box critical"><strong>Analysis Failed:</strong> ${err.message}. Ensure Pyodide or FastAPI backend is active.</div>`;
  } finally {
    btn.disabled = false;
    btn.innerHTML = `<span>⚡</span> Run Specialist Clinical Synthesis`;
  }
}

function renderCaseAnalysis(data) {
  const output = document.getElementById("case-output-container");
  if (!data) return;

  let html = `
    <div class="card" style="margin-bottom: 20px;">
      <div class="card-header">
        <div>
          <h3 class="card-title">${escapeHtml(data.title || "Clinical Synthesis")}</h3>
          <p class="card-subtitle">Synthesized by MD Medicine Reasoning Engine</p>
        </div>
      </div>
  `;

  // Vital & Lab Alerts
  if ((data.vital_alerts && data.vital_alerts.length > 0) || (data.critical_lab_alerts && data.critical_lab_alerts.length > 0)) {
    html += `<div class="section-block"><div class="section-title-sm">🚨 Hemodynamic & Laboratory Alerts</div>`;
    (data.vital_alerts || []).forEach(alert => {
      html += `<div class="alert-box ${alert.type}"><strong>Vital Alert:</strong> ${escapeHtml(alert.message)}</div>`;
    });
    (data.critical_lab_alerts || []).forEach(alert => {
      html += `<div class="alert-box ${alert.type}"><strong>Critical Biomarker:</strong> ${escapeHtml(alert.message)}</div>`;
    });
    html += `</div>`;
  }

  // Problem Representation
  if (data.problem_representation) {
    html += `
      <div class="section-block">
        <div class="section-title-sm">🩺 Specialist Problem Representation</div>
        <div class="problem-box">${escapeHtml(data.problem_representation)}</div>
      </div>
    `;
  }

  // 3-Tier Differential Diagnoses
  if (data.differentials) {
    html += `<div class="section-block"><div class="section-title-sm">🎯 3-Tier Differential Diagnoses</div>`;
    
    // Tier 1: High Probability
    if (data.differentials.high_probability && data.differentials.high_probability.length > 0) {
      data.differentials.high_probability.forEach(item => {
        html += `
          <div class="diff-card">
            <div class="diff-header">
              <span class="diff-diagnosis">${escapeHtml(item.diagnosis)}</span>
              <span class="tier-badge tier-1">Tier 1: High Probability (${escapeHtml(item.probability || "Leading")})</span>
            </div>
            <p class="diff-text"><strong>Supporting:</strong> ${escapeHtml(item.supporting_features)}</p>
            ${item.contra_features ? `<p class="diff-text" style="color:var(--text-muted); margin-top:4px;"><strong>Differentiating:</strong> ${escapeHtml(item.contra_features)}</p>` : ""}
          </div>
        `;
      });
    }

    // Tier 2: Cannot-Miss Emergencies
    if (data.differentials.cannot_miss_emergencies && data.differentials.cannot_miss_emergencies.length > 0) {
      data.differentials.cannot_miss_emergencies.forEach(item => {
        html += `
          <div class="diff-card" style="border-left: 3px solid var(--accent-red);">
            <div class="diff-header">
              <span class="diff-diagnosis" style="color:#fca5a5;">${escapeHtml(item.diagnosis)}</span>
              <span class="tier-badge tier-2">Tier 2: Cannot-Miss Emergency (${escapeHtml(item.severity || "STAT")})</span>
            </div>
            <p class="diff-text">${escapeHtml(item.rationale)}</p>
          </div>
        `;
      });
    }

    // Tier 3: Rare Zebras
    if (data.differentials.rare_zebras && data.differentials.rare_zebras.length > 0) {
      data.differentials.rare_zebras.forEach(item => {
        html += `
          <div class="diff-card">
            <div class="diff-header">
              <span class="diff-diagnosis">${escapeHtml(item.diagnosis)}</span>
              <span class="tier-badge tier-3">Tier 3: Zebra / Atypical</span>
            </div>
            <p class="diff-text">${escapeHtml(item.rationale)}</p>
          </div>
        `;
      });
    }

    // Fallback if differentials is an array
    if (Array.isArray(data.differentials)) {
      data.differentials.forEach(diff => {
        html += `
          <div class="diff-card">
            <div class="diff-header">
              <span class="diff-diagnosis">${escapeHtml(diff.diagnosis || diff)}</span>
              <span class="tier-badge tier-1">Differential</span>
            </div>
            <p class="diff-text">${escapeHtml(diff.rationale || "")}</p>
          </div>
        `;
      });
    }

    html += `</div>`;
  }

  // Diagnostic Workup & Initial Management
  html += `
    <div class="detail-grid">
      <div class="detail-block">
        <h4>🔬 Targeted Diagnostic Workup</h4>
  `;
  if (data.diagnostic_workup && data.diagnostic_workup.length > 0) {
    data.diagnostic_workup.forEach(tierObj => {
      html += `<div style="font-size:12px; font-weight:700; color:var(--accent-cyan); margin: 8px 0 4px;">${escapeHtml(tierObj.tier || "Workup Tier")}</div><ul class="detail-list">`;
      (tierObj.tests || []).forEach(test => {
        html += `<li>${escapeHtml(test)}</li>`;
      });
      html += `</ul>`;
    });
  } else {
    html += `<ul class="detail-list"><li>Routine comprehensive diagnostic evaluation indicated.</li></ul>`;
  }
  html += `
      </div>
      <div class="detail-block">
        <h4>💊 Initial Evidence-Based Management</h4>
  `;
  if (data.management_protocol) {
    if (data.management_protocol.clinical_score) {
      html += `<div style="font-size:12px; background:rgba(6,182,212,0.1); border:1px solid rgba(6,182,212,0.3); padding:6px 10px; border-radius:4px; margin-bottom:8px; color:#bae6fd;"><strong>Clinical Score:</strong> ${escapeHtml(data.management_protocol.clinical_score)}</div>`;
    }
    if (data.management_protocol.initial_regimen && data.management_protocol.initial_regimen.length > 0) {
      html += `<div style="font-size:12px; font-weight:700; color:var(--accent-teal); margin-bottom:4px;">Primary Regimen:</div><ul class="detail-list">`;
      data.management_protocol.initial_regimen.forEach(act => {
        html += `<li>${escapeHtml(act)}</li>`;
      });
      html += `</ul>`;
    }
    if (data.management_protocol.prophylaxis && data.management_protocol.prophylaxis.length > 0) {
      html += `<div style="font-size:12px; font-weight:700; color:var(--accent-amber); margin:8px 0 4px;">Prophylaxis & Protection:</div><ul class="detail-list">`;
      data.management_protocol.prophylaxis.forEach(pr => {
        html += `<li>${escapeHtml(pr)}</li>`;
      });
      html += `</ul>`;
    }
    if (data.management_protocol.monitoring) {
      html += `<div style="font-size:11px; color:var(--text-muted); margin-top:8px;"><strong>Monitoring:</strong> ${escapeHtml(data.management_protocol.monitoring)}</div>`;
    }
  } else {
    html += `<ul class="detail-list"><li>Hemodynamic stabilization & supportive therapy.</li></ul>`;
  }
  html += `
      </div>
    </div>
  `;

  // Red Flags & Specialist Consultations
  if ((data.red_flags && data.red_flags.length > 0) || (data.specialist_consultations && data.specialist_consultations.length > 0)) {
    html += `<div class="detail-grid" style="margin-top: 16px;">`;
    if (data.red_flags && data.red_flags.length > 0) {
      html += `
        <div class="detail-block" style="border-color: rgba(239, 68, 68, 0.4);">
          <h4 style="color:var(--accent-red);">⚠️ High-Risk Red Flags</h4>
          <ul class="detail-list">
      `;
      data.red_flags.forEach(flag => {
        html += `<li style="color:#fca5a5;">${escapeHtml(flag)}</li>`;
      });
      html += `</ul></div>`;
    }
    if (data.specialist_consultations && data.specialist_consultations.length > 0) {
      html += `
        <div class="detail-block">
          <h4 style="color:var(--accent-purple);">🩺 Subspecialty Consultations</h4>
          <ul class="detail-list">
      `;
      data.specialist_consultations.forEach(c => {
        html += `<li><strong>${escapeHtml(c)}</strong></li>`;
      });
      html += `</ul></div>`;
    }
    html += `</div>`;
  }

  html += `</div>`;
  output.innerHTML = html;
}

/* ---------------- Research Paper Summarization ---------------- */
async function handlePaperSummarization() {
  const paperText = document.getElementById("paper-input").value.trim();
  const paperTitle = document.getElementById("paper-title").value.trim();
  const outputContainer = document.getElementById("paper-output-container");
  const btn = document.getElementById("summarize-paper-btn");

  if (!paperText) {
    alert("Please enter or select a clinical paper abstract.");
    return;
  }

  btn.disabled = true;
  btn.innerHTML = `<span class="engine-dot loading"></span> Parsing Trial & Statistics...`;
  outputContainer.innerHTML = `<div class="output-placeholder"><div class="engine-dot loading" style="width:24px;height:24px;margin-bottom:12px;"></div><p>Extracting PICO, calculating ARR/NNT & synthesizing MD takeaways...</p></div>`;

  try {
    let result = null;
    if (state.currentEngine === "fastapi" && state.fastApiAvailable) {
      const response = await fetch("/api/paper/summarize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ paper_text: paperText, title: paperTitle || undefined })
      });
      if (!response.ok) throw new Error(`FastAPI error: ${response.statusText}`);
      result = await response.json();
    } else {
      result = await window.pyodideSummarizePaper(paperText, paperTitle);
    }
    renderPaperSummary(result);
  } catch (err) {
    console.error("Paper Summarization Error:", err);
    outputContainer.innerHTML = `<div class="alert-box critical"><strong>Summarization Failed:</strong> ${err.message}.</div>`;
  } finally {
    btn.disabled = false;
    btn.innerHTML = `<span>📑</span> Generate Trial Analysis & MD Summary`;
  }
}

function renderPaperSummary(data) {
  const output = document.getElementById("paper-output-container");
  if (!data) return;

  let html = `
    <div class="card" style="margin-bottom: 20px;">
      <div class="card-header">
        <div>
          <h3 class="card-title">${escapeHtml(data.title || "Trial Summary")}</h3>
          <p class="card-subtitle">${escapeHtml(data.study_type || "Clinical Trial")} • ${escapeHtml(data.sample_size || "")} • Follow-up: ${escapeHtml(data.follow_up || "")}</p>
        </div>
      </div>
  `;

  // PICO Framework
  if (data.pico) {
    html += `
      <div class="section-block">
        <div class="section-title-sm">📋 PICO Trial Framework</div>
        <div class="detail-grid">
          <div class="detail-block">
            <h4>Population (P)</h4>
            <p style="font-size:13px; color:var(--text-secondary);">${escapeHtml(data.pico.population)}</p>
          </div>
          <div class="detail-block">
            <h4>Intervention (I) vs Control (C)</h4>
            <p style="font-size:13px; color:var(--text-secondary);"><strong>Intervention:</strong> ${escapeHtml(data.pico.intervention)}</p>
            <p style="font-size:13px; color:var(--text-secondary); margin-top:6px;"><strong>Comparator:</strong> ${escapeHtml(data.pico.comparator)}</p>
          </div>
        </div>
        <div class="detail-block" style="margin-top: 12px;">
          <h4>Prespecified Primary Endpoint (O)</h4>
          <p style="font-size:13px; color:var(--text-secondary);">${escapeHtml(data.pico.outcomes.primary_composite || data.pico.outcomes)}</p>
        </div>
      </div>
    `;
  }

  // Statistical Endpoints Table
  if (data.statistical_findings && data.statistical_findings.length > 0) {
    html += `
      <div class="section-block">
        <div class="section-title-sm">📊 Statistical Findings & Clinical Magnitude</div>
        <div class="table-wrapper">
          <table class="stats-table">
            <thead>
              <tr>
                <th>Outcome Metric</th>
                <th>Hazard / Rate Ratio</th>
                <th>95% CI</th>
                <th>P-Value</th>
                <th>ARR</th>
                <th>NNT</th>
              </tr>
            </thead>
            <tbody>
    `;
    data.statistical_findings.forEach(row => {
      html += `
        <tr>
          <td style="font-weight:600; color:#fff;">${escapeHtml(row.metric)}</td>
          <td class="metric-highlight">${escapeHtml(row.hazard_ratio)}</td>
          <td>${escapeHtml(row.ci_95)}</td>
          <td>${escapeHtml(row.p_value)}</td>
          <td><span style="color:var(--accent-green); font-weight:600;">${escapeHtml(row.arr || "—")}</span></td>
          <td><span style="color:var(--accent-cyan); font-weight:600;">${escapeHtml(row.nnt || "—")}</span></td>
        </tr>
      `;
    });
    html += `
            </tbody>
          </table>
        </div>
      </div>
    `;
  }

  // Methodological Strengths & Limitations
  if (data.methodological_critique) {
    html += `
      <div class="detail-grid">
        <div class="detail-block">
          <h4 style="color:var(--accent-green);">✅ Methodological Strengths</h4>
          <ul class="detail-list">
    `;
    (data.methodological_critique.strengths || []).forEach(s => {
      html += `<li>${escapeHtml(s)}</li>`;
    });
    html += `
          </ul>
        </div>
        <div class="detail-block">
          <h4 style="color:var(--accent-amber);">⚠️ Methodological Limitations</h4>
          <ul class="detail-list">
    `;
    (data.methodological_critique.limitations || []).forEach(l => {
      html += `<li>${escapeHtml(l)}</li>`;
    });
    html += `
          </ul>
        </div>
      </div>
    `;
  }

  // Practice Changing Takeaway
  if (data.practice_changing_takeaway) {
    html += `
      <div class="section-block" style="margin-top: 20px;">
        <div class="section-title-sm">💡 Practice-Changing Takeaway for MD Specialists</div>
        <div class="takeaway-box">
          ${escapeHtml(data.practice_changing_takeaway)}
        </div>
      </div>
    `;
  }

  html += `</div>`;
  output.innerHTML = html;
}

/* ---------------- Guidelines Explorer ---------------- */
async function filterGuidelines() {
  const query = (document.getElementById("guideline-search-input").value || "").trim();
  const specialty = (document.getElementById("specialty-filter-select").value || "").trim();

  if (state.currentEngine === "fastapi" && state.fastApiAvailable) {
    try {
      const url = new URL("/api/guidelines", window.location.origin);
      if (query) url.searchParams.set("query", query);
      if (specialty) url.searchParams.set("specialty", specialty);
      const res = await fetch(url);
      if (res.ok) {
        const data = await res.json();
        renderGuidelineList(data.guidelines || []);
        return;
      }
    } catch (e) {
      console.warn("FastAPI guideline fetch failed, using fallback:", e);
    }
  }

  // Pyodide or client-side filtering
  if (window.pyodideSearchGuidelines && state.currentEngine === "pyodide") {
    try {
      const res = await window.pyodideSearchGuidelines(query, specialty);
      renderGuidelineList(res);
      return;
    } catch (e) {
      console.warn("Pyodide guideline search failed, using client data:", e);
    }
  }

  // Pure JS fallback filtering on state.guidelines
  let filtered = state.guidelines;
  if (specialty && specialty.toLowerCase() !== "all") {
    filtered = filtered.filter(g => (g.specialty || "").toLowerCase().includes(specialty.toLowerCase()));
  }
  if (query) {
    const q = query.toLowerCase();
    filtered = filtered.filter(g =>
      (g.name || "").toLowerCase().includes(q) ||
      (g.society || "").toLowerCase().includes(q) ||
      (g.pillars || []).some(p =>
        (p.drug_class || "").toLowerCase().includes(q) ||
        (p.pearls || "").toLowerCase().includes(q)
      )
    );
  }
  renderGuidelineList(filtered);
}

function renderGuidelineList(list) {
  const container = document.getElementById("guidelines-list-container");
  if (!container) return;

  if (!list || list.length === 0) {
    container.innerHTML = `<div class="output-placeholder"><div class="icon">🔍</div><p>No guidelines found matching your search criteria.</p></div>`;
    return;
  }

  let html = "";
  list.forEach(g => {
    html += `
      <div class="guideline-item">
        <div class="guideline-header">
          <div>
            <h3 style="font-size: 16px; font-weight: 700; color: #fff;">${escapeHtml(g.name)}</h3>
            <p style="font-size: 13px; color: var(--text-secondary); margin-top: 2px;">
              <strong>${escapeHtml(g.society)}</strong> • ${escapeHtml(g.version || "Current Guideline")}
            </p>
          </div>
          <span class="guideline-badge">${escapeHtml(g.specialty)}</span>
        </div>

        <div class="pillar-grid">
    `;

    (g.pillars || []).forEach(p => {
      html += `
        <div class="pillar-card">
          <div class="pillar-class">${escapeHtml(p.drug_class)}</div>
          <span class="pillar-rec">${escapeHtml(p.recommendation)}</span>
          <div class="pillar-dosing"><strong>Start:</strong> ${escapeHtml(p.starting_dose)}</div>
          <div class="pillar-dosing"><strong>Target:</strong> ${escapeHtml(p.target_dose)}</div>
          <div class="pillar-pearls">💡 ${escapeHtml(p.pearls)}</div>
        </div>
      `;
    });

    html += `
        </div>
    `;

    if (g.device_therapy) {
      html += `
        <div style="margin-top: 14px; padding: 10px 14px; background: rgba(56, 189, 248, 0.08); border-left: 3px solid var(--accent-cyan); border-radius: 4px; font-size: 12px; color: #bae6fd;">
          <strong>Device & Escalation Pathway:</strong> ${escapeHtml(g.device_therapy)}
        </div>
      `;
    }

    html += `</div>`;
  });

  container.innerHTML = html;
}

/* ---------------- Utilities ---------------- */
function escapeHtml(str) {
  if (typeof str !== "string") return str;
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
