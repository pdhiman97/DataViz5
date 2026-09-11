/* ============================================================
   VOICES FROM THE STATES — script.js
   Data: PRS India 17th Lok Sabha questioning matrix
   ============================================================ */

'use strict';

// ===== COLOUR SCALES =====
const C = {
  ember: '#c8602a',
  emberLight: '#e8864a',
  emberPale: '#f5c49e',
  ice: '#4a7fa5',
  iceLight: '#7aafc8',
  cream: '#ede8da',
  fog: '#8a8580',
  ash: '#5a5550',
  smoke: '#3a3530',
  ink: '#0d0d0d',
  rule: 'rgba(245,240,232,0.12)',
};

let DATA = null;
let selectedSector = null;
let lockedState = null;

// ===== LOAD DATA =====
async function init() {
  try {
    DATA = (typeof VIZ_DATA !== 'undefined') ? VIZ_DATA : await d3.json('../../data/loksabha-questions/curated/viz_data.json');
  } catch (e) {
    console.error('Failed to load data:', e);
    return;
  }

  setupHeroCanvas();
  setupScrollSpy();
  setupNavLinks();
  drawChapter1();
  drawChapter2();
  drawChapter3();
  drawChapter4();
  drawChapter5();

  // Trigger initial bar animations after a small delay
  setTimeout(() => {
    document.querySelectorAll('.bar-fill').forEach(el => {
      el.style.transform = `scaleX(${el.dataset.scale})`;
    });
  }, 400);
}

// ===== HERO CANVAS — particle field =====
function setupHeroCanvas() {
  const canvas = document.getElementById('hero-canvas');
  const ctx = canvas.getContext('2d');
  let W, H, particles = [];

  function resize() {
    W = canvas.width = canvas.offsetWidth;
    H = canvas.height = canvas.offsetHeight;
  }

  function mkParticle() {
    return {
      x: Math.random() * W,
      y: Math.random() * H,
      r: Math.random() * 1.5 + 0.3,
      vx: (Math.random() - 0.5) * 0.18,
      vy: (Math.random() - 0.5) * 0.18,
      alpha: Math.random() * 0.5 + 0.1,
      hue: Math.random() > 0.85 ? '#c8602a' : '#ede8da',
    };
  }

  function initParticles() {
    particles = [];
    const n = Math.floor(W * H / 5000);
    for (let i = 0; i < n; i++) particles.push(mkParticle());
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);
    // Draw gradient background
    const grad = ctx.createLinearGradient(0, 0, 0, H);
    grad.addColorStop(0, '#0d0d0d');
    grad.addColorStop(0.6, '#111009');
    grad.addColorStop(1, '#1a1814');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, W, H);

    // Draw connections
    ctx.strokeStyle = 'rgba(245,240,232,0.04)';
    ctx.lineWidth = 0.5;
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 90) {
          ctx.globalAlpha = (1 - dist / 90) * 0.12;
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.stroke();
        }
      }
    }

    // Draw particles
    particles.forEach(p => {
      ctx.globalAlpha = p.alpha;
      ctx.fillStyle = p.hue;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fill();

      p.x += p.vx;
      p.y += p.vy;
      if (p.x < 0) p.x = W;
      if (p.x > W) p.x = 0;
      if (p.y < 0) p.y = H;
      if (p.y > H) p.y = 0;
    });

    ctx.globalAlpha = 1;
    requestAnimationFrame(draw);
  }

  resize();
  initParticles();
  draw();
  window.addEventListener('resize', () => { resize(); initParticles(); });
}

// ===== NAV SCROLL SPY =====
function setupScrollSpy() {
  const chapters = document.querySelectorAll('.chapter, section[id^="chapter"]');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting && e.intersectionRatio > 0.3) {
        const id = e.target.id;
        const ch = id.replace('chapter-', '');
        document.querySelectorAll('.nav-link').forEach(a => {
          a.classList.toggle('active', a.dataset.chapter === ch);
        });
      }
    });
  }, { threshold: 0.3 });
  chapters.forEach(c => observer.observe(c));
}

function setupNavLinks() {
  document.querySelectorAll('.nav-link').forEach(a => {
    a.addEventListener('click', e => {
      e.preventDefault();
      const target = document.querySelector(a.getAttribute('href'));
      if (target) target.scrollIntoView({ behavior: 'smooth' });
    });
  });
}

// ===== TOOLTIP =====
const tt = document.getElementById('tooltip');

function showTooltip(html, x, y) {
  tt.innerHTML = html;
  tt.classList.remove('hidden');
  const tw = tt.offsetWidth, th = tt.offsetHeight;
  const px = Math.min(x + 14, window.innerWidth - tw - 16);
  const py = Math.min(y + 14, window.innerHeight - th - 16);
  tt.style.left = px + 'px';
  tt.style.top = py + 'px';
}

function hideTooltip() {
  tt.classList.add('hidden');
}

// ===== CHAPTER 1: GLOBAL BAR CHART =====
function drawChapter1() {
  const container = document.getElementById('global-bars');
  const top20 = DATA.top20_sectors;
  const maxVal = Math.max(...top20.map(s => DATA.global_shares[s]));

  top20.forEach(sector => {
    const val = DATA.global_shares[sector];
    const label = DATA.short_labels[sector] || sector;
    const pct = val;
    const scale = val / maxVal;

    const row = document.createElement('div');
    row.className = 'bar-row';
    row.innerHTML = `
      <div class="bar-label" title="${sector}">${label}</div>
      <div class="bar-track">
        <div class="bar-fill" data-scale="${scale}" style="width:100%;transform:scaleX(0)"></div>
      </div>
      <div class="bar-value">${pct.toFixed(1)}%</div>
    `;
    container.appendChild(row);
  });

  // Animate on intersection
  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.querySelectorAll('.bar-fill').forEach(el => {
          el.style.transition = 'transform 0.9s cubic-bezier(0.4,0,0.2,1)';
          el.style.transform = `scaleX(${el.dataset.scale})`;
        });
        observer.disconnect();
      }
    });
  }, { threshold: 0.2 });
  observer.observe(container);
}

// ===== CHAPTER 2: STATE HEATMAP =====
function drawChapter2() {
  const container = document.getElementById('state-heatmap');
  const stateData = DATA.state_data;
  const states = Object.keys(stateData).sort();
  const sectors = DATA.top20_sectors;

  const cellW = 34, cellH = 22;
  const labelW = 170, labelH = 80;
  const margin = { top: labelH, left: labelW, bottom: 20, right: 20 };
  const W = sectors.length * cellW + margin.left + margin.right;
  const H = states.length * cellH + margin.top + margin.bottom;

  const svg = d3.select(container)
    .append('svg')
    .attr('width', W)
    .attr('height', H);

  // Colour scale: diverging ice -> dark -> ember
  const allVals = [];
  states.forEach(st => {
    sectors.forEach(sec => {
      allVals.push(stateData[st].distinctiveness[sec] || 0);
    });
  });
  const ext = d3.max(allVals.map(Math.abs));
  const colorScale = d3.scaleDiverging()
    .domain([-ext, 0, ext])
    .interpolator(d3.interpolateRgbBasis([C.ice, '#1a1814', C.ember]));

  // Column headers (rotated sector names)
  const sectorLabels = svg.selectAll('.sec-label')
    .data(sectors)
    .join('text')
    .attr('class', 'sec-label')
    .attr('x', (_, i) => margin.left + i * cellW + cellW / 2)
    .attr('y', margin.top - 8)
    .attr('transform', (_, i) => `rotate(-60,${margin.left + i * cellW + cellW / 2},${margin.top - 8})`)
    .attr('text-anchor', 'end')
    .attr('fill', C.ash)
    .attr('font-size', '9px')
    .attr('font-family', 'Space Mono, monospace')
    .text(s => DATA.short_labels[s] || s);

  // Row groups
  const rows = svg.selectAll('.state-row')
    .data(states)
    .join('g')
    .attr('class', 'state-row')
    .attr('transform', (_, i) => `translate(0,${margin.top + i * cellH})`);

  // State labels
  rows.append('text')
    .attr('x', margin.left - 8)
    .attr('y', cellH / 2 + 4)
    .attr('text-anchor', 'end')
    .attr('fill', C.fog)
    .attr('font-size', '10px')
    .attr('font-family', 'Space Mono, monospace')
    .attr('cursor', 'pointer')
    .text(st => st)
    .on('mouseenter', function(_, st) {
      d3.select(this).attr('fill', C.cream);
    })
    .on('mouseleave', function(_, st) {
      if (lockedState !== st) d3.select(this).attr('fill', C.fog);
    })
    .on('click', (_, st) => {
      if (lockedState === st) {
        lockedState = null;
        hideStateDetail();
      } else {
        lockedState = st;
        showStateDetail(st);
      }
    });

  // Cells
  rows.selectAll('.cell')
    .data(st => sectors.map(sec => ({ state: st, sector: sec, val: stateData[st].distinctiveness[sec] || 0 })))
    .join('rect')
    .attr('class', 'cell')
    .attr('x', (_, i) => margin.left + i * cellW + 1)
    .attr('y', 1)
    .attr('width', cellW - 2)
    .attr('height', cellH - 2)
    .attr('rx', 1)
    .attr('fill', d => colorScale(d.val))
    .attr('opacity', 0.9)
    .attr('cursor', 'pointer')
    .on('mouseenter', function(e, d) {
      d3.select(this).attr('opacity', 1).attr('stroke', C.cream).attr('stroke-width', 1);
      const sign = d.val >= 0 ? '+' : '';
      showTooltip(`
        <div class="tt-title">${d.state}</div>
        <div class="tt-sub">${DATA.short_labels[d.sector] || d.sector}</div>
        <div class="tt-body">
          <div class="tt-row"><span>Deviation from national avg</span><span class="tt-val">${sign}${d.val.toFixed(2)} pp</span></div>
          <div class="tt-row"><span>State avg share</span><span class="tt-val">${((DATA.global_shares[d.sector] + d.val)).toFixed(1)}%</span></div>
          <div class="tt-row"><span>National avg</span><span class="tt-val">${DATA.global_shares[d.sector].toFixed(1)}%</span></div>
        </div>
      `, e.clientX, e.clientY);
    })
    .on('mousemove', (e) => {
      const tw = tt.offsetWidth;
      tt.style.left = Math.min(e.clientX + 14, window.innerWidth - tw - 16) + 'px';
      tt.style.top = Math.min(e.clientY + 14, window.innerHeight - tt.offsetHeight - 16) + 'px';
    })
    .on('mouseleave', function() {
      d3.select(this).attr('opacity', 0.9).attr('stroke', 'none');
      hideTooltip();
    })
    .on('click', (_, d) => {
      if (lockedState === d.state) {
        lockedState = null;
        hideStateDetail();
      } else {
        lockedState = d.state;
        showStateDetail(d.state);
      }
    });

  // Legend gradient
  const defs = svg.append('defs');
  const lgId = 'heatmap-grad';
  const lg = defs.append('linearGradient').attr('id', lgId);
  lg.append('stop').attr('offset', '0%').attr('stop-color', C.ice);
  lg.append('stop').attr('offset', '50%').attr('stop-color', '#1a1814');
  lg.append('stop').attr('offset', '100%').attr('stop-color', C.ember);

  const legendEl = document.getElementById('state-legend');
  legendEl.innerHTML = `
    <span class="legend-label">Below avg</span>
    <svg width="80" height="8"><defs><linearGradient id="ll"><stop offset="0%" stop-color="${C.ice}"/><stop offset="50%" stop-color="#1a1814"/><stop offset="100%" stop-color="${C.ember}"/></linearGradient></defs><rect width="80" height="8" rx="1" fill="url(#ll)"/></svg>
    <span class="legend-label">Above avg</span>
  `;
}

function showStateDetail(state) {
  const d = DATA.state_data[state];
  const panel = document.getElementById('state-detail-panel');
  document.getElementById('sdp-state-name').textContent = state;
  document.getElementById('sdp-mp-count').textContent = `${d.n} MPs`;

  const topEl = document.getElementById('sdp-top-sectors');
  topEl.innerHTML = d.top_positive.slice(0, 4).map(([s, v]) =>
    `<div class="sdp-sector"><span>${DATA.short_labels[s] || s}</span><span>+${v.toFixed(1)} pp</span></div>`
  ).join('');

  const botEl = document.getElementById('sdp-bot-sectors');
  botEl.innerHTML = d.top_negative.slice(0, 3).map(([s, v]) =>
    `<div class="sdp-sector"><span>${DATA.short_labels[s] || s}</span><span style="color:var(--ice-light)">${v.toFixed(1)} pp</span></div>`
  ).join('');

  panel.classList.remove('hidden');
}

function hideStateDetail() {
  document.getElementById('state-detail-panel').classList.add('hidden');
}

document.getElementById('sdp-close').addEventListener('click', () => {
  lockedState = null;
  hideStateDetail();
});

// ===== CHAPTER 3: SCATTER PLOT =====
function drawChapter3() {
  const container = document.getElementById('scatter-container');
  const stateData = DATA.state_data;
  const states = Object.keys(stateData);

  const margin = { top: 30, right: 30, bottom: 50, left: 60 };
  const totalW = container.offsetWidth || 560;
  const totalH = 420;
  const W = totalW - margin.left - margin.right;
  const H = totalH - margin.top - margin.bottom;

  const svg = d3.select(container)
    .append('svg')
    .attr('width', totalW)
    .attr('height', totalH);

  const g = svg.append('g').attr('transform', `translate(${margin.left},${margin.top})`);

  const xScale = d3.scaleLinear()
    .domain([0, d3.max(states, s => stateData[s].max_distinctiveness) * 1.1])
    .range([0, W]);

  const yScale = d3.scaleLinear()
    .domain([0, d3.max(states, s => stateData[s].avg_within_std) * 1.1])
    .range([H, 0]);

  const rScale = d3.scaleSqrt()
    .domain([0, d3.max(states, s => stateData[s].n)])
    .range([4, 24]);

  // Grid
  g.append('g').attr('class', 'grid')
    .call(d3.axisLeft(yScale).tickSize(-W).tickFormat(''))
    .selectAll('line').attr('stroke', C.rule);
  g.append('g').attr('class', 'grid')
    .attr('transform', `translate(0,${H})`)
    .call(d3.axisBottom(xScale).tickSize(-H).tickFormat(''))
    .selectAll('line').attr('stroke', C.rule);

  // Axes
  g.append('g')
    .attr('transform', `translate(0,${H})`)
    .call(d3.axisBottom(xScale).ticks(5).tickFormat(d => d.toFixed(1) + ' pp'))
    .selectAll('text').attr('fill', C.ash).attr('font-size', '9px');

  g.append('g')
    .call(d3.axisLeft(yScale).ticks(5).tickFormat(d => d.toFixed(1) + ' pp'))
    .selectAll('text').attr('fill', C.ash).attr('font-size', '9px');

  // Axis labels
  g.append('text')
    .attr('x', W / 2).attr('y', H + 42)
    .attr('text-anchor', 'middle')
    .attr('fill', C.ash).attr('font-size', '9px').attr('font-family', 'Space Mono, monospace')
    .text('MAX SECTOR DEVIATION FROM NATIONAL AVG (pp)');

  g.append('text')
    .attr('transform', 'rotate(-90)')
    .attr('x', -H / 2).attr('y', -48)
    .attr('text-anchor', 'middle')
    .attr('fill', C.ash).attr('font-size', '9px').attr('font-family', 'Space Mono, monospace')
    .text('AVG WITHIN-STATE SPREAD (pp)');

  // Quadrant annotation
  g.append('text')
    .attr('x', W - 4).attr('y', H - 10)
    .attr('text-anchor', 'end')
    .attr('fill', C.ember + '80').attr('font-size', '9px').attr('font-family', 'Space Mono, monospace')
    .text('Distinctive + Cohesive');

  // Bubbles
  const bubbles = g.selectAll('.bubble')
    .data(states)
    .join('circle')
    .attr('class', 'bubble')
    .attr('cx', s => xScale(stateData[s].max_distinctiveness))
    .attr('cy', s => yScale(stateData[s].avg_within_std))
    .attr('r', 0)
    .attr('fill', s => {
      const dist = stateData[s].max_distinctiveness;
      const cohesion = stateData[s].avg_within_std;
      // Highlight: distinctive & cohesive = ember; scattered = ice; average = ash
      if (dist > 6 && cohesion < 1.5) return C.ember + 'cc';
      if (cohesion > 2) return C.ice + 'cc';
      return C.ash + '88';
    })
    .attr('stroke', C.rule)
    .attr('stroke-width', 1)
    .attr('cursor', 'pointer');

  // Animate radii
  const obs3 = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        bubbles.transition().delay((_, i) => i * 30).duration(600)
          .attr('r', s => rScale(stateData[s].n));
        obs3.disconnect();
      }
    });
  }, { threshold: 0.3 });
  obs3.observe(container);

  // Labels for notable states
  const notable = states.filter(s =>
    stateData[s].max_distinctiveness > 5 || stateData[s].avg_within_std > 2.3
  );

  g.selectAll('.bubble-label')
    .data(notable)
    .join('text')
    .attr('class', 'bubble-label')
    .attr('x', s => xScale(stateData[s].max_distinctiveness) + rScale(stateData[s].n) + 4)
    .attr('y', s => yScale(stateData[s].avg_within_std) + 4)
    .attr('fill', C.cream)
    .attr('font-size', '8px')
    .attr('font-family', 'Space Mono, monospace')
    .text(s => s);

  // Hover
  bubbles
    .on('mouseenter', function(e, s) {
      d3.select(this).attr('stroke', C.cream).attr('stroke-width', 1.5);
      const d = stateData[s];
      showTooltip(`
        <div class="tt-title">${s}</div>
        <div class="tt-sub">${d.n} MPs</div>
        <div class="tt-body">
          <div class="tt-row"><span>Within-state spread</span><span class="tt-val">${d.avg_within_std.toFixed(2)} pp avg σ</span></div>
          <div class="tt-row"><span>Max distinctiveness</span><span class="tt-val">+${d.max_distinctiveness.toFixed(1)} pp</span></div>
          <div class="tt-row"><span>Top sector</span><span class="tt-val">${DATA.short_labels[d.top_sectors[0]] || d.top_sectors[0]}</span></div>
        </div>
      `, e.clientX, e.clientY);
    })
    .on('mousemove', e => {
      tt.style.left = Math.min(e.clientX + 14, window.innerWidth - tt.offsetWidth - 16) + 'px';
      tt.style.top = Math.min(e.clientY + 14, window.innerHeight - tt.offsetHeight - 16) + 'px';
    })
    .on('mouseleave', function() {
      d3.select(this).attr('stroke', C.rule).attr('stroke-width', 1);
      hideTooltip();
    });
}

// ===== CHAPTER 4: SECTOR FOCUS BARS =====
function drawChapter4() {
  const topSectors = DATA.top20_sectors.slice(0, 16);
  selectedSector = topSectors[0];

  // Build selector
  const selectorEl = document.getElementById('sector-selector');
  topSectors.forEach(s => {
    const btn = document.createElement('button');
    btn.className = 'sector-btn' + (s === selectedSector ? ' active' : '');
    btn.textContent = DATA.short_labels[s] || s;
    btn.addEventListener('click', () => {
      document.querySelectorAll('.sector-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      selectedSector = s;
      updateSectorBars(s);
    });
    selectorEl.appendChild(btn);
  });

  // Draw initial
  updateSectorBars(selectedSector);
}

function updateSectorBars(sector) {
  document.getElementById('sector-vis-title').textContent =
    `Sector focus: ${DATA.short_labels[sector] || sector}`;

  const container = document.getElementById('sector-state-bars');
  container.innerHTML = '';

  const stateData = DATA.state_data;
  const states = Object.keys(stateData).sort((a, b) =>
    (stateData[b].avg_shares[sector] || 0) - (stateData[a].avg_shares[sector] || 0)
  );

  const globalAvg = DATA.global_shares[sector];
  const maxVal = Math.max(globalAvg * 2.5, ...states.map(s => stateData[s].avg_shares[sector] || 0));

  const margin = { top: 10, right: 120, bottom: 30, left: 170 };
  const totalW = container.parentElement.offsetWidth || 700;
  const totalH = Math.max(400, states.length * 26 + margin.top + margin.bottom);
  const W = totalW - margin.left - margin.right;
  const H = totalH - margin.top - margin.bottom;

  const svg = d3.select(container)
    .append('svg')
    .attr('width', totalW)
    .attr('height', totalH);

  const g = svg.append('g').attr('transform', `translate(${margin.left},${margin.top})`);

  const xScale = d3.scaleLinear().domain([0, maxVal]).range([0, W]);
  const yScale = d3.scaleBand().domain(states).range([0, H]).padding(0.3);

  // State labels
  g.selectAll('.state-label')
    .data(states)
    .join('text')
    .attr('class', 'state-label')
    .attr('x', -8)
    .attr('y', s => yScale(s) + yScale.bandwidth() / 2 + 4)
    .attr('text-anchor', 'end')
    .attr('fill', C.fog)
    .attr('font-size', '10px')
    .attr('font-family', 'Space Mono, monospace')
    .text(s => s);

  // Background tracks
  g.selectAll('.track')
    .data(states)
    .join('rect')
    .attr('class', 'track')
    .attr('x', 0)
    .attr('y', s => yScale(s))
    .attr('width', W)
    .attr('height', yScale.bandwidth())
    .attr('fill', 'rgba(245,240,232,0.03)')
    .attr('rx', 1);

  // State avg bars
  const bars = g.selectAll('.state-bar')
    .data(states)
    .join('rect')
    .attr('class', 'state-bar')
    .attr('x', 0)
    .attr('y', s => yScale(s))
    .attr('height', yScale.bandwidth())
    .attr('rx', 1)
    .attr('fill', s => {
      const val = stateData[s].avg_shares[sector] || 0;
      return val > globalAvg ? C.ember + 'bb' : C.ice + '88';
    })
    .attr('width', 0);

  // Animate
  bars.transition().duration(700).delay((_, i) => i * 18)
    .attr('width', s => xScale(stateData[s].avg_shares[sector] || 0));

  // Individual MP dots
  const mpsByState = {};
  states.forEach(state => {
    mpsByState[state] = DATA.mps.filter(m => m.state === state);
  });

  states.forEach(state => {
    const mps = mpsByState[state];
    mps.forEach(mp => {
      const val = mp.shares[sector] || 0;
      g.append('circle')
        .attr('cx', xScale(val))
        .attr('cy', yScale(state) + yScale.bandwidth() / 2)
        .attr('r', 3)
        .attr('fill', C.cream + '60')
        .attr('stroke', C.cream + '40')
        .attr('stroke-width', 0.5)
        .attr('cursor', 'pointer')
        .on('mouseenter', function(e) {
          d3.select(this).attr('r', 5).attr('fill', C.cream);
          showTooltip(`
            <div class="tt-title">${mp.name}</div>
            <div class="tt-sub">${mp.party} · ${mp.state}</div>
            <div class="tt-body">
              <div class="tt-row"><span>${DATA.short_labels[sector] || sector}</span><span class="tt-val">${val.toFixed(1)}%</span></div>
              <div class="tt-row"><span>National avg</span><span class="tt-val">${globalAvg.toFixed(1)}%</span></div>
              <div class="tt-row"><span>Total questions</span><span class="tt-val">${mp.total_questions}</span></div>
            </div>
          `, e.clientX, e.clientY);
        })
        .on('mousemove', e => {
          tt.style.left = Math.min(e.clientX + 14, window.innerWidth - tt.offsetWidth - 16) + 'px';
          tt.style.top = Math.min(e.clientY + 14, window.innerHeight - tt.offsetHeight - 16) + 'px';
        })
        .on('mouseleave', function() {
          d3.select(this).attr('r', 3).attr('fill', C.cream + '60');
          hideTooltip();
        });
    });
  });

  // National avg line
  g.append('line')
    .attr('x1', xScale(globalAvg)).attr('x2', xScale(globalAvg))
    .attr('y1', 0).attr('y2', H)
    .attr('stroke', C.ember)
    .attr('stroke-width', 1)
    .attr('stroke-dasharray', '4,3')
    .attr('opacity', 0.7);

  g.append('text')
    .attr('x', xScale(globalAvg) + 4)
    .attr('y', -4)
    .attr('fill', C.ember)
    .attr('font-size', '8px')
    .attr('font-family', 'Space Mono, monospace')
    .text('National avg');

  // Value labels
  g.selectAll('.val-label')
    .data(states)
    .join('text')
    .attr('class', 'val-label')
    .attr('x', s => xScale(stateData[s].avg_shares[sector] || 0) + 5)
    .attr('y', s => yScale(s) + yScale.bandwidth() / 2 + 4)
    .attr('fill', C.ash)
    .attr('font-size', '9px')
    .attr('font-family', 'Space Mono, monospace')
    .text(s => (stateData[s].avg_shares[sector] || 0).toFixed(1) + '%');
}

// ===== CHAPTER 5: PARTY CHART =====
function drawChapter5() {
  const container = document.getElementById('party-chart');
  const partyData = DATA.party_data;
  const parties = Object.keys(partyData).sort((a, b) => partyData[b].n - partyData[a].n);
  const sectors = DATA.top20_sectors.slice(0, 15);

  const cellW = 38, cellH = 30;
  const labelW = 100, labelH = 95;
  const margin = { top: labelH, left: labelW, bottom: 20, right: 20 };
  const W = sectors.length * cellW + margin.left + margin.right;
  const H = parties.length * cellH + margin.top + margin.bottom;

  const svg = d3.select(container)
    .append('svg')
    .attr('width', Math.min(W, container.offsetWidth || W))
    .attr('height', H)
    .attr('overflow', 'visible');

  // Colour scale
  const allVals2 = [];
  parties.forEach(p => {
    sectors.forEach(s => {
      const v = partyData[p].distinctiveness[s] * 100;
      allVals2.push(v);
    });
  });
  const ext2 = d3.max(allVals2.map(Math.abs));
  const colorScale2 = d3.scaleDiverging()
    .domain([-ext2, 0, ext2])
    .interpolator(d3.interpolateRgbBasis([C.ice, '#1a1814', C.ember]));

  // Column headers
  svg.selectAll('.p-sec-label')
    .data(sectors)
    .join('text')
    .attr('x', (_, i) => margin.left + i * cellW + cellW / 2)
    .attr('y', margin.top - 8)
    .attr('transform', (_, i) => `rotate(-55,${margin.left + i * cellW + cellW / 2},${margin.top - 8})`)
    .attr('text-anchor', 'end')
    .attr('fill', C.ash).attr('font-size', '9px').attr('font-family', 'Space Mono, monospace')
    .text(s => DATA.short_labels[s] || s);

  // Party rows
  const pRows = svg.selectAll('.party-row')
    .data(parties)
    .join('g')
    .attr('class', 'party-row')
    .attr('transform', (_, i) => `translate(0,${margin.top + i * cellH})`);

  pRows.append('text')
    .attr('x', margin.left - 10)
    .attr('y', cellH / 2 + 4)
    .attr('text-anchor', 'end')
    .attr('fill', C.fog).attr('font-size', '10px').attr('font-family', 'Space Mono, monospace')
    .text(p => `${p} (${partyData[p].n})`);

  pRows.selectAll('.p-cell')
    .data(p => sectors.map(sec => ({
      party: p, sector: sec,
      val: (partyData[p].distinctiveness[sec] || 0) * 100
    })))
    .join('rect')
    .attr('class', 'p-cell')
    .attr('x', (_, i) => margin.left + i * cellW + 1)
    .attr('y', 1)
    .attr('width', cellW - 2)
    .attr('height', cellH - 2)
    .attr('rx', 1)
    .attr('fill', d => colorScale2(d.val))
    .attr('opacity', 0.9)
    .attr('cursor', 'pointer')
    .on('mouseenter', function(e, d) {
      d3.select(this).attr('opacity', 1).attr('stroke', C.cream).attr('stroke-width', 1);
      const sign = d.val >= 0 ? '+' : '';
      showTooltip(`
        <div class="tt-title">${d.party}</div>
        <div class="tt-sub">${DATA.short_labels[d.sector] || d.sector}</div>
        <div class="tt-body">
          <div class="tt-row"><span>Deviation from national avg</span><span class="tt-val">${sign}${d.val.toFixed(2)} pp</span></div>
          <div class="tt-row"><span>Party avg</span><span class="tt-val">${(DATA.global_shares[d.sector] + d.val).toFixed(1)}%</span></div>
          <div class="tt-row"><span>National avg</span><span class="tt-val">${DATA.global_shares[d.sector].toFixed(1)}%</span></div>
        </div>
      `, e.clientX, e.clientY);
    })
    .on('mousemove', e => {
      tt.style.left = Math.min(e.clientX + 14, window.innerWidth - tt.offsetWidth - 16) + 'px';
      tt.style.top = Math.min(e.clientY + 14, window.innerHeight - tt.offsetHeight - 16) + 'px';
    })
    .on('mouseleave', function() {
      d3.select(this).attr('opacity', 0.9).attr('stroke', 'none');
      hideTooltip();
    });
}

// ===== KICK OFF =====
document.addEventListener('DOMContentLoaded', init);
