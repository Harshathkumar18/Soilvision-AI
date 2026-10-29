/* ============================================================
   SoilVision AI — Analyzer Dashboard JavaScript
   Handles form submission, API calls, chart rendering, results display
   ============================================================ */

'use strict';

// ── State ──────────────────────────────────────────────────
let radarChartInst = null;
let npkChartInst   = null;
let currentRecordId = null;

// ── DOM Refs ───────────────────────────────────────────────
const form           = document.getElementById('soilForm');
const analyzeBtn     = document.getElementById('analyzeBtn');
const resultsPlaceholder = document.getElementById('resultsPlaceholder');
const scanAnim       = document.getElementById('scanAnimation');
const resultsArea    = document.getElementById('resultsArea');
const resetBtn       = document.getElementById('resetBtn');

// ── Tab Switching ──────────────────────────────────────────
window.switchTab = function(tab, btn) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById('tab-' + tab).classList.add('active');
};

// ── Inline Upload (pre-fill form) ──────────────────────────
const inlineFileInput  = document.getElementById('inlineFileInput');
const inlineUploadZone = document.getElementById('inlineUploadZone');
const inlineUploadStatus = document.getElementById('inlineUploadStatus');

function showUploadStatus(html) {
  inlineUploadStatus.innerHTML = html;
  inlineUploadStatus.style.display = 'block';
}

if (inlineFileInput) {
  inlineFileInput.addEventListener('change', handleInlineUpload);
}
if (inlineUploadZone) {
  inlineUploadZone.addEventListener('dragover', e => { e.preventDefault(); inlineUploadZone.classList.add('dragover'); });
  inlineUploadZone.addEventListener('dragleave', () => inlineUploadZone.classList.remove('dragover'));
  inlineUploadZone.addEventListener('drop', e => {
    e.preventDefault();
    inlineUploadZone.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file) { inlineFileInput.files = e.dataTransfer.files; handleInlineUpload(); }
  });
}

async function handleInlineUpload() {
  const file = inlineFileInput.files[0];
  if (!file) return;
  showUploadStatus('<div class="scan-animation active" style="padding:1rem;"><div class="scan-circle"></div><span class="text-sm text-muted">Extracting parameters…</span></div>');
  const fd = new FormData();
  fd.append('report_file', file);
  try {
    const res = await fetch('/api/upload', { method: 'POST', body: fd });
    const data = await res.json();
    if (data.error) { showUploadStatus(`<div class="alert alert-danger"><i class="fa-solid fa-circle-xmark"></i> ${data.error}</div>`); return; }
    const extracted = data.extracted || {};
    let filled = 0;
    const mapping = { ph:'ph', ec:'ec', oc:'oc', nitrogen:'nitrogen', phosphorus:'phosphorus', potassium:'potassium', zinc:'zinc', iron:'iron', copper:'copper', manganese:'manganese', boron:'boron', sulphur:'sulphur' };
    Object.entries(mapping).forEach(([key, name]) => {
      if (extracted[key] !== undefined && extracted[key] !== null) {
        const el = form.querySelector(`[name="${name}"]`);
        if (el) { el.value = extracted[key]; filled++; }
      }
    });
    showUploadStatus(`<div class="alert alert-success"><i class="fa-solid fa-circle-check"></i> Extracted ${filled} parameter${filled!==1?'s':''} from report. Review and click "Analyze Soil Health".</div>`);
    switchTab('manual', document.querySelectorAll('.tab-btn')[0]);
  } catch(e) {
    showUploadStatus(`<div class="alert alert-danger"><i class="fa-solid fa-circle-xmark"></i> Upload failed. Please try again.</div>`);
  }
}

// ── Form Submission ────────────────────────────────────────
if (form) {
  form.addEventListener('submit', async e => {
    e.preventDefault();
    await runAnalysis();
  });
}

async function runAnalysis() {
  const fd = new FormData(form);
  const data = {};
  fd.forEach((v, k) => { if (v.trim()) data[k] = v.trim(); });

  // Require at least pH or one nutrient
  const hasNum = ['ph','ec','oc','nitrogen','phosphorus','potassium'].some(k => data[k]);
  if (!hasNum) {
    alert('Please enter at least one soil parameter (e.g. Soil pH) to begin analysis.');
    return;
  }

  // Show scanning state
  resultsPlaceholder.style.display = 'none';
  resultsArea.classList.remove('active');
  scanAnim.classList.add('active');
  analyzeBtn.classList.add('btn-loading');
  analyzeBtn.disabled = true;

  try {
    const res = await fetch('/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error('Server error ' + res.status);
    const analysis = await res.json();
    currentRecordId = analysis.record_id;
    renderResults(analysis, data);
  } catch(err) {
    scanAnim.classList.remove('active');
    resultsPlaceholder.style.display = 'block';
    resultsPlaceholder.innerHTML = `<div class="no-data"><i class="fa-solid fa-circle-xmark" style="color:#f87171;"></i><p>Analysis failed: ${err.message}</p><button class="btn btn-secondary btn-sm" onclick="location.reload()">Reload</button></div>`;
  } finally {
    analyzeBtn.classList.remove('btn-loading');
    analyzeBtn.disabled = false;
  }
}

// ── Render Results ─────────────────────────────────────────
function renderResults(a, inputData) {
  scanAnim.classList.remove('active');
  resultsArea.classList.add('active');
  resultsArea.scrollIntoView({ behavior: 'smooth', block: 'start' });

  // Health score
  renderScore(a.health_index, a.concerns || []);

  // Insufficient data
  const insuffBanner = document.getElementById('insufficientDataBanner');
  insuffBanner.style.display = a.has_sufficient_data ? 'none' : 'flex';

  // Testing gaps
  renderTestingGaps(a.testing_gaps || []);

  // Charts
  renderCharts(a);

  // Nutrient bars
  renderNutrientBars(a.ratings || {});

  // Concerns
  renderConcerns(a.concerns || []);

  // Strengths
  renderStrengths(a.strengths || []);

  // Crop info
  renderCropInfo(a.target_crop, a.crop_info);

  // Recommendations
  renderRecommendations(a.recommendations || []);

  // Report link
  if (currentRecordId) {
    document.getElementById('viewReportBtn').href = `/report/${currentRecordId}`;
  }
}

// Score Ring
function renderScore(score, concerns) {
  const scoreVal  = document.getElementById('scoreValue');
  const scoreCond = document.getElementById('scoreCondition');
  const scoreDesc = document.getElementById('scoreDesc');
  const circle    = document.getElementById('scoreCircle');

  if (score === null || score === undefined) {
    scoreVal.textContent = 'N/A';
    scoreCond.textContent = 'Insufficient Data';
    scoreCond.style.color = 'var(--clr-text-muted)';
    scoreDesc.textContent = 'Enter more parameters for a complete health index.';
    return;
  }

  // Animate counter
  let cur = 0;
  const target = score;
  const timer = setInterval(() => {
    cur = Math.min(cur + 2, target);
    scoreVal.textContent = cur;
    const offset = 427 - (427 * cur / 100);
    circle.style.strokeDashoffset = offset;
    if (cur >= target) clearInterval(timer);
  }, 20);

  // Condition label
  let cond, color, desc;
  if (score >= 75)      { cond='Excellent'; color='#4ade80';  desc='Your soil is in great shape. Minor optimizations can further improve crop yield potential.'; }
  else if (score >= 55) { cond='Good';      color='#86efac';  desc='Soil health is satisfactory. Address the identified concerns to unlock higher yield potential.'; }
  else if (score >= 35) { cond='Fair';      color='#fbbf24';  desc='Several soil issues need attention. Follow the recommendations below to improve soil condition.'; }
  else                  { cond='Poor';      color='#f87171';  desc='Critical soil health issues detected. Immediate corrective action is strongly recommended.'; }

  scoreCond.textContent = cond;
  scoreCond.style.color = color;
  scoreDesc.textContent = desc;
}

// Testing Gaps
function renderTestingGaps(gaps) {
  const section = document.getElementById('testingGapsSection');
  const list    = document.getElementById('testingGapsList');
  if (!gaps.length) { section.style.display = 'none'; return; }
  section.style.display = 'block';
  list.innerHTML = gaps.map(g => `
    <div class="testing-gap-item">
      <i class="fa-solid fa-circle-exclamation"></i>
      <span>${g}</span>
    </div>`).join('');
}

// Charts
function renderCharts(a) {
  const radarData = a.radar_data || {};
  const ratings   = a.ratings || {};

  // Radar
  if (radarChartInst) { radarChartInst.destroy(); radarChartInst = null; }
  const radarLabels = Object.keys(radarData);
  const radarVals   = Object.values(radarData);

  if (radarLabels.length >= 2) {
    const radarCtx = document.getElementById('radarChart');
    radarChartInst = new Chart(radarCtx, {
      type: 'radar',
      data: {
        labels: radarLabels,
        datasets: [{
          label: 'Soil Health',
          data: radarVals,
          backgroundColor: 'rgba(34,197,94,0.15)',
          borderColor: '#22c55e',
          pointBackgroundColor: '#22c55e',
          pointRadius: 4,
          borderWidth: 2
        }]
      },
      options: {
        responsive: true, maintainAspectRatio: true,
        scales: {
          r: {
            min: 0, max: 100,
            backgroundColor: 'rgba(0,0,0,0)',
            grid:      { color: 'rgba(255,255,255,0.07)' },
            angleLines: { color: 'rgba(255,255,255,0.07)' },
            ticks: { display: false, stepSize: 25 },
            pointLabels: { color: '#7aaa7a', font: { size: 11, family: 'Inter' } }
          }
        },
        plugins: { legend: { display: false } }
      }
    });
  }

  // NPK Bar
  if (npkChartInst) { npkChartInst.destroy(); npkChartInst = null; }
  const npkKeys    = ['nitrogen','phosphorus','potassium'];
  const npkLabels  = ['Nitrogen (N)','Phosphorus (P)','Potassium (K)'];
  const npkVals    = npkKeys.map(k => ratings[k] ? ratings[k].value : null);
  const npkOptimal = [420, 17.5, 195];
  const validNPK   = npkVals.some(v => v !== null);

  if (validNPK) {
    const npkCtx = document.getElementById('npkChart');
    npkChartInst = new Chart(npkCtx, {
      type: 'bar',
      data: {
        labels: npkLabels,
        datasets: [
          {
            label: 'Your Soil',
            data: npkVals,
            backgroundColor: ['rgba(34,197,94,0.7)','rgba(59,130,246,0.7)','rgba(245,158,11,0.7)'],
            borderColor:     ['#22c55e','#3b82f6','#f59e0b'],
            borderWidth: 1, borderRadius: 6
          },
          {
            label: 'Optimal Midpoint',
            data: npkOptimal,
            backgroundColor: 'rgba(255,255,255,0.06)',
            borderColor: 'rgba(255,255,255,0.2)',
            borderWidth: 1, borderRadius: 6, type: 'bar'
          }
        ]
      },
      options: {
        responsive: true, maintainAspectRatio: true,
        plugins: {
          legend: { labels: { color: '#7aaa7a', font: { size: 11 } } },
          tooltip: { callbacks: { label: ctx => ` ${ctx.dataset.label}: ${ctx.raw} kg/ha` } }
        },
        scales: {
          x: { ticks: { color: '#7aaa7a' }, grid: { color: 'rgba(255,255,255,0.05)' } },
          y: { ticks: { color: '#7aaa7a' }, grid: { color: 'rgba(255,255,255,0.05)' } }
        }
      }
    });
  }
}

// Nutrient bars
const BAR_PARAM_CONFIG = {
  ph:         { label:'Soil pH',          min:0,  max:14,  unit:'',      optMin:6.5, optMax:7.5 },
  ec:         { label:'EC (dS/m)',         min:0,  max:8,   unit:' dS/m', optMin:0, optMax:1.0 },
  oc:         { label:'Organic Carbon',   min:0,  max:3,   unit:'%',     optMin:0.75, optMax:3 },
  nitrogen:   { label:'Nitrogen (N)',      min:0,  max:800, unit:' kg/ha',optMin:280, optMax:560 },
  phosphorus: { label:'Phosphorus (P)',    min:0,  max:60,  unit:' kg/ha',optMin:10, optMax:25 },
  potassium:  { label:'Potassium (K)',     min:0,  max:400, unit:' kg/ha',optMin:110, optMax:280 },
  zinc:       { label:'Zinc (Zn)',         min:0,  max:4,   unit:' ppm',  optMin:0.6, optMax:4 },
  iron:       { label:'Iron (Fe)',         min:0,  max:20,  unit:' ppm',  optMin:4.5, optMax:20 },
  copper:     { label:'Copper (Cu)',       min:0,  max:5,   unit:' ppm',  optMin:0.2, optMax:5 },
  manganese:  { label:'Manganese (Mn)',    min:0,  max:10,  unit:' ppm',  optMin:2.0, optMax:10 },
  boron:      { label:'Boron (B)',         min:0,  max:3,   unit:' ppm',  optMin:0.5, optMax:3 },
  sulphur:    { label:'Sulphur (S)',       min:0,  max:50,  unit:' ppm',  optMin:10, optMax:50 }
};

function renderNutrientBars(ratings) {
  const container = document.getElementById('nutrientBarsContainer');
  if (!Object.keys(ratings).length) {
    container.innerHTML = '<p class="text-sm text-muted">No evaluated parameters to display.</p>';
    return;
  }
  container.innerHTML = Object.entries(ratings).map(([key, r]) => {
    const cfg = BAR_PARAM_CONFIG[key] || { label: key, min:0, max:100, unit:'' };
    const pct = Math.min(100, Math.max(0, ((r.value - cfg.min) / (cfg.max - cfg.min)) * 100));
    const barClass = r.badge === 'success' ? 'bar-success' : r.badge === 'warning' ? 'bar-warning' : r.badge === 'danger' ? 'bar-danger' : 'bar-info';
    return `
      <div class="nutrient-bar-item">
        <div class="nutrient-bar-header">
          <span class="text-sm" style="font-weight:600;">${cfg.label}</span>
          <div style="display:flex;align-items:center;gap:0.5rem;">
            <span class="badge badge-${r.badge}" style="font-size:0.68rem;">${r.rating}</span>
            <span class="text-sm text-muted">${r.value}${cfg.unit}</span>
          </div>
        </div>
        <div class="nutrient-bar-track">
          <div class="nutrient-bar-fill ${barClass}" style="width:0%" data-target="${pct}"></div>
        </div>
        <div class="text-xs text-faint" style="margin-top:4px;">${r.explanation}</div>
      </div>`;
  }).join('');

  // Animate bars after paint
  requestAnimationFrame(() => {
    setTimeout(() => {
      container.querySelectorAll('.nutrient-bar-fill').forEach(bar => {
        bar.style.width = bar.dataset.target + '%';
      });
    }, 100);
  });
}

// Concerns
function renderConcerns(concerns) {
  const section = document.getElementById('concernsSection');
  const list    = document.getElementById('concernsList');
  if (!concerns.length) { section.style.display = 'none'; return; }
  section.style.display = 'block';
  list.innerHTML = concerns.map(c => `
    <div class="concern-card severity-${c.severity}">
      <div class="concern-card-icon">
        <i class="fa-solid ${c.severity === 'high' ? 'fa-circle-xmark' : 'fa-triangle-exclamation'}"></i>
      </div>
      <div>
        <h4>${c.title} <span class="badge badge-${c.severity === 'high' ? 'danger' : 'warning'}" style="font-size:0.65rem;margin-left:4px;">${c.severity.toUpperCase()}</span></h4>
        <p>${c.description}</p>
      </div>
    </div>`).join('');
}

// Strengths
function renderStrengths(strengths) {
  const section = document.getElementById('strengthsSection');
  const list    = document.getElementById('strengthsList');
  if (!strengths.length) { section.style.display = 'none'; return; }
  section.style.display = 'block';
  list.innerHTML = strengths.map(s => `
    <div class="strength-item">
      <i class="fa-solid fa-circle-check"></i>
      <span>${s}</span>
    </div>`).join('');
}

// Crop info
function renderCropInfo(cropName, cropInfo) {
  const card    = document.getElementById('cropInfoCard');
  const nameEl  = document.getElementById('cropInfoName');
  const content = document.getElementById('cropInfoContent');
  if (!cropInfo || !cropName) { card.style.display = 'none'; return; }
  card.style.display = 'block';
  nameEl.textContent = cropName;
  content.innerHTML = `
    <div class="form-grid-2">
      <div class="report-param-item">
        <div class="report-param-label">Ideal pH Range</div>
        <div class="report-param-value">${cropInfo.ideal_ph ? cropInfo.ideal_ph[0] + ' – ' + cropInfo.ideal_ph[1] : 'N/A'}</div>
      </div>
      <div class="report-param-item">
        <div class="report-param-label">Salinity Tolerance</div>
        <div class="report-param-value" style="font-size:0.95rem;">${cropInfo.salinity_tolerance || 'Medium'}</div>
      </div>
    </div>
    <div style="margin-top:var(--space-4);">
      <div class="report-param-label" style="margin-bottom:6px;">Key Nutrients</div>
      <div style="display:flex;flex-wrap:wrap;gap:6px;">
        ${(cropInfo.key_nutrients || []).map(n => `<span class="tag">${n}</span>`).join('')}
      </div>
    </div>
    ${cropInfo.special_notes ? `<div class="rec-tip" style="margin-top:var(--space-4);"><i class="fa-solid fa-lightbulb"></i><span>${cropInfo.special_notes}</span></div>` : ''}
  `;
}

// Recommendations
function renderRecommendations(recs) {
  const list = document.getElementById('recommendationsList');
  if (!recs.length) {
    list.innerHTML = '<p class="text-muted text-sm">No specific recommendations generated for the provided data.</p>';
    return;
  }
  list.innerHTML = recs.map(r => `
    <div class="rec-card">
      <div class="rec-card-header">
        <div class="rec-icon"><i class="${r.icon || 'fa-solid fa-seedling'}"></i></div>
        <div class="rec-meta">
          <div class="rec-category">${r.category}</div>
          <div class="rec-title">${r.title}</div>
        </div>
        <span class="badge priority-badge-${r.priority}">${r.priority}</span>
      </div>
      <p class="rec-action">${r.action}</p>
      <div class="rec-tip">
        <i class="fa-solid fa-leaf"></i>
        <span><strong>Sustainable Tip:</strong> ${r.sustainable_tip}</span>
      </div>
    </div>`).join('');
}

// Reset
if (resetBtn) {
  resetBtn.addEventListener('click', () => {
    form.reset();
    resultsArea.classList.remove('active');
    scanAnim.classList.remove('active');
    resultsPlaceholder.style.display = 'block';
    resultsPlaceholder.innerHTML = `
      <div style="font-size:3rem;margin-bottom:var(--space-4);opacity:0.3;"><i class="fa-solid fa-flask"></i></div>
      <h3 style="margin-bottom:var(--space-3);color:var(--clr-text-muted);">Results Appear Here</h3>
      <p style="font-size:0.875rem;">Fill in your soil parameters and click "Analyze Soil Health" to see your detailed report.</p>`;
    if (radarChartInst) { radarChartInst.destroy(); radarChartInst = null; }
    if (npkChartInst)   { npkChartInst.destroy();   npkChartInst = null; }
    currentRecordId = null;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}
