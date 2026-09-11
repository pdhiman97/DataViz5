import json

with open('/Users/aashima/Desktop/DataViz5/outcome/loksabha-questions/viz_inline.js') as f:
    inline_data = f.read()

html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Parliamentary Voices — 17th Lok Sabha</title>
<style>
/* ── RESET & TOKENS ── */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0a0a0f;
  --surface:#12121a;
  --border:rgba(255,255,255,0.07);
  --ember:#f07030;
  --ember2:#f8a060;
  --ice:#4a9ed4;
  --cream:#e8e0d0;
  --fog:#9090a0;
  --ash:#4a4a5a;
  --pill-bg:rgba(255,255,255,0.06);
  --pill-hover:rgba(255,255,255,0.12);
  --pill-active-bg:var(--ember);
  --pill-active-text:#0a0a0f;
  --font-serif:'Georgia',serif;
  --font-mono:'SF Mono','Fira Mono','Courier New',monospace;
}
html{font-size:15px;background:var(--bg)}
body{font-family:var(--font-mono);color:var(--cream);min-height:100vh;display:flex;flex-direction:column;overflow-x:hidden}

/* ── LAYOUT ── */
header{padding:2rem 2.5rem 1.2rem;border-bottom:1px solid var(--border)}
.hdr-top{display:flex;align-items:baseline;justify-content:space-between;flex-wrap:wrap;gap:0.5rem}
h1{font-family:var(--font-serif);font-size:1.55rem;font-weight:400;letter-spacing:-0.01em;color:var(--cream)}
h1 em{font-style:italic;color:var(--ember2)}
.hdr-meta{font-size:0.65rem;color:var(--fog);letter-spacing:0.08em;text-transform:uppercase}
.hdr-sub{font-size:0.78rem;color:var(--fog);margin-top:0.5rem;line-height:1.6;max-width:600px}

/* ── FILTER BAR ── */
.filter-bar{display:flex;flex-wrap:wrap;gap:0.9rem;padding:1.1rem 2.5rem;border-bottom:1px solid var(--border);align-items:center}
.filter-group{display:flex;align-items:center;gap:0.5rem;flex-wrap:wrap}
.filter-label{font-size:0.6rem;letter-spacing:0.12em;text-transform:uppercase;color:var(--ash);white-space:nowrap}
.pill{font-family:var(--font-mono);font-size:0.62rem;letter-spacing:0.04em;text-transform:uppercase;padding:0.28rem 0.65rem;border-radius:100px;background:var(--pill-bg);color:var(--fog);border:1px solid var(--border);cursor:pointer;transition:all 0.18s;white-space:nowrap;user-select:none}
.pill:hover{background:var(--pill-hover);color:var(--cream);border-color:rgba(255,255,255,0.18)}
.pill.active{background:var(--ember);color:#0a0a0f;border-color:var(--ember);font-weight:700}
.pill.party-active{border-color:currentColor}
.sep{width:1px;height:20px;background:var(--border);margin:0 0.2rem}

/* Search box */
.search-wrap{position:relative;margin-left:auto}
#mp-search{background:var(--pill-bg);border:1px solid var(--border);color:var(--cream);font-family:var(--font-mono);font-size:0.7rem;padding:0.3rem 0.7rem 0.3rem 1.8rem;border-radius:100px;outline:none;width:180px;transition:border-color 0.2s}
#mp-search::placeholder{color:var(--ash)}
#mp-search:focus{border-color:rgba(255,255,255,0.25)}
.search-icon{position:absolute;left:0.55rem;top:50%;transform:translateY(-50%);color:var(--ash);font-size:0.7rem;pointer-events:none}

/* ── MAIN VIZ ── */
main{flex:1;display:grid;grid-template-columns:1fr 340px;gap:0;height:calc(100vh - 165px)}
@media(max-width:900px){main{grid-template-columns:1fr;height:auto}}

/* Dot field */
#dot-field{position:relative;overflow:hidden;background:var(--bg)}
#dot-canvas{position:absolute;inset:0;width:100%;height:100%}
.field-overlay{position:absolute;inset:0;pointer-events:none}

/* Sector axis labels */
#sector-axis{position:absolute;bottom:0;left:0;right:0;height:40px;display:flex;align-items:center;padding:0 2rem;pointer-events:none}
.axis-label{font-size:0.58rem;color:var(--ash);letter-spacing:0.05em;text-transform:uppercase;text-align:center;flex:1}

/* Y axis */
#y-axis{position:absolute;top:0;bottom:40px;left:0;width:40px;display:flex;flex-direction:column;justify-content:space-between;align-items:flex-end;padding:0.5rem 0.4rem;pointer-events:none}
.y-tick{font-size:0.55rem;color:var(--ash)}

/* Hint */
#field-hint{position:absolute;top:0.8rem;right:1rem;font-size:0.58rem;color:var(--ash);letter-spacing:0.06em;pointer-events:none}

/* ── SIDE PANEL ── */
#side-panel{background:var(--surface);border-left:1px solid var(--border);display:flex;flex-direction:column;overflow-y:auto}
.panel-header{padding:1.2rem 1.4rem 0.8rem;border-bottom:1px solid var(--border);flex-shrink:0}
.panel-title{font-size:0.62rem;letter-spacing:0.12em;text-transform:uppercase;color:var(--ash);margin-bottom:0.4rem}

/* Stats strip */
.stats-strip{display:grid;grid-template-columns:1fr 1fr 1fr;gap:1px;background:var(--border);border-bottom:1px solid var(--border);flex-shrink:0}
.stat-box{background:var(--surface);padding:0.9rem 1rem}
.stat-num{font-family:var(--font-serif);font-size:1.5rem;color:var(--cream);line-height:1}
.stat-lbl{font-size:0.58rem;color:var(--fog);letter-spacing:0.08em;text-transform:uppercase;margin-top:0.2rem}

/* Sector breakdown */
.breakdown{padding:1rem 1.4rem;flex:1}
.breakdown-title{font-size:0.6rem;letter-spacing:0.1em;text-transform:uppercase;color:var(--ash);margin-bottom:1rem}
.sector-row{margin-bottom:0.65rem}
.sector-meta{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:0.25rem}
.sector-name{font-size:0.72rem;color:var(--fog)}
.sector-val{font-size:0.7rem;color:var(--cream);font-weight:700}
.sector-track{height:4px;background:rgba(255,255,255,0.06);border-radius:2px;position:relative;overflow:visible}
.sector-bar{height:100%;border-radius:2px;transition:width 0.5s cubic-bezier(0.4,0,0.2,1)}
.sector-avg-tick{position:absolute;top:-2px;bottom:-2px;width:2px;background:var(--fog);border-radius:1px;opacity:0.5}

/* MP card (appears on dot hover) */
#mp-card{padding:1rem 1.4rem;border-top:1px solid var(--border);flex-shrink:0}
.mp-name{font-family:var(--font-serif);font-size:1rem;color:var(--cream);margin-bottom:0.2rem}
.mp-meta{font-size:0.65rem;color:var(--fog)}
.mp-meta strong{color:var(--ember2)}

/* Legend strip */
#legend{padding:0.8rem 1.4rem;border-top:1px solid var(--border);flex-shrink:0}
.legend-title{font-size:0.58rem;letter-spacing:0.1em;text-transform:uppercase;color:var(--ash);margin-bottom:0.6rem}
.legend-items{display:flex;flex-wrap:wrap;gap:0.4rem 0.8rem}
.legend-dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:0.3rem;vertical-align:middle}
.legend-item{font-size:0.62rem;color:var(--fog);cursor:pointer;transition:color 0.15s}
.legend-item:hover{color:var(--cream)}
.legend-item.dim{opacity:0.35}

/* ── TOOLTIP ── */
#tooltip{position:fixed;z-index:999;background:#1a1a26;border:1px solid rgba(255,255,255,0.15);border-radius:6px;padding:0.7rem 0.9rem;pointer-events:none;font-size:0.72rem;color:var(--cream);max-width:220px;box-shadow:0 8px 32px rgba(0,0,0,0.6);transition:opacity 0.1s;opacity:0}
#tooltip.show{opacity:1}
.tt-name{font-family:var(--font-serif);font-size:0.95rem;margin-bottom:0.2rem}
.tt-line{color:var(--fog);margin-bottom:0.15rem}
.tt-line strong{color:var(--ember2)}
.tt-sector{margin-top:0.5rem;padding-top:0.4rem;border-top:1px solid rgba(255,255,255,0.1)}
.tt-sector-row{display:flex;justify-content:space-between;gap:0.8rem;margin-bottom:0.15rem}
.tt-sector-name{color:var(--fog);font-size:0.65rem}
.tt-sector-val{color:var(--cream);font-size:0.65rem;font-weight:700}

/* ── COUNT DISPLAY ── */
#count-badge{position:absolute;top:0.8rem;left:2.5rem;font-size:0.65rem;color:var(--fog);letter-spacing:0.06em;background:rgba(10,10,15,0.7);padding:0.25rem 0.6rem;border-radius:100px;border:1px solid var(--border)}

/* Scrollbar */
#side-panel::-webkit-scrollbar{width:4px}
#side-panel::-webkit-scrollbar-track{background:transparent}
#side-panel::-webkit-scrollbar-thumb{background:var(--ash);border-radius:2px}
</style>
</head>
<body>

<header>
  <div class="hdr-top">
    <h1>Parliamentary <em>Voices</em></h1>
    <div class="hdr-meta">17th Lok Sabha &nbsp;·&nbsp; 499 MPs &nbsp;·&nbsp; 12 Sectors</div>
  </div>
  <div class="hdr-sub">Each dot is an MP. Position encodes their top two questioning sectors. Colour is party. Filter, search, and hover to explore.</div>
</header>

<!-- FILTER BAR -->
<div class="filter-bar">
  <div class="filter-group">
    <span class="filter-label">Sector (x-axis)</span>
    <div id="sector-x-pills"></div>
  </div>
  <div class="sep"></div>
  <div class="filter-group">
    <span class="filter-label">Sector (y-axis)</span>
    <div id="sector-y-pills"></div>
  </div>
  <div class="sep"></div>
  <div class="filter-group">
    <span class="filter-label">State</span>
    <div id="state-pills"></div>
  </div>
  <div class="sep"></div>
  <div class="filter-group">
    <span class="filter-label">Gender</span>
    <div id="gender-pills"></div>
  </div>
  <div class="search-wrap">
    <span class="search-icon">⌕</span>
    <input id="mp-search" type="text" placeholder="Search MP…" autocomplete="off">
  </div>
</div>

<main>
  <!-- DOT FIELD -->
  <div id="dot-field">
    <canvas id="dot-canvas"></canvas>
    <div id="count-badge">499 MPs</div>
    <div id="field-hint">hover a dot · click to lock</div>

    <!-- Axis labels placeholder -->
    <div id="x-axis-label" style="position:absolute;bottom:8px;left:50%;transform:translateX(-50%);font-size:0.62rem;color:var(--fog);letter-spacing:0.08em;pointer-events:none"></div>
    <div id="y-axis-label" style="position:absolute;left:8px;top:50%;transform:translateY(-50%) rotate(-90deg);font-size:0.62rem;color:var(--fog);letter-spacing:0.08em;pointer-events:none;white-space:nowrap"></div>

    <!-- Grid labels -->
    <div id="grid-labels"></div>
  </div>

  <!-- SIDE PANEL -->
  <div id="side-panel">
    <div class="panel-header">
      <div class="panel-title">Filtered snapshot</div>
    </div>
    <div class="stats-strip">
      <div class="stat-box">
        <div class="stat-num" id="stat-mps">499</div>
        <div class="stat-lbl">MPs shown</div>
      </div>
      <div class="stat-box">
        <div class="stat-num" id="stat-states">26</div>
        <div class="stat-lbl">States</div>
      </div>
      <div class="stat-box">
        <div class="stat-num" id="stat-parties">37</div>
        <div class="stat-lbl">Parties</div>
      </div>
    </div>
    <div class="breakdown">
      <div class="breakdown-title">Average sector share — filtered MPs</div>
      <div id="sector-breakdown"></div>
    </div>
    <div id="mp-card" style="display:none"></div>
    <div id="legend">
      <div class="legend-title">Party</div>
      <div class="legend-items" id="legend-items"></div>
    </div>
  </div>
</main>

<div id="tooltip"></div>

<script>
''' + inline_data + '''

// ── CONSTANTS ──
const SECTORS = DATA.sectors;
const LABELS = DATA.labels;
const PARTY_COLORS = DATA.party_colors;

const SCOLOR = s => PARTY_COLORS[s] || '#888';

const PARTIES_KNOWN = ['BJP','INC','DMK','YSRCP','AITC','SS','JD(U)','BJD','BSP','BRS'];
const STATES_LIST = [...new Set(DATA.mps.map(m => m.state))].sort();
const TOP_STATES = [...STATES_LIST].sort((a,b) => {
  const ca = DATA.mps.filter(m=>m.state===a).length;
  const cb = DATA.mps.filter(m=>m.state===b).length;
  return cb - ca;
}).slice(0,8);

// ── STATE ──
let state = {
  xSector: SECTORS[0],
  ySector: SECTORS[1],
  stateFilter: null,
  genderFilter: null,
  searchQuery: '',
  lockedMP: null,
  hoveredMP: null,
};

let dots = []; // computed positions
const canvas = document.getElementById('dot-canvas');
const ctx = canvas.getContext('2d');
let W = 0, H = 0;
const PAD = { top:32, right:24, bottom:48, left:52 };

// ── FILTER BUILDER ──
function buildPills(containerId, items, getActive, onClick, colorFn) {
  const el = document.getElementById(containerId);
  el.innerHTML = '';
  items.forEach(item => {
    const p = document.createElement('span');
    p.className = 'pill' + (getActive(item) ? ' active' : '');
    p.textContent = item;
    if (colorFn && getActive(item)) {
      p.style.background = colorFn(item);
      p.style.borderColor = colorFn(item);
      p.style.color = '#fff';
    }
    p.addEventListener('click', () => onClick(item));
    el.appendChild(p);
  });
}

function buildFilters() {
  // X-axis sector
  buildPills('sector-x-pills', SECTORS, s => s === state.xSector, s => {
    if (s === state.ySector) return; // can't be same as y
    state.xSector = s;
    refresh();
  });

  // Y-axis sector
  buildPills('sector-y-pills', SECTORS, s => s === state.ySector, s => {
    if (s === state.xSector) return;
    state.ySector = s;
    refresh();
  });

  // States (top 8 + all)
  const stateItems = ['All', ...TOP_STATES];
  buildPills('state-pills', stateItems, s => {
    if (s === 'All') return state.stateFilter === null;
    return state.stateFilter === s;
  }, s => {
    state.stateFilter = s === 'All' ? null : s;
    state.lockedMP = null;
    refresh();
  });

  // Gender
  buildPills('gender-pills', ['All','Male','Female'], g => {
    if (g === 'All') return state.genderFilter === null;
    return state.genderFilter === g;
  }, g => {
    state.genderFilter = g === 'All' ? null : g;
    state.lockedMP = null;
    refresh();
  });
}

// ── FILTERED MPs ──
function filteredMPs() {
  return DATA.mps.filter(m => {
    if (state.stateFilter && m.state !== state.stateFilter) return false;
    if (state.genderFilter && m.gender.toLowerCase() !== state.genderFilter.toLowerCase()) return false;
    if (state.searchQuery) {
      const q = state.searchQuery.toLowerCase();
      if (!m.name.toLowerCase().includes(q) && !m.state.toLowerCase().includes(q) && !m.party.toLowerCase().includes(q)) return false;
    }
    return true;
  });
}

// ── CANVAS DRAW ──
function resize() {
  const rect = canvas.parentElement.getBoundingClientRect();
  W = rect.width;
  H = rect.height;
  canvas.width = W * devicePixelRatio;
  canvas.height = H * devicePixelRatio;
  canvas.style.width = W + 'px';
  canvas.style.height = H + 'px';
  ctx.scale(devicePixelRatio, devicePixelRatio);
}

function plotW() { return W - PAD.left - PAD.right; }
function plotH() { return H - PAD.top - PAD.bottom; }

function toCanvas(xVal, yVal) {
  return {
    cx: PAD.left + (xVal / 25) * plotW(),
    cy: PAD.top + (1 - yVal / 25) * plotH(),
  };
}

function jitter(mp, i) {
  // Small deterministic jitter to separate overlapping dots
  const h = mp.id.split('').reduce((a,c) => (a*31 + c.charCodeAt(0)) & 0xffffffff, 0);
  return { dx: ((h & 0xff) - 128) / 128 * 6, dy: (((h>>8) & 0xff) - 128) / 128 * 6 };
}

function draw() {
  ctx.clearRect(0, 0, W, H);
  const pw = plotW(), ph = plotH();

  // Background grid
  ctx.strokeStyle = 'rgba(255,255,255,0.04)';
  ctx.lineWidth = 0.5;
  [5, 10, 15, 20].forEach(v => {
    const x = PAD.left + (v / 25) * pw;
    const y = PAD.top + (1 - v / 25) * ph;
    ctx.beginPath(); ctx.moveTo(x, PAD.top); ctx.lineTo(x, PAD.top + ph); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(PAD.left, y); ctx.lineTo(PAD.left + pw, y); ctx.stroke();
  });

  // Axis ticks
  ctx.fillStyle = 'rgba(144,144,160,0.6)';
  ctx.font = `${9 * devicePixelRatio / devicePixelRatio}px SF Mono, Fira Mono, monospace`;
  ctx.textAlign = 'right';
  [0,5,10,15,20,25].forEach(v => {
    const y = PAD.top + (1 - v / 25) * ph;
    ctx.fillText(v + '%', PAD.left - 6, y + 3);
  });
  ctx.textAlign = 'center';
  [0,5,10,15,20,25].forEach(v => {
    const x = PAD.left + (v / 25) * pw;
    ctx.fillText(v + '%', x, PAD.top + ph + 18);
  });

  // Avg lines
  const xAvg = DATA.avg[state.xSector];
  const yAvg = DATA.avg[state.ySector];
  const {cx: axLine} = toCanvas(xAvg, 0);
  const {cy: ayLine} = toCanvas(0, yAvg);
  ctx.strokeStyle = 'rgba(240,112,48,0.25)';
  ctx.lineWidth = 1;
  ctx.setLineDash([4,4]);
  ctx.beginPath(); ctx.moveTo(axLine, PAD.top); ctx.lineTo(axLine, PAD.top + ph); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(PAD.left, ayLine); ctx.lineTo(PAD.left + pw, ayLine); ctx.stroke();
  ctx.setLineDash([]);

  // Draw dots
  const active = new Set(filteredMPs().map(m => m.id));

  dots.forEach(d => {
    const isActive = active.has(d.mp.id);
    const isLocked = state.lockedMP && state.lockedMP.id === d.mp.id;
    const isHovered = state.hoveredMP && state.hoveredMP.id === d.mp.id;
    const isSearch = state.searchQuery && d.mp.name.toLowerCase().includes(state.searchQuery.toLowerCase());

    let r = isLocked || isHovered ? 7 : 4.5;
    let alpha = isActive ? (isLocked || isHovered || isSearch ? 1 : 0.72) : 0.08;

    const col = SCOLOR(d.mp.party);
    ctx.globalAlpha = alpha;
    ctx.beginPath();
    ctx.arc(d.cx + d.dx, d.cy + d.dy, r, 0, Math.PI * 2);
    ctx.fillStyle = col;
    ctx.fill();

    if ((isLocked || isHovered) && isActive) {
      ctx.globalAlpha = 1;
      ctx.strokeStyle = '#fff';
      ctx.lineWidth = 1.5;
      ctx.stroke();
    }
  });
  ctx.globalAlpha = 1;

  // Axis labels
  document.getElementById('x-axis-label').textContent = LABELS[state.xSector] || state.xSector;
  document.getElementById('y-axis-label').textContent = LABELS[state.ySector] || state.ySector;
}

function computeDots() {
  dots = DATA.mps.map((mp, i) => {
    const xVal = mp.s[state.xSector] || 0;
    const yVal = mp.s[state.ySector] || 0;
    const {cx, cy} = toCanvas(xVal, yVal);
    const {dx, dy} = jitter(mp, i);
    return {mp, cx, cy, dx, dy, xVal, yVal};
  });
}

// ── SIDE PANEL ──
function updatePanel() {
  const fps = filteredMPs();
  document.getElementById('stat-mps').textContent = fps.length;
  document.getElementById('stat-states').textContent = new Set(fps.map(m => m.state)).size;
  document.getElementById('stat-parties').textContent = new Set(fps.map(m => m.party)).size;
  document.getElementById('count-badge').textContent = fps.length + ' MPs';

  // Sector breakdown
  const avgs = SECTORS.map(s => {
    const vals = fps.map(m => m.s[s] || 0);
    const avg = vals.length ? vals.reduce((a,b)=>a+b,0)/vals.length : 0;
    return {s, avg};
  }).sort((a,b) => b.avg - a.avg).slice(0,12);

  const maxAvg = Math.max(...avgs.map(a => a.avg), 1);
  const bd = document.getElementById('sector-breakdown');
  bd.innerHTML = avgs.map(({s, avg}) => {
    const globalAvg = DATA.avg[s];
    const tickPos = (globalAvg / 25) * 100;
    const barW = (avg / 25) * 100;
    const col = avg > globalAvg ? 'var(--ember)' : 'var(--ice)';
    return `<div class="sector-row">
      <div class="sector-meta">
        <span class="sector-name">${LABELS[s] || s}</span>
        <span class="sector-val">${avg.toFixed(1)}%</span>
      </div>
      <div class="sector-track">
        <div class="sector-bar" style="width:${barW}%;background:${col};opacity:0.85"></div>
        <div class="sector-avg-tick" style="left:${tickPos}%"></div>
      </div>
    </div>`;
  }).join('');

  // MP card
  const focused = state.lockedMP || state.hoveredMP;
  const card = document.getElementById('mp-card');
  if (focused) {
    card.style.display = 'block';
    const topSectors = SECTORS
      .map(s => ({s, v: focused.s[s] || 0}))
      .sort((a,b) => b.v - a.v).slice(0,4);
    card.innerHTML = `
      <div class="mp-name">${focused.name}</div>
      <div class="mp-meta" style="margin-bottom:0.6rem">
        <strong>${focused.party}</strong> &nbsp;·&nbsp; ${focused.state} &nbsp;·&nbsp; ${focused.gender}
      </div>
      <div style="font-size:0.6rem;letter-spacing:0.08em;text-transform:uppercase;color:var(--ash);margin-bottom:0.5rem">Top sectors</div>
      ${topSectors.map(({s,v}) => `
        <div style="display:flex;justify-content:space-between;margin-bottom:0.3rem">
          <span style="font-size:0.7rem;color:var(--fog)">${LABELS[s]||s}</span>
          <span style="font-size:0.7rem;color:var(--cream)">${v.toFixed(1)}%</span>
        </div>
        <div style="height:3px;background:rgba(255,255,255,0.06);border-radius:1px;margin-bottom:0.5rem">
          <div style="height:100%;width:${(v/25*100).toFixed(1)}%;background:var(--ember);border-radius:1px"></div>
        </div>
      `).join('')}
      <div style="font-size:0.65rem;color:var(--ash);margin-top:0.4rem">${focused.total.toLocaleString()} questions total</div>
      ${state.lockedMP ? '<div style="font-size:0.58rem;color:var(--ash);margin-top:0.3rem">Click dot again to unlock</div>' : ''}
    `;
  } else {
    card.style.display = 'none';
  }

  // Legend
  const partiesPresent = [...new Set(fps.map(m => m.party))].sort((a,b)=>{
    const an = fps.filter(m=>m.party===a).length;
    const bn = fps.filter(m=>m.party===b).length;
    return bn-an;
  });
  const legend = document.getElementById('legend-items');
  legend.innerHTML = partiesPresent.map(p => {
    const col = SCOLOR(p);
    const n = fps.filter(m=>m.party===p).length;
    return `<span class="legend-item" title="${p}: ${n} MPs">
      <span class="legend-dot" style="background:${col}"></span>${p} <span style="color:var(--ash)">${n}</span>
    </span>`;
  }).join('');
}

// ── TOOLTIP ──
const tooltip = document.getElementById('tooltip');
function showTip(mp, x, y) {
  const topSectors = SECTORS.map(s=>({s,v:mp.s[s]||0})).sort((a,b)=>b.v-a.v).slice(0,3);
  tooltip.innerHTML = `
    <div class="tt-name">${mp.name}</div>
    <div class="tt-line"><strong>${mp.party}</strong> · ${mp.state}</div>
    <div class="tt-line">${mp.gender} · ${mp.total.toLocaleString()} questions</div>
    <div class="tt-sector">
      ${topSectors.map(({s,v})=>`<div class="tt-sector-row"><span class="tt-sector-name">${LABELS[s]||s}</span><span class="tt-sector-val">${v.toFixed(1)}%</span></div>`).join('')}
    </div>`;
  const tw = tooltip.offsetWidth, th = tooltip.offsetHeight;
  tooltip.style.left = Math.min(x+14, window.innerWidth-tw-12)+'px';
  tooltip.style.top = Math.min(y+14, window.innerHeight-th-12)+'px';
  tooltip.classList.add('show');
}
function hideTip() { tooltip.classList.remove('show'); }

// ── HIT TEST ──
function hitTest(mx, my) {
  const active = new Set(filteredMPs().map(m => m.id));
  let best = null, bestDist = 12;
  dots.forEach(d => {
    if (!active.has(d.mp.id)) return;
    const dx = mx - (d.cx + d.dx);
    const dy = my - (d.cy + d.dy);
    const dist = Math.sqrt(dx*dx + dy*dy);
    if (dist < bestDist) { bestDist = dist; best = d; }
  });
  return best ? best.mp : null;
}

// ── CANVAS EVENTS ──
canvas.addEventListener('mousemove', e => {
  const rect = canvas.getBoundingClientRect();
  const mx = e.clientX - rect.left;
  const my = e.clientY - rect.top;
  const mp = hitTest(mx, my);
  if (mp) {
    canvas.style.cursor = 'pointer';
    state.hoveredMP = mp;
    showTip(mp, e.clientX, e.clientY);
  } else {
    canvas.style.cursor = 'default';
    if (!state.lockedMP) state.hoveredMP = null;
    hideTip();
  }
  if (!state.lockedMP) {
    updatePanel();
    draw();
  }
});

canvas.addEventListener('click', e => {
  const rect = canvas.getBoundingClientRect();
  const mx = e.clientX - rect.left;
  const my = e.clientY - rect.top;
  const mp = hitTest(mx, my);
  if (mp) {
    if (state.lockedMP && state.lockedMP.id === mp.id) {
      state.lockedMP = null;
    } else {
      state.lockedMP = mp;
    }
  } else {
    state.lockedMP = null;
  }
  state.hoveredMP = mp;
  updatePanel();
  draw();
});

canvas.addEventListener('mouseleave', () => {
  hideTip();
  if (!state.lockedMP) {
    state.hoveredMP = null;
    updatePanel();
    draw();
  }
});

// ── SEARCH ──
document.getElementById('mp-search').addEventListener('input', e => {
  state.searchQuery = e.target.value.trim();
  state.lockedMP = null;
  refresh();
});

// ── REFRESH ──
function refresh() {
  buildFilters();
  computeDots();
  updatePanel();
  draw();
}

// ── RESIZE ──
let resizeTimer;
window.addEventListener('resize', () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => {
    resize();
    computeDots();
    draw();
  }, 100);
});

// ── INIT ──
resize();
buildFilters();
computeDots();
updatePanel();
draw();
</script>
</body>
</html>'''

with open('/Users/aashima/Desktop/DataViz5/outcome/loksabha-questions/simple.html', 'w') as f:
    f.write(html)

print(f"Written: {len(html)//1024} KB")
