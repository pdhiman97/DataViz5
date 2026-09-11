import json

# Load all data
with open('/Users/aashima/Desktop/DataViz5/data/loksabha-questions/curated/viz_v3_data.json') as f:
    data_str = f.read()

with open('/Users/aashima/Desktop/DataViz5/data/loksabha-questions/curated/mp_images.json') as f:
    imgs_raw = json.load(f)
imgs_clean = {k:v for k,v in imgs_raw.items() if v}
imgs_str = json.dumps(imgs_clean, separators=(',',':'))

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Parliamentary Voices — 17th Lok Sabha</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#07070f;--surf:#0f0f1c;--surf2:#13131f;
  --bdr:rgba(255,255,255,0.07);--bdr2:rgba(255,255,255,0.04);
  --ember:#f0783c;--ember2:#f8a878;--ice:#48a0d8;--ice2:#80c0e8;
  --cream:#ddd8cc;--fog:#8888a0;--ash:#44445a;--ghost:rgba(255,255,255,0.04);
  --font:'SF Mono','Fira Mono','Courier New',monospace;
  --serif:Georgia,serif;
}
html,body{height:100%;overflow:hidden;background:var(--bg);color:var(--cream);font-family:var(--font);font-size:13px}

/* ── LAYOUT ── */
#app{display:grid;grid-template-rows:auto auto 1fr;height:100vh}

/* HEADER */
#hdr{display:flex;align-items:center;gap:1rem;padding:0.6rem 1.4rem;border-bottom:1px solid var(--bdr);flex-wrap:wrap}
#hdr h1{font-family:var(--serif);font-size:1.15rem;font-weight:400;color:var(--cream);white-space:nowrap}
#hdr h1 em{color:var(--ember);font-style:italic}
#hdr-sub{font-size:0.6rem;color:var(--ash);letter-spacing:0.06em;flex:1}
#hdr-count{font-size:0.6rem;color:var(--ember);letter-spacing:0.1em;text-transform:uppercase;white-space:nowrap}

/* FILTER BAR */
#filters{display:flex;align-items:center;gap:0.6rem;padding:0.45rem 1.4rem;border-bottom:1px solid var(--bdr);background:var(--surf);overflow-x:auto;flex-shrink:0}
#filters::-webkit-scrollbar{display:none}
.fl{font-size:0.55rem;letter-spacing:0.12em;text-transform:uppercase;color:var(--ash);white-space:nowrap}
.sep{width:1px;height:16px;background:var(--bdr);flex-shrink:0}
.pills{display:flex;gap:0.25rem;flex-shrink:0}
.pill{font-family:var(--font);font-size:0.58rem;letter-spacing:0.03em;padding:0.2rem 0.5rem;border-radius:100px;background:rgba(255,255,255,0.04);color:var(--fog);border:1px solid var(--bdr);cursor:pointer;transition:all 0.15s;white-space:nowrap;user-select:none}
.pill:hover{background:rgba(255,255,255,0.09);color:var(--cream);border-color:rgba(255,255,255,0.18)}
.pill.on{background:var(--ember);color:#07070f;border-color:var(--ember);font-weight:700}
.pill.party-on{font-weight:700}

/* SEARCH */
.srch-wrap{position:relative;margin-left:auto;flex-shrink:0}
#srch{background:rgba(255,255,255,0.04);border:1px solid var(--bdr);color:var(--cream);font-family:var(--font);font-size:0.62rem;padding:0.22rem 0.6rem 0.22rem 1.5rem;border-radius:100px;outline:none;width:150px;transition:border-color 0.2s}
#srch::placeholder{color:var(--ash)}
#srch:focus{border-color:rgba(255,255,255,0.2)}
.si{position:absolute;left:0.5rem;top:50%;transform:translateY(-50%);color:var(--ash);pointer-events:none;font-size:0.7rem}

/* BODY: ranking + canvas */
#body{display:grid;grid-template-columns:264px 1fr;min-height:0;overflow:hidden}

/* ── LEFT PANEL: RANKING ── */
#rank-panel{background:var(--surf2);border-right:1px solid var(--bdr);display:flex;flex-direction:column;overflow:hidden}
#rank-header{padding:0.8rem 1rem 0.5rem;border-bottom:1px solid var(--bdr);flex-shrink:0}
#rank-title{font-size:0.58rem;letter-spacing:0.1em;text-transform:uppercase;color:var(--ash);margin-bottom:0.15rem}
#rank-context{font-size:0.75rem;color:var(--cream);font-family:var(--serif);line-height:1.3;min-height:1.1rem;transition:color 0.3s}

/* Ranking list */
#rank-list{flex:1;overflow-y:auto;padding:0.5rem 0;position:relative}
#rank-list::-webkit-scrollbar{width:2px}
#rank-list::-webkit-scrollbar-thumb{background:var(--ash)}

.rank-item{display:flex;align-items:center;gap:0.55rem;padding:0.38rem 1rem;transition:background 0.15s;cursor:default;position:relative}
.rank-item:hover{background:rgba(255,255,255,0.03)}
.rank-num{font-size:0.62rem;color:var(--ash);flex:0 0 18px;text-align:right;font-weight:700;transition:color 0.3s}
.rank-num.top{color:var(--ember)}
.rank-bar-wrap{flex:1;height:3px;background:rgba(255,255,255,0.05);border-radius:1px;overflow:hidden}
.rank-bar{height:100%;border-radius:1px;transition:width 0.5s cubic-bezier(0.4,0,0.2,1),background 0.3s}
.rank-name{font-size:0.68rem;color:var(--fog);flex:0 0 90px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;transition:color 0.2s}
.rank-val{font-size:0.65rem;color:var(--cream);flex:0 0 34px;text-align:right;font-weight:700;font-variant-numeric:tabular-nums}
.rank-item.top1 .rank-name{color:var(--cream)}
.rank-item.top1 .rank-bar{background:var(--ember)}
.rank-item.top2 .rank-bar{background:#c06030}
.rank-item.top3 .rank-bar{background:#905028}
.rank-item:not(.top1):not(.top2):not(.top3) .rank-bar{background:#404060}

/* ── MP CARD (in rank panel) ── */
#mp-card{border-top:1px solid var(--bdr);flex-shrink:0;max-height:240px;overflow-y:auto}
#mp-card::-webkit-scrollbar{display:none}
#mp-card.hidden{display:none}
.mp-top{display:flex;gap:0.75rem;padding:0.8rem 1rem 0.5rem;align-items:flex-start}
.mp-img-wrap{flex-shrink:0}
.mp-img{width:52px;height:52px;border-radius:50%;object-fit:cover;object-position:top;background:var(--surf);border:1.5px solid var(--bdr)}
.mp-init{width:52px;height:52px;border-radius:50%;background:var(--surf);border:1.5px solid var(--bdr);display:flex;align-items:center;justify-content:center;font-family:var(--serif);font-size:1.1rem;color:var(--ash)}
.mp-info{flex:1;min-width:0}
.mp-name{font-family:var(--serif);font-size:0.9rem;color:var(--cream);line-height:1.2;margin-bottom:0.1rem;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.mp-meta{font-size:0.6rem;color:var(--fog);line-height:1.5}
.mp-badge{display:inline-block;margin-top:0.25rem;padding:0.1rem 0.4rem;border-radius:100px;font-size:0.57rem;font-weight:700;letter-spacing:0.04em}
.mp-qs{font-size:0.6rem;color:var(--ash);padding:0 1rem 0.6rem}
.unlock-hint{font-size:0.56rem;color:var(--ash);padding:0 1rem 0.5rem;cursor:pointer}
.unlock-hint:hover{color:var(--fog)}

/* ── CANVAS AREA ── */
#canvas-wrap{position:relative;overflow:hidden;background:var(--bg)}
#c{position:absolute;inset:0;display:block;cursor:grab}
#c.grabbing{cursor:grabbing}

/* Zoom controls */
#zoom-ctrl{position:absolute;bottom:1rem;right:1rem;display:flex;flex-direction:column;gap:0.3rem;z-index:10}
.z-btn{width:28px;height:28px;border:1px solid var(--bdr);background:rgba(15,15,28,0.85);color:var(--fog);border-radius:4px;font-size:1rem;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all 0.15s}
.z-btn:hover{background:rgba(255,255,255,0.1);color:var(--cream)}

/* Context hint */
#field-hint{position:absolute;bottom:1rem;left:1rem;font-size:0.57rem;color:var(--ash);letter-spacing:0.05em;pointer-events:none}
#zoom-pct{position:absolute;bottom:1rem;left:50%;transform:translateX(-50%);font-size:0.57rem;color:var(--ash);letter-spacing:0.08em;pointer-events:none}

/* ── TOOLTIP ── */
#tt{position:fixed;z-index:1000;background:#12122a;border:1px solid rgba(255,255,255,0.14);border-radius:8px;overflow:hidden;pointer-events:none;max-width:220px;box-shadow:0 16px 48px rgba(0,0,0,0.75);opacity:0;transition:opacity 0.1s}
#tt.show{opacity:1}
.tt-photo{width:100%;height:80px;object-fit:cover;object-position:center top;display:block;background:var(--surf)}
.tt-init{width:100%;height:80px;display:flex;align-items:center;justify-content:center;background:var(--surf2);font-family:var(--serif);font-size:2rem;color:var(--ash)}
.tt-body{padding:0.6rem 0.75rem 0.7rem}
.tt-name{font-family:var(--serif);font-size:0.9rem;color:var(--cream);margin-bottom:0.1rem}
.tt-sub{font-size:0.6rem;color:var(--fog);margin-bottom:0.3rem}
.tt-badge{display:inline-block;padding:0.1rem 0.4rem;border-radius:100px;font-size:0.57rem;font-weight:700;letter-spacing:0.04em;margin-bottom:0.45rem}
.tt-qs{font-size:0.65rem;color:var(--cream);font-weight:700;margin-bottom:0.3rem}
.tt-top-label{font-size:0.57rem;color:var(--ash);letter-spacing:0.08em;text-transform:uppercase;margin-bottom:0.25rem}
.tt-sec-row{display:flex;justify-content:space-between;gap:0.5rem;margin-bottom:0.2rem}
.tt-sec-n{font-size:0.62rem;color:var(--fog)}
.tt-sec-v{font-size:0.62rem;color:var(--ember2);font-weight:700}

/* ── Y-AXIS LABEL ── */
#y-label{position:absolute;left:0;top:50%;transform:translateY(-50%) rotate(-90deg);font-size:0.6rem;color:var(--ice);letter-spacing:0.1em;text-transform:uppercase;pointer-events:none;transform-origin:center;white-space:nowrap;opacity:0.8}

/* State label style (shown on canvas) */
</style>
</head>
<body>
<div id="app">

  <!-- HEADER -->
  <div id="hdr">
    <h1>Parliamentary <em>Voices</em></h1>
    <span id="hdr-sub">17th Lok Sabha · Each bubble = 1 MP · Height = questions asked · Grouped by state</span>
    <span id="hdr-count">499 MPs</span>
  </div>

  <!-- FILTER BAR -->
  <div id="filters">
    <span class="fl">State</span>
    <div class="pills" id="p-state"></div>
    <div class="sep"></div>
    <span class="fl">Party</span>
    <div class="pills" id="p-party"></div>
    <div class="sep"></div>
    <span class="fl">Gender</span>
    <div class="pills" id="p-gender"></div>
    <div class="srch-wrap">
      <span class="si">⌕</span>
      <input id="srch" type="text" placeholder="Search MP…" autocomplete="off">
    </div>
  </div>

  <!-- BODY -->
  <div id="body">

    <!-- LEFT: RANKING -->
    <div id="rank-panel">
      <div id="rank-header">
        <div id="rank-title">Top sectors by % of questions</div>
        <div id="rank-context">All 499 MPs</div>
      </div>
      <div id="rank-list"></div>
      <div id="mp-card" class="hidden"></div>
    </div>

    <!-- RIGHT: CANVAS -->
    <div id="canvas-wrap">
      <canvas id="c"></canvas>
      <div id="y-label">Questions asked</div>
      <div id="zoom-ctrl">
        <button class="z-btn" id="z-in" title="Zoom in">+</button>
        <button class="z-btn" id="z-reset" title="Reset view" style="font-size:0.65rem;letter-spacing:0">fit</button>
        <button class="z-btn" id="z-out" title="Zoom out">−</button>
      </div>
      <div id="field-hint">scroll to zoom · drag to pan · click to lock</div>
      <div id="zoom-pct">100%</div>
    </div>

  </div>
</div>

<div id="tt"></div>

<script>
// ─── DATA ───
const DATA = __DATA__;
const MP_IMGS = __IMGS__;

// ─── PARTY COLOURS ───
const PC={BJP:'#FF6B35',INC:'#19B5FF',DMK:'#E31E24',YSRCP:'#2196F3',AITC:'#2ECC71',
  SS:'#FF9933',SHS:'#FF9933','JD(U)':'#3CB371',BJD:'#009900',BSP:'#1565C0',
  BRS:'#E91E8C',TDP:'#F9A825',NCP:'#0D47A1',SP:'#CC3232',CPIM:'#C62828',OTHER:'#6060A0'};
const pc=p=>PC[p]||PC.OTHER;

// ─── CANVAS SETUP ───
const canvas=document.getElementById('c');
const ctx=canvas.getContext('2d');
let W=0,H=0,DPR=devicePixelRatio||1;

function resizeCanvas(){
  const wrap=document.getElementById('canvas-wrap');
  W=wrap.clientWidth; H=wrap.clientHeight;
  canvas.width=W*DPR; canvas.height=H*DPR;
  canvas.style.width=W+'px'; canvas.style.height=H+'px';
  ctx.scale(DPR,DPR);
}

// ─── VIEW TRANSFORM ───
// We use a virtual "world" space then a camera transform
// World: x=state col (0..stateCount*COL_W), y=questions (0..maxQ)
// Camera: scale, offsetX, offsetY
let cam={scale:1, ox:0, oy:0};
const COL_W=60; // pixels per state column in world space (before scale)
const PAD_T=30, PAD_B=50, PAD_L=50, PAD_R=20;

function worldToScreen(wx,wy){
  return {
    sx: (wx*cam.scale)+cam.ox,
    sy: (wy*cam.scale)+cam.oy
  };
}
function screenToWorld(sx,sy){
  return {
    wx:(sx-cam.ox)/cam.scale,
    wy:(sy-cam.oy)/cam.scale
  };
}

// ─── DOTS ───
let allDots=[];   // {mp, wx, wy, r}
let filteredSet=new Set(); // mp ids currently active

const MAX_Q=DATA.max_q;
const STATES=DATA.state_order;
const N_STATES=STATES.length;
const DOT_R_MIN=3, DOT_R_MAX=10;

function getR(total){
  const t=(total-1)/(MAX_Q-1);
  return DOT_R_MIN+t*(DOT_R_MAX-DOT_R_MIN);
}

// Compute world positions: beeswarm per state
function computeDots(){
  allDots=[];
  // group by state
  const byState={};
  STATES.forEach(s=>{ byState[s]=[]; });
  DATA.mps.forEach(m=>{ if(byState[m.state]) byState[m.state].push(m); });

  const worldH=H-PAD_T-PAD_B; // height in screen px before cam transform — we compute in world coords
  // world y: wy=0 → max questions (top), wy=MAX_Q → 0 (bottom)
  // We'll compute wy directly in screen-space so 1 world unit = 1 screen px at scale=1

  STATES.forEach((state,si)=>{
    const mps=byState[state];
    // sort by total questions
    mps.sort((a,b)=>a.total-b.total);
    // x center for this state (world)
    const xCenter=PAD_L+si*COL_W+COL_W/2;

    // spread horizontally: alternate left/right of center
    const spread=Math.min(COL_W*0.4, mps.length*2.5);
    mps.forEach((mp,i)=>{
      const r=getR(mp.total);
      // Deterministic jitter for x
      let h=0; for(let c of mp.id) h=(h*31+c.charCodeAt(0))&0x7fffffff;
      const frac=((h&0xff)/255)-0.5; // -0.5..0.5
      const wx=xCenter+frac*spread;
      // wy: world y = direct screen y at scale=1
      // We want wy=0 at top (y=PAD_T) and wy=worldH at bottom (y=H-PAD_B)
      const yFrac=1-(mp.total/MAX_Q); // 0=top (most qs), 1=bottom (fewest)
      const wy=PAD_T+yFrac*(H-PAD_T-PAD_B);
      allDots.push({mp,wx,wy,r});
    });
  });

  // Reset camera to fit
  resetCam(false);
}

// ─── CAMERA ───
function resetCam(animate){
  const worldW=PAD_L+N_STATES*COL_W+PAD_R;
  const scaleX=W/worldW;
  const scaleY=1; // y is already in screen coords
  cam.scale=Math.min(scaleX,1);
  cam.ox=0;
  cam.oy=0;
  // center horizontally
  const scaledW=worldW*cam.scale;
  cam.ox=(W-scaledW)/2;
  draw();
}

function zoom(factor, cx, cy){
  // zoom around point (cx,cy) in screen coords
  const prevScale=cam.scale;
  cam.scale=Math.max(0.4,Math.min(8,cam.scale*factor));
  const sf=cam.scale/prevScale;
  cam.ox=cx-(cx-cam.ox)*sf;
  cam.oy=cy-(cy-cam.oy)*sf;
  draw();
}

// ─── DRAW ───
function draw(){
  ctx.clearRect(0,0,W,H);

  const worldH=H-PAD_T-PAD_B;

  // ── Grid lines & Y axis ──
  ctx.font=`${8.5}px SF Mono,monospace`;
  ctx.textAlign='right';
  const yTicks=[0,100,200,300,400,500,600];
  yTicks.forEach(q=>{
    const yFrac=1-(q/MAX_Q);
    const wy=PAD_T+yFrac*worldH; // world y
    const {sx,sy}=worldToScreen(0,wy);
    // grid line
    ctx.strokeStyle='rgba(255,255,255,0.04)';
    ctx.lineWidth=0.5;
    ctx.beginPath();
    ctx.moveTo(0,sy);
    ctx.lineTo(W,sy);
    ctx.stroke();
    // label
    ctx.fillStyle='rgba(100,120,160,0.6)';
    ctx.fillText(q,40,sy+3);
  });

  // ── State labels & column lines ──
  ctx.textAlign='center';
  ctx.font=`${8}px SF Mono,monospace`;
  STATES.forEach((state,si)=>{
    const xCenter=PAD_L+si*COL_W+COL_W/2;
    const {sx:sx0}=worldToScreen(xCenter,0);
    // Only draw if in viewport
    if(sx0<-80||sx0>W+80) return;
    // faint column line
    ctx.strokeStyle='rgba(255,255,255,0.03)';
    ctx.lineWidth=0.5;
    const {sx:sxL}=worldToScreen(xCenter-COL_W/2,0);
    ctx.beginPath();
    ctx.moveTo(sxL,0);
    ctx.lineTo(sxL,H-PAD_B);
    ctx.stroke();

    // State label at bottom
    ctx.fillStyle='rgba(120,120,160,0.55)';
    // Shorten state names
    const shortState=state.replace(' Pradesh','').replace(' and Nicobar Islands','&NI')
      .replace('and Nicobar','&NI').replace('Himachal','HP').replace('Uttarakhand','Ukhand')
      .replace('Chhattisgarh','CG').replace('Jharkhand','JH').replace('Telangana','TG')
      .replace('Karnataka','KA').replace('Maharashtra','MH').replace('Rajasthan','RJ')
      .replace('Tamil Nadu','TN').replace('West Bengal','WB').replace('Jammu and Kashmir','J&K')
      .replace('Andhra','AP').replace('Meghalaya','ML').replace('Manipur','MN')
      .replace('Tripura','TR').replace('Assam','AS').replace('Punjab','PB')
      .replace('Haryana','HR').replace('Odisha','OD').replace('Kerala','KL')
      .replace('Dadra Nagar Haveli','DNH').replace('Gujarat','GJ').replace('Bihar','BR')
      .replace('Uttar','UP ').replace(' Pradesh','').trim()
      .replace('Dadra and Nagar Haveli','DNH');

    // Only show label if zoomed enough or always
    const visW=COL_W*cam.scale;
    if(visW>20){
      ctx.save();
      ctx.translate(sx0,H-PAD_B+12);
      if(visW<45) ctx.rotate(-Math.PI/4);
      ctx.fillText(shortState,0,0);
      ctx.restore();
    }
  });

  // ── X axis line ──
  ctx.strokeStyle='rgba(255,255,255,0.08)';
  ctx.lineWidth=0.5;
  ctx.beginPath();
  ctx.moveTo(0,H-PAD_B);
  ctx.lineTo(W,H-PAD_B);
  ctx.stroke();

  // ── Y axis label ──
  ctx.save();
  ctx.translate(12,H/2);
  ctx.rotate(-Math.PI/2);
  ctx.fillStyle='rgba(72,160,216,0.5)';
  ctx.font=`9px SF Mono,monospace`;
  ctx.textAlign='center';
  ctx.fillText('QUESTIONS ASKED →',0,0);
  ctx.restore();

  // X label
  ctx.fillStyle='rgba(120,120,160,0.4)';
  ctx.font=`9px SF Mono,monospace`;
  ctx.textAlign='center';
  ctx.fillText('← STATES →',W/2,H-4);

  // ── Dots ──
  const lockedId=locked?.id;
  const hovId=hovered?.id;

  // Draw dimmed first, then active
  allDots.forEach(d=>{
    const isActive=filteredSet.has(d.mp.id);
    const isLocked=d.mp.id===lockedId;
    const isHov=d.mp.id===hovId;
    const {sx,sy}=worldToScreen(d.wx,d.wy);
    if(sx<-30||sx>W+30||sy<-30||sy>H+30) return; // cull
    const r=Math.max(1.5,d.r*cam.scale*0.8);
    const col=pc(d.mp.party);

    if(!isActive){
      ctx.globalAlpha=0.055;
      ctx.beginPath();ctx.arc(sx,sy,r,0,Math.PI*2);
      ctx.fillStyle=col;ctx.fill();
    }
  });

  allDots.forEach(d=>{
    const isActive=filteredSet.has(d.mp.id);
    if(!isActive) return;
    const isLocked=d.mp.id===lockedId;
    const isHov=d.mp.id===hovId;
    const {sx,sy}=worldToScreen(d.wx,d.wy);
    if(sx<-30||sx>W+30||sy<-30||sy>H+30) return;
    const r=Math.max(1.5,d.r*cam.scale*0.8);
    const col=pc(d.mp.party);

    ctx.globalAlpha=isLocked||isHov?1:0.75;
    if(isLocked){ctx.shadowColor=col;ctx.shadowBlur=16;}
    ctx.beginPath();ctx.arc(sx,sy,r,0,Math.PI*2);
    ctx.fillStyle=col;ctx.fill();
    ctx.shadowBlur=0;

    if(isLocked||isHov){
      ctx.globalAlpha=1;
      ctx.strokeStyle=isLocked?'#fff':'rgba(255,255,255,0.7)';
      ctx.lineWidth=isLocked?1.5:1;
      ctx.stroke();
    }

    // Show MP name if zoomed in a lot
    if((isLocked||isHov||S.query.length>1)&&isActive&&cam.scale>2){
      ctx.globalAlpha=1;
      ctx.fillStyle='#ddd';
      ctx.font=`bold ${8}px SF Mono,monospace`;
      ctx.textAlign='center';
      ctx.fillText(d.mp.name.split(' ')[0],sx,sy-r-3);
    }
  });

  ctx.globalAlpha=1;

  // Zoom %
  document.getElementById('zoom-pct').textContent=Math.round(cam.scale*100)+'%';
}

// ─── HIT TEST ───
function hitTest(sx,sy){
  const active=[...allDots].filter(d=>filteredSet.has(d.mp.id));
  let best=null,bestD=18;
  active.sort((a,b)=>b.mp.total-a.mp.total).forEach(d=>{
    const {sx:dx,sy:dy}=worldToScreen(d.wx,d.wy);
    const dist=Math.sqrt((sx-dx)**2+(sy-dy)**2);
    const hitR=Math.max(d.r*cam.scale*0.8+3,6);
    if(dist<hitR&&dist<bestD){bestD=dist;best=d;}
  });
  return best?.mp||null;
}

// ─── STATE ───
let S={state:null,party:null,gender:null,query:''};
let locked=null,hovered=null;

function filteredMPs(){
  return DATA.mps.filter(m=>{
    if(S.state&&m.state!==S.state)return false;
    if(S.party&&m.party!==S.party)return false;
    if(S.gender&&m.gender.toLowerCase()!==S.gender.toLowerCase())return false;
    if(S.query){
      const q=S.query.toLowerCase();
      return m.name.toLowerCase().includes(q)||m.state.toLowerCase().includes(q)||m.party.toLowerCase().includes(q);
    }
    return true;
  });
}

// ─── RANKING UPDATE ───
let rankAnimFrame=null;
function updateRanking(mp){
  // Compute ranking from: locked MP > filter context > all
  let label,shares;

  if(mp){
    label=mp.name;
    shares=mp.s;
  } else {
    const fps=filteredMPs();
    if(fps.length===0){label='(no MPs)';shares=DATA.avg;}
    else if(fps.length===DATA.mps.length){label='All '+DATA.total_mps+' MPs';}
    else if(S.state){label=S.state;}
    else if(S.party){label=S.party+' MPs ('+fps.length+')';}
    else label=fps.length+' MPs (filtered)';

    // Average shares for this filtered set
    shares={};
    DATA.sectors.forEach(s=>{
      const vals=fps.map(m=>m.s[s]||0);
      shares[s]=vals.length?vals.reduce((a,b)=>a+b,0)/vals.length:0;
    });
  }

  document.getElementById('rank-context').textContent=label;

  // Sort sectors by value
  const ranked=DATA.sectors.map(s=>({s,v:shares[s]||0})).sort((a,b)=>b.v-a.v);
  const maxV=ranked[0]?.v||1;

  const list=document.getElementById('rank-list');
  // Animate: if items already exist, animate their positions
  const existing={};
  list.querySelectorAll('.rank-item').forEach(el=>{ existing[el.dataset.sec]=el; });

  // Remove items no longer needed
  Object.keys(existing).forEach(k=>{
    if(!ranked.find(r=>r.s===k)) existing[k].remove();
  });

  ranked.forEach(({s,v},i){
    const name=DATA.labels[s]||s;
    const pct=v.toFixed(1);
    const barW=Math.round((v/maxV)*100);
    const cls='rank-item'+(i===0?' top1':i===1?' top2':i===2?' top3':'');
    const numCls='rank-num'+(i<3?' top':'');

    let el=existing[s];
    if(!el){
      el=document.createElement('div');
      el.className=cls;
      el.dataset.sec=s;
      el.innerHTML=`<span class="${numCls}">${i+1}</span><div class="rank-bar-wrap"><div class="rank-bar" style="width:0%"></div></div><span class="rank-name" title="${name}">${name}</span><span class="rank-val">${pct}%</span>`;
      list.appendChild(el);
    } else {
      el.className=cls;
      el.querySelector('.rank-num').className=numCls;
      el.querySelector('.rank-num').textContent=i+1;
      el.querySelector('.rank-name').textContent=name;
      el.querySelector('.rank-val').textContent=pct+'%';
    }
    // Animate bar
    const bar=el.querySelector('.rank-bar');
    requestAnimationFrame(()=>{ bar.style.width=barW+'%'; });

    // Move to correct position
    list.appendChild(el);
  });
}

// ─── MP CARD ───
function showMPCard(mp,lock){
  const card=document.getElementById('mp-card');
  if(!mp){card.className='hidden';return;}
  card.className='';
  const imgUrl=MP_IMGS[mp.id];
  const col=pc(mp.party);
  const init=mp.name.split(' ').slice(0,2).map(w=>w[0]).join('');
  const topSecs=DATA.sectors.map(s=>({s,v:mp.s[s]||0})).sort((a,b)=>b.v-a.v).slice(0,4);

  card.innerHTML=`
    <div class="mp-top">
      <div class="mp-img-wrap">
        ${imgUrl?`<img class="mp-img" src="${imgUrl}" alt="" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'"><div class="mp-init" style="display:none">${init}</div>`:`<div class="mp-init">${init}</div>`}
      </div>
      <div class="mp-info">
        <div class="mp-name">${mp.name}</div>
        <div class="mp-meta">${mp.constituency}</div>
        <div class="mp-meta">${mp.state}</div>
        <div class="mp-badge" style="background:${col}22;color:${col};border:1px solid ${col}44">${mp.party} · ${mp.gender}</div>
      </div>
    </div>
    <div class="mp-qs">${mp.total.toLocaleString()} questions total</div>
    ${lock?'<div class="unlock-hint" id="unlock-hint">Click dot or here to unlock ↑</div>':''}
  `;
  if(lock){
    document.getElementById('unlock-hint').onclick=()=>{
      locked=null;hovered=null;
      showMPCard(null,false);
      updateRanking(null);
      draw();
    };
  }
}

// ─── TOOLTIP ───
const tt=document.getElementById('tt');
function showTT(mp,x,y){
  const imgUrl=MP_IMGS[mp.id];
  const col=pc(mp.party);
  const init=mp.name.split(' ').slice(0,2).map(w=>w[0]).join('');
  const topSecs=DATA.sectors.map(s=>({s,v:mp.s[s]||0})).sort((a,b)=>b.v-a.v).slice(0,3);

  tt.innerHTML=`
    ${imgUrl?`<img class="tt-photo" src="${imgUrl}" alt="" onerror="this.style.display='none'">`:`<div class="tt-init">${init}</div>`}
    <div class="tt-body">
      <div class="tt-name">${mp.name}</div>
      <div class="tt-sub">${mp.constituency} · ${mp.state}</div>
      <span class="tt-badge" style="background:${col}22;color:${col};border:1px solid ${col}44">${mp.party}</span>
      <div class="tt-qs">${mp.total.toLocaleString()} questions asked</div>
      <div class="tt-top-label">Top sectors</div>
      ${topSecs.map(({s,v})=>`<div class="tt-sec-row"><span class="tt-sec-n">${DATA.labels[s]||s}</span><span class="tt-sec-v">${v.toFixed(1)}%</span></div>`).join('')}
    </div>`;

  const tw=tt.offsetWidth,th=tt.offsetHeight;
  tt.style.left=Math.min(x+14,window.innerWidth-tw-8)+'px';
  tt.style.top=Math.min(y+12,window.innerHeight-th-8)+'px';
  tt.classList.add('show');
}
function hideTT(){tt.classList.remove('show');}

// ─── CANVAS EVENTS ───
let drag=null;
canvas.addEventListener('wheel',e=>{
  e.preventDefault();
  const rect=canvas.getBoundingClientRect();
  const cx=e.clientX-rect.left, cy=e.clientY-rect.top;
  const factor=e.deltaY<0?1.15:1/1.15;
  zoom(factor,cx,cy);
},{passive:false});

canvas.addEventListener('mousedown',e=>{
  drag={sx:e.clientX,sy:e.clientY,ox:cam.ox,oy:cam.oy};
  canvas.classList.add('grabbing');
});
window.addEventListener('mousemove',e=>{
  if(drag){
    cam.ox=drag.ox+(e.clientX-drag.sx);
    cam.oy=drag.oy+(e.clientY-drag.sy);
    draw();
    return;
  }
  const rect=canvas.getBoundingClientRect();
  const mp=hitTest(e.clientX-rect.left,e.clientY-rect.top);
  if(mp){
    canvas.style.cursor='pointer';
    hovered=mp;
    showTT(mp,e.clientX,e.clientY);
    if(!locked){updateRanking(mp);showMPCard(mp,false);}
    draw();
  } else {
    canvas.style.cursor=drag?'grabbing':'grab';
    hideTT();
    if(!locked){
      if(hovered){hovered=null;updateRanking(null);showMPCard(null,false);draw();}
    }
  }
});
window.addEventListener('mouseup',e=>{
  if(drag){
    const moved=Math.abs(e.clientX-drag.sx)+Math.abs(e.clientY-drag.sy);
    drag=null;
    canvas.classList.remove('grabbing');
    if(moved<4){
      // treat as click
      const rect=canvas.getBoundingClientRect();
      const mp=hitTest(e.clientX-rect.left,e.clientY-rect.top);
      if(mp){
        locked=locked?.id===mp.id?null:mp;
        hovered=mp;
        updateRanking(locked||mp);
        showMPCard(locked||mp,!!locked);
      } else {
        locked=null;hovered=null;
        updateRanking(null);showMPCard(null,false);
      }
      draw();
    }
  }
});
canvas.addEventListener('mouseleave',()=>{
  hideTT();
  if(!locked){hovered=null;updateRanking(null);showMPCard(null,false);draw();}
});

// Touch zoom
let lastTouchDist=null;
canvas.addEventListener('touchstart',e=>{if(e.touches.length===2)lastTouchDist=Math.hypot(e.touches[0].clientX-e.touches[1].clientX,e.touches[0].clientY-e.touches[1].clientY);},{passive:true});
canvas.addEventListener('touchmove',e=>{
  if(e.touches.length===2){
    const d=Math.hypot(e.touches[0].clientX-e.touches[1].clientX,e.touches[0].clientY-e.touches[1].clientY);
    if(lastTouchDist){const cx=(e.touches[0].clientX+e.touches[1].clientX)/2,cy=(e.touches[0].clientY+e.touches[1].clientY)/2;zoom(d/lastTouchDist,cx,cy);}
    lastTouchDist=d;
  }
},{passive:true});

// Zoom buttons
document.getElementById('z-in').onclick=()=>zoom(1.4,W/2,H/2);
document.getElementById('z-out').onclick=()=>zoom(1/1.4,W/2,H/2);
document.getElementById('z-reset').onclick=()=>{computeDots();draw();};

// ─── FILTERS ───
const TOP_STATES=DATA.state_order.slice(0,10);
const PARTIES=['BJP','INC','DMK','YSRCP','AITC','SS','JD(U)','BJD','BSP','BRS'];

function buildFilters(){
  // State
  const spEl=document.getElementById('p-state');
  spEl.innerHTML='';
  ['All',...TOP_STATES].forEach(st=>{
    const p=mk('span','pill'+(S.state===null&&st==='All'?' on':S.state===st?' on':''));
    p.textContent=st==='All'?'All':st.replace(' Pradesh','P.').replace('Tamil Nadu','TN').replace('West Bengal','WB').replace('Uttar','UP').replace(' Pradesh','');
    p.title=st;
    p.onclick=()=>{S.state=st==='All'?null:st;locked=null;hovered=null;refresh();};
    spEl.appendChild(p);
  });

  // Party
  const ppEl=document.getElementById('p-party');
  ppEl.innerHTML='';
  ['All',...PARTIES].forEach(pt=>{
    const on=S.party===null&&pt==='All'||S.party===pt;
    const p=mk('span','pill'+(on?' on':'')+(on&&pt!=='All'?' party-on':''));
    if(on&&pt!=='All'){p.style.background=pc(pt);p.style.borderColor=pc(pt);p.style.color='#fff';}
    p.textContent=pt;
    p.onclick=()=>{S.party=pt==='All'?null:pt;locked=null;hovered=null;refresh();};
    ppEl.appendChild(p);
  });

  // Gender
  const gpEl=document.getElementById('p-gender');
  gpEl.innerHTML='';
  ['All','Male','Female'].forEach(g=>{
    const p=mk('span','pill'+(S.gender===null&&g==='All'?' on':S.gender===g?' on':''));
    p.textContent=g;
    p.onclick=()=>{S.gender=g==='All'?null:g;locked=null;hovered=null;refresh();};
    gpEl.appendChild(p);
  });
}

function mk(t,c){const e=document.createElement(t);e.className=c;return e;}

document.getElementById('srch').addEventListener('input',e=>{
  S.query=e.target.value.trim();locked=null;hovered=null;refresh();
});

// ─── REFRESH ───
function refresh(){
  const fps=filteredMPs();
  filteredSet=new Set(fps.map(m=>m.id));
  document.getElementById('hdr-count').textContent=fps.length+' MPs';
  buildFilters();
  updateRanking(null);
  showMPCard(null,false);
  draw();
}

// ─── RESIZE ───
let rt;
window.addEventListener('resize',()=>{
  clearTimeout(rt);
  rt=setTimeout(()=>{resizeCanvas();computeDots();draw();},120);
});

// ─── INIT ───
resizeCanvas();
computeDots();
filteredSet=new Set(DATA.mps.map(m=>m.id));
buildFilters();
updateRanking(null);
draw();
</script>
</body>
</html>"""

# Inject data
HTML = HTML.replace('__DATA__', data_str)
HTML = HTML.replace('__IMGS__', imgs_str)

with open('/Users/aashima/Desktop/DataViz5/outcome/loksabha-questions/viz_v3.html', 'w') as f:
    f.write(HTML)

print(f"Written viz_v3.html: {len(HTML)//1024} KB")
print(f"Has DATA: {'const DATA =' in HTML}")
print(f"Has MP_IMGS: {'const MP_IMGS =' in HTML}")
brace_o=HTML.count('{'); brace_c=HTML.count('}')
print(f"Braces: {brace_o} open, {brace_c} close — {'OK' if brace_o==brace_c else 'MISMATCH'}")
paren_o=HTML.count('('); paren_c=HTML.count(')')
print(f"Parens: {paren_o} open, {paren_c} close — {'OK' if paren_o==paren_c else 'MISMATCH'}")
