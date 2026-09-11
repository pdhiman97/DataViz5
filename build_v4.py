import json

with open('/Users/aashima/Desktop/DataViz5/data/loksabha-questions/curated/viz_v4_data.json') as f:
    data_str = f.read()
with open('/Users/aashima/Desktop/DataViz5/data/loksabha-questions/curated/mp_images.json') as f:
    imgs_raw = json.load(f)
imgs_str = json.dumps({k:v for k,v in imgs_raw.items() if v}, separators=(',',':'))

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Parliamentary Voices — 17th Lok Sabha</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#f7f5f0;
  --white:#ffffff;
  --ink:#1a1830;
  --ink2:#3a3850;
  --mid:#7070a0;
  --light:#a0a0c0;
  --rule:#e4e0d8;
  --rule2:#ede9e0;
  --ember:#d85820;
  --ember-soft:#f0a060;
  --ember-pale:#fceee4;
  --blue:#2060c8;
  --blue-soft:#6090e0;
  --blue-pale:#e8eef8;
  --font:'Inter',system-ui,-apple-system,sans-serif;
  --mono:'SF Mono','Fira Mono',monospace;
  --serif:Georgia,serif;
}
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

html,body{height:100%;overflow:hidden;background:var(--bg);color:var(--ink);font-family:var(--font)}

/* ── LAYOUT ── */
#app{display:grid;grid-template-rows:auto auto 1fr;height:100vh;overflow:hidden}

/* ── HEADER ── */
#hdr{padding:0.75rem 1.5rem;background:var(--white);border-bottom:1px solid var(--rule);display:flex;align-items:center;gap:1.2rem}
#hdr h1{font-size:1.05rem;font-weight:600;color:var(--ink);letter-spacing:-0.02em;white-space:nowrap}
#hdr h1 span{color:var(--ember)}
.hdr-meta{font-size:0.68rem;color:var(--mid);font-weight:400;flex:1}
#vis-count{font-size:0.68rem;font-weight:600;color:var(--ember);letter-spacing:0.02em;white-space:nowrap;background:var(--ember-pale);padding:0.2rem 0.55rem;border-radius:100px}

/* ── FILTER BAR ── */
#filters{background:var(--white);border-bottom:1px solid var(--rule);padding:0.5rem 1.5rem;display:flex;align-items:center;gap:0.8rem;overflow-x:auto;flex-shrink:0}
#filters::-webkit-scrollbar{display:none}
.fg{display:flex;align-items:center;gap:0.35rem;flex-shrink:0}
.fl{font-size:0.6rem;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;color:var(--light);white-space:nowrap}
.sep{width:1px;height:18px;background:var(--rule);flex-shrink:0;margin:0 0.1rem}
.pill{font-family:var(--font);font-size:0.62rem;font-weight:500;padding:0.22rem 0.6rem;border-radius:100px;background:var(--bg);color:var(--mid);border:1.5px solid var(--rule);cursor:pointer;transition:all 0.15s;white-space:nowrap;user-select:none;letter-spacing:0.01em}
.pill:hover{background:var(--ember-pale);color:var(--ember);border-color:var(--ember-soft)}
.pill.on{background:var(--ember);color:#fff;border-color:var(--ember);font-weight:600}
.pill.party-on{color:#fff;font-weight:600}
.pill.cat-on{background:var(--blue);color:#fff;border-color:var(--blue)}

/* Search */
.sw{position:relative;margin-left:auto;flex-shrink:0}
#srch{background:var(--bg);border:1.5px solid var(--rule);color:var(--ink);font-family:var(--font);font-size:0.65rem;padding:0.24rem 0.7rem 0.24rem 1.7rem;border-radius:100px;outline:none;width:160px;transition:border-color 0.2s;font-weight:400}
#srch::placeholder{color:var(--light)}
#srch:focus{border-color:var(--ember-soft);background:var(--white)}
.si{position:absolute;left:0.55rem;top:50%;transform:translateY(-50%);color:var(--light);font-size:0.75rem;pointer-events:none}

/* ── BODY ── */
#body{display:grid;grid-template-columns:1fr 300px;min-height:0;overflow:hidden}

/* ── CANVAS AREA ── */
#cw{position:relative;overflow:hidden;background:var(--bg)}
#c{position:absolute;inset:0;display:block}
#c.grab{cursor:grab}
#c.grabbing{cursor:grabbing}
#c.pointer{cursor:pointer}

/* Zoom controls */
#zc{position:absolute;bottom:1.1rem;right:1.1rem;display:flex;flex-direction:column;gap:0.3rem}
.zb{width:30px;height:30px;background:var(--white);border:1.5px solid var(--rule);color:var(--mid);border-radius:6px;font-size:1rem;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all 0.15s;font-weight:400;font-family:var(--font)}
.zb:hover{background:var(--ember);color:#fff;border-color:var(--ember)}
.zb.sm{font-size:0.55rem;font-weight:600;letter-spacing:0.04em}
#zpct{position:absolute;bottom:1.1rem;left:50%;transform:translateX(-50%);font-size:0.58rem;color:var(--light);font-weight:500;letter-spacing:0.05em;pointer-events:none;background:var(--white);padding:0.2rem 0.55rem;border-radius:100px;border:1px solid var(--rule)}

/* ── RIGHT PANEL ── */
#rp{background:var(--white);border-left:1.5px solid var(--rule);display:flex;flex-direction:column;overflow:hidden}

/* Panel header */
.rp-head{padding:0.9rem 1.1rem 0.6rem;border-bottom:1px solid var(--rule2);flex-shrink:0}
.rp-title{font-size:0.6rem;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:var(--light);margin-bottom:0.2rem}
#rp-context{font-size:0.88rem;font-weight:600;color:var(--ink);line-height:1.3;min-height:1.1em}

/* MP card */
#mp-card{padding:0.9rem 1.1rem;border-bottom:1px solid var(--rule2);flex-shrink:0}
#mp-card.empty{display:none}
.mc-row{display:flex;gap:0.8rem;align-items:flex-start;margin-bottom:0.6rem}
.mc-img{width:56px;height:56px;border-radius:10px;object-fit:cover;object-position:top;background:var(--bg);border:1.5px solid var(--rule);flex-shrink:0}
.mc-init{width:56px;height:56px;border-radius:10px;background:var(--bg);border:1.5px solid var(--rule);display:flex;align-items:center;justify-content:center;font-family:var(--serif);font-size:1.2rem;color:var(--mid);flex-shrink:0}
.mc-info{flex:1;min-width:0}
.mc-name{font-size:0.88rem;font-weight:600;color:var(--ink);margin-bottom:0.1rem;line-height:1.25;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.mc-sub{font-size:0.6rem;color:var(--mid);line-height:1.5}
.mc-badge{display:inline-block;margin-top:0.25rem;padding:0.12rem 0.45rem;border-radius:100px;font-size:0.57rem;font-weight:600;letter-spacing:0.03em}
.mc-total{display:flex;align-items:baseline;gap:0.3rem}
.mc-total-n{font-size:1.5rem;font-weight:300;color:var(--ink);font-variant-numeric:tabular-nums;letter-spacing:-0.02em}
.mc-total-l{font-size:0.6rem;color:var(--mid);font-weight:500}
.unlock{font-size:0.6rem;color:var(--light);cursor:pointer;margin-top:0.3rem}
.unlock:hover{color:var(--ember)}

/* ── SECTOR RANKING ── */
#rank-wrap{flex:1;overflow-y:auto;padding:0.6rem 0 0.4rem;min-height:0}
#rank-wrap::-webkit-scrollbar{width:3px}
#rank-wrap::-webkit-scrollbar-thumb{background:var(--rule);border-radius:1px}
.rank-head{padding:0 1.1rem 0.4rem;display:flex;align-items:center;justify-content:space-between}
.rank-head-l{font-size:0.6rem;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;color:var(--light)}
.rank-head-r{font-size:0.58rem;color:var(--light)}

.ri{display:flex;align-items:center;gap:0.5rem;padding:0.32rem 1.1rem;transition:background 0.12s;cursor:default}
.ri:hover{background:var(--rule2)}
.rn{font-size:0.68rem;font-weight:700;flex:0 0 18px;text-align:right;color:var(--light);transition:color 0.3s;font-variant-numeric:tabular-nums}
.rn.t{color:var(--ember)}
.rname{font-size:0.7rem;color:var(--ink2);flex:0 0 100px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-weight:400;transition:color 0.2s}
.ri.r1 .rname,.ri.r2 .rname,.ri.r3 .rname{font-weight:500;color:var(--ink)}
.rbar-wrap{flex:1;height:4px;background:var(--rule2);border-radius:2px;overflow:hidden}
.rbar{height:100%;border-radius:2px;transition:width 0.55s cubic-bezier(0.4,0,0.2,1),background 0.3s}
.ri.r1 .rbar{background:var(--ember)}
.ri.r2 .rbar{background:var(--ember-soft)}
.ri.r3 .rbar{background:#e0b080}
.ri:not(.r1):not(.r2):not(.r3) .rbar{background:#c0c8e0}
.rval{font-size:0.65rem;font-weight:600;color:var(--ink);flex:0 0 36px;text-align:right;font-variant-numeric:tabular-nums}

/* ── TOOLTIP ── */
#tt{position:fixed;z-index:999;background:var(--white);border:1.5px solid var(--rule);border-radius:12px;overflow:hidden;pointer-events:none;max-width:210px;box-shadow:0 8px 40px rgba(26,24,48,0.12),0 2px 8px rgba(26,24,48,0.08);opacity:0;transition:opacity 0.1s}
#tt.show{opacity:1}
.tt-img{width:100%;height:75px;object-fit:cover;object-position:top;display:block;background:var(--bg)}
.tt-init{width:100%;height:75px;display:flex;align-items:center;justify-content:center;background:var(--bg);font-family:var(--serif);font-size:1.8rem;color:var(--light)}
.tt-body{padding:0.65rem 0.8rem 0.75rem}
.tt-name{font-size:0.88rem;font-weight:600;color:var(--ink);margin-bottom:0.05rem;line-height:1.2}
.tt-sub{font-size:0.6rem;color:var(--mid);margin-bottom:0.3rem}
.tt-badge{display:inline-block;padding:0.1rem 0.4rem;border-radius:100px;font-size:0.57rem;font-weight:600;letter-spacing:0.02em;margin-bottom:0.4rem}
.tt-qs{font-size:0.78rem;font-weight:700;color:var(--ink);margin-bottom:0.35rem}
.tt-qs span{font-size:0.6rem;font-weight:400;color:var(--mid)}
.tt-label{font-size:0.57rem;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;color:var(--light);margin-bottom:0.2rem}
.tt-row{display:flex;justify-content:space-between;align-items:center;gap:0.4rem;margin-bottom:0.18rem}
.tt-sn{font-size:0.62rem;color:var(--mid)}
.tt-sv{font-size:0.62rem;font-weight:600;color:var(--ink)}
</style>
</head>
<body>
<div id="app">

  <!-- HEADER -->
  <div id="hdr">
    <h1>Parliamentary <span>Voices</span></h1>
    <span class="hdr-meta">17th Lok Sabha · 499 MPs · Each circle = one MP · Height = total questions asked · Position = activity rank</span>
    <span id="vis-count">499 MPs</span>
  </div>

  <!-- FILTERS -->
  <div id="filters">
    <div class="fg">
      <span class="fl">State</span>
      <div id="fp-state" style="display:flex;gap:0.3rem;flex-wrap:nowrap"></div>
    </div>
    <div class="sep"></div>
    <div class="fg">
      <span class="fl">Topic</span>
      <div id="fp-cat" style="display:flex;gap:0.3rem;flex-wrap:nowrap"></div>
    </div>
    <div class="sep"></div>
    <div class="fg">
      <span class="fl">Gender</span>
      <div id="fp-gender" style="display:flex;gap:0.3rem"></div>
    </div>
    <div class="sep"></div>
    <div class="fg">
      <span class="fl">Party</span>
      <div id="fp-party" style="display:flex;gap:0.3rem;flex-wrap:nowrap"></div>
    </div>
    <div class="sw">
      <span class="si">⌕</span>
      <input id="srch" type="text" placeholder="Search MP…" autocomplete="off">
    </div>
  </div>

  <!-- BODY -->
  <div id="body">
    <!-- CANVAS -->
    <div id="cw">
      <canvas id="c" class="grab"></canvas>
      <div id="zc">
        <button class="zb" id="z-in">+</button>
        <button class="zb sm" id="z-fit">fit</button>
        <button class="zb" id="z-out">−</button>
      </div>
      <div id="zpct">100%</div>
    </div>

    <!-- RIGHT PANEL -->
    <div id="rp">
      <div class="rp-head">
        <div class="rp-title">Showing data for</div>
        <div id="rp-context">All 499 MPs</div>
      </div>

      <div id="mp-card" class="empty"></div>

      <div id="rank-wrap">
        <div class="rank-head">
          <span class="rank-head-l">Top 10 debate topics</span>
          <span class="rank-head-r">% of questions</span>
        </div>
        <div id="rank-list"></div>
      </div>
    </div>
  </div>
</div>

<div id="tt"></div>

<script>
const DATA=__DATA__;
const MP_IMGS=__IMGS__;

// Party colours (warm, readable on white)
const PC={
  BJP:'#e05010',INC:'#1060c0',DMK:'#b01010',YSRCP:'#1040a8',
  AITC:'#108040',SS:'#c07010','JD(U)':'#207840',BJD:'#006828',
  BSP:'#004aaa',BRS:'#b01880',TDP:'#c09000',NCP:'#003488',
  SP:'#a81818',CPIM:'#800000',OTHER:'#506090'
};
const pc=p=>PC[p]||PC.OTHER;

// ── CANVAS ──
const canvas=document.getElementById('c');
const ctx=canvas.getContext('2d');
let W=0,H=0,DPR=Math.min(devicePixelRatio||1,2);

function resizeCanvas(){
  const wrap=document.getElementById('cw');
  W=wrap.clientWidth;H=wrap.clientHeight;
  canvas.width=W*DPR;canvas.height=H*DPR;
  canvas.style.width=W+'px';canvas.style.height=H+'px';
  ctx.scale(DPR,DPR);
}

// ── VIEW / CAMERA ──
let cam={scale:1,ox:0,oy:0};

function wts(wx,wy){return{sx:wx*cam.scale+cam.ox,sy:wy*cam.scale+cam.oy};}
function stw(sx,sy){return{wx:(sx-cam.ox)/cam.scale,wy:(sy-cam.oy)/cam.scale};}

function doZoom(f,cx,cy){
  const ps=cam.scale;
  cam.scale=Math.max(0.3,Math.min(10,cam.scale*f));
  const sf=cam.scale/ps;
  cam.ox=cx-(cx-cam.ox)*sf;
  cam.oy=cy-(cy-cam.oy)*sf;
  draw();
}

// ── DOTS ──
// PAD in world-space (pixels at scale=1, relative to canvas coords)
// World x: rank 1..499 spread across [PAD_L .. W-PAD_R]
// World y: questions, 0 at bottom (PAD_B), max at top (PAD_T)
const PAD_L=56,PAD_R=24,PAD_T=24,PAD_B=52;

let dots=[];
let maxQ=DATA.max_q;

function getR(total){
  // Proportional: sqrt scale so area is proportional to total
  const t=(total-DATA.min_q)/(maxQ-DATA.min_q);
  // min radius 5px, max 18px (at scale=1)
  return 5+t*13;
}

function computeDots(){
  // X: evenly distribute 499 MPs left to right (rank order = left to right)
  // Y: proportional to total questions
  const pw=W-PAD_L-PAD_R;
  const ph=H-PAD_T-PAD_B;
  const n=DATA.mps.length;

  dots=DATA.mps.map((mp,i)=>{
    const wx=PAD_L+(i/(n-1))*pw; // rank already sorted 0..n-1
    const yFrac=mp.total/maxQ;
    const wy=PAD_T+(1-yFrac)*ph;
    return{mp,wx,wy,r:getR(mp.total)};
  });
}

// ── FIT CAMERA ──
function fitCam(){
  cam.scale=1;cam.ox=0;cam.oy=0;
  draw();
}

// ── STATE ──
let F={state:null,cat:null,gender:null,party:null,query:''};
let locked=null,hovered=null;
let activeSet=new Set();

function filteredMPs(){
  return DATA.mps.filter(m=>{
    if(F.state&&m.state!==F.state)return false;
    if(F.party&&m.party!==F.party)return false;
    if(F.gender&&m.gender.toLowerCase()!==F.gender.toLowerCase())return false;
    if(F.cat){
      // Show only MPs whose share of cat is >= avg (they focus on it)
      const avg=DATA.avg[F.cat]||0;
      if((m.s[F.cat]||0)<avg*0.5)return false;
    }
    if(F.query){
      const q=F.query.toLowerCase();
      return m.name.toLowerCase().includes(q)||m.state.toLowerCase().includes(q)||m.party.toLowerCase().includes(q);
    }
    return true;
  });
}

// ── DRAW ──
function draw(){
  ctx.clearRect(0,0,W,H);
  const pw=W-PAD_L-PAD_R;
  const ph=H-PAD_T-PAD_B;

  // Background
  ctx.fillStyle='#f7f5f0';
  ctx.fillRect(0,0,W,H);

  // Grid lines (Y)
  const yTicks=[0,100,200,300,400,500,600];
  ctx.font=`${9}px Inter,system-ui,sans-serif`;
  ctx.textAlign='right';
  yTicks.forEach(q=>{
    const yFrac=q/maxQ;
    const wy=PAD_T+(1-yFrac)*ph;
    const{sy}=wts(0,wy);
    if(sy<0||sy>H)return;
    ctx.strokeStyle=q===0?'rgba(26,24,48,0.1)':'rgba(26,24,48,0.05)';
    ctx.lineWidth=q===0?1:0.5;
    ctx.beginPath();ctx.moveTo(PAD_L-8,sy);ctx.lineTo(W,sy);ctx.stroke();
    ctx.fillStyle='rgba(100,100,140,0.55)';
    ctx.fillText(q,PAD_L-12,sy+3);
  });

  // Curved trend line (optional: show the power-law curve of the filtered set)
  const active=filteredMPs();
  if(active.length>5){
    const n=DATA.mps.length;
    ctx.strokeStyle='rgba(216,88,32,0.1)';
    ctx.lineWidth=1.5;
    ctx.setLineDash([4,6]);
    ctx.beginPath();
    let first=true;
    DATA.mps.forEach((mp,i)=>{
      const wx=PAD_L+(i/(n-1))*pw;
      const yFrac=mp.total/maxQ;
      const wy=PAD_T+(1-yFrac)*ph;
      const{sx,sy}=wts(wx,wy);
      if(first){ctx.moveTo(sx,sy);first=false;}else ctx.lineTo(sx,sy);
    });
    ctx.stroke();
    ctx.setLineDash([]);
  }

  // X axis
  const{sy:sy0}=wts(0,PAD_T+ph);
  ctx.strokeStyle='rgba(26,24,48,0.12)';
  ctx.lineWidth=1;
  ctx.beginPath();ctx.moveTo(PAD_L,sy0);ctx.lineTo(W,sy0);ctx.stroke();

  // X tick labels (rank milestones)
  ctx.fillStyle='rgba(100,100,140,0.55)';
  ctx.font='9px Inter,system-ui,sans-serif';
  ctx.textAlign='center';
  [1,100,200,300,400,499].forEach(rank=>{
    const i=rank-1;
    const n=DATA.mps.length;
    const wx=PAD_L+(i/(n-1))*pw;
    const{sx}=wts(wx,0);
    if(sx<0||sx>W)return;
    ctx.fillText('Rank '+rank,sx,sy0+14);
    ctx.strokeStyle='rgba(26,24,48,0.08)';
    ctx.lineWidth=0.5;
    ctx.beginPath();ctx.moveTo(sx,sy0);ctx.lineTo(sx,sy0+5);ctx.stroke();
  });

  // Axis labels
  ctx.save();
  ctx.translate(14,H/2);ctx.rotate(-Math.PI/2);
  ctx.fillStyle='rgba(96,96,140,0.7)';
  ctx.font='9px Inter,system-ui,sans-serif';
  ctx.textAlign='center';
  ctx.fillText('Questions asked →',0,0);
  ctx.restore();

  ctx.fillStyle='rgba(96,96,140,0.55)';
  ctx.font='9px Inter,system-ui,sans-serif';
  ctx.textAlign='center';
  ctx.fillText('← Most active MPs · Ranked by total questions asked · Least active →',W/2,sy0+28);

  // ── DOTS ──
  const lockedId=locked?.id;
  const hovId=hovered?.id;
  const activeIds=new Set(active.map(m=>m.id));
  const catFilter=F.cat;

  // Draw dimmed first
  dots.forEach(d=>{
    if(activeIds.has(d.mp.id))return;
    const{sx,sy}=wts(d.wx,d.wy);
    if(sx<-20||sx>W+20||sy<-20||sy>H+20)return;
    const r=Math.max(1.5,d.r*cam.scale);
    ctx.globalAlpha=0.07;
    ctx.beginPath();ctx.arc(sx,sy,r,0,Math.PI*2);
    ctx.fillStyle=pc(d.mp.party);ctx.fill();
  });
  ctx.globalAlpha=1;

  // Draw active dots — sort by size so small ones appear on top of large
  const activeDots=dots.filter(d=>activeIds.has(d.mp.id))
    .sort((a,b)=>b.r-a.r);

  activeDots.forEach(d=>{
    const{sx,sy}=wts(d.wx,d.wy);
    if(sx<-30||sx>W+30||sy<-30||sy>H+30)return;

    // When category filter active, modulate opacity by that sector's share
    let opacity=0.82;
    if(catFilter){
      const share=d.mp.s[catFilter]||0;
      const avg=DATA.avg[catFilter]||1;
      opacity=0.15+Math.min(1,(share/avg)*0.7);
    }

    const isLocked=d.mp.id===lockedId;
    const isHov=d.mp.id===hovId;
    const r=Math.max(2,d.r*cam.scale);
    const col=pc(d.mp.party);

    ctx.globalAlpha=isLocked||isHov?1:opacity;
    // Shadow for locked
    if(isLocked){ctx.shadowColor=col;ctx.shadowBlur=20;ctx.shadowOffsetX=0;ctx.shadowOffsetY=4;}
    ctx.beginPath();ctx.arc(sx,sy,r,0,Math.PI*2);
    ctx.fillStyle=col;ctx.fill();
    ctx.shadowBlur=0;

    // Stroke ring for locked/hovered
    if(isLocked||isHov){
      ctx.globalAlpha=1;
      ctx.strokeStyle=isLocked?col:'rgba(26,24,48,0.4)';
      ctx.lineWidth=isLocked?2.5:1.5;
      ctx.stroke();
      // Inner white ring
      if(isLocked){
        ctx.strokeStyle='rgba(255,255,255,0.8)';
        ctx.lineWidth=1.5;
        ctx.beginPath();ctx.arc(sx,sy,r-2,0,Math.PI*2);ctx.stroke();
      }
    }
  });
  ctx.globalAlpha=1;

  // Name labels for hovered/locked at high zoom
  if(cam.scale>2){
    activeDots.forEach(d=>{
      if(d.mp.id!==lockedId&&d.mp.id!==hovId)return;
      const{sx,sy}=wts(d.wx,d.wy);
      const r=d.r*cam.scale;
      ctx.fillStyle='rgba(26,24,48,0.85)';
      ctx.font=`bold 9px Inter,system-ui,sans-serif`;
      ctx.textAlign='center';
      ctx.fillText(d.mp.name.split(' ').slice(0,2).join(' '),sx,sy-r-5);
    });
  }

  // Zoom %
  document.getElementById('zpct').textContent=Math.round(cam.scale*100)+'%';
}

// ── HIT TEST ──
function hit(sx,sy){
  const activeIds=new Set(filteredMPs().map(m=>m.id));
  let best=null,bestD=20;
  // Check smaller (on-top) dots first by iterating in reverse size order
  [...dots].filter(d=>activeIds.has(d.mp.id))
    .sort((a,b)=>a.r-b.r)
    .forEach(d=>{
      const{sx:dx,sy:dy}=wts(d.wx,d.wy);
      const dist=Math.sqrt((sx-dx)**2+(sy-dy)**2);
      const hitR=Math.max(d.r*cam.scale+2,8);
      if(dist<hitR&&dist<bestD){bestD=dist;best=d;}
    });
  return best?.mp||null;
}

// ── RANKING ──
function updateRanking(mp){
  let ctx_label,shares;
  if(mp){
    ctx_label=mp.name;shares=mp.s;
  } else {
    const fps=filteredMPs();
    if(fps.length===DATA.total_mps)ctx_label='All '+DATA.total_mps+' MPs';
    else if(F.state)ctx_label=F.state+(F.party?' · '+F.party:'');
    else if(F.party)ctx_label=F.party+' ('+fps.length+' MPs)';
    else if(F.cat)ctx_label=(DATA.labels[F.cat]||F.cat)+' focus ('+fps.length+' MPs)';
    else if(F.gender)ctx_label=F.gender+' MPs ('+fps.length+')';
    else ctx_label=fps.length+' MPs';
    shares={};
    DATA.sectors.forEach(s=>{
      const vals=fps.map(m=>m.s[s]||0);
      shares[s]=vals.length?vals.reduce((a,b)=>a+b,0)/vals.length:0;
    });
  }

  document.getElementById('rp-context').textContent=ctx_label;

  // Top 10 only
  const ranked=DATA.sectors.map(s=>({s,v:shares[s]||0})).sort((a,b)=>b.v-a.v).slice(0,10);
  const maxV=ranked[0]?.v||1;

  const list=document.getElementById('rank-list');
  const prev={};
  list.querySelectorAll('.ri').forEach(el=>{prev[el.dataset.s]=el;});

  ranked.forEach(({s,v},i)=>{
    const name=DATA.labels[s]||s;
    const cls='ri r'+(i+1);
    const numCls='rn'+(i<3?' t':'');
    const barW=Math.round((v/maxV)*100);

    let el=prev[s];
    if(!el){
      el=document.createElement('div');
      el.className=cls;el.dataset.s=s;
      el.innerHTML=`<span class="${numCls}">${i+1}</span><span class="rname" title="${name}">${name}</span><div class="rbar-wrap"><div class="rbar" style="width:0%"></div></div><span class="rval">${v.toFixed(1)}%</span>`;
      list.appendChild(el);
    } else {
      el.className=cls;
      el.querySelector('.rn').className=numCls;
      el.querySelector('.rn').textContent=i+1;
      el.querySelector('.rname').textContent=name;
      el.querySelector('.rval').textContent=v.toFixed(1)+'%';
    }
    requestAnimationFrame(()=>{el.querySelector('.rbar').style.width=barW+'%';});
    list.appendChild(el);
  });

  // Remove old items
  Object.entries(prev).forEach(([k,el])=>{
    if(!ranked.find(r=>r.s===k))el.remove();
  });
}

// ── MP CARD ──
function showCard(mp,isLocked){
  const card=document.getElementById('mp-card');
  if(!mp){card.className='empty';return;}
  card.className='';
  const imgUrl=MP_IMGS[mp.id];
  const col=pc(mp.party);
  const init=mp.name.split(' ').slice(0,2).map(w=>w[0]).join('');

  card.innerHTML=`
    <div class="mc-row">
      ${imgUrl
        ?`<img class="mc-img" src="${imgUrl}" alt="" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'"><div class="mc-init" style="display:none">${init}</div>`
        :`<div class="mc-init">${init}</div>`
      }
      <div class="mc-info">
        <div class="mc-name">${mp.name}</div>
        <div class="mc-sub">${mp.constituency}</div>
        <div class="mc-sub">${mp.state}</div>
        <div class="mc-badge" style="background:${col}18;color:${col};border:1px solid ${col}40">${mp.party} · ${mp.gender}</div>
      </div>
    </div>
    <div class="mc-total">
      <span class="mc-total-n">${mp.total.toLocaleString()}</span>
      <span class="mc-total-l">questions asked &nbsp;·&nbsp; Rank #${mp.rank}</span>
    </div>
    ${isLocked?`<div class="unlock" id="ul-btn">← Click dot again or here to deselect</div>`:''}
  `;
  if(isLocked&&document.getElementById('ul-btn')){
    document.getElementById('ul-btn').onclick=()=>{
      locked=null;hovered=null;
      showCard(null,false);updateRanking(null);draw();
    };
  }
}

// ── TOOLTIP ──
const ttEl=document.getElementById('tt');
function showTT(mp,x,y){
  const imgUrl=MP_IMGS[mp.id];
  const col=pc(mp.party);
  const init=mp.name.split(' ').slice(0,2).map(w=>w[0]).join('');
  const top3=DATA.sectors.map(s=>({s,v:mp.s[s]||0})).sort((a,b)=>b.v-a.v).slice(0,3);
  ttEl.innerHTML=`
    ${imgUrl?`<img class="tt-img" src="${imgUrl}" alt="" onerror="this.style.display='none'">`:`<div class="tt-init">${init}</div>`}
    <div class="tt-body">
      <div class="tt-name">${mp.name}</div>
      <div class="tt-sub">${mp.constituency} · ${mp.state}</div>
      <span class="tt-badge" style="background:${col}18;color:${col};border:1px solid ${col}40">${mp.party}</span>
      <div class="tt-qs">${mp.total.toLocaleString()} <span>questions · Rank #${mp.rank}</span></div>
      <div class="tt-label">Top topics</div>
      ${top3.map(({s,v})=>`<div class="tt-row"><span class="tt-sn">${DATA.labels[s]||s}</span><span class="tt-sv">${v.toFixed(1)}%</span></div>`).join('')}
    </div>`;
  const tw=ttEl.offsetWidth,th=ttEl.offsetHeight;
  ttEl.style.left=Math.min(x+14,window.innerWidth-tw-8)+'px';
  ttEl.style.top=Math.min(y+10,window.innerHeight-th-8)+'px';
  ttEl.classList.add('show');
}
function hideTT(){ttEl.classList.remove('show');}

// ── CANVAS EVENTS ──
let drag=null;
canvas.addEventListener('wheel',e=>{
  e.preventDefault();
  const r=canvas.getBoundingClientRect();
  doZoom(e.deltaY<0?1.18:1/1.18,e.clientX-r.left,e.clientY-r.top);
},{passive:false});

canvas.addEventListener('mousedown',e=>{
  drag={x:e.clientX,y:e.clientY,ox:cam.ox,oy:cam.oy};
  canvas.className='grabbing';
});
window.addEventListener('mousemove',e=>{
  if(drag){
    cam.ox=drag.ox+(e.clientX-drag.x);
    cam.oy=drag.oy+(e.clientY-drag.y);
    draw();return;
  }
  const r=canvas.getBoundingClientRect();
  const mp=hit(e.clientX-r.left,e.clientY-r.top);
  if(mp){
    canvas.className='pointer';
    hovered=mp;
    showTT(mp,e.clientX,e.clientY);
    if(!locked){updateRanking(mp);showCard(mp,false);}
    draw();
  } else {
    canvas.className='grab';
    hideTT();
    if(!locked&&hovered){hovered=null;updateRanking(null);showCard(null,false);draw();}
    else if(!locked) hovered=null;
  }
});
window.addEventListener('mouseup',e=>{
  if(drag){
    const moved=Math.abs(e.clientX-drag.x)+Math.abs(e.clientY-drag.y);
    drag=null;canvas.className=hovered?'pointer':'grab';
    if(moved<5){
      const r=canvas.getBoundingClientRect();
      const mp=hit(e.clientX-r.left,e.clientY-r.top);
      if(mp){
        locked=locked?.id===mp.id?null:mp;
        updateRanking(locked||mp);showCard(locked||mp,!!locked);
      } else {
        locked=null;updateRanking(null);showCard(null,false);
      }
      draw();
    }
  }
});
canvas.addEventListener('mouseleave',()=>{
  hideTT();
  if(!locked){hovered=null;updateRanking(null);showCard(null,false);draw();}
});

// Zoom buttons
document.getElementById('z-in').onclick=()=>doZoom(1.4,W/2,H/2);
document.getElementById('z-out').onclick=()=>doZoom(1/1.4,W/2,H/2);
document.getElementById('z-fit').onclick=()=>{fitCam();};

// ── FILTERS ──
function buildFilters(){
  // State (top 10)
  const topStates=DATA.states.slice(0,10);
  fp('fp-state',['All',...topStates],s=>s==='All'?F.state===null:F.state===s,s=>{
    F.state=s==='All'?null:s;reset();
  },s=>s==='All'?'All':s.replace(' Pradesh','').replace('Tamil Nadu','TN').replace('West Bengal','WB').replace('Uttar','UP').replace(' Pradesh','').replace('Andhra','AP').replace('Himachal','HP'));

  // Category/topic (top 12 sectors short names)
  const sectors=DATA.sectors.slice(0,12);
  const fpCat=document.getElementById('fp-cat');
  fpCat.innerHTML='';
  const allBtn=document.createElement('span');
  allBtn.className='pill cat-on'.replace('cat-on',F.cat===null?'pill on':'pill');
  allBtn.textContent='All';
  allBtn.onclick=()=>{F.cat=null;reset();};
  fpCat.appendChild(allBtn);
  sectors.forEach(s=>{
    const p=document.createElement('span');
    p.className='pill'+(F.cat===s?' cat-on':'');
    p.textContent=DATA.labels[s]||s;
    p.onclick=()=>{F.cat=F.cat===s?null:s;reset();};
    fpCat.appendChild(p);
  });

  // Gender
  fp('fp-gender',['All','Male','Female'],g=>g==='All'?F.gender===null:F.gender===g,g=>{
    F.gender=g==='All'?null:g;reset();
  });

  // Party
  fp('fp-party',['All',...DATA.parties],p=>p==='All'?F.party===null:F.party===p,p=>{
    F.party=p==='All'?null:p;reset();
  },p=>{
    if(p==='All')return'All';return p;
  });
}

function fp(id,items,isOn,onClick,label){
  const el=document.getElementById(id);el.innerHTML='';
  items.forEach(item=>{
    const p=document.createElement('span');
    const on=isOn(item);
    const lbl=label?label(item):item;
    p.className='pill'+(on?' on':'');
    if(on&&item!=='All'&&id==='fp-party'){p.style.background=pc(item);p.style.borderColor=pc(item);p.style.color='#fff';}
    p.textContent=lbl;p.title=item;
    p.onclick=()=>onClick(item);
    el.appendChild(p);
  });
}

function reset(){
  locked=null;hovered=null;
  activeSet=new Set(filteredMPs().map(m=>m.id));
  buildFilters();
  updateRanking(null);showCard(null,false);
  const fps=filteredMPs();
  document.getElementById('vis-count').textContent=fps.length+' MPs';
  draw();
}

document.getElementById('srch').addEventListener('input',e=>{
  F.query=e.target.value.trim();
  locked=null;hovered=null;reset();
});

// ── RESIZE ──
let rt;
window.addEventListener('resize',()=>{
  clearTimeout(rt);
  rt=setTimeout(()=>{resizeCanvas();computeDots();fitCam();},120);
});

// ── INIT ──
resizeCanvas();
computeDots();
fitCam();
activeSet=new Set(DATA.mps.map(m=>m.id));
buildFilters();
updateRanking(null);
draw();
</script>
</body>
</html>"""

HTML=HTML.replace('__DATA__',data_str).replace('__IMGS__',imgs_str)

with open('/Users/aashima/Desktop/DataViz5/outcome/loksabha-questions/viz_v4.html','w') as f:
    f.write(HTML)

bO=HTML.count('{');bC=HTML.count('}')
pO=HTML.count('(');pC=HTML.count(')')
print(f"Written: {len(HTML)//1024} KB")
print(f"Braces: {bO}/{bC} {'OK' if bO==bC else 'MISMATCH'}")
print(f"Parens: {pO}/{pC} {'OK' if pO==pC else 'MISMATCH'}")
