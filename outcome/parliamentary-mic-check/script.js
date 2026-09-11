/* ============================================================
   THE PARLIAMENTARY MIC CHECK — script.js
   D3.js powered scrollytelling data story
   ============================================================ */

'use strict';

// ── CATEGORY CONFIG ─────────────────────────────────────────
const CATEGORIES = [
  { key: 'State & Special Motions',   color: '#8B5CF6', emoji: '⚡', pct: 21.6, units: 22, ruling: 38.2, opposition: 34.1, regional: 27.7, desc: 'Civil aviation, telecom, tourism, textiles, labour' },
  { key: 'Health, Education & Welfare', color: '#EC4899', emoji: '🩺', pct: 21.5, units: 22, ruling: 42.1, opposition: 33.8, regional: 24.1, desc: 'Health, education, women, social justice, AYUSH' },
  { key: 'Infrastructure & Energy',   color: '#F59E0B', emoji: '🏗️', pct: 18.2, units: 18, ruling: 48.3, opposition: 27.9, regional: 23.8, desc: 'Railways, roads, power, coal, petroleum, steel' },
  { key: 'Agriculture & Rural',       color: '#22C55E', emoji: '🌾', pct: 13.2, units: 13, ruling: 41.5, opposition: 36.2, regional: 22.3, desc: 'Farmers welfare, rural dev, food, fisheries, co-ops' },
  { key: 'Finance & Economy',         color: '#3B82F6', emoji: '💼', pct: 10.0, units: 10, ruling: 55.2, opposition: 31.4, regional: 13.4, desc: 'Finance, commerce, MSMEs, corporate affairs' },
  { key: 'Environment & Water',       color: '#10B981', emoji: '🌍', pct: 7.9,  units: 8,  ruling: 40.8, opposition: 35.7, regional: 23.5, desc: 'Environment, Jal Shakti, earth sciences, panchayat' },
  { key: 'Law & Home Affairs',        color: '#F87171', emoji: '⚖️', pct: 4.6,  units: 5,  ruling: 43.2, opposition: 38.6, regional: 18.2, desc: 'Home affairs, law & justice, parliamentary affairs' },
  { key: 'Defence & Foreign Affairs', color: '#64748B', emoji: '🛡️', pct: 2.9,  units: 3,  ruling: 62.1, opposition: 24.3, regional: 13.6, desc: 'Defence, external affairs, atomic energy, space' },
];

const ARCHETYPES = {
  'Policy Hawk':    { color: '#F59E0B', emoji: '🦁', desc: 'High debates, broad national focus' },
  'Local Champion': { color: '#22C55E', emoji: '📢', desc: 'Constituency-focused, zero hour specialist' },
  'Question Machine':{ color: '#3B82F6', emoji: '📑', desc: 'Low floor time, top written-question volume' },
  'Silent Observer':{ color: '#475569', emoji: '🤫', desc: 'High attendance, minimal floor speech' },
};

const CAT_COLOR_MAP = Object.fromEntries(CATEGORIES.map(c => [c.key, c.color]));

// ── STATE ────────────────────────────────────────────────────
let allMPs = [];
let filteredMPs = [];
let currentStep = 0;
let partyViewMode = 'raw'; // 'raw' | 'pct'
let beeswarmSim = null;

// ── DATA LOADING ─────────────────────────────────────────────
async function loadData() {
  // Use embedded data (data_embedded.js loaded before this script)
  if (typeof MP_MASTER !== 'undefined' && MP_MASTER.length) {
    allMPs = MP_MASTER;
    filteredMPs = [...allMPs];
    console.log(`Loaded ${allMPs.length} MPs from embedded data`);
  } else {
    console.warn('Embedded data not found, using generated fallback sample');
    allMPs = generateSampleData();
    filteredMPs = [...allMPs];
  }
}

function generateSampleData() {
  const parties = ['BJP','BJP','BJP','BJP','BJP','BJP','BJP','INC','INC','DMK','YSRCP','AITC','SS','JD(U)','BJD','BSP','NCP'];
  const states = ['Uttar Pradesh','Maharashtra','Tamil Nadu','West Bengal','Andhra Pradesh','Kerala','Bihar','Rajasthan','Karnataka','Gujarat'];
  const archetypes = ['Policy Hawk','Policy Hawk','Question Machine','Question Machine','Question Machine','Silent Observer','Silent Observer','Silent Observer','Silent Observer','Local Champion'];
  const cats = CATEGORIES.map(c=>c.key);
  return Array.from({length: 559}, (_, i) => {
    const party = parties[i % parties.length];
    const arch = archetypes[i % archetypes.length];
    const debates = arch === 'Policy Hawk' ? 80 + Math.floor(Math.random()*200) :
                    arch === 'Local Champion' ? 40 + Math.floor(Math.random()*60) :
                    arch === 'Question Machine' ? 5 + Math.floor(Math.random()*45) :
                    10 + Math.floor(Math.random()*30);
    const questions = arch === 'Question Machine' ? 300 + Math.floor(Math.random()*350) :
                      100 + Math.floor(Math.random()*200);
    const topDist = {};
    cats.forEach(c => { topDist[c] = Math.floor(Math.random()*50); });
    return {
      mp_id: `MP_${i}`, name: `MP ${i+1}`, party, state: states[i%states.length],
      constituency: `Constituency ${i+1}`, gender: i%5===0?'Female':'Male',
      age: `${35+Math.floor(Math.random()*25)} years`, education: 'Graduate',
      attendance_pct: 50 + Math.random()*50, debates_count: debates,
      questions_count: questions, bills_count: Math.floor(Math.random()*5),
      profile_url: '#', top_category: cats[i%cats.length], archetype: arch,
      topic_distribution: topDist
    };
  });
}

// ── SCROLL PROGRESS ──────────────────────────────────────────
function initProgressBar() {
  const bar = document.getElementById('progress-bar');
  window.addEventListener('scroll', () => {
    const total = document.body.scrollHeight - window.innerHeight;
    const pct = Math.min(100, (window.scrollY / total) * 100);
    bar.style.width = pct + '%';
  }, { passive: true });
}

// ── HERO COUNTER ANIMATION ────────────────────────────────────
function animateCounters() {
  document.querySelectorAll('[data-count]').forEach(el => {
    const target = parseInt(el.dataset.count);
    const duration = 1800;
    const start = performance.now();
    const fmt = el.dataset.fmt || '';
    function tick(now) {
      const t = Math.min(1, (now - start) / duration);
      const ease = 1 - Math.pow(1 - t, 4);
      el.textContent = Math.floor(ease * target).toLocaleString('en-IN') + fmt;
      if (t < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  });
}

// ── WAFFLE CHART ─────────────────────────────────────────────
function buildWaffle() {
  const grid = document.getElementById('waffle-grid');
  const legend = document.getElementById('waffle-legend');
  if (!grid) return;

  grid.innerHTML = '';
  legend.innerHTML = '';

  const cells = [];
  CATEGORIES.forEach(cat => {
    for (let i = 0; i < cat.units; i++) {
      cells.push(cat);
    }
  });

  // Pad to 100 if needed
  while (cells.length < 100) cells.push({ color: 'rgba(255,255,255,0.04)', key: '', pct: 0, desc: '' });

  cells.forEach((cat, idx) => {
    const cell = document.createElement('div');
    cell.className = 'waffle-cell';
    cell.style.background = cat.color;
    cell.dataset.cat = cat.key;
    if (cat.key) {
      cell.addEventListener('mouseenter', (e) => showTooltip(e, cat));
      cell.addEventListener('mousemove', (e) => moveTooltip(e));
      cell.addEventListener('mouseleave', hideTooltip);
      cell.addEventListener('click', () => highlightCategory(cat.key));
    }
    grid.appendChild(cell);
  });

  CATEGORIES.forEach(cat => {
    const item = document.createElement('div');
    item.className = 'legend-item';
    item.innerHTML = `
      <div class="legend-dot" style="background:${cat.color}"></div>
      <div class="legend-text">
        <strong>${cat.emoji} ${cat.key}</strong>
        ${cat.pct}% of questions
      </div>`;
    item.addEventListener('click', () => highlightCategory(cat.key));
    legend.appendChild(item);
  });
}

function highlightCategory(catKey) {
  document.querySelectorAll('.waffle-cell').forEach(cell => {
    const active = !catKey || cell.dataset.cat === catKey;
    cell.style.opacity = active ? '1' : '0.2';
    cell.style.filter = active ? 'brightness(1.1)' : 'none';
  });
}

// ── TOOLTIP ──────────────────────────────────────────────────
const tooltip = document.getElementById('tooltip');

function showTooltip(e, cat) {
  if (!tooltip) return;
  tooltip.innerHTML = `
    <div class="tooltip-cat" style="color:${cat.color}">${cat.emoji} ${cat.key}</div>
    <div class="tooltip-pct">${cat.pct}% of all questions</div>
    <div class="tooltip-detail">${cat.units} / 100 debate units<br>${cat.desc}</div>`;
  tooltip.classList.add('visible');
  moveTooltip(e);
}

function moveTooltip(e) {
  if (!tooltip) return;
  const x = e.clientX + 14;
  const y = e.clientY - 10;
  const maxX = window.innerWidth - tooltip.offsetWidth - 10;
  const maxY = window.innerHeight - tooltip.offsetHeight - 10;
  tooltip.style.left = Math.min(x, maxX) + 'px';
  tooltip.style.top = Math.min(y, maxY) + 'px';
}

function hideTooltip() {
  if (!tooltip) return;
  tooltip.classList.remove('visible');
}

// ── PARTY BARS ───────────────────────────────────────────────
function buildPartyBars() {
  const container = document.getElementById('party-bars-svg-area');
  if (!container) return;
  renderPartyBars('raw');

  document.querySelectorAll('.toggle-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.toggle-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      partyViewMode = btn.dataset.mode;
      renderPartyBars(partyViewMode);
    });
  });
}

function renderPartyBars(mode) {
  const container = document.getElementById('party-bars-svg-area');
  if (!container) return;
  container.innerHTML = '';

  const partyGroups = [
    {
      label: 'BJP & Ruling Coalition',
      color: '#F97316',
      data: CATEGORIES.map(c => ({ cat: c.key, color: c.color, val: c.ruling, raw: Math.round(c.ruling * 308 / 100) }))
    },
    {
      label: 'INC & Main Opposition',
      color: '#06B6D4',
      data: CATEGORIES.map(c => ({ cat: c.key, color: c.color, val: c.opposition, raw: Math.round(c.opposition * 54 / 100) }))
    },
    {
      label: 'Regional Parties',
      color: '#8B5CF6',
      data: CATEGORIES.map(c => ({ cat: c.key, color: c.color, val: c.regional, raw: Math.round(c.regional * 197 / 100) }))
    }
  ];

  partyGroups.forEach(group => {
    const div = document.createElement('div');
    div.className = 'party-bar-group';

    const total = group.data.reduce((s, d) => s + (mode === 'raw' ? d.raw : d.val), 0);
    const displayTotal = mode === 'raw' ? total.toLocaleString('en-IN') : '100%';

    div.innerHTML = `
      <div class="party-bar-label">
        <span class="party-bar-name" style="color:${group.color}">${group.label}</span>
        <span class="party-bar-value">${displayTotal}</span>
      </div>
      <div class="party-bar-track" id="track-${group.label.replace(/\s/g,'_')}"></div>`;

    container.appendChild(div);

    const track = div.querySelector('.party-bar-track');
    group.data.forEach(d => {
      const seg = document.createElement('div');
      seg.className = 'party-bar-segment';
      seg.style.background = d.color;
      const val = mode === 'raw' ? d.raw : d.val;
      const pct = total > 0 ? (val / total * 100) : 0;
      seg.style.width = pct + '%';
      seg.title = `${d.cat}: ${val}${mode === 'pct' ? '%' : ''}`;
      if (pct > 8) seg.textContent = `${Math.round(pct)}%`;
      track.appendChild(seg);
    });
  });

  // Mini legend
  const legendDiv = document.createElement('div');
  legendDiv.className = 'mini-legend';
  CATEGORIES.slice(0, 5).forEach(cat => {
    legendDiv.innerHTML += `
      <div class="mini-legend-item">
        <div class="mini-legend-dot" style="background:${cat.color}"></div>
        ${cat.emoji} ${cat.key.split(' ')[0]}
      </div>`;
  });
  container.appendChild(legendDiv);
}

// ── BEESWARM PLOT ─────────────────────────────────────────────
let beeSimNodes = [];

function buildBeeswarm() {
  const container = document.getElementById('beeswarm-svg-wrap');
  if (!container || !allMPs.length) return;

  const W = container.clientWidth || 500;
  const H = container.clientHeight || 380;
  const margin = { top: 30, right: 20, bottom: 50, left: 55 };
  const innerW = W - margin.left - margin.right;
  const innerH = H - margin.top - margin.bottom;

  const svg = d3.select('#beeswarm-svg');
  svg.selectAll('*').remove();
  svg.attr('viewBox', `0 0 ${W} ${H}`);

  const g = svg.append('g').attr('transform', `translate(${margin.left},${margin.top})`);

  // Scales
  const maxDebates = d3.max(allMPs, d => d.debates_count) || 600;
  const xScale = d3.scaleLinear().domain([0, maxDebates]).range([0, innerW]).nice();

  // Y: ratio of 'national' to 'local' topics
  // National: Finance, Defence, Law, Environment
  // Local: State & Special Motions, Agriculture
  const nationalCats = ['Finance & Economy','Defence & Foreign Affairs','Law & Home Affairs','Environment & Water'];
  const localCats = ['State & Special Motions','Agriculture & Rural'];

  function nationalRatio(mp) {
    const dist = mp.topic_distribution || {};
    const nat = nationalCats.reduce((s, k) => s + (dist[k] || 0), 0);
    const loc = localCats.reduce((s, k) => s + (dist[k] || 0), 0);
    const total = nat + loc;
    return total > 0 ? nat / total : 0.5;
  }

  const yScale = d3.scaleLinear().domain([0, 1]).range([innerH, 0]);

  // Grid
  g.append('g').attr('class', 'bee-grid')
    .selectAll('line').data(xScale.ticks(5)).enter().append('line')
    .attr('x1', d => xScale(d)).attr('x2', d => xScale(d))
    .attr('y1', 0).attr('y2', innerH)
    .attr('class', 'bee-grid-line').attr('stroke-width', 1);

  // Axes
  g.append('g').attr('transform', `translate(0,${innerH})`)
    .call(d3.axisBottom(xScale).ticks(5).tickFormat(d => d))
    .call(ax => {
      ax.select('.domain').remove();
      ax.selectAll('line').remove();
      ax.selectAll('text').attr('class', 'bee-axis-label').attr('fill', 'rgba(148,163,184,0.7)');
    });

  g.append('g')
    .call(d3.axisLeft(yScale).ticks(3).tickFormat(d => d === 0 ? 'Local' : d === 1 ? 'National' : ''))
    .call(ax => {
      ax.select('.domain').remove();
      ax.selectAll('line').remove();
      ax.selectAll('text').attr('class', 'bee-axis-label').attr('fill', 'rgba(148,163,184,0.7)');
    });

  // Axis labels
  g.append('text').attr('class', 'bee-axis-label')
    .attr('x', innerW / 2).attr('y', innerH + 40).attr('text-anchor', 'middle')
    .attr('fill', 'rgba(148,163,184,0.5)').text('Debates Participated In →');

  g.append('text').attr('class', 'bee-axis-label')
    .attr('x', -innerH/2).attr('y', -42).attr('transform', 'rotate(-90)')
    .attr('text-anchor', 'middle').attr('fill', 'rgba(148,163,184,0.5)')
    .text('↑ National Focus');

  // Prep nodes
  beeSimNodes = allMPs.map(mp => ({
    ...mp,
    x: xScale(Math.min(mp.debates_count, maxDebates)),
    y: yScale(nationalRatio(mp)),
    r: Math.max(2.5, Math.min(6, Math.sqrt(mp.questions_count / 10))),
    color: ARCHETYPES[mp.archetype]?.color || '#475569',
  }));

  // Force simulation for collision avoidance
  const sim = d3.forceSimulation(beeSimNodes)
    .force('x', d3.forceX(d => d.x).strength(1))
    .force('y', d3.forceY(d => d.y).strength(0.7))
    .force('collide', d3.forceCollide(d => d.r + 1.2).strength(0.85))
    .stop();

  // Run sim synchronously
  for (let i = 0; i < 150; i++) sim.tick();

  // Draw dots
  const dots = g.selectAll('.bee-dot')
    .data(beeSimNodes)
    .enter().append('circle')
    .attr('class', 'bee-dot')
    .attr('cx', d => Math.max(0, Math.min(innerW, d.x)))
    .attr('cy', d => Math.max(0, Math.min(innerH, d.y)))
    .attr('r', d => d.r)
    .attr('fill', d => d.color)
    .attr('fill-opacity', 0.8)
    .attr('stroke', 'rgba(255,255,255,0.12)')
    .attr('stroke-width', 0.5)
    .on('mouseenter', function(event, d) {
      d3.select(this).attr('r', d.r * 1.8).attr('stroke-width', 1.5).attr('stroke', '#fff');
      showMPTooltip(event, d);
    })
    .on('mousemove', moveTooltip)
    .on('mouseleave', function(event, d) {
      d3.select(this).attr('r', d.r).attr('stroke-width', 0.5).attr('stroke', 'rgba(255,255,255,0.12)');
      hideTooltip();
    })
    .on('click', (event, d) => openMPModal(d));

  // Store ref
  window._beeDots = dots;
  window._beeScale = { xScale, yScale, innerW, innerH };
}

function showMPTooltip(event, mp) {
  if (!tooltip) return;
  const arch = ARCHETYPES[mp.archetype] || {};
  tooltip.innerHTML = `
    <div class="tooltip-cat" style="color:${arch.color}">${arch.emoji || ''} ${mp.name}</div>
    <div class="tooltip-pct" style="font-size:0.85rem">${mp.party} · ${mp.state}</div>
    <div class="tooltip-detail">
      ${mp.debates_count} debates · ${mp.questions_count} questions<br>
      <em style="color:${arch.color}">${mp.archetype}</em>
    </div>`;
  tooltip.classList.add('visible');
  moveTooltip(event);
}

// ── BEESWARM SEARCH & FILTER ─────────────────────────────────
function initBeeswarmControls() {
  const searchInput = document.getElementById('mp-search-input');
  const partyFilter = document.getElementById('filter-party');
  const genderFilter = document.getElementById('filter-gender');
  const archetypeFilter = document.getElementById('filter-archetype');

  function applyFilters() {
    if (!window._beeDots) return;
    const query = searchInput?.value.toLowerCase().trim() || '';
    const party = partyFilter?.value || '';
    const gender = genderFilter?.value || '';
    const arch = archetypeFilter?.value || '';

    window._beeDots.each(function(d) {
      const matchSearch = !query || d.name.toLowerCase().includes(query) || d.constituency.toLowerCase().includes(query) || d.state.toLowerCase().includes(query);
      const matchParty = !party || d.party === party;
      const matchGender = !gender || d.gender === gender;
      const matchArch = !arch || d.archetype === arch;
      const show = matchSearch && matchParty && matchGender && matchArch;
      d3.select(this).classed('dimmed', !show);
    });

    // Spotlight searched MP
    if (query && window._beeDots) {
      window._beeDots.each(function(d) {
        const match = d.name.toLowerCase().includes(query) || d.constituency.toLowerCase().includes(query);
        if (match) {
          d3.select(this).attr('r', d.r * 2.5).attr('stroke', '#fff').attr('stroke-width', 2);
        } else {
          d3.select(this).attr('r', d.r).attr('stroke', 'rgba(255,255,255,0.12)').attr('stroke-width', 0.5);
        }
      });
    }
  }

  searchInput?.addEventListener('input', applyFilters);
  partyFilter?.addEventListener('change', applyFilters);
  genderFilter?.addEventListener('change', applyFilters);
  archetypeFilter?.addEventListener('change', applyFilters);

  // Populate party dropdown
  if (partyFilter) {
    const parties = [...new Set(allMPs.map(d => d.party))].sort();
    parties.forEach(p => {
      const opt = document.createElement('option');
      opt.value = p; opt.textContent = p;
      partyFilter.appendChild(opt);
    });
  }
}

// ── MP MODAL ─────────────────────────────────────────────────
function openMPModal(mp) {
  const modal = document.getElementById('mp-modal');
  const card = document.getElementById('mp-card');
  if (!modal || !card) return;

  const arch = ARCHETYPES[mp.archetype] || { color: '#475569', emoji: '👤' };
  const initials = mp.name.split(' ').slice(0,2).map(w=>w[0]).join('');
  const dist = mp.topic_distribution || {};
  const distSorted = Object.entries(dist).sort((a,b)=>b[1]-a[1]).slice(0,5);
  const maxVal = distSorted[0]?.[1] || 1;

  const badgeBg = arch.color + '22';
  const attendance = typeof mp.attendance_pct === 'number' ? mp.attendance_pct.toFixed(0)+'%' : 'N/A';

  card.innerHTML = `
    <button id="mp-card-close" aria-label="Close">✕</button>
    <div class="mp-card-header">
      <div class="mp-avatar" style="color:${arch.color};border-color:${arch.color}30">${initials}</div>
      <div>
        <div class="mp-card-name">${mp.name}</div>
        <div class="mp-card-meta">${mp.party} · ${mp.constituency}, ${mp.state}</div>
        <div class="mp-card-meta">${mp.gender} · ${mp.age} · ${mp.education}</div>
        <div class="mp-archetype-badge" style="background:${badgeBg};color:${arch.color};border:1px solid ${arch.color}40">
          ${arch.emoji} ${mp.archetype}
        </div>
      </div>
    </div>
    <div class="mp-stats-grid">
      <div class="mp-stat-cell">
        <span class="mp-stat-num">${mp.debates_count}</span>
        <span class="mp-stat-lbl">Debates</span>
      </div>
      <div class="mp-stat-cell">
        <span class="mp-stat-num">${mp.questions_count}</span>
        <span class="mp-stat-lbl">Questions</span>
      </div>
      <div class="mp-stat-cell">
        <span class="mp-stat-num">${attendance}</span>
        <span class="mp-stat-lbl">Attendance</span>
      </div>
    </div>
    <div class="mp-topic-bars">
      <div style="font-size:0.72rem;color:var(--text-mute);margin-bottom:0.5rem;font-family:var(--font-mono);letter-spacing:0.07em;text-transform:uppercase">Top Topics</div>
      ${distSorted.map(([cat, val]) => `
        <div class="mp-topic-bar-row">
          <div class="mp-topic-bar-label">${CATEGORIES.find(c=>c.key===cat)?.emoji||'•'} ${cat.split(' ').slice(0,2).join(' ')}</div>
          <div class="mp-topic-bar-track">
            <div class="mp-topic-bar-fill" style="width:${(val/maxVal*100).toFixed(1)}%;background:${CAT_COLOR_MAP[cat]||'#64748B'}"></div>
          </div>
          <div class="mp-topic-bar-val">${val}</div>
        </div>`).join('')}
    </div>
    ${mp.profile_url && mp.profile_url !== '#' ? `
      <a href="${mp.profile_url}" target="_blank" rel="noopener" class="mp-profile-link">
        View PRS Profile ↗
      </a>` : ''}`;

  modal.classList.add('open');
  card.querySelector('#mp-card-close').addEventListener('click', closeMPModal);
  modal.addEventListener('click', e => { if (e.target === modal) closeMPModal(); });
}

function closeMPModal() {
  const modal = document.getElementById('mp-modal');
  if (modal) modal.classList.remove('open');
}

// ── CONCLUSION ───────────────────────────────────────────────
function animateConclusion() {
  const fill = document.querySelector('.participation-fill');
  if (fill) {
    setTimeout(() => { fill.style.width = '42.1%'; }, 300);
  }
}

// ── SCROLLYTELLING DRIVER ─────────────────────────────────────
function initScrollytelling() {
  const steps = document.querySelectorAll('.step');
  const canvasPanels = document.querySelectorAll('.canvas-panel');

  if (!steps.length) return;

  const observerOptions = {
    root: null,
    rootMargin: '-35% 0px -45% 0px',
    threshold: 0,
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const stepEl = entry.target;
        const stepId = stepEl.dataset.step;

        // Activate step text
        steps.forEach(s => s.classList.remove('is-active'));
        stepEl.classList.add('is-active');

        // Switch canvas panel
        canvasPanels.forEach(p => {
          p.style.display = 'none';
          p.style.opacity = '0';
          p.classList.remove('is-active');
        });

        const panel = document.getElementById(`panel-${stepId}`);
        if (panel) {
          panel.style.display = 'flex';
          setTimeout(() => {
            panel.style.opacity = '1';
            panel.classList.add('is-active');
          }, 50);
        }

        // Trigger step-specific effects
        if (stepId === 'step-1b') buildWaffle();
        if (stepId === 'step-2') buildPartyBars();
        if (stepId === 'step-4') {
          setTimeout(() => {
            buildBeeswarm();
            initBeeswarmControls();
          }, 200);
        }
        if (stepId === 'step-5') {
          setTimeout(animateConclusion, 400);
        }
      }
    });
  }, observerOptions);

  steps.forEach(step => observer.observe(step));

  // Activate first step immediately
  if (steps[0]) {
    steps[0].classList.add('is-active');
    const firstPanel = document.getElementById('panel-step-0');
    if (firstPanel) {
      firstPanel.style.display = 'flex';
      firstPanel.style.opacity = '1';
      firstPanel.classList.add('is-active');
    }
  }
}

// ── PARTICLE BURST (Hero) ─────────────────────────────────────
function initParticleBurst() {
  const canvas = document.getElementById('hero-canvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  canvas.width = canvas.offsetWidth;
  canvas.height = canvas.offsetHeight;

  const N = 180;
  const particles = Array.from({ length: N }, (_, i) => ({
    x: canvas.width / 2 + (Math.random() - 0.5) * 40,
    y: canvas.height / 2 + (Math.random() - 0.5) * 40,
    vx: (Math.random() - 0.5) * 6,
    vy: (Math.random() - 0.5) * 6 - 2,
    alpha: 0.8 + Math.random() * 0.2,
    radius: 2 + Math.random() * 3,
    color: CATEGORIES[i % CATEGORIES.length].color,
    decay: 0.012 + Math.random() * 0.01,
  }));

  let frame = 0;
  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach(p => {
      p.x += p.vx;
      p.y += p.vy;
      p.vy += 0.08; // gravity
      p.alpha -= p.decay;
      if (p.alpha <= 0) return;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      ctx.fillStyle = p.color + Math.floor(p.alpha * 255).toString(16).padStart(2,'0');
      ctx.fill();
    });
    frame++;
    if (frame < 200 && particles.some(p => p.alpha > 0)) {
      requestAnimationFrame(draw);
    }
  }

  // Trigger after a short delay
  setTimeout(draw, 600);
}

// ── INIT ──────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', async () => {
  await loadData();
  initProgressBar();
  initScrollytelling();
  initParticleBurst();

  // Animate hero counters when visible
  const heroObserver = new IntersectionObserver(entries => {
    if (entries[0].isIntersecting) {
      animateCounters();
      heroObserver.disconnect();
    }
  });
  const hero = document.getElementById('hero');
  if (hero) heroObserver.observe(hero);

  // Close modal on Escape
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeMPModal();
  });

  // Handle resize
  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      if (document.querySelector('#panel-step-4.is-active')) {
        buildBeeswarm();
        initBeeswarmControls();
      }
    }, 300);
  });
});
