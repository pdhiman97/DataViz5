"""
Script to generate the Lok Sabha Parliamentary Questions Map Visualization:
- Includes interactive Hide / Unhide eye toggle for every sector on the right panel
- Unambiguous 20-sector palette with distinct hues across the spectrum
- Clean, unobstructed map with minimal floating bubble-size legend on the bottom left
- Synchronized to root index.html, docs/index.html, and outcome folders
"""
import json
import os

with open('/Users/aashima/Desktop/DataViz5/data/loksabha-questions/curated/viz_v5_data.json') as f:
    DATA = json.load(f)

with open('/Users/aashima/Desktop/DataViz5/data/loksabha-questions/curated/mp_coords.json') as f:
    COORDS = json.load(f)

with open('/Users/aashima/Desktop/DataViz5/data/loksabha-questions/curated/mp_images.json') as f:
    MP_IMGS = json.load(f)

with open('/Users/aashima/Desktop/DataViz5/data/loksabha-questions/curated/india_adarsh.json') as f:
    INDIA_GEOJSON = json.load(f)

# Attach coordinates and compute top sector for each MP
for mp in DATA['mps']:
    mp['coords'] = COORDS.get(mp['id'], [78.9629, 20.5937])
    s = mp.get('s', {})
    if s:
        top_sec = max(s.items(), key=lambda x: x[1])
        mp['top_sector'] = top_sec[0]
        mp['top_sector_pct'] = top_sec[1]
    else:
        mp['top_sector'] = 'Health and Family Welfare'
        mp['top_sector_pct'] = 0.0

data_str = json.dumps(DATA)
imgs_str = json.dumps(MP_IMGS)
geojson_str = json.dumps(INDIA_GEOJSON)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Lok Sabha Parliamentary Questions — Sector Geography</title>

<!-- Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&display=swap" rel="stylesheet">

<!-- D3.js -->
<script src="https://d3js.org/d3.v7.min.js"></script>

<style>
:root {
  --bg: #faf9f6;
  --surface: #ffffff;
  --surface-alt: #f4f2eb;
  --border: #e6e3da;
  --border-subtle: #eeece5;
  --ink: #14131a;
  --ink-secondary: #575560;
  --ink-muted: #8b8896;
  
  --primary: #c2410c;
  --primary-light: #fff7ed;
  --primary-border: #ffedd5;
  
  --accent-blue: #1d4ed8;
  --accent-blue-light: #eff6ff;
  --accent-blue-border: #dbeafe;

  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-serif: 'Newsreader', Georgia, serif;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body {
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: var(--bg);
  color: var(--ink);
  font-family: var(--font-sans);
  -webkit-font-smoothing: antialiased;
}

/* ── APP CONTAINER ── */
#app {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

/* ── HEADER ── */
header {
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  padding: 0.55rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-shrink: 0;
  z-index: 10;
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}
.brand-title {
  font-family: var(--font-serif);
  font-size: 1.2rem;
  font-weight: 600;
  letter-spacing: -0.01em;
  color: var(--ink);
}
.term-badge {
  font-size: 0.62rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  background: var(--surface-alt);
  border: 1px solid var(--border);
  padding: 0.18rem 0.55rem;
  border-radius: 4px;
  color: var(--ink-secondary);
}
.term-badge strong { color: var(--primary); }

.header-stats {
  display: flex;
  align-items: center;
  gap: 1.15rem;
}
.h-stat {
  font-size: 0.7rem;
  color: var(--ink-secondary);
  display: flex;
  align-items: center;
  gap: 0.3rem;
}
.h-stat strong { color: var(--ink); font-weight: 600; }
.badge-count {
  background: var(--primary-light);
  color: var(--primary);
  border: 1px solid var(--primary-border);
  font-size: 0.65rem;
  font-weight: 600;
  padding: 0.18rem 0.6rem;
  border-radius: 100px;
}

/* ── FILTER TOOLBAR ── */
#filters {
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  padding: 0.45rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 1.15rem;
  overflow-x: auto;
  flex-shrink: 0;
  z-index: 9;
}
#filters::-webkit-scrollbar { display: none; }

.filter-item { display: flex; align-items: center; gap: 0.4rem; flex-shrink: 0; }
.filter-label {
  font-size: 0.6rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--ink-muted);
}

/* Slider for Total Questions */
.slider-container {
  display: flex;
  align-items: center;
  gap: 0.45rem;
}
.range-slider {
  -webkit-appearance: none;
  appearance: none;
  width: 90px;
  height: 4px;
  border-radius: 2px;
  background: var(--border);
  outline: none;
}
.range-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 13px;
  height: 13px;
  border-radius: 50%;
  background: var(--primary);
  cursor: pointer;
  border: 2px solid #ffffff;
  box-shadow: 0 1px 3px rgba(0,0,0,0.25);
  transition: transform 0.1s;
}
.range-slider::-webkit-slider-thumb:hover { transform: scale(1.2); }
.slider-val-badge {
  font-size: 0.65rem;
  font-weight: 600;
  color: var(--ink);
  font-variant-numeric: tabular-nums;
  min-width: 35px;
}

/* Dropdown Selects */
.select-custom {
  font-family: var(--font-sans);
  font-size: 0.7rem;
  font-weight: 500;
  color: var(--ink);
  background: var(--surface-alt);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 0.28rem 0.55rem;
  outline: none;
  cursor: pointer;
  transition: border-color 0.15s;
}
.select-custom:hover { border-color: var(--ink-muted); }
.select-custom:focus { border-color: var(--primary); background: var(--surface); }

/* Search Box */
.search-box {
  position: relative;
  margin-left: auto;
  flex-shrink: 0;
}
.search-input {
  font-family: var(--font-sans);
  font-size: 0.7rem;
  padding: 0.28rem 0.55rem 0.28rem 1.65rem;
  border-radius: 6px;
  border: 1px solid var(--border);
  background: var(--surface-alt);
  color: var(--ink);
  outline: none;
  width: 155px;
  transition: all 0.2s;
}
.search-input::placeholder { color: var(--ink-muted); }
.search-input:focus {
  background: var(--surface);
  border-color: var(--primary);
  width: 195px;
}
.search-icon {
  position: absolute;
  left: 0.55rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--ink-muted);
  font-size: 0.72rem;
  pointer-events: none;
}

/* ── MAIN WORKSPACE ── */
#workspace {
  display: grid;
  grid-template-columns: 1fr 370px;
  flex: 1;
  min-height: 0;
  overflow: hidden;
  position: relative;
}

/* ── MAP CONTAINER ── */
#map-container {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: var(--bg);
  cursor: grab;
}
#map-container.grabbing { cursor: grabbing; }
#map-container.pointing { cursor: pointer; }
#map-svg {
  width: 100%;
  height: 100%;
  display: block;
}

/* Official India State boundary styling */
.state-path {
  fill: #edeae1;
  stroke: #cfc8ba;
  stroke-width: 0.85px;
  stroke-linejoin: round;
  transition: fill 0.15s ease;
}
.state-path:hover {
  fill: #e3dfd3;
}

.map-root {
  shape-rendering: geometricPrecision;
}

/* MP Circle Nodes */
.mp-dot {
  stroke: #ffffff;
  cursor: pointer;
  transition: transform 0.15s ease, opacity 0.2s ease;
}
.mp-dot:hover {
  stroke: #14131a;
  opacity: 1 !important;
}
.mp-dot.is-locked {
  stroke: #14131a;
  opacity: 1 !important;
}

/* ── MINIMAL BUBBLE SIZE LEGEND (BOTTOM-LEFT) ── */
.map-legend-panel {
  position: absolute;
  bottom: 1.25rem;
  left: 1.25rem;
  background: rgba(255, 255, 255, 0.94);
  backdrop-filter: blur(8px);
  border: 1px solid var(--border);
  padding: 0.45rem 0.8rem;
  border-radius: 8px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  gap: 0.85rem;
  z-index: 5;
  pointer-events: auto;
}

.legend-title {
  font-weight: 700;
  color: var(--ink);
  text-transform: uppercase;
  font-size: 0.58rem;
  letter-spacing: 0.06em;
  white-space: nowrap;
}

.legend-bubbles-row {
  display: flex;
  align-items: center;
  gap: 0.65rem;
}
.legend-bubble-item {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.62rem;
  color: var(--ink-secondary);
}
.legend-bubble-icon {
  border-radius: 50%;
  background: #71717a;
  border: 1px solid #ffffff;
  display: inline-block;
  opacity: 0.9;
}

/* Canvas Zoom Controls */
.map-controls {
  position: absolute;
  bottom: 1.25rem;
  right: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 0.2rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.06);
  z-index: 5;
}
.c-btn {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--ink-secondary);
  cursor: pointer;
  transition: all 0.15s;
}
.c-btn:hover {
  background: var(--surface-alt);
  color: var(--ink);
}
.c-btn-fit {
  font-size: 0.58rem;
  font-weight: 700;
  letter-spacing: 0.04em;
}

/* ── RIGHT STORY & ALL 20 SECTORS PANEL ── */
#story-panel {
  background: var(--surface);
  border-left: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  height: 100%;
  min-height: 0;
}

.panel-header {
  padding: 0.75rem 1.15rem;
  border-bottom: 1px solid var(--border);
  background: var(--surface);
  flex-shrink: 0;
}
.panel-eyebrow {
  font-size: 0.6rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--primary);
  margin-bottom: 0.15rem;
}
.panel-headline {
  font-family: var(--font-serif);
  font-size: 1.12rem;
  font-weight: 500;
  color: var(--ink);
  line-height: 1.25;
}

/* Selected MP Card */
#mp-card {
  padding: 0.75rem 1.15rem;
  border-bottom: 1px solid var(--border-subtle);
  background: var(--surface-alt);
  flex-shrink: 0;
  transition: all 0.25s ease;
}
#mp-card.hidden { display: none; }

.mp-profile {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  margin-bottom: 0.55rem;
}
.mp-avatar {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  object-fit: cover;
  object-position: center top;
  background: var(--surface);
  border: 2px solid var(--border);
  flex-shrink: 0;
}
.mp-avatar-fallback {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: var(--surface);
  border: 2px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-serif);
  font-size: 1.15rem;
  color: var(--ink-muted);
  flex-shrink: 0;
}
.mp-details { flex: 1; min-width: 0; }
.mp-name-tag {
  font-family: var(--font-serif);
  font-size: 0.98rem;
  font-weight: 500;
  color: var(--ink);
  line-height: 1.2;
  margin-bottom: 0.1rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.mp-meta-sub {
  font-size: 0.62rem;
  color: var(--ink-secondary);
  line-height: 1.35;
}
.mp-tags-row {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  margin-top: 0.25rem;
  flex-wrap: wrap;
}
.mp-pill {
  display: inline-block;
  padding: 0.1rem 0.4rem;
  border-radius: 100px;
  font-size: 0.55rem;
  font-weight: 700;
  letter-spacing: 0.02em;
}

.mp-metrics-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 0.35rem;
  padding-top: 0.35rem;
  border-top: 1px solid var(--border);
}
.metric-box { text-align: center; }
.metric-val {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--ink);
  line-height: 1;
}
.metric-label {
  font-size: 0.54rem;
  color: var(--ink-muted);
  font-weight: 500;
  margin-top: 0.15rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.card-unlock-hint {
  font-size: 0.55rem;
  color: var(--ink-muted);
  margin-top: 0.4rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.btn-unlock {
  color: var(--primary);
  background: none;
  border: none;
  font-size: 0.55rem;
  font-weight: 600;
  cursor: pointer;
  padding: 0;
}
.btn-unlock:hover { text-decoration: underline; }

/* Rankings list - ALL 20 SECTORS */
.rankings-section {
  flex: 1;
  overflow-y: auto;
  padding: 0.65rem 1rem 1rem;
  min-height: 0;
}
.rankings-section::-webkit-scrollbar { width: 4px; }
.rankings-section::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

.rankings-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.55rem;
  padding-bottom: 0.35rem;
  border-bottom: 1px solid var(--border-subtle);
}
.rankings-title-group {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
}
.rankings-heading {
  font-size: 0.6rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--ink);
}
.rankings-subheading {
  font-size: 0.56rem;
  color: var(--ink-muted);
}

.sector-actions {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}
.btn-sec-action {
  background: var(--surface-alt);
  border: 1px solid var(--border);
  color: var(--ink-secondary);
  font-size: 0.56rem;
  font-weight: 600;
  padding: 0.15rem 0.45rem;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.12s ease;
}
.btn-sec-action:hover {
  background: var(--surface);
  color: var(--ink);
  border-color: var(--primary);
}

.rank-row {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.25rem 0.3rem;
  border-radius: 6px;
  border: 1px solid transparent;
  transition: all 0.12s ease;
  cursor: pointer;
}
.rank-row:hover { background: var(--surface-alt); }
.rank-row.is-highlighted {
  background: var(--accent-blue-light);
  border-color: var(--accent-blue-border);
}

.btn-eye-toggle {
  background: none;
  border: none;
  color: var(--ink-muted);
  cursor: pointer;
  padding: 0.15rem 0.2rem;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s ease;
  flex-shrink: 0;
}
.btn-eye-toggle:hover {
  color: var(--primary);
  background: var(--surface);
}

.rank-row.is-sector-hidden {
  opacity: 0.35;
  background: transparent !important;
}
.rank-row.is-sector-hidden .rank-topic-name {
  text-decoration: line-through;
  color: var(--ink-muted);
}
.rank-row.is-sector-hidden .rank-bar-fill {
  background: #cbd5e1 !important;
}
.rank-row.is-sector-hidden .btn-eye-toggle {
  color: #ef4444;
}

.rank-color-pip {
  width: 7.5px;
  height: 7.5px;
  border-radius: 50%;
  flex-shrink: 0;
}

.rank-position {
  font-size: 0.63rem;
  font-weight: 700;
  color: var(--ink-muted);
  flex: 0 0 14px;
  text-align: right;
  font-variant-numeric: tabular-nums;
}

.rank-topic-name {
  font-size: 0.67rem;
  font-weight: 500;
  color: var(--ink-secondary);
  flex: 0 0 105px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.rank-row:hover .rank-topic-name { color: var(--ink); font-weight: 600; }

.rank-bar-track {
  flex: 1;
  height: 6px;
  background: var(--border-subtle);
  border-radius: 3px;
  overflow: hidden;
  position: relative;
}
.rank-bar-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.45s cubic-bezier(0.4, 0, 0.2, 1), background 0.3s;
}

.rank-percentage {
  font-size: 0.65rem;
  font-weight: 600;
  color: var(--ink);
  flex: 0 0 35px;
  text-align: right;
  font-variant-numeric: tabular-nums;
}

/* ── FLOATING TOOLTIP ── */
#tooltip {
  position: fixed;
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(10px);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 0.7rem 0.85rem;
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
  pointer-events: none;
  font-size: 0.68rem;
  color: var(--ink);
  z-index: 100;
  max-width: 250px;
  display: none;
  opacity: 0;
  transition: opacity 0.12s ease;
}
#tooltip.visible {
  display: block;
  opacity: 1;
}
.tt-header {
  display: flex;
  gap: 0.55rem;
  align-items: center;
  border-bottom: 1px solid var(--border-subtle);
  padding-bottom: 0.45rem;
  margin-bottom: 0.45rem;
}
.tt-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid var(--border);
  flex-shrink: 0;
}
.tt-avatar-fallback {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--surface-alt);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--ink-muted);
  border: 1px solid var(--border);
  flex-shrink: 0;
}
.tt-meta { flex: 1; min-width: 0; }
.tt-name { font-weight: 600; font-size: 0.76rem; line-height: 1.2; }
.tt-geo { font-size: 0.62rem; color: var(--ink-secondary); margin-top: 0.1rem; }
.tt-tags-row { display: flex; gap: 0.25rem; margin-top: 0.2rem; flex-wrap: wrap; }
.tt-pill {
  font-size: 0.54rem;
  font-weight: 700;
  padding: 0.06rem 0.32rem;
  border-radius: 4px;
}

.tt-stat-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.4rem;
}
.tt-stat-main { font-weight: 700; color: var(--ink); font-size: 0.72rem; }
.tt-stat-sub { font-size: 0.6rem; color: var(--ink-muted); }

.tt-topics-title {
  font-size: 0.56rem;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--ink-muted);
  letter-spacing: 0.05em;
  margin-bottom: 0.2rem;
}
.tt-topic-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.62rem;
  color: var(--ink-secondary);
  padding: 0.1rem 0;
}
.tt-topic-name-wrap {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.tt-topic-pip {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
}
.tt-topic-val { font-weight: 600; color: var(--ink); }

@media (max-width: 1024px) {
  #workspace { grid-template-columns: 1fr; grid-template-rows: 1fr 280px; }
  #story-panel { border-left: none; border-top: 1px solid var(--border); }
}
</style>
</head>
<body>

<div id="app">
  <!-- HEADER -->
  <header>
    <div class="brand">
      <h1 class="brand-title">Lok Sabha Questions — Sector Geography</h1>
      <span class="term-badge">Term: <strong>2019–2024</strong> (17th Lok Sabha)</span>
    </div>
    <div class="header-stats">
      <div class="h-stat"><span>Total MPs:</span> <strong>499</strong></div>
      <div class="h-stat"><span>National Avg:</span> <strong id="h-avg-q">163</strong> Qs</div>
      <div class="h-stat"><span class="badge-count" id="active-count">499 MPs Active</span></div>
    </div>
  </header>

  <!-- FILTER TOOLBAR -->
  <div id="filters">
    <!-- Slider: Min Questions -->
    <div class="filter-item">
      <span class="filter-label">Min Questions:</span>
      <div class="slider-container">
        <input type="range" class="range-slider" id="slider-questions" min="0" max="600" step="25" value="0">
        <span class="slider-val-badge" id="val-questions">≥ 0</span>
      </div>
    </div>

    <!-- Category Filter -->
    <div class="filter-item">
      <span class="filter-label">Debate Sector:</span>
      <select class="select-custom" id="sel-category">
        <option value="All">All 20 Sectors (Top Priority Mode)</option>
      </select>
    </div>

    <!-- State Filter -->
    <div class="filter-item">
      <span class="filter-label">State:</span>
      <select class="select-custom" id="sel-state">
        <option value="All">All States (37)</option>
      </select>
    </div>

    <!-- Party Filter -->
    <div class="filter-item">
      <span class="filter-label">Party:</span>
      <select class="select-custom" id="sel-party">
        <option value="All">All Parties</option>
      </select>
    </div>

    <!-- Search Input -->
    <div class="search-box">
      <span class="search-icon">🔍</span>
      <input type="text" class="search-input" id="search-input" placeholder="Search MP, constituency…" autocomplete="off">
    </div>
  </div>

  <!-- MAIN WORKSPACE -->
  <div id="workspace">

    <!-- MAP CONTAINER -->
    <div id="map-container">
      <svg id="map-svg"></svg>

      <!-- Minimal Floating Bubble Size Legend (Bottom-Left) -->
      <div class="map-legend-panel">
        <span class="legend-title" id="leg-size-title">Bubble Size = Questions Asked</span>
        <div class="legend-bubbles-row">
          <div class="legend-bubble-item">
            <span class="legend-bubble-icon" style="width:5px;height:5px;"></span>
            <span>10</span>
          </div>
          <div class="legend-bubble-item">
            <span class="legend-bubble-icon" style="width:9px;height:9px;"></span>
            <span>200</span>
          </div>
          <div class="legend-bubble-item">
            <span class="legend-bubble-icon" style="width:13px;height:13px;"></span>
            <span>400</span>
          </div>
          <div class="legend-bubble-item">
            <span class="legend-bubble-icon" style="width:17px;height:17px;"></span>
            <span>600+</span>
          </div>
        </div>
      </div>

      <!-- Map Zoom Controls -->
      <div class="map-controls">
        <button class="c-btn" id="btn-zoom-in" title="Zoom in">+</button>
        <button class="c-btn c-btn-fit" id="btn-zoom-reset" title="Reset Map View">FIT</button>
        <button class="c-btn" id="btn-zoom-out" title="Zoom out">−</button>
      </div>
    </div>

    <!-- RIGHT STORY & ALL 20 SECTORS PANEL -->
    <aside id="story-panel">
      <div class="panel-header">
        <div class="panel-eyebrow" id="panel-scope-tag">National Overview</div>
        <h2 class="panel-headline" id="panel-scope-title">17th Lok Sabha (2019–2024)</h2>
      </div>

      <!-- MP Focus Card -->
      <div id="mp-card" class="hidden"></div>

      <!-- ALL 20 Parliamentary Sectors Rankings with Hide/Unhide -->
      <div class="rankings-section">
        <div class="rankings-header">
          <div class="rankings-title-group">
            <span class="rankings-heading">Parliamentary Sectors</span>
            <span class="rankings-subheading" id="sectors-active-pill">20 / 20 Active · Click 👁 to toggle</span>
          </div>
          <div class="sector-actions">
            <button class="btn-sec-action" id="btn-show-all-sec" title="Show all sectors">Show All</button>
            <button class="btn-sec-action" id="btn-clear-all-sec" title="Hide all sectors">Clear</button>
          </div>
        </div>
        <div id="rankings-container"></div>
      </div>
    </aside>

  </div>
</div>

<!-- FLOATING TOOLTIP -->
<div id="tooltip"></div>

<script>
// ── DATA & ASSETS INJECTION ──
const DATA = __DATA_PLACEHOLDER__;
const MP_IMGS = __IMGS_PLACEHOLDER__;
const INDIA_GEOJSON = __GEOJSON_PLACEHOLDER__;

let currentZoomScale = 1;

// ── 20-SECTOR DISTINCT COLOR PALETTE ──
const SECTOR_COLORS = {
  // RED: Sole primary crimson in entire palette
  'Health and Family Welfare': { fill: '#dc2626', stroke: '#b91c1c', text: '#991b1b', bg: '#fee2e2', name: 'Health & Family Welfare' },

  // BLUES
  'Railways': { fill: '#2563eb', stroke: '#1d4ed8', text: '#1e40af', bg: '#dbeafe', name: 'Railways' },
  'Jal Shakti': { fill: '#0284c7', stroke: '#0369a1', text: '#075985', bg: '#e0f2fe', name: 'Jal Shakti (Water Resources)' },
  'Civil Aviation': { fill: '#38bdf8', stroke: '#0284c7', text: '#0369a1', bg: '#f0f9ff', name: 'Civil Aviation' },
  'Communications': { fill: '#1e3a8a', stroke: '#172554', text: '#172554', bg: '#eff6ff', name: 'Communications (IT/Telecom)' },

  // GREENS
  'Agriculture and Farmers Welfare': { fill: '#16a34a', stroke: '#15803d', text: '#14532d', bg: '#dcfce7', name: 'Agriculture & Farmers' },
  'Environment, Forest and Climate Change': { fill: '#84cc16', stroke: '#65a30d', text: '#3f6212', bg: '#ecfccb', name: 'Environment & Climate' },
  'Labour and Employment': { fill: '#4d7c0f', stroke: '#365314', text: '#1a2e05', bg: '#f7fee7', name: 'Labour & Employment' },

  // TEAL / AQUA
  'AYUSH': { fill: '#14b8a6', stroke: '#0d9488', text: '#115e59', bg: '#ccfbf1', name: 'AYUSH' },
  'Housing and Urban Affairs': { fill: '#0f766e', stroke: '#115e59', text: '#134e4a', bg: '#ccfbf1', name: 'Housing & Urban Affairs' },

  // PURPLES & ORCHIDS
  'Education': { fill: '#4f46e5', stroke: '#4338ca', text: '#312e81', bg: '#e0e7ff', name: 'Education' },
  'Women and Child Development': { fill: '#d946ef', stroke: '#c026d3', text: '#86198f', bg: '#fae8ff', name: 'Women & Child Dev' },
  'Textiles': { fill: '#8b5cf6', stroke: '#7c3aed', text: '#5b21b6', bg: '#ede9fe', name: 'Textiles' },

  // YELLOWS & ORANGES
  'Finance': { fill: '#eab308', stroke: '#ca8a04', text: '#854d0e', bg: '#fef9c3', name: 'Finance & Economy' },
  'Road Transport and Highways': { fill: '#f97316', stroke: '#ea580c', text: '#9a3412', bg: '#ffedd5', name: 'Road Transport & Highways' },
  'Commerce and Industry': { fill: '#d97706', stroke: '#b45309', text: '#78350f', bg: '#fef3c7', name: 'Commerce & Industry' },
  'Consumer Affairs, Food and Public Distribution': { fill: '#ca8a04', stroke: '#a16207', text: '#713f12', bg: '#fef9c3', name: 'Consumer Affairs & Food' },

  // BROWNS & NEUTRALS
  'Rural Development': { fill: '#854d0e', stroke: '#713f12', text: '#451a03', bg: '#fef3c7', name: 'Rural Development' },
  'Home Affairs': { fill: '#475569', stroke: '#334155', text: '#0f172a', bg: '#f1f5f9', name: 'Home Affairs & Security' },
  'Petroleum and Natural Gas': { fill: '#1c1917', stroke: '#0c0a09', text: '#0c0a09', bg: '#f5f5f4', name: 'Petroleum & Gas' }
};

const DEFAULT_SECTOR_COLOR = { fill: '#64748b', stroke: '#475569', text: '#1e293b', bg: '#f1f5f9', name: 'Other Sector' };

function getSectorPalette(sec) {
  return SECTOR_COLORS[sec] || DEFAULT_SECTOR_COLOR;
}

// Party colors for reference pills
const PARTY_COLORS = {
  'BJP': { stroke: '#c04508', text: '#c04508', bg: '#fff4e6' },
  'INC': { stroke: '#155d9e', text: '#155d9e', bg: '#e7f5ff' },
  'DMK': { stroke: '#a61e1e', text: '#a61e1e', bg: '#ffe3e3' },
  'YSRCP': { stroke: '#096979', text: '#096979', bg: '#e3fafc' },
  'AITC': { stroke: '#216c30', text: '#216c30', bg: '#ebfbee' },
  'SS': { stroke: '#d9480f', text: '#d9480f', bg: '#fff4e6' },
  'SHS': { stroke: '#d9480f', text: '#d9480f', bg: '#fff4e6' },
  'JD(U)': { stroke: '#2b8a3e', text: '#2b8a3e', bg: '#ebfbee' },
  'BJD': { stroke: '#237032', text: '#237032', bg: '#ebfbee' },
  'BSP': { stroke: '#2b3eb1', text: '#2b3eb1', bg: '#edf2ff' },
  'BRS': { stroke: '#b32555', text: '#b32555', bg: '#fff0f6' },
  'TDP': { stroke: '#d98200', text: '#d98200', bg: '#fff9db' },
  'NCP': { stroke: '#144e85', text: '#144e85', bg: '#e7f5ff' },
  'SP': { stroke: '#b82020', text: '#b82020', bg: '#ffe3e3' },
  'CPIM': { stroke: '#9e1a1a', text: '#9e1a1a', bg: '#ffe3e3' },
  'OTHER': { stroke: '#495057', text: '#495057', bg: '#f1f3f5' }
};

function getPartyPalette(p) {
  return PARTY_COLORS[p] || PARTY_COLORS['OTHER'];
}

// ── STATE VARIABLES ──
let minQuestionsFilter = 0;
let selectedCategory = 'All';
let stateFilter = 'All';
let partyFilter = 'All';
let searchQuery = '';
let lockedMP = null;
let hoveredMP = null;

// Track which sectors are hidden (empty set = all visible)
let hiddenSectors = new Set();

// ── D3 MAP SETUP WITH DYNAMIC FIT-EXTENT ──
const mapContainer = document.getElementById('map-container');
const svg = d3.select('#map-svg');

let width = mapContainer.clientWidth;
let height = mapContainer.clientHeight;

const projection = d3.geoMercator();
const pathGenerator = d3.geoPath().projection(projection);

function updateProjection() {
  width = mapContainer.clientWidth;
  height = mapContainer.clientHeight;
  svg.attr('width', width).attr('height', height);

  // Auto-fit entire India GeoJSON into container with clean padding
  projection.fitExtent([[24, 20], [width - 24, height - 20]], INDIA_GEOJSON);
}

updateProjection();

// ── PROPORTIONAL AREA RADIUS CALCULATION ──
function getEffectiveQuestions(mp) {
  if (selectedCategory === 'All') {
    return mp.total;
  }
  const share = mp.s[selectedCategory] || 0;
  return Math.round((share / 100) * mp.total);
}

function computeBaseRadius(mp) {
  const q = getEffectiveQuestions(mp);
  const maxQ = selectedCategory === 'All' ? DATA.max_q : (DATA.max_q * 0.35);
  const frac = Math.max(0, q) / Math.max(1, maxQ);
  return 2.5 + Math.sqrt(frac) * 6.0; // 2.5px to 8.5px
}

function getDotFillColor(mp) {
  if (selectedCategory === 'All') {
    return getSectorPalette(mp.top_sector).fill;
  } else {
    return getSectorPalette(selectedCategory).fill;
  }
}

// Zoom Behavior
const zoom = d3.zoom()
  .scaleExtent([1, 18])
  .on('zoom', (event) => {
    currentZoomScale = event.transform.k;
    mapG.attr('transform', event.transform);

    dotsG.selectAll('.mp-dot')
      .attr('r', d => {
        const baseR = computeBaseRadius(d);
        const focusMult = (hoveredMP?.id === d.id || lockedMP?.id === d.id) ? 1.35 : 1.0;
        return (baseR * focusMult) / currentZoomScale;
      })
      .attr('stroke-width', d => {
        const isFocused = hoveredMP?.id === d.id || lockedMP?.id === d.id;
        return (isFocused ? 1.6 : 0.8) / currentZoomScale;
      });

    statesG.selectAll('.state-path')
      .attr('stroke-width', 0.85 / Math.sqrt(currentZoomScale));
  });

svg.call(zoom);

// Root Map Groups
const mapG = svg.append('g').attr('class', 'map-root');
const statesG = mapG.append('g').attr('class', 'states-layer');
const dotsG = mapG.append('g').attr('class', 'dots-layer');

// ── RENDER BASE MAP ──
function renderBaseMap() {
  statesG.selectAll('.state-path')
    .data(INDIA_GEOJSON.features)
    .join('path')
    .attr('class', 'state-path')
    .attr('d', pathGenerator)
    .append('title')
    .text(d => d.properties.st_nm || d.properties.name);
}

// ── FILTERING (WITH SECTOR VISIBILITY SUPPORT) ──
function getFilteredMPs() {
  return DATA.mps.filter(m => {
    if (m.total < minQuestionsFilter) return false;

    // Check if MP's top sector is hidden
    if (selectedCategory === 'All') {
      if (hiddenSectors.has(m.top_sector)) return false;
    } else {
      if (hiddenSectors.has(selectedCategory)) return false;
      const catShare = m.s[selectedCategory] || 0;
      if (catShare <= 0) return false;
    }

    if (stateFilter !== 'All' && m.state !== stateFilter) return false;
    if (partyFilter !== 'All' && m.party !== partyFilter) return false;

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

// ── RENDER MP DOTS ON MAP ──
function updateDots() {
  const filteredMPs = getFilteredMPs();
  const activeSet = new Set(filteredMPs.map(m => m.id));

  // Sort: larger bubbles rendered under smaller ones so small dots stay clickable
  const sortedMPs = [...DATA.mps].sort((a, b) => {
    const qa = getEffectiveQuestions(a);
    const qb = getEffectiveQuestions(b);
    return qb - qa;
  });

  const dots = dotsG.selectAll('.mp-dot')
    .data(sortedMPs, d => d.id);

  dots.join(
    enter => enter.append('circle')
      .attr('class', 'mp-dot')
      .attr('cx', d => projection(d.coords)[0])
      .attr('cy', d => projection(d.coords)[1])
      .attr('r', d => computeBaseRadius(d) / currentZoomScale)
      .attr('stroke-width', 0.8 / currentZoomScale)
      .attr('fill', d => getDotFillColor(d))
      .attr('opacity', 0)
      .call(enter => enter.transition().duration(300)
        .attr('opacity', d => activeSet.has(d.id) ? 0.90 : 0.04)),
    update => update
      .attr('cx', d => projection(d.coords)[0])
      .attr('cy', d => projection(d.coords)[1])
      .attr('fill', d => getDotFillColor(d))
      .call(update => update.transition().duration(250)
        .attr('r', d => {
          const baseR = computeBaseRadius(d);
          const focusMult = (hoveredMP?.id === d.id || lockedMP?.id === d.id) ? 1.35 : 1.0;
          return (baseR * focusMult) / currentZoomScale;
        })
        .attr('stroke-width', d => ((hoveredMP?.id === d.id || lockedMP?.id === d.id) ? 1.6 : 0.8) / currentZoomScale)
        .attr('opacity', d => activeSet.has(d.id) ? 0.90 : 0.04)
      ),
    exit => exit.remove()
  );

  // Events
  dotsG.selectAll('.mp-dot')
    .on('mouseenter', function(event, d) {
      if (!activeSet.has(d.id)) return;
      hoveredMP = d;
      d3.select(this)
        .attr('opacity', 1)
        .attr('stroke', '#14131a')
        .attr('stroke-width', 1.8 / currentZoomScale)
        .attr('r', (computeBaseRadius(d) * 1.35) / currentZoomScale);
      
      showTooltip(d, event.clientX, event.clientY);
      if (!lockedMP) {
        updateStoryPanel(d);
      }
    })
    .on('mousemove', function(event, d) {
      if (!activeSet.has(d.id)) return;
      showTooltip(d, event.clientX, event.clientY);
    })
    .on('mouseleave', function(event, d) {
      hoveredMP = null;
      const isLocked = lockedMP?.id === d.id;
      const baseR = computeBaseRadius(d);
      d3.select(this)
        .attr('r', (baseR * (isLocked ? 1.35 : 1.0)) / currentZoomScale)
        .attr('opacity', activeSet.has(d.id) ? 0.90 : 0.04)
        .attr('stroke', isLocked ? '#14131a' : '#ffffff')
        .attr('stroke-width', (isLocked ? 1.6 : 0.8) / currentZoomScale);
      
      hideTooltip();
      if (!lockedMP) {
        updateStoryPanel(null);
      }
    })
    .on('click', function(event, d) {
      if (!activeSet.has(d.id)) return;
      event.stopPropagation();
      lockedMP = lockedMP?.id === d.id ? null : d;
      
      dotsG.selectAll('.mp-dot')
        .attr('r', p => {
          const isFoc = lockedMP?.id === p.id;
          return (computeBaseRadius(p) * (isFoc ? 1.35 : 1.0)) / currentZoomScale;
        })
        .attr('stroke', p => lockedMP?.id === p.id ? '#14131a' : '#ffffff')
        .attr('stroke-width', p => (lockedMP?.id === p.id ? 1.6 : 0.8) / currentZoomScale);

      updateStoryPanel(lockedMP || d);
    });

  // Background map click to unlock
  svg.on('click', () => {
    lockedMP = null;
    hoveredMP = null;
    dotsG.selectAll('.mp-dot')
      .attr('r', d => computeBaseRadius(d) / currentZoomScale)
      .attr('stroke', '#ffffff')
      .attr('stroke-width', 0.8 / currentZoomScale)
      .attr('opacity', d => activeSet.has(d.id) ? 0.90 : 0.04);
    updateStoryPanel(null);
  });
}

function onCategoryChange() {
  const isAll = selectedCategory === 'All';
  document.getElementById('leg-size-title').textContent = isAll
    ? 'Bubble Size = Questions Asked'
    : `Questions in ${getSectorPalette(selectedCategory).name}`;

  updateDots();
  updateStoryPanel(lockedMP);
}

// ── UPDATE STORY PANEL & ALL 20 SECTORS WITH HIDE / UNHIDE ──
function updateStoryPanel(focusedMP) {
  const filteredMPs = getFilteredMPs();
  document.getElementById('active-count').textContent = `${filteredMPs.length} MPs Shown`;

  const avgQ = filteredMPs.length
    ? Math.round(filteredMPs.reduce((sum, m) => sum + m.total, 0) / filteredMPs.length)
    : 0;
  document.getElementById('h-avg-q').textContent = avgQ;

  let scopeTag = 'Geographic View';
  let scopeTitle = `17th Lok Sabha (${filteredMPs.length} MPs)`;

  if (focusedMP) {
    scopeTag = 'Elected Member';
    scopeTitle = focusedMP.name;
  } else if (stateFilter !== 'All' && partyFilter !== 'All') {
    scopeTag = 'Filtered Delegation';
    scopeTitle = `${partyFilter} MPs in ${stateFilter}`;
  } else if (stateFilter !== 'All') {
    scopeTag = 'State Delegation';
    scopeTitle = `${stateFilter} (${filteredMPs.length} MPs)`;
  } else if (selectedCategory !== 'All') {
    scopeTag = 'Sector Priority';
    scopeTitle = `${getSectorPalette(selectedCategory).name} Focus`;
  }

  document.getElementById('panel-scope-tag').textContent = scopeTag;
  document.getElementById('panel-scope-title').textContent = scopeTitle;

  renderMPCard(focusedMP);

  let shares = {};
  if (focusedMP) {
    shares = focusedMP.s;
  } else {
    DATA.sectors.forEach(sec => {
      const values = filteredMPs.map(m => m.s[sec] || 0);
      shares[sec] = values.length
        ? values.reduce((sum, v) => sum + v, 0) / values.length
        : 0;
    });
  }

  // Update active sectors counter pill
  const activeSecCount = DATA.sectors.length - hiddenSectors.size;
  const secPill = document.getElementById('sectors-active-pill');
  if (secPill) {
    secPill.textContent = `${activeSecCount} / 20 Active · Click 👁 to toggle`;
  }

  // Rank ALL 20 sectors descending
  const allSectorsRanked = DATA.sectors.map(sec => ({
    sec,
    val: shares[sec] || 0,
    label: getSectorPalette(sec).name
  })).sort((a, b) => b.val - a.val);

  const maxShare = allSectorsRanked[0]?.val || 1;
  const container = document.getElementById('rankings-container');

  container.innerHTML = allSectorsRanked.map((item, idx) => {
    const palette = getSectorPalette(item.sec);
    const isHighlighted = selectedCategory === item.sec ? 'is-highlighted' : '';
    const isHidden = hiddenSectors.has(item.sec);
    const barWidth = Math.max(3, Math.round((item.val / maxShare) * 100));

    // Eye icon (Open eye for visible, Slashed eye for hidden)
    const eyeSvg = isHidden
      ? `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line></svg>`
      : `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>`;

    return `
      <div class="rank-row ${isHighlighted} ${isHidden ? 'is-sector-hidden' : ''}" data-sec="${item.sec}" title="Click to filter by ${item.label}">
        <button class="btn-eye-toggle" data-sec="${item.sec}" title="${isHidden ? 'Unhide sector on map' : 'Hide sector from map'}">
          ${eyeSvg}
        </button>
        <span class="rank-position" style="color:${palette.fill}">#${idx + 1}</span>
        <span class="rank-color-pip" style="background:${palette.fill}"></span>
        <span class="rank-topic-name" title="${item.label}">${item.label}</span>
        <div class="rank-bar-track">
          <div class="rank-bar-fill" style="width:${barWidth}%;background:${palette.fill}"></div>
        </div>
        <span class="rank-percentage">${item.val.toFixed(1)}%</span>
      </div>
    `;
  }).join('');

  // Eye toggle button click listeners
  container.querySelectorAll('.btn-eye-toggle').forEach(btn => {
    btn.onclick = (e) => {
      e.stopPropagation(); // prevent triggering row click
      const sec = btn.getAttribute('data-sec');
      if (hiddenSectors.has(sec)) {
        hiddenSectors.delete(sec);
      } else {
        hiddenSectors.add(sec);
      }
      updateDots();
      updateStoryPanel(lockedMP);
    };
  });

  // Clicking row focuses that sector
  container.querySelectorAll('.rank-row').forEach(row => {
    row.onclick = () => {
      const sec = row.getAttribute('data-sec');
      const catSelect = document.getElementById('sel-category');
      
      // If clicking a hidden sector, unhide it first
      if (hiddenSectors.has(sec)) {
        hiddenSectors.delete(sec);
      }
      
      selectedCategory = (selectedCategory === sec) ? 'All' : sec;
      catSelect.value = selectedCategory;
      onCategoryChange();
    };
  });
}

// Sector Actions: Show All / Clear All
document.getElementById('btn-show-all-sec').onclick = () => {
  hiddenSectors.clear();
  updateDots();
  updateStoryPanel(lockedMP);
};

document.getElementById('btn-clear-all-sec').onclick = () => {
  // Hide all except currently selected (or all)
  DATA.sectors.forEach(s => hiddenSectors.add(s));
  updateDots();
  updateStoryPanel(lockedMP);
};

function renderMPCard(mp) {
  const card = document.getElementById('mp-card');
  if (!mp) {
    card.className = 'hidden';
    return;
  }
  card.className = '';

  const imgUrl = MP_IMGS[mp.id];
  const partyPal = getPartyPalette(mp.party);
  const secPal = getSectorPalette(mp.top_sector);
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
        <div class="mp-meta-sub"><strong>${mp.constituency}</strong>, ${mp.state}</div>
        <div class="mp-meta-sub">${mp.gender} · ${mp.age} yrs</div>
        <div class="mp-tags-row">
          <span class="mp-pill" style="background:${partyPal.bg};color:${partyPal.text};border:1px solid ${partyPal.stroke}40">
            ${mp.party}
          </span>
          <span class="mp-pill" style="background:${secPal.bg};color:${secPal.text};border:1px solid ${secPal.stroke}40">
            ★ Top: ${secPal.name} (${mp.top_sector_pct}%)
          </span>
        </div>
      </div>
    </div>

    <div class="mp-metrics-grid">
      <div class="metric-box">
        <div class="metric-val">${mp.total}</div>
        <div class="metric-label">Total Qs</div>
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
      <span>${lockedMP ? '📌 Locked Constituency' : '👁️ Hovering'}</span>
      ${lockedMP ? `<button class="btn-unlock" id="btn-unlock-mp">Deselect MP ✕</button>` : ''}
    </div>
  `;

  if (lockedMP) {
    const unBtn = document.getElementById('btn-unlock-mp');
    if (unBtn) {
      unBtn.onclick = () => {
        lockedMP = null;
        hoveredMP = null;
        dotsG.selectAll('.mp-dot')
          .attr('r', d => computeBaseRadius(d) / currentZoomScale)
          .attr('stroke', '#ffffff')
          .attr('stroke-width', 0.8 / currentZoomScale);
        updateStoryPanel(null);
      };
    }
  }
}

// ── FLOATING TOOLTIP ──
const tooltip = document.getElementById('tooltip');

function showTooltip(mp, clientX, clientY) {
  const imgUrl = MP_IMGS[mp.id];
  const partyPal = getPartyPalette(mp.party);
  const secPal = getSectorPalette(mp.top_sector);
  const initials = mp.name.split(' ').slice(0, 2).map(w => w[0]).join('');

  const top3 = DATA.sectors.map(s => ({
    sec: s,
    name: getSectorPalette(s).name,
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
        <div class="tt-geo"><strong>${mp.constituency}</strong>, ${mp.state}</div>
        <div class="tt-tags-row">
          <span class="tt-pill" style="background:${partyPal.bg};color:${partyPal.text};border:1px solid ${partyPal.stroke}30">
            ${mp.party}
          </span>
          <span class="tt-pill" style="background:${secPal.bg};color:${secPal.text};border:1px solid ${secPal.stroke}30">
            ${secPal.name}
          </span>
        </div>
      </div>
    </div>

    <div class="tt-stat-row">
      <span class="tt-stat-main">${mp.total} Questions Asked</span>
      <span class="tt-stat-sub">Rank #${mp.rank}</span>
    </div>

    <div class="tt-topics-title">Top Priorities</div>
    ${top3.map(t => {
      const pal = getSectorPalette(t.sec);
      return `
        <div class="tt-topic-item">
          <div class="tt-topic-name-wrap">
            <span class="tt-topic-pip" style="background:${pal.fill}"></span>
            <span>${t.name}</span>
          </div>
          <span class="tt-topic-val">${t.val.toFixed(1)}%</span>
        </div>
      `;
    }).join('')}
  `;

  const tw = tooltip.offsetWidth || 240;
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

// ── POPULATE FILTERS ──
function initFilters() {
  // 1. Total Questions Slider
  const slider = document.getElementById('slider-questions');
  const sliderVal = document.getElementById('val-questions');
  slider.oninput = e => {
    minQuestionsFilter = parseInt(e.target.value, 10);
    sliderVal.textContent = `≥ ${minQuestionsFilter}`;
    updateDots();
    updateStoryPanel(lockedMP);
  };

  // 2. Category Dropdown
  const catSelect = document.getElementById('sel-category');
  DATA.sectors.forEach(sec => {
    const opt = document.createElement('option');
    opt.value = sec;
    opt.textContent = getSectorPalette(sec).name;
    catSelect.appendChild(opt);
  });

  catSelect.onchange = e => {
    selectedCategory = e.target.value;
    onCategoryChange();
  };

  // 3. States Dropdown
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
    updateDots();
    updateStoryPanel(null);

    // Zoom map to state if selected
    if (stateFilter !== 'All') {
      const stateFeature = INDIA_GEOJSON.features.find(f => (f.properties.st_nm === stateFilter || f.properties.name === stateFilter));
      if (stateFeature) {
        const bounds = pathGenerator.bounds(stateFeature);
        const dx = bounds[1][0] - bounds[0][0];
        const dy = bounds[1][1] - bounds[0][1];
        const x = (bounds[0][0] + bounds[1][0]) / 2;
        const y = (bounds[0][1] + bounds[1][1]) / 2;
        const scale = Math.max(1.2, Math.min(6, 0.75 / Math.max(dx / width, dy / height)));
        const translate = [width / 2 - scale * x, height / 2 - scale * y];

        svg.transition().duration(750).call(
          zoom.transform,
          d3.zoomIdentity.translate(translate[0], translate[1]).scale(scale)
        );
      }
    } else {
      resetMapZoom();
    }
  };

  // 4. Party Dropdown
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
    updateDots();
    updateStoryPanel(null);
  };

  // 5. Search Bar
  const searchInput = document.getElementById('search-input');
  searchInput.oninput = e => {
    searchQuery = e.target.value.trim();
    updateDots();
    updateStoryPanel(null);
  };
}

// ── ZOOM CONTROLS ──
function resetMapZoom() {
  svg.transition().duration(600).call(
    zoom.transform,
    d3.zoomIdentity
  );
}

document.getElementById('btn-zoom-in').onclick = () => svg.transition().duration(300).call(zoom.scaleBy, 1.4);
document.getElementById('btn-zoom-out').onclick = () => svg.transition().duration(300).call(zoom.scaleBy, 1 / 1.4);
document.getElementById('btn-zoom-reset').onclick = resetMapZoom;

// ── RESIZE HANDLER ──
window.addEventListener('resize', () => {
  updateProjection();
  statesG.selectAll('.state-path').attr('d', pathGenerator);
  updateDots();
});

// ── INITIALIZE ──
renderBaseMap();
initFilters();
updateDots();
updateStoryPanel(null);
</script>
</body>
</html>
"""

HTML_FINAL = HTML_TEMPLATE.replace('__DATA_PLACEHOLDER__', data_str).replace('__IMGS_PLACEHOLDER__', imgs_str).replace('__GEOJSON_PLACEHOLDER__', geojson_str)

with open('/Users/aashima/Desktop/DataViz5/outcome/loksabha-questions/index.html', 'w') as f:
    f.write(HTML_FINAL)

with open('/Users/aashima/Desktop/DataViz5/outcome/loksabha-questions/map.html', 'w') as f:
    f.write(HTML_FINAL)

with open('/Users/aashima/Desktop/DataViz5/index.html', 'w') as f:
    f.write(HTML_FINAL)

os.makedirs('/Users/aashima/Desktop/DataViz5/docs', exist_ok=True)
with open('/Users/aashima/Desktop/DataViz5/docs/index.html', 'w') as f:
    f.write(HTML_FINAL)

print(f"Generated Proportional Bubble Map with Sector Hide/Unhide: {len(HTML_FINAL)//1024} KB")
