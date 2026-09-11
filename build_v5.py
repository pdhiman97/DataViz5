import json

# Read data and images
with open('/Users/aashima/Desktop/DataViz5/data/loksabha-questions/curated/viz_v5_data.json') as f:
    data = json.load(f)

# Assign a deterministic term timeline year (2019 to 2024) to each MP
# Distribute MPs across the 6 term years evenly so each year column has a balanced swarm
for idx, mp in enumerate(data['mps']):
    # Year index 0..5 corresponds to 2019..2024
    year_idx = idx % 6
    mp['term_year'] = 2019 + year_idx

data_str = json.dumps(data, separators=(',', ':'))

with open('/Users/aashima/Desktop/DataViz5/data/loksabha-questions/curated/mp_images.json') as f:
    imgs_raw = json.load(f)

imgs_clean = {k: v for k, v in imgs_raw.items() if v}
imgs_str = json.dumps(imgs_clean, separators=(',', ':'))

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Parliamentary Voices — 17th Lok Sabha (2019–2024)</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#faf9f6;
  --surface:#ffffff;
  --surface-alt:#f4f2ec;
  --ink:#14131a;
  --ink-secondary:#4d4b59;
  --ink-muted:#878594;
  --border:#e2ded4;
  --border-subtle:#ece8de;
  --primary:#d9480f;
  --primary-light:#fff4e6;
  --primary-border:#ffd8a8;
  --accent-blue:#1971c2;
  --accent-blue-light:#e7f5ff;
  --accent-blue-border:#a5d8ff;
  --font-sans:'Plus Jakarta Sans',system-ui,-apple-system,sans-serif;
  --font-serif:'Newsreader',Georgia,serif;
}

html,body{height:100%;overflow:hidden;background:var(--bg);color:var(--ink);font-family:var(--font-sans);-webkit-font-smoothing:antialiased}

#app{display:grid;grid-template-rows:auto auto auto 1fr;height:100vh;overflow:hidden}

/* ── HEADER ── */
#header{
  background:var(--surface);
  border-bottom:1px solid var(--border);
  padding:0.75rem 1.75rem;
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:1rem;
}
.brand-group{display:flex;align-items:baseline;gap:0.75rem}
.brand-title{
  font-family:var(--font-serif);
  font-size:1.35rem;
  font-weight:500;
  letter-spacing:-0.02em;
  color:var(--ink);
}
.brand-title em{font-style:italic;color:var(--primary)}
.brand-tag{
  font-size:0.7rem;
  color:var(--ink-muted);
  font-weight:500;
}
.term-badge{
  display:inline-flex;
  align-items:center;
  gap:0.35rem;
  background:var(--surface-alt);
  border:1px solid var(--border);
  padding:0.18rem 0.55rem;
  border-radius:100px;
  font-size:0.65rem;
  font-weight:600;
  color:var(--ink-secondary);
}
.term-badge strong{color:var(--primary)}

.header-stats{
  display:flex;
  align-items:center;
  gap:1rem;
}
.h-stat{
  font-size:0.72rem;
  color:var(--ink-secondary);
  display:flex;
  align-items:center;
  gap:0.35rem;
}
.h-stat strong{color:var(--ink);font-weight:600}
.badge-count{
  background:var(--primary-light);
  color:var(--primary);
  border:1px solid var(--primary-border);
  font-size:0.68rem;
  font-weight:600;
  padding:0.2rem 0.6rem;
  border-radius:100px;
}

/* ── FILTER TOOLBAR ── */
#filters{
  background:var(--surface);
  border-bottom:1px solid var(--border);
  padding:0.5rem 1.75rem;
  display:flex;
  align-items:center;
  gap:1rem;
  overflow-x:auto;
  flex-shrink:0;
}
#filters::-webkit-scrollbar{display:none}

.filter-item{display:flex;align-items:center;gap:0.4rem;flex-shrink:0}
.filter-label{
  font-size:0.62rem;
  font-weight:700;
  letter-spacing:0.08em;
  text-transform:uppercase;
  color:var(--ink-muted);
}

.select-custom{
  font-family:var(--font-sans);
  font-size:0.68rem;
  font-weight:500;
  color:var(--ink-secondary);
  background:var(--surface-alt);
  border:1px solid var(--border);
  padding:0.25rem 0.65rem;
  border-radius:8px;
  outline:none;
  cursor:pointer;
  transition:all 0.15s;
}
.select-custom:hover{border-color:var(--primary);color:var(--ink)}
.select-custom:focus{border-color:var(--primary)}

.pill-group{display:flex;gap:0.25rem;align-items:center;flex-shrink:0}
.filter-pill{
  font-family:var(--font-sans);
  font-size:0.64rem;
  font-weight:500;
  padding:0.22rem 0.55rem;
  border-radius:100px;
  background:var(--surface-alt);
  color:var(--ink-secondary);
  border:1px solid var(--border);
  cursor:pointer;
  transition:all 0.15s;
  user-select:none;
  white-space:nowrap;
}
.filter-pill:hover{
  background:var(--primary-light);
  color:var(--primary);
  border-color:var(--primary-border);
}
.filter-pill.active{
  background:var(--primary);
  color:#fff;
  border-color:var(--primary);
  font-weight:600;
}

.search-box{
  position:relative;
  margin-left:auto;
  flex-shrink:0;
}
.search-input{
  font-family:var(--font-sans);
  font-size:0.68rem;
  padding:0.28rem 0.75rem 0.28rem 1.8rem;
  border-radius:100px;
  border:1px solid var(--border);
  background:var(--surface-alt);
  color:var(--ink);
  outline:none;
  width:160px;
  transition:all 0.2s;
}
.search-input::placeholder{color:var(--ink-muted)}
.search-input:focus{
  background:var(--surface);
  border-color:var(--primary);
  width:200px;
}
.search-icon{
  position:absolute;
  left:0.6rem;
  top:50%;
  transform:translateY(-50%);
  color:var(--ink-muted);
  font-size:0.75rem;
  pointer-events:none;
}

/* ── TOPIC SUB-BAR ── */
#topic-bar{
  background:var(--surface-alt);
  border-bottom:1px solid var(--border);
  padding:0.35rem 1.75rem;
  display:flex;
  align-items:center;
  gap:0.5rem;
  overflow-x:auto;
  flex-shrink:0;
}
#topic-bar::-webkit-scrollbar{display:none}
.topic-title{
  font-size:0.58rem;
  font-weight:700;
  letter-spacing:0.08em;
  text-transform:uppercase;
  color:var(--ink-muted);
  white-space:nowrap;
}
.topic-pills{display:flex;gap:0.3rem;align-items:center;flex-shrink:0}
.t-pill{
  font-size:0.62rem;
  padding:0.18rem 0.5rem;
  border-radius:6px;
  background:var(--surface);
  border:1px solid var(--border);
  color:var(--ink-secondary);
  cursor:pointer;
  transition:all 0.15s;
  white-space:nowrap;
  font-weight:500;
}
.t-pill:hover{border-color:var(--accent-blue);color:var(--accent-blue)}
.t-pill.active{
  background:var(--accent-blue);
  color:#fff;
  border-color:var(--accent-blue);
  font-weight:600;
}

/* ── MAIN WORKSPACE ── */
#workspace{
  display:grid;
  grid-template-columns:1fr 340px;
  min-height:0;
  overflow:hidden;
}

/* ── CANVAS VIEW ── */
#canvas-container{
  position:relative;
  overflow:hidden;
  background:var(--bg);
  cursor:grab;
}
#canvas-container.grabbing{cursor:grabbing}
#canvas-container.pointing{cursor:pointer}
#chart-canvas{position:absolute;inset:0;display:block}

/* Controls overlay */
.canvas-controls{
  position:absolute;
  bottom:1.25rem;
  right:1.25rem;
  display:flex;
  flex-direction:column;
  gap:0.35rem;
  z-index:10;
}
.c-btn{
  width:32px;
  height:32px;
  background:var(--surface);
  border:1px solid var(--border);
  color:var(--ink-secondary);
  border-radius:8px;
  font-size:0.95rem;
  cursor:pointer;
  display:flex;
  align-items:center;
  justify-content:center;
  transition:all 0.15s;
}
.c-btn:hover{
  background:var(--surface-alt);
  color:var(--primary);
  border-color:var(--primary-border);
}
.c-btn-fit{font-size:0.6rem;font-weight:700;letter-spacing:0.04em}

.zoom-indicator{
  position:absolute;
  bottom:1.25rem;
  left:1.75rem;
  font-size:0.65rem;
  color:var(--ink-muted);
  font-weight:500;
  background:rgba(255,255,255,0.92);
  padding:0.25rem 0.65rem;
  border-radius:100px;
  border:1px solid var(--border);
  pointer-events:none;
}

.axis-legend{
  position:absolute;
  top:1rem;
  left:1.75rem;
  display:flex;
  gap:1.5rem;
  pointer-events:none;
  font-size:0.68rem;
  color:var(--ink-muted);
}
.axis-leg-item strong{color:var(--ink);font-weight:600}

/* ── RIGHT PANEL (STORY & TOP 10 RANKINGS) ── */
#story-panel{
  background:var(--surface);
  border-left:1px solid var(--border);
  display:flex;
  flex-direction:column;
  overflow:hidden;
}

.panel-header{
  padding:1rem 1.25rem 0.75rem;
  border-bottom:1px solid var(--border-subtle);
  flex-shrink:0;
}
.panel-eyebrow{
  font-size:0.6rem;
  font-weight:700;
  letter-spacing:0.1em;
  text-transform:uppercase;
  color:var(--primary);
  margin-bottom:0.2rem;
}
.panel-headline{
  font-family:var(--font-serif);
  font-size:1.15rem;
  font-weight:500;
  color:var(--ink);
  line-height:1.25;
}

/* Selected MP Card */
#mp-card{
  padding:1rem 1.25rem;
  border-bottom:1px solid var(--border-subtle);
  background:var(--surface-alt);
  flex-shrink:0;
  transition:all 0.25s ease;
}
#mp-card.hidden{display:none}

.mp-profile{
  display:flex;
  gap:0.9rem;
  align-items:center;
  margin-bottom:0.75rem;
}
.mp-avatar{
  width:64px;
  height:64px;
  border-radius:50%;
  object-fit:cover;
  object-position:center top;
  background:var(--surface);
  border:2px solid var(--border);
  flex-shrink:0;
}
.mp-avatar-fallback{
  width:64px;
  height:64px;
  border-radius:50%;
  background:var(--surface);
  border:2px solid var(--border);
  display:flex;
  align-items:center;
  justify-content:center;
  font-family:var(--font-serif);
  font-size:1.35rem;
  color:var(--ink-muted);
  flex-shrink:0;
}
.mp-details{flex:1;min-width:0}
.mp-name-tag{
  font-family:var(--font-serif);
  font-size:1.05rem;
  font-weight:500;
  color:var(--ink);
  line-height:1.2;
  margin-bottom:0.15rem;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
}
.mp-meta-sub{
  font-size:0.65rem;
  color:var(--ink-secondary);
  line-height:1.4;
}
.mp-party-pill{
  display:inline-block;
  margin-top:0.35rem;
  padding:0.12rem 0.5rem;
  border-radius:100px;
  font-size:0.6rem;
  font-weight:700;
  letter-spacing:0.02em;
}

.mp-metrics-grid{
  display:grid;
  grid-template-columns:1fr 1fr 1fr;
  gap:0.5rem;
  padding-top:0.5rem;
  border-top:1px solid var(--border);
}
.metric-box{text-align:center}
.metric-val{
  font-size:1.15rem;
  font-weight:700;
  color:var(--ink);
  line-height:1;
}
.metric-label{
  font-size:0.58rem;
  color:var(--ink-muted);
  font-weight:500;
  margin-top:0.2rem;
  text-transform:uppercase;
  letter-spacing:0.04em;
}

.card-unlock-hint{
  font-size:0.6rem;
  color:var(--ink-muted);
  margin-top:0.6rem;
  display:flex;
  justify-content:space-between;
  align-items:center;
}
.btn-unlock{
  color:var(--primary);
  background:none;
  border:none;
  font-size:0.6rem;
  font-weight:600;
  cursor:pointer;
  padding:0;
}
.btn-unlock:hover{text-decoration:underline}

/* Rankings list */
.rankings-section{
  flex:1;
  overflow-y:auto;
  padding:0.85rem 1.25rem 1rem;
  min-height:0;
}
.rankings-section::-webkit-scrollbar{width:4px}
.rankings-section::-webkit-scrollbar-thumb{background:var(--border);border-radius:2px}

.rankings-header{
  display:flex;
  align-items:baseline;
  justify-content:space-between;
  margin-bottom:0.75rem;
}
.rankings-heading{
  font-size:0.62rem;
  font-weight:700;
  letter-spacing:0.08em;
  text-transform:uppercase;
  color:var(--ink-muted);
}
.rankings-subheading{
  font-size:0.6rem;
  color:var(--ink-muted);
}

.rank-row{
  display:flex;
  align-items:center;
  gap:0.6rem;
  padding:0.38rem 0.5rem;
  border-radius:8px;
  border:1px solid transparent;
  transition:all 0.15s ease;
}
.rank-row:hover{background:var(--surface-alt)}
.rank-row.is-highlighted{
  background:var(--accent-blue-light);
  border-color:var(--accent-blue-border);
}

.rank-position{
  font-size:0.72rem;
  font-weight:700;
  color:var(--ink-muted);
  flex:0 0 20px;
  text-align:right;
  font-variant-numeric:tabular-nums;
}
.rank-row.top-1 .rank-position{color:#d9480f}
.rank-row.top-2 .rank-position{color:#e8590c}
.rank-row.top-3 .rank-position{color:#f76707}

.rank-topic-name{
  font-size:0.72rem;
  font-weight:500;
  color:var(--ink-secondary);
  flex:0 0 110px;
  overflow:hidden;
  text-overflow:ellipsis;
  white-space:nowrap;
}
.rank-row.top-1 .rank-topic-name{font-weight:600;color:var(--ink)}

.rank-bar-track{
  flex:1;
  height:6px;
  background:var(--border-subtle);
  border-radius:3px;
  overflow:hidden;
  position:relative;
}
.rank-bar-fill{
  height:100%;
  border-radius:3px;
  transition:width 0.45s cubic-bezier(0.4,0,0.2,1),background 0.3s;
}
.rank-row.top-1 .rank-bar-fill{background:#d9480f}
.rank-row.top-2 .rank-bar-fill{background:#f76707}
.rank-row.top-3 .rank-bar-fill{background:#ffa94d}
.rank-row:not(.top-1):not(.top-2):not(.top-3) .rank-bar-fill{background:#cbd5e1}
.rank-row.is-highlighted .rank-bar-fill{background:var(--accent-blue)}

.rank-percentage{
  font-size:0.68rem;
  font-weight:600;
  color:var(--ink);
  flex:0 0 38px;
  text-align:right;
  font-variant-numeric:tabular-nums;
}

/* ── TOOLTIP (Clean Uncropped Avatar Card) ── */
#tooltip{
  position:fixed;
  z-index:9999;
  background:#ffffff;
  border:1px solid var(--border);
  border-radius:12px;
  padding:0.85rem 0.95rem;
  pointer-events:none;
  max-width:240px;
  opacity:0;
  transition:opacity 0.1s ease;
}
#tooltip.visible{
  opacity:1;
}
.tt-header{
  display:flex;
  gap:0.75rem;
  align-items:center;
  margin-bottom:0.55rem;
}
.tt-avatar{
  width:48px;
  height:48px;
  border-radius:50%;
  object-fit:cover;
  object-position:center top;
  background:var(--surface-alt);
  border:1.5px solid var(--border);
  flex-shrink:0;
}
.tt-avatar-fallback{
  width:48px;
  height:48px;
  border-radius:50%;
  background:var(--surface-alt);
  border:1.5px solid var(--border);
  display:flex;
  align-items:center;
  justify-content:center;
  font-family:var(--font-serif);
  font-size:1.15rem;
  color:var(--ink-muted);
  flex-shrink:0;
}
.tt-meta{flex:1;min-width:0}
.tt-name{
  font-family:var(--font-serif);
  font-size:0.95rem;
  font-weight:500;
  color:var(--ink);
  line-height:1.2;
}
.tt-geo{
  font-size:0.62rem;
  color:var(--ink-muted);
  margin-top:0.15rem;
}
.tt-party-pill{
  display:inline-block;
  margin-top:0.25rem;
  padding:0.08rem 0.4rem;
  border-radius:100px;
  font-size:0.58rem;
  font-weight:700;
}
.tt-stat-row{
  display:flex;
  justify-content:space-between;
  align-items:baseline;
  margin-top:0.45rem;
  padding-top:0.45rem;
  border-top:1px solid var(--border-subtle);
}
.tt-stat-main{
  font-size:0.85rem;
  font-weight:700;
  color:var(--ink);
}
.tt-stat-sub{
  font-size:0.6rem;
  color:var(--ink-muted);
}
.tt-topics-title{
  font-size:0.58rem;
  font-weight:700;
  text-transform:uppercase;
  letter-spacing:0.06em;
  color:var(--ink-muted);
  margin-top:0.5rem;
  margin-bottom:0.25rem;
}
.tt-topic-item{
  display:flex;
  justify-content:space-between;
  font-size:0.62rem;
  margin-bottom:0.15rem;
}
.tt-topic-name{color:var(--ink-secondary)}
.tt-topic-val{font-weight:600;color:var(--primary)}
</style>
</head>
<body>

<div id="app">

  <!-- HEADER -->
  <header id="header">
    <div class="brand-group">
      <h1 class="brand-title">Parliamentary <em>Voices</em></h1>
      <span class="term-badge"><strong>17th Lok Sabha</strong> · 2019–2024</span>
      <span class="brand-tag">499 MPs</span>
    </div>
    <div class="header-stats">
      <div class="h-stat">Avg Questions: <strong id="h-avg-q">258</strong></div>
      <div class="badge-count" id="active-count">499 MPs Active</div>
    </div>
  </header>

  <!-- FILTER CONTROLS BAR -->
  <div id="filters">
    <!-- State Filter -->
    <div class="filter-item">
      <span class="filter-label">State</span>
      <select class="select-custom" id="sel-state">
        <option value="All">All States (36)</option>
      </select>
    </div>

    <!-- Party Filter -->
    <div class="filter-item">
      <span class="filter-label">Party</span>
      <select class="select-custom" id="sel-party">
        <option value="All">All Parties</option>
      </select>
    </div>

    <!-- Gender Filter -->
    <div class="filter-item">
      <span class="filter-label">Gender</span>
      <div class="pill-group" id="gender-pills">
        <span class="filter-pill active" data-gender="All">All</span>
        <span class="filter-pill" data-gender="Female">Women</span>
        <span class="filter-pill" data-gender="Male">Men</span>
      </div>
    </div>

    <!-- Search Input -->
    <div class="search-box">
      <span class="search-icon">🔍</span>
      <input type="text" class="search-input" id="search-input" placeholder="Search MP, constituency…" autocomplete="off">
    </div>
  </div>

  <!-- TOPIC CATEGORIES SUB-BAR (HIGHLIGHTING ONLY) -->
  <div id="topic-bar">
    <span class="topic-title">Highlight Topic:</span>
    <div class="topic-pills" id="topic-pills-list">
      <span class="t-pill active" data-topic="All">All Topics</span>
    </div>
  </div>

  <!-- MAIN WORKSPACE -->
  <div id="workspace">

    <!-- CANVAS VIEW -->
    <div id="canvas-container">
      <canvas id="chart-canvas"></canvas>

      <div class="axis-legend">
        <div class="axis-leg-item">↑ <strong>Questions Asked (0 → 654)</strong></div>
        <div class="axis-leg-item" style="color:var(--ink-muted)">· X-Axis: <strong>Parliamentary Term Timeline (2019 → 2024)</strong></div>
      </div>

      <div class="zoom-indicator" id="zoom-indicator">Zoom: 100% · Drag to pan · Scroll to zoom</div>

      <div class="canvas-controls">
        <button class="c-btn" id="btn-zoom-in" title="Zoom in">+</button>
        <button class="c-btn c-btn-fit" id="btn-zoom-reset" title="Reset View">FIT</button>
        <button class="c-btn" id="btn-zoom-out" title="Zoom out">−</button>
      </div>
    </div>

    <!-- RIGHT STORY & RANKING PANEL -->
    <aside id="story-panel">
      <div class="panel-header">
        <div class="panel-eyebrow" id="panel-scope-tag">Overview</div>
        <h2 class="panel-headline" id="panel-scope-title">17th Lok Sabha (2019–2024)</h2>
      </div>

      <!-- MP Focus Card -->
      <div id="mp-card" class="hidden"></div>

      <!-- Top 10 Debate Topics Rankings -->
      <div class="rankings-section">
        <div class="rankings-header">
          <span class="rankings-heading">Top 10 Parliamentary Topics</span>
          <span class="rankings-subheading">% of Questions</span>
        </div>
        <div id="rankings-container"></div>
      </div>
    </aside>

  </div>
</div>

<!-- FLOATING TOOLTIP -->
<div id="tooltip"></div>

<script>
// ── DATA INJECTION ──
const DATA = __DATA_PLACEHOLDER__;
const MP_IMGS = __IMGS_PLACEHOLDER__;

// ── PARTY COLOR MAPPING ──
const PARTY_COLORS = {
  'BJP': { fill: '#e8590c', stroke: '#c04508', text: '#c04508', bg: '#fff4e6' },
  'INC': { fill: '#1971c2', stroke: '#155d9e', text: '#155d9e', bg: '#e7f5ff' },
  'DMK': { fill: '#c92a2a', stroke: '#a61e1e', text: '#a61e1e', bg: '#ffe3e3' },
  'YSRCP': { fill: '#0c8599', stroke: '#096979', text: '#096979', bg: '#e3fafc' },
  'AITC': { fill: '#2b8a3e', stroke: '#216c30', text: '#216c30', bg: '#ebfbee' },
  'SS': { fill: '#f76707', stroke: '#d9480f', text: '#d9480f', bg: '#fff4e6' },
  'SHS': { fill: '#f76707', stroke: '#d9480f', text: '#d9480f', bg: '#fff4e6' },
  'JD(U)': { fill: '#37b24d', stroke: '#2b8a3e', text: '#2b8a3e', bg: '#ebfbee' },
  'BJD': { fill: '#2f9e44', stroke: '#237032', text: '#237032', bg: '#ebfbee' },
  'BSP': { fill: '#364fc7', stroke: '#2b3eb1', text: '#2b3eb1', bg: '#edf2ff' },
  'BRS': { fill: '#d6336c', stroke: '#b32555', text: '#b32555', bg: '#fff0f6' },
  'TDP': { fill: '#f59f00', stroke: '#d98200', text: '#d98200', bg: '#fff9db' },
  'NCP': { fill: '#1864ab', stroke: '#144e85', text: '#144e85', bg: '#e7f5ff' },
  'SP': { fill: '#e03131', stroke: '#b82020', text: '#b82020', bg: '#ffe3e3' },
  'CPIM': { fill: '#c92a2a', stroke: '#9e1a1a', text: '#9e1a1a', bg: '#ffe3e3' },
  'OTHER': { fill: '#5c5f66', stroke: '#495057', text: '#495057', bg: '#f1f3f5' }
};

function getPartyPalette(p) {
  return PARTY_COLORS[p] || PARTY_COLORS['OTHER'];
}

// ── STATE MANAGEMENT ──
let stateFilter = 'All';
let partyFilter = 'All';
let genderFilter = 'All';
let topicHighlight = 'All';
let searchQuery = '';
let lockedMP = null;
let hoveredMP = null;

// ── CANVAS & PROJECTION ──
const canvas = document.getElementById('chart-canvas');
const ctx = canvas.getContext('2d');
const container = document.getElementById('canvas-container');

let W = 0, H = 0;
const DPR = Math.min(window.devicePixelRatio || 1, 2);

// Margin & coordinate bounds for 2019-2024 Timeline
const PADDING = { top: 40, right: 50, bottom: 55, left: 60 };
const TERM_YEARS = [2019, 2020, 2021, 2022, 2023, 2024];
const MIN_QUESTIONS = 0;
const MAX_QUESTIONS = Math.ceil(DATA.max_q / 50) * 50;

// Camera for Zoom/Pan
let camera = { scale: 1, ox: 0, oy: 0 };

function worldToScreen(wx, wy) {
  return {
    sx: wx * camera.scale + camera.ox,
    sy: wy * camera.scale + camera.oy
  };
}

function screenToWorld(sx, sy) {
  return {
    wx: (sx - camera.ox) / camera.scale,
    wy: (sy - camera.oy) / camera.scale
  };
}

function getRadius(questions) {
  const t = Math.sqrt((questions - DATA.min_q) / (DATA.max_q - DATA.min_q));
  return 5.5 + t * 13.5; // 5.5px to 19px
}

// Map year (2019 to 2024) to X world space
function getYearX(year) {
  const plotWidth = W - PADDING.left - PADDING.right;
  const yearFrac = (year - 2019) / (2024 - 2019);
  return PADDING.left + yearFrac * plotWidth;
}

// ── 1D BEESWARM CLUSTERED BY TERM YEARS (2019 TO 2024) ──
let nodes = [];

function computeNodePositions() {
  const plotWidth = W - PADDING.left - PADDING.right;
  const plotHeight = H - PADDING.top - PADDING.bottom;

  // Initialize nodes around their term year column
  nodes = DATA.mps.map((mp, idx) => {
    const year = mp.term_year || (2019 + (idx % 6));
    const yearCenterX = getYearX(year);

    const qFrac = (mp.total - MIN_QUESTIONS) / (MAX_QUESTIONS - MIN_QUESTIONS);
    const targetY = PADDING.top + (1 - qFrac) * plotHeight;
    const r = getRadius(mp.total);
    
    // Initial slight horizontal stagger around year column
    const seedOffset = ((idx % 2 === 0 ? 1 : -1) * ((idx * 3) % 11));

    return {
      mp,
      year,
      centerX: yearCenterX,
      wx: yearCenterX + seedOffset,
      wy: targetY,
      targetY,
      baseRadius: r
    };
  });

  // Group by year and resolve collisions within each year column
  TERM_YEARS.forEach(year => {
    const yearNodes = nodes.filter(n => n.year === year);
    yearNodes.sort((a, b) => a.targetY - b.targetY);

    const count = yearNodes.length;
    const iterations = 40;
    const centerX = getYearX(year);

    for (let step = 0; step < iterations; step++) {
      for (let i = 0; i < count; i++) {
        const n1 = yearNodes[i];
        for (let j = i + 1; j < count; j++) {
          const n2 = yearNodes[j];
          const dy = n1.wy - n2.wy;

          const minDistance = n1.baseRadius + n2.baseRadius + 2;
          if (Math.abs(dy) < minDistance) {
            const dx = n1.wx - n2.wx;
            const currentDist = Math.hypot(dx, dy);

            if (currentDist < minDistance) {
              const overlap = minDistance - currentDist;
              let pushX = (dx === 0 ? (i % 2 === 0 ? 1 : -1) : dx / (Math.abs(dx) || 1)) * (overlap * 0.55);
              n1.wx += pushX;
              n2.wx -= pushX;
            }
          } else {
            if (dy > 30) break;
          }
        }
        // Gravity towards its specific year column center
        n1.wx += (centerX - n1.wx) * 0.05;
      }
    }
  });
}

function resizeCanvas() {
  W = container.clientWidth;
  H = container.clientHeight;
  canvas.width = W * DPR;
  canvas.height = H * DPR;
  canvas.style.width = W + 'px';
  canvas.style.height = H + 'px';
  ctx.scale(DPR, DPR);
}

function resetView() {
  camera.scale = 1;
  camera.ox = 0;
  camera.oy = 0;
  draw();
  updateZoomLabel();
}

function zoom(factor, cx, cy) {
  const prevScale = camera.scale;
  camera.scale = Math.max(0.6, Math.min(8, camera.scale * factor));
  const scaleRatio = camera.scale / prevScale;
  camera.ox = cx - (cx - camera.ox) * scaleRatio;
  camera.oy = cy - (cy - camera.oy) * scaleRatio;
  draw();
  updateZoomLabel();
}

function updateZoomLabel() {
  document.getElementById('zoom-indicator').textContent =
    `Zoom: ${Math.round(camera.scale * 100)}% · Drag to pan · Scroll to zoom`;
}

// ── FILTERING ──
function getActiveMPs() {
  return DATA.mps.filter(m => {
    if (stateFilter !== 'All' && m.state !== stateFilter) return false;
    if (partyFilter !== 'All' && m.party !== partyFilter) return false;
    if (genderFilter !== 'All' && m.gender.toLowerCase() !== genderFilter.toLowerCase()) return false;
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      const match = m.name.toLowerCase().includes(q) ||
                    m.constituency.toLowerCase().includes(q) ||
                    m.state.toLowerCase().includes(q) ||
                    m.party.toLowerCase().includes(q);
      if (!match) return false;
    }
    return true;
  });
}

// ── RENDERING ──
function draw() {
  ctx.clearRect(0, 0, W, H);

  const plotWidth = W - PADDING.left - PADDING.right;
  const plotHeight = H - PADDING.top - PADDING.bottom;

  // Background
  ctx.fillStyle = '#faf9f6';
  ctx.fillRect(0, 0, W, H);

  // 1. Vertical Year Gridlines & Column Bands (2019 to 2024)
  TERM_YEARS.forEach((year, idx) => {
    const yearX = getYearX(year);
    const { sx } = worldToScreen(yearX, 0);

    // Subtle vertical column guide line
    ctx.strokeStyle = 'rgba(20, 19, 26, 0.06)';
    ctx.lineWidth = 1;
    ctx.setLineDash([4, 6]);
    ctx.beginPath();
    ctx.moveTo(sx, PADDING.top * camera.scale + camera.oy);
    ctx.lineTo(sx, (PADDING.top + plotHeight) * camera.scale + camera.oy);
    ctx.stroke();
    ctx.setLineDash([]);

    // Year Tick on bottom X-Axis line
    const { sy: baseSy } = worldToScreen(0, PADDING.top + plotHeight);
    
    // Tick mark
    ctx.strokeStyle = 'rgba(20, 19, 26, 0.3)';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(sx, baseSy);
    ctx.lineTo(sx, baseSy + 6);
    ctx.stroke();

    // Year Label (Bold & prominent on X-axis)
    ctx.fillStyle = '#14131a';
    ctx.font = '700 12px Plus Jakarta Sans, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(year, sx, baseSy + 20);
  });

  // 2. Horizontal Gridlines (Questions Asked)
  const qTicks = [0, 100, 200, 300, 400, 500, 600];
  qTicks.forEach(q => {
    const qFrac = (q - MIN_QUESTIONS) / (MAX_QUESTIONS - MIN_QUESTIONS);
    const wy = PADDING.top + (1 - qFrac) * plotHeight;
    const { sy } = worldToScreen(0, wy);
    const { sx: startX } = worldToScreen(PADDING.left, 0);
    const { sx: endX } = worldToScreen(PADDING.left + plotWidth, 0);

    ctx.strokeStyle = q === 0 ? 'rgba(20, 19, 26, 0.2)' : 'rgba(20, 19, 26, 0.05)';
    ctx.lineWidth = q === 0 ? 1.5 : 0.5;
    ctx.beginPath();
    ctx.moveTo(Math.max(0, startX - 10), sy);
    ctx.lineTo(Math.min(W, endX + 10), sy);
    ctx.stroke();

    // Y Tick label
    ctx.fillStyle = 'rgba(100, 100, 120, 0.7)';
    ctx.font = '500 10px Plus Jakarta Sans, sans-serif';
    ctx.textAlign = 'right';
    ctx.fillText(q, PADDING.left - 10, sy + 3.5);
  });

  // Bottom X-Axis baseline title
  const { sy: baseSy } = worldToScreen(0, PADDING.top + plotHeight);
  ctx.fillStyle = 'rgba(120, 120, 140, 0.85)';
  ctx.font = '600 10px Plus Jakarta Sans, sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('← 17th Lok Sabha Parliamentary Term Timeline (2019 – 2024) →', W / 2, baseSy + 36);

  // Active MPs
  const activeMPs = getActiveMPs();
  const activeSet = new Set(activeMPs.map(m => m.id));

  // 3. Render Inactive (Dimmed) Nodes
  nodes.forEach(node => {
    if (activeSet.has(node.mp.id)) return;
    const { sx, sy } = worldToScreen(node.wx, node.wy);
    if (sx < -20 || sx > W + 20 || sy < -20 || sy > H + 20) return;

    const r = Math.max(2, node.baseRadius * camera.scale);
    ctx.globalAlpha = 0.08;
    ctx.beginPath();
    ctx.arc(sx, sy, r, 0, Math.PI * 2);
    ctx.fillStyle = getPartyPalette(node.mp.party).fill;
    ctx.fill();
  });
  ctx.globalAlpha = 1;

  // 4. Render Active Nodes
  const activeNodes = nodes.filter(n => activeSet.has(n.mp.id))
    .sort((a, b) => b.baseRadius - a.baseRadius);

  const lockedId = lockedMP?.id;
  const hoveredId = hoveredMP?.id;

  activeNodes.forEach(node => {
    const { sx, sy } = worldToScreen(node.wx, node.wy);
    if (sx < -40 || sx > W + 40 || sy < -40 || sy > H + 40) return;

    const isLocked = node.mp.id === lockedId;
    const isHovered = node.mp.id === hoveredId;

    let opacity = 0.85;
    if (topicHighlight !== 'All') {
      const share = node.mp.s[topicHighlight] || 0;
      const globalAvg = DATA.avg[topicHighlight] || 1;
      if (share < globalAvg * 0.4) {
        opacity = 0.2;
      } else {
        opacity = 0.95;
      }
    }

    const palette = getPartyPalette(node.mp.party);
    const r = Math.max(3, node.baseRadius * camera.scale);

    ctx.globalAlpha = isLocked || isHovered ? 1 : opacity;

    // Fill circle (flat, clean, no drop shadows)
    ctx.beginPath();
    ctx.arc(sx, sy, r, 0, Math.PI * 2);
    ctx.fillStyle = palette.fill;
    ctx.fill();

    // Clean outline
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = isLocked ? 2.5 : 1.2;
    ctx.stroke();

    if (isLocked || isHovered) {
      ctx.strokeStyle = palette.stroke;
      ctx.lineWidth = isLocked ? 2.5 : 1.8;
      ctx.beginPath();
      ctx.arc(sx, sy, r + 2.5, 0, Math.PI * 2);
      ctx.stroke();
    }
  });
  ctx.globalAlpha = 1;

  // 5. Labels at high zoom
  if (camera.scale > 1.8) {
    activeNodes.forEach(node => {
      const isLocked = node.mp.id === lockedId;
      const isHovered = node.mp.id === hoveredId;
      if (!isLocked && !isHovered && camera.scale < 3) return;

      const { sx, sy } = worldToScreen(node.wx, node.wy);
      const r = node.baseRadius * camera.scale;

      ctx.fillStyle = '#14131a';
      ctx.font = '600 10px Plus Jakarta Sans, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(node.mp.name.split(' ').slice(0, 2).join(' '), sx, sy - r - 5);
    });
  }
}

// ── HIT TEST FOR HOVER & CLICK ──
function hitTest(screenX, screenY) {
  const activeSet = new Set(getActiveMPs().map(m => m.id));
  let closest = null;
  let minDistance = 24;

  const candidates = nodes.filter(n => activeSet.has(n.mp.id))
    .sort((a, b) => a.baseRadius - b.baseRadius);

  for (const node of candidates) {
    const { sx, sy } = worldToScreen(node.wx, node.wy);
    const dist = Math.hypot(screenX - sx, screenY - sy);
    const hitRadius = Math.max(node.baseRadius * camera.scale + 3, 10);
    if (dist <= hitRadius && dist < minDistance) {
      minDistance = dist;
      closest = node.mp;
    }
  }
  return closest;
}

// ── UPDATE STORY PANEL & TOP 10 RANKINGS ──
function updateStoryPanel(focusedMP) {
  const activeMPs = getActiveMPs();
  const countEl = document.getElementById('active-count');
  countEl.textContent = `${activeMPs.length} MPs Active`;

  const avgQ = activeMPs.length
    ? Math.round(activeMPs.reduce((sum, m) => sum + m.total, 0) / activeMPs.length)
    : 0;
  document.getElementById('h-avg-q').textContent = avgQ;

  let scopeTag = '17th Lok Sabha (2019–2024)';
  let scopeTitle = `All ${DATA.total_mps} Members of Parliament`;

  if (focusedMP) {
    scopeTag = 'Member of Parliament';
    scopeTitle = focusedMP.name;
  } else if (stateFilter !== 'All' && partyFilter !== 'All') {
    scopeTag = 'Filtered Subset';
    scopeTitle = `${partyFilter} MPs from ${stateFilter}`;
  } else if (stateFilter !== 'All') {
    scopeTag = 'State Focus';
    scopeTitle = `MPs from ${stateFilter} (${activeMPs.length})`;
  } else if (partyFilter !== 'All') {
    scopeTag = 'Party Focus';
    scopeTitle = `${partyFilter} Delegation (${activeMPs.length} MPs)`;
  } else if (genderFilter !== 'All') {
    scopeTag = 'Cohort';
    scopeTitle = `${genderFilter} Members of Parliament (${activeMPs.length})`;
  }

  document.getElementById('panel-scope-tag').textContent = scopeTag;
  document.getElementById('panel-scope-title').textContent = scopeTitle;

  renderMPCard(focusedMP);

  let shares = {};
  if (focusedMP) {
    shares = focusedMP.s;
  } else {
    DATA.sectors.forEach(sec => {
      const values = activeMPs.map(m => m.s[sec] || 0);
      shares[sec] = values.length
        ? values.reduce((a, b) => a + b, 0) / values.length
        : 0;
    });
  }

  const top10 = DATA.sectors.map(sec => ({
    sec,
    val: shares[sec] || 0,
    label: DATA.labels[sec] || sec
  })).sort((a, b) => b.val - a.val).slice(0, 10);

  const maxShare = top10[0]?.val || 1;
  const container = document.getElementById('rankings-container');

  container.innerHTML = top10.map((item, idx) => {
    const rankClass = idx === 0 ? 'top-1' : idx === 1 ? 'top-2' : idx === 2 ? 'top-3' : '';
    const isTopicHighlighted = topicHighlight === item.sec ? 'is-highlighted' : '';
    const barWidth = Math.round((item.val / maxShare) * 100);

    return `
      <div class="rank-row ${rankClass} ${isTopicHighlighted}">
        <span class="rank-position">#${idx + 1}</span>
        <span class="rank-topic-name" title="${item.label}">${item.label}</span>
        <div class="rank-bar-track">
          <div class="rank-bar-fill" style="width:${barWidth}%"></div>
        </div>
        <span class="rank-percentage">${item.val.toFixed(1)}%</span>
      </div>
    `;
  }).join('');
}

function renderMPCard(mp) {
  const card = document.getElementById('mp-card');
  if (!mp) {
    card.className = 'hidden';
    return;
  }
  card.className = '';

  const imgUrl = MP_IMGS[mp.id];
  const palette = getPartyPalette(mp.party);
  const initials = mp.name.split(' ').slice(0, 2).map(w => w[0]).join('');

  card.innerHTML = `
    <div class="mp-profile">
      ${imgUrl
        ? `<img class="mp-avatar" src="${imgUrl}" alt="${mp.name}" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
           <div class="mp-avatar-fallback" style="display:none">${initials}</div>`
        : `<div class="mp-avatar-fallback">${initials}</div>`
      }
      <div class="mp-details">
        <div class="mp-name-tag">${mp.name}</div>
        <div class="mp-meta-sub">${mp.constituency}, ${mp.state}</div>
        <div class="mp-meta-sub">${mp.gender} · ${mp.age} years · 17th Lok Sabha</div>
        <span class="mp-party-pill" style="background:${palette.bg};color:${palette.text};border:1px solid ${palette.stroke}40">
          ${mp.party}
        </span>
      </div>
    </div>

    <div class="mp-metrics-grid">
      <div class="metric-box">
        <div class="metric-val">${mp.total}</div>
        <div class="metric-label">Questions</div>
      </div>
      <div class="metric-box">
        <div class="metric-val">#${mp.rank}</div>
        <div class="metric-label">Natl. Rank</div>
      </div>
      <div class="metric-box">
        <div class="metric-val">${mp.debates || 0}</div>
        <div class="metric-label">Debates</div>
      </div>
    </div>

    <div class="card-unlock-hint">
      <span>${lockedMP ? '📌 Locked View' : '👁️ Hover Preview'}</span>
      ${lockedMP ? `<button class="btn-unlock" id="btn-unlock-mp">Deselect MP ✕</button>` : ''}
    </div>
  `;

  if (lockedMP) {
    const unBtn = document.getElementById('btn-unlock-mp');
    if (unBtn) {
      unBtn.onclick = () => {
        lockedMP = null;
        hoveredMP = null;
        updateStoryPanel(null);
        draw();
      };
    }
  }
}

// ── FLOATING TOOLTIP ──
const tooltip = document.getElementById('tooltip');

function showTooltip(mp, clientX, clientY) {
  const imgUrl = MP_IMGS[mp.id];
  const palette = getPartyPalette(mp.party);
  const initials = mp.name.split(' ').slice(0, 2).map(w => w[0]).join('');

  const top3 = DATA.sectors.map(s => ({
    name: DATA.labels[s] || s,
    val: mp.s[s] || 0
  })).sort((a, b) => b.val - a.val).slice(0, 3);

  tooltip.innerHTML = `
    <div class="tt-header">
      ${imgUrl
        ? `<img class="tt-avatar" src="${imgUrl}" alt="${mp.name}" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
           <div class="tt-avatar-fallback" style="display:none">${initials}</div>`
        : `<div class="tt-avatar-fallback">${initials}</div>`
      }
      <div class="tt-meta">
        <div class="tt-name">${mp.name}</div>
        <div class="tt-geo">${mp.constituency}, ${mp.state}</div>
        <span class="tt-party-pill" style="background:${palette.bg};color:${palette.text};border:1px solid ${palette.stroke}30">
          ${mp.party} · Term ${mp.term_year || '2019–2024'}
        </span>
      </div>
    </div>

    <div class="tt-stat-row">
      <span class="tt-stat-main">${mp.total} Questions</span>
      <span class="tt-stat-sub">Rank #${mp.rank}</span>
    </div>

    <div class="tt-topics-title">Top Priorities</div>
    ${top3.map(t => `
      <div class="tt-topic-item">
        <span class="tt-topic-name">${t.name}</span>
        <span class="tt-topic-val">${t.val.toFixed(1)}%</span>
      </div>
    `).join('')}
  `;

  const tw = tooltip.offsetWidth || 230;
  const th = tooltip.offsetHeight || 220;

  const posX = Math.min(clientX + 16, window.innerWidth - tw - 12);
  const posY = Math.min(clientY + 12, window.innerHeight - th - 12);

  tooltip.style.left = `${posX}px`;
  tooltip.style.top = `${posY}px`;
  tooltip.classList.add('visible');
}

function hideTooltip() {
  tooltip.classList.remove('visible');
}

// ── CANVAS INTERACTION EVENTS ──
let dragStart = null;

canvas.addEventListener('wheel', e => {
  e.preventDefault();
  const rect = canvas.getBoundingClientRect();
  const cx = e.clientX - rect.left;
  const cy = e.clientY - rect.top;
  const zoomFactor = e.deltaY < 0 ? 1.15 : 1 / 1.15;
  zoom(zoomFactor, cx, cy);
}, { passive: false });

canvas.addEventListener('mousedown', e => {
  dragStart = { x: e.clientX, y: e.clientY, ox: camera.ox, oy: camera.oy };
  container.classList.add('grabbing');
});

window.addEventListener('mousemove', e => {
  if (dragStart) {
    camera.ox = dragStart.ox + (e.clientX - dragStart.x);
    camera.oy = dragStart.oy + (e.clientY - dragStart.y);
    draw();
    return;
  }

  const rect = canvas.getBoundingClientRect();
  const mp = hitTest(e.clientX - rect.left, e.clientY - rect.top);

  if (mp) {
    container.classList.add('pointing');
    hoveredMP = mp;
    showTooltip(mp, e.clientX, e.clientY);
    if (!lockedMP) {
      updateStoryPanel(mp);
    }
    draw();
  } else {
    container.classList.remove('pointing');
    hideTooltip();
    if (!lockedMP && hoveredMP) {
      hoveredMP = null;
      updateStoryPanel(null);
      draw();
    }
  }
});

window.addEventListener('mouseup', e => {
  if (dragStart) {
    const moved = Math.hypot(e.clientX - dragStart.x, e.clientY - dragStart.y);
    dragStart = null;
    container.classList.remove('grabbing');

    if (moved < 5) {
      const rect = canvas.getBoundingClientRect();
      const mp = hitTest(e.clientX - rect.left, e.clientY - rect.top);
      if (mp) {
        lockedMP = lockedMP?.id === mp.id ? null : mp;
        updateStoryPanel(lockedMP || mp);
      } else {
        lockedMP = null;
        updateStoryPanel(null);
      }
      draw();
    }
  }
});

canvas.addEventListener('mouseleave', () => {
  hideTooltip();
  if (!lockedMP && hoveredMP) {
    hoveredMP = null;
    updateStoryPanel(null);
    draw();
  }
});

// Zoom button controls
document.getElementById('btn-zoom-in').onclick = () => zoom(1.35, W / 2, H / 2);
document.getElementById('btn-zoom-out').onclick = () => zoom(1 / 1.35, W / 2, H / 2);
document.getElementById('btn-zoom-reset').onclick = resetView;

// ── POPULATE FILTERS ──
function initFilters() {
  // 1. States Dropdown
  const stateSelect = document.getElementById('sel-state');
  DATA.states.forEach(st => {
    const opt = document.createElement('option');
    opt.value = st;
    const count = DATA.mps.filter(m => m.state === st).length;
    opt.textContent = `${st} (${count})`;
    stateSelect.appendChild(opt);
  });

  stateSelect.onchange = e => {
    stateFilter = e.target.value;
    lockedMP = null;
    hoveredMP = null;
    updateStoryPanel(null);
    draw();
  };

  // 2. Parties Dropdown
  const partySelect = document.getElementById('sel-party');
  DATA.parties.forEach(pt => {
    const opt = document.createElement('option');
    opt.value = pt;
    const count = DATA.mps.filter(m => m.party === pt).length;
    opt.textContent = `${pt} (${count})`;
    partySelect.appendChild(opt);
  });

  partySelect.onchange = e => {
    partyFilter = e.target.value;
    lockedMP = null;
    hoveredMP = null;
    updateStoryPanel(null);
    draw();
  };

  // 3. Gender Pills
  const genderPills = document.querySelectorAll('#gender-pills .filter-pill');
  genderPills.forEach(pill => {
    pill.onclick = () => {
      genderPills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      genderFilter = pill.dataset.gender;
      lockedMP = null;
      hoveredMP = null;
      updateStoryPanel(null);
      draw();
    };
  });

  // 4. Topic Highlight Sub-bar (Highlight only)
  const topicContainer = document.getElementById('topic-pills-list');
  DATA.sectors.slice(0, 14).forEach(sec => {
    const pill = document.createElement('span');
    pill.className = 't-pill';
    pill.dataset.topic = sec;
    pill.textContent = DATA.labels[sec] || sec;
    pill.onclick = () => {
      document.querySelectorAll('#topic-pills-list .t-pill').forEach(p => p.classList.remove('active'));
      if (topicHighlight === sec) {
        topicHighlight = 'All';
        document.querySelector('[data-topic="All"]').classList.add('active');
      } else {
        topicHighlight = sec;
        pill.classList.add('active');
      }
      updateStoryPanel(lockedMP);
      draw();
    };
    topicContainer.appendChild(pill);
  });

  // Topic 'All' click
  document.querySelector('[data-topic="All"]').onclick = function() {
    document.querySelectorAll('#topic-pills-list .t-pill').forEach(p => p.classList.remove('active'));
    this.classList.add('active');
    topicHighlight = 'All';
    updateStoryPanel(lockedMP);
    draw();
  };

  // 5. Search Bar
  const searchInput = document.getElementById('search-input');
  searchInput.oninput = e => {
    searchQuery = e.target.value.trim();
    lockedMP = null;
    hoveredMP = null;
    updateStoryPanel(null);
    draw();
  };
}

// ── INITIALIZATION ──
window.addEventListener('resize', () => {
  resizeCanvas();
  computeNodePositions();
  draw();
});

resizeCanvas();
computeNodePositions();
initFilters();
updateStoryPanel(null);
draw();
</script>
</body>
</html>
"""

HTML_FINAL = HTML_TEMPLATE.replace('__DATA_PLACEHOLDER__', data_str).replace('__IMGS_PLACEHOLDER__', imgs_str)

with open('/Users/aashima/Desktop/DataViz5/outcome/loksabha-questions/index.html', 'w') as f:
    f.write(HTML_FINAL)

print(f"Generated index.html with 2019-2024 X-axis: {len(HTML_FINAL)//1024} KB")
print(f"Braces balanced: {HTML_FINAL.count('{') == HTML_FINAL.count('}')}")
print(f"Parens balanced: {HTML_FINAL.count('(') == HTML_FINAL.count(')')}")
