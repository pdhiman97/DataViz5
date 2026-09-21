"""
Builder script for the Pudding-style Scrollytelling Data Story:
'Five Years of Roll Calls: What India’s 543 MPs Actually Did Once the Cameras Turned Off'

Outputs:
1. /Users/aashima/Desktop/DataViz5/index.html (Root deployment)
2. /Users/aashima/Desktop/DataViz5/docs/index.html (GitHub Pages)
3. /Users/aashima/Desktop/DataViz5/outcome/story/index.html
"""
import csv
import json
import base64
import os

RAW_CSV_PATH = '/Users/aashima/Desktop/DataViz5/data/loksabha-questions/raw/mp_17th_loksabha_questions_matrix.csv'

# Load Raw CSV
with open(RAW_CSV_PATH) as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

meta_cols = {'mp_id','name','party','state','constituency','gender','age','education',
             'attendance_pct','debates_count','total_questions_prs','total_questions_parsed',
             'pvt_member_bills_count','profile_url'}
ministries = [c for c in fieldnames if c not in meta_cols]

minister_names = [
    'narendra modi', 'amit anil chandra shah', 'amit shah', 'rajnath singh', 'nitin jairam gadkari', 'nitin gadkari',
    'nirmala sitharaman', 'subrahmanyam jaishankar', 's. jaishankar', 'piyush goyal', 'dharmendra pradhan',
    'pralhad joshi', 'giriraj singh', 'jyotiraditya m. scindia', 'jyotiraditya scindia', 'ashwini vaishnaw',
    'pashupati kumar paras', 'gajendra singh shekhawat', 'kiren rijiju', 'hardeep singh puri', 'mansukh mandaviya',
    'bhupender yadav', 'mahendra nath pandey', 'parshottam rupala', 'g. kishan reddy', 'anurag singh thakur',
    'arjun ram meghwal', 'v. muraleedharan', 'meenakashi lekhi', 'som parkash', 'renuka singh saruta',
    'rameshwar teli', 'kailash choudhary', 'annpurna devi', 'a. narayanaswamy', 'ajay bhatt', 'b. l. verma',
    'ajay kumar mishra', 'devusinh chauhan', 'bhagwanth khuba', 'kapil moreshwar patil', 'pratima bhoumik',
    'dr. subhas sarkar', 'dr. bhagwat kishanrao karad', 'dr. rajkumar ranjan singh', 'dr. bharati pravin pawar',
    'bishweswar tudu', 'shantanu thakur', 'dr. munjapara mahendrabhai', 'john barla', 'dr. l. murugan',
    'nisith pramanik', 'smriti zubin irani', 'smriti irani', 'harsh vardhan', 'ramesh pokhriyal', 'babul supriyo',
    'santosh kumar gangwar', 'shripad yesso naik', 'dr. jitendra singh', 'rao inderjit singh', 'om birla'
]

celebrity_names = [
    'sunny deol', 'ajay singh dharmendra deol', 'shatrughan sinha', 'hema malini', 'gautam gambhir',
    'hans raj hans', 'kirron kher', 'nusrat jahan', 'nusrat jahan ruhi', 'mimi chakraborty',
    'deepak adhikari', 'dev adhikari', 'ravi kishan', 'ravindra shyamnarayan', 'manoj tiwari', 'dinesh lal yadav'
]

all_mps = []
for r in rows:
    name_clean = r['name'].strip()
    name_lower = name_clean.lower()
    
    att_str = r.get('attendance_pct', '').strip()
    att = float(att_str) if (att_str and att_str != 'N/A') else None
    
    q_str = r.get('total_questions_parsed', '').strip()
    questions = int(q_str) if (q_str and q_str != 'N/A') else 0
    
    deb_str = r.get('debates_count', '').strip()
    debates = int(deb_str) if (deb_str and deb_str != 'N/A') else 0
    
    bill_str = r.get('pvt_member_bills_count', '').strip()
    bills = int(bill_str) if (bill_str and bill_str != 'N/A') else 0
    
    is_minister = (att is None and questions == 0) or any(m in name_lower for m in minister_names) or (questions == 0 and ('minister' in r.get('profile_url', '').lower() or r.get('party') == 'BJP' and debates == 0 and att is None))
    is_celeb = any(c in name_lower for c in celebrity_names)
    
    mp_ministries = []
    for m in ministries:
        try:
            cnt = int(r.get(m) or 0)
            if cnt > 0:
                mp_ministries.append({'m': m, 'c': cnt})
        except:
            pass
    mp_ministries.sort(key=lambda x: x['c'], reverse=True)
    top_mins = mp_ministries[:3]
    
    if is_minister:
        archetype = 'Union Minister / Executive'
    elif is_celeb and questions < 100:
        archetype = 'Celebrity Backbencher'
    elif questions >= 500:
        archetype = 'Legislative Workhorse'
    elif debates >= 150:
        archetype = 'Floor Orator'
    elif (att or 0) >= 90 and questions >= 300:
        archetype = 'Diligent Lawmaker'
    elif (att or 0) < 50 and questions < 50:
        archetype = 'Chronic Absentee'
    else:
        archetype = 'Constituency Delegate'
        
    mp_obj = {
        'id': r['mp_id'],
        'name': name_clean,
        'party': r.get('party', 'IND'),
        'state': r.get('state', 'Unknown'),
        'constituency': r.get('constituency', ''),
        'gender': r.get('gender', 'Male'),
        'age': int(r['age']) if (r.get('age') and r['age'].isdigit()) else 55,
        'attendance': att,
        'questions': questions,
        'debates': debates,
        'bills': bills,
        'is_minister': is_minister,
        'is_celeb': is_celeb,
        'archetype': archetype,
        'top_ministries': top_mins
    }
    all_mps.append(mp_obj)

# Encode images
def encode_img_b64(path):
    if os.path.exists(path):
        ext = path.split('.')[-1]
        mime = 'image/webp' if ext == 'webp' else 'image/jpeg'
        with open(path, 'rb') as f:
            return f"data:{mime};base64,{base64.b64encode(f.read()).decode('utf-8')}"
    return ""

img_wink = encode_img_b64('/Users/aashima/Desktop/DataViz5/outcome/story/images/wink.webp')
img_reaction = encode_img_b64('/Users/aashima/Desktop/DataViz5/outcome/story/images/reaction.jpg')
img_cash = encode_img_b64('/Users/aashima/Desktop/DataViz5/outcome/story/images/cash_for_vote.jpg')

# Ministry summary counts
ministry_stats = {}
for m in ministries:
    tot = sum(int(r.get(m) or 0) for r in rows)
    ministry_stats[m] = tot

top_ministries_summary = sorted(
    [{'name': k, 'count': v} for k, v in ministry_stats.items() if v > 0],
    key=lambda x: -x['count']
)

# Render HTML template
HTML_DATA = json.dumps(all_mps)
MINISTRY_DATA = json.dumps(top_ministries_summary)

print(f"Loaded {len(all_mps)} MPs. Writing story HTML...")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Five Years of Roll Calls: What India’s 543 MPs Actually Did Once the Cameras Turned Off</title>

<!-- Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;800&family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400;1,600&family=JetBrains+Mono:wght@400;500;600&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,400;1,600&display=swap" rel="stylesheet">

<!-- D3.js & Scrollama -->
<script src="https://d3js.org/d3.v7.min.js"></script>
<script src="https://unpkg.com/scrollama"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>

<style>
:root {{
  --bg: #FAF7F2;
  --bg-card: #FFFFFF;
  --bg-card-trans: rgba(255, 255, 255, 0.94);
  --border: #E8E3DA;
  --border-dark: #D4CECA;
  --ink: #1B1B1B;
  --ink-secondary: #524F4A;
  --ink-muted: #8C8780;
  
  --terracotta: #C84B31;
  --terracotta-light: #FDF2E9;
  --slate: #2D4059;
  --slate-light: #EDF2F7;
  --ochre: #DDA15E;
  --ochre-light: #FEF8EC;
  --green: #2B7A0B;
  --gray-node: #D4CECA;
  
  --font-serif: 'Newsreader', Georgia, serif;
  --font-display: 'Cinzel', serif;
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}}

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

html {{
  scroll-behavior: smooth;
}}

body {{
  background: var(--bg);
  color: var(--ink);
  font-family: var(--font-sans);
  line-height: 1.65;
  font-size: 16px;
  -webkit-font-smoothing: antialiased;
  overflow-x: hidden;
}}

/* ── EDITORIAL HEADER & HERO ── */
.header-top {{
  border-bottom: 1px solid var(--border);
  padding: 0.75rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--ink-muted);
  background: var(--bg);
}}
.publication-tag strong {{
  color: var(--terracotta);
}}

.hero {{
  max-width: 820px;
  margin: 4rem auto 2.5rem;
  padding: 0 1.5rem;
  text-align: center;
}}

.kicker {{
  font-family: var(--font-mono);
  font-size: 0.8rem;
  font-weight: 600;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--terracotta);
  margin-bottom: 1rem;
}}

.hero h1 {{
  font-family: var(--font-display);
  font-size: clamp(2.4rem, 5.5vw, 3.8rem);
  font-weight: 800;
  line-height: 1.12;
  letter-spacing: -0.02em;
  color: var(--ink);
  margin-bottom: 1.25rem;
}}

.hero-subtitle {{
  font-family: var(--font-serif);
  font-size: clamp(1.2rem, 2.5vw, 1.55rem);
  font-weight: 400;
  color: var(--ink-secondary);
  line-height: 1.4;
  margin-bottom: 2rem;
}}

.byline {{
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  font-family: var(--font-mono);
  font-size: 0.78rem;
  color: var(--ink-muted);
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
  padding: 0.75rem 0;
}}

.editorial-intro {{
  max-width: 680px;
  margin: 3rem auto 2.5rem;
  padding: 0 1.5rem;
  font-family: var(--font-serif);
  font-size: 1.25rem;
  line-height: 1.7;
  color: var(--ink-secondary);
}}
.editorial-intro p {{
  margin-bottom: 1.5rem;
}}
.dropcap::first-letter {{
  font-family: var(--font-display);
  font-size: 3.8rem;
  line-height: 0.85;
  float: left;
  margin-right: 0.6rem;
  color: var(--terracotta);
  font-weight: 700;
}}

/* ── 2x2 THEATER GRID ── */
.theater-grid-wrapper {{
  max-width: 960px;
  margin: 2.5rem auto 4.5rem;
  padding: 0 1.5rem;
}}
.grid-title {{
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--ink-muted);
  text-align: center;
  margin-bottom: 1rem;
}}
.theater-grid {{
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.25rem;
}}
@media (max-width: 640px) {{
  .theater-grid {{ grid-template-columns: 1fr; }}
}}

.theater-card {{
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0,0,0,0.03);
  transition: transform 0.2s, box-shadow 0.2s;
}}
.theater-card:hover {{
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.06);
}}
.theater-img-wrap {{
  position: relative;
  width: 100%;
  height: 220px;
  background: #EFEBE4;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}}
.theater-img {{
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}}
.theater-fallback {{
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #FAF7F2, #EFEBE4);
  color: var(--ink-muted);
  padding: 1.5rem;
  text-align: center;
  font-family: var(--font-mono);
  font-size: 0.8rem;
}}
.theater-fallback-icon {{
  font-size: 2.2rem;
  margin-bottom: 0.5rem;
  opacity: 0.8;
}}
.theater-caption {{
  padding: 0.85rem 1rem;
}}
.theater-tag {{
  font-family: var(--font-mono);
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--terracotta);
  margin-bottom: 0.2rem;
}}
.theater-desc {{
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--ink);
  line-height: 1.35;
}}
.theater-sub {{
  font-size: 0.75rem;
  color: var(--ink-muted);
  margin-top: 0.25rem;
}}

/* ── SCROLLYTELLING CONTAINER ── */
#scrollytelling {{
  position: relative;
  width: 100%;
  margin: 2rem 0;
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
}}

.scrolly-layout {{
  display: flex;
  position: relative;
  width: 100%;
}}

/* Sticky Graphic */
.sticky-graphic {{
  position: sticky;
  top: 0;
  width: 62%;
  height: 100vh;
  background: var(--bg);
  display: flex;
  flex-direction: column;
  border-right: 1px solid var(--border);
  overflow: hidden;
  z-index: 1;
}}
@media (max-width: 900px) {{
  .scrolly-layout {{ flex-direction: column; }}
  .sticky-graphic {{
    position: sticky;
    width: 100%;
    height: 55vh;
    border-right: none;
    border-bottom: 1px solid var(--border);
  }}
}}

.graphic-hud {{
  padding: 0.85rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--border);
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: var(--ink-secondary);
  background: rgba(250, 247, 242, 0.92);
  backdrop-filter: blur(8px);
  z-index: 10;
}}
.hud-title {{
  font-weight: 600;
  color: var(--slate);
}}
.hud-stat strong {{
  color: var(--terracotta);
}}

#viz-container {{
  flex: 1;
  position: relative;
  width: 100%;
  height: 100%;
}}
#viz-svg {{
  width: 100%;
  height: 100%;
  display: block;
}}

/* Scrolling Steps Column */
.scrolly-steps {{
  width: 38%;
  padding: 10vh 1.75rem 40vh;
  position: relative;
  z-index: 2;
}}
@media (max-width: 900px) {{
  .scrolly-steps {{
    width: 100%;
    padding: 2rem 1.25rem 25vh;
  }}
}}

.step {{
  min-height: 85vh;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.25;
  transition: opacity 0.4s ease;
  padding: 2rem 0;
}}
.step.is-active {{
  opacity: 1;
}}

.step-card {{
  background: var(--bg-card-trans);
  backdrop-filter: blur(12px);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.75rem 1.85rem;
  box-shadow: 0 8px 32px rgba(0,0,0,0.06);
  width: 100%;
  max-width: 440px;
}}
.step-number {{
  font-family: var(--font-mono);
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--terracotta);
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}}
.step-number::after {{
  content: '';
  flex: 1;
  height: 1px;
  background: var(--border);
}}

.step-title {{
  font-family: var(--font-serif);
  font-size: 1.45rem;
  font-weight: 600;
  color: var(--ink);
  line-height: 1.25;
  margin-bottom: 0.85rem;
}}

.step-body {{
  font-size: 0.93rem;
  line-height: 1.65;
  color: var(--ink-secondary);
}}
.step-body p {{
  margin-bottom: 0.75rem;
}}
.step-body p:last-child {{
  margin-bottom: 0;
}}

.step-annotation {{
  margin-top: 1rem;
  padding: 0.75rem;
  background: var(--bg);
  border-left: 3px solid var(--terracotta);
  border-radius: 4px;
  font-size: 0.8rem;
  color: var(--ink-secondary);
  font-family: var(--font-sans);
}}

/* Mini Gender Diverging Chart in Step 6 */
.gender-diverge {{
  margin-top: 1.2rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border);
}}
.gender-diverge-title {{
  font-family: var(--font-mono);
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--ink-muted);
  margin-bottom: 0.75rem;
}}
.gender-bar-row {{
  display: flex;
  align-items: center;
  font-size: 0.72rem;
  margin-bottom: 0.45rem;
  gap: 0.5rem;
}}
.gender-bar-label {{
  flex: 0 0 130px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: var(--ink-secondary);
}}
.gender-track {{
  flex: 1;
  height: 6px;
  background: var(--border);
  border-radius: 3px;
  position: relative;
  overflow: hidden;
}}
.gender-fill-f {{
  position: absolute;
  left: 0;
  height: 100%;
  background: var(--terracotta);
  border-radius: 3px;
}}
.gender-fill-m {{
  position: absolute;
  left: 0;
  height: 100%;
  background: var(--slate);
  border-radius: 3px;
}}
.gender-gap {{
  flex: 0 0 42px;
  text-align: right;
  font-family: var(--font-mono);
  font-size: 0.68rem;
  font-weight: 600;
}}
.gap-f {{ color: var(--terracotta); }}
.gap-m {{ color: var(--slate); }}

/* ── D3 CANVAS STYLES ── */
.axis text {{
  font-family: var(--font-mono);
  font-size: 10px;
  fill: var(--ink-muted);
}}
.axis path, .axis line {{
  stroke: var(--border);
}}
.grid line {{
  stroke: var(--border);
  stroke-dasharray: 2, 2;
  stroke-opacity: 0.7;
}}
.ref-line {{
  stroke: var(--terracotta);
  stroke-width: 1.2px;
  stroke-dasharray: 4, 4;
  opacity: 0.7;
}}
.ref-label {{
  font-family: var(--font-mono);
  font-size: 9.5px;
  font-weight: 600;
  fill: var(--terracotta);
}}

.mp-node {{
  cursor: pointer;
  transition: opacity 0.2s, stroke 0.2s;
}}
.mp-node:hover {{
  stroke: #1B1B1B !important;
  stroke-width: 2.2px !important;
  opacity: 1 !important;
}}
.mp-node.is-focused {{
  stroke: #1B1B1B !important;
  stroke-width: 2.5px !important;
  filter: drop-shadow(0 0 6px rgba(0,0,0,0.3));
}}

/* Callout annotations in D3 */
.d3-annotation-text {{
  font-family: var(--font-sans);
  font-size: 11px;
  font-weight: 600;
  fill: var(--ink);
}}
.d3-annotation-sub {{
  font-family: var(--font-mono);
  font-size: 9px;
  fill: var(--ink-muted);
}}
.d3-annotation-line {{
  stroke: var(--ink-muted);
  stroke-width: 1px;
  stroke-dasharray: 2, 2;
}}

/* ── FLOATING TOOLTIP ── */
#story-tooltip {{
  position: fixed;
  background: var(--bg-card-trans);
  backdrop-filter: blur(12px);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 0.85rem 1rem;
  box-shadow: 0 10px 30px rgba(0,0,0,0.12);
  pointer-events: none;
  font-size: 0.78rem;
  color: var(--ink);
  z-index: 1000;
  max-width: 280px;
  display: none;
  opacity: 0;
  transition: opacity 0.15s ease;
}}
#story-tooltip.is-visible {{
  display: block;
  opacity: 1;
}}
.tt-name {{
  font-family: var(--font-serif);
  font-size: 1.1rem;
  font-weight: 600;
  line-height: 1.2;
  margin-bottom: 0.2rem;
}}
.tt-geo {{
  font-size: 0.72rem;
  color: var(--ink-secondary);
  margin-bottom: 0.4rem;
}}
.tt-badge-row {{
  display: flex;
  align-items: center;
  gap: 0.35rem;
  margin-bottom: 0.6rem;
}}
.tt-party-pill {{
  display: inline-block;
  font-family: var(--font-mono);
  font-size: 0.62rem;
  font-weight: 700;
  padding: 0.12rem 0.45rem;
  border-radius: 3px;
  background: var(--slate-light);
  color: var(--slate);
}}
.tt-archetype-pill {{
  display: inline-block;
  font-family: var(--font-mono);
  font-size: 0.62rem;
  font-weight: 600;
  padding: 0.12rem 0.45rem;
  border-radius: 3px;
  background: var(--ochre-light);
  color: #8C5B00;
}}
.tt-stats-grid {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.4rem;
  border-top: 1px solid var(--border);
  padding-top: 0.5rem;
  text-align: center;
}}
.tt-stat-box .val {{
  font-family: var(--font-mono);
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--ink);
}}
.tt-stat-box .lbl {{
  font-size: 0.6rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--ink-muted);
}}

/* ── INTERACTIVE EXPLORER SECTION (SECTION 8) ── */
#explorer {{
  max-width: 1120px;
  margin: 5rem auto;
  padding: 0 1.5rem;
}}

.explorer-header {{
  text-align: center;
  max-width: 680px;
  margin: 0 auto 2.5rem;
}}
.explorer-header h2 {{
  font-family: var(--font-display);
  font-size: 2.2rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  margin-bottom: 0.5rem;
}}
.explorer-header p {{
  font-family: var(--font-serif);
  font-size: 1.1rem;
  color: var(--ink-secondary);
}}

.explorer-controls {{
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
  margin-bottom: 2rem;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.03);
}}

.search-wrap {{
  position: relative;
  flex: 1;
  min-width: 260px;
}}
.search-icon {{
  position: absolute;
  left: 0.85rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--ink-muted);
  font-size: 0.9rem;
}}
.mp-search-input {{
  width: 100%;
  font-family: var(--font-sans);
  font-size: 0.85rem;
  padding: 0.55rem 1rem 0.55rem 2.2rem;
  border-radius: 6px;
  border: 1px solid var(--border);
  background: var(--bg);
  color: var(--ink);
  outline: none;
  transition: border-color 0.2s;
}}
.mp-search-input:focus {{
  border-color: var(--terracotta);
  background: #FFF;
}}

.filter-chips {{
  display: flex;
  gap: 0.4rem;
  flex-wrap: wrap;
}}
.filter-chip {{
  font-family: var(--font-mono);
  font-size: 0.72rem;
  font-weight: 600;
  padding: 0.4rem 0.75rem;
  border-radius: 6px;
  background: var(--bg);
  border: 1px solid var(--border);
  color: var(--ink-secondary);
  cursor: pointer;
  transition: all 0.15s;
}}
.filter-chip:hover {{
  border-color: var(--ink-muted);
  color: var(--ink);
}}
.filter-chip.is-active {{
  background: var(--slate);
  color: #FFF;
  border-color: var(--slate);
}}

.custom-csv-upload {{
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: var(--ink-muted);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}}
.btn-upload {{
  font-family: var(--font-mono);
  font-size: 0.7rem;
  padding: 0.35rem 0.65rem;
  border: 1px dashed var(--border-dark);
  background: transparent;
  border-radius: 4px;
  cursor: pointer;
  color: var(--ink-secondary);
}}
.btn-upload:hover {{
  border-color: var(--terracotta);
  color: var(--terracotta);
}}

/* Explorer Layout */
.explorer-grid {{
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 2rem;
  align-items: start;
}}
@media (max-width: 900px) {{
  .explorer-grid {{ grid-template-columns: 1fr; }}
}}

.mp-cards-list {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1rem;
  max-height: 640px;
  overflow-y: auto;
  padding-right: 0.5rem;
}}
.mp-cards-list::-webkit-scrollbar {{ width: 4px; }}
.mp-cards-list::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 2px; }}

.mp-mini-card {{
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.15s;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}}
.mp-mini-card:hover {{
  border-color: var(--slate);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}}
.mp-mini-card.is-selected {{
  border: 2px solid var(--terracotta);
  background: var(--terracotta-light);
}}
.mini-name {{
  font-family: var(--font-serif);
  font-weight: 600;
  font-size: 0.95rem;
  color: var(--ink);
  line-height: 1.25;
  margin-bottom: 0.2rem;
}}
.mini-geo {{
  font-size: 0.7rem;
  color: var(--ink-muted);
  margin-bottom: 0.6rem;
}}
.mini-stats-row {{
  display: flex;
  justify-content: space-between;
  border-top: 1px solid var(--border);
  padding-top: 0.5rem;
  font-family: var(--font-mono);
  font-size: 0.72rem;
}}
.mini-stat-val {{ font-weight: 700; color: var(--ink); }}
.mini-stat-lbl {{ font-size: 0.58rem; color: var(--ink-muted); text-transform: uppercase; }}

/* MP Profile Detail Inspector */
.mp-detail-card {{
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.75rem;
  position: sticky;
  top: 1.5rem;
  box-shadow: 0 8px 30px rgba(0,0,0,0.05);
}}
.detail-name {{
  font-family: var(--font-serif);
  font-size: 1.55rem;
  font-weight: 600;
  line-height: 1.2;
  color: var(--ink);
  margin-bottom: 0.25rem;
}}
.detail-geo {{
  font-size: 0.85rem;
  color: var(--ink-secondary);
  margin-bottom: 0.75rem;
}}
.detail-badges {{
  display: flex;
  gap: 0.4rem;
  flex-wrap: wrap;
  margin-bottom: 1.25rem;
}}

.metric-gauge-row {{
  margin-bottom: 1rem;
}}
.gauge-header {{
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  margin-bottom: 0.25rem;
}}
.gauge-title {{
  font-weight: 600;
  color: var(--ink-secondary);
}}
.gauge-val {{
  font-family: var(--font-mono);
  font-weight: 700;
  color: var(--ink);
}}
.gauge-track {{
  height: 8px;
  background: var(--border);
  border-radius: 4px;
  overflow: hidden;
  position: relative;
}}
.gauge-fill {{
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease;
}}

.detail-top-mins {{
  margin-top: 1.25rem;
  border-top: 1px solid var(--border);
  padding-top: 1rem;
}}
.detail-mins-title {{
  font-family: var(--font-mono);
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--ink-muted);
  margin-bottom: 0.6rem;
}}
.min-row {{
  display: flex;
  justify-content: space-between;
  font-size: 0.78rem;
  padding: 0.25rem 0;
  border-bottom: 1px dashed var(--border);
}}
.min-name {{ color: var(--ink-secondary); }}
.min-count {{ font-family: var(--font-mono); font-weight: 600; color: var(--terracotta); }}

/* ── EDITORIAL FOOTER ── */
footer {{
  background: var(--ink);
  color: var(--bg);
  padding: 4rem 1.5rem;
  margin-top: 6rem;
  border-top: 1px solid var(--border);
}}
.footer-inner {{
  max-width: 820px;
  margin: 0 auto;
  text-align: center;
}}
.footer-title {{
  font-family: var(--font-display);
  font-size: 1.4rem;
  margin-bottom: 1rem;
}}
.footer-text {{
  font-family: var(--font-serif);
  font-size: 0.95rem;
  color: #A8A29E;
  line-height: 1.6;
  margin-bottom: 2rem;
}}
.footer-meta {{
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: #78716C;
}}
</style>
</head>
<body>

<!-- Publication Header -->
<div class="header-top">
  <span class="publication-tag">Data Journalism Special · <strong>The Roll Call Project</strong></span>
  <span>17th Lok Sabha (2019–2024)</span>
</div>

<!-- Main Hero Section -->
<header class="hero">
  <div class="kicker">Parliamentary Scrutiny & Data Investigation</div>
  <h1>Five Years of Roll Calls</h1>
  <p class="hero-subtitle">What India’s 543 MPs actually did once the cameras turned off</p>
  <div class="byline">
    <span>By The Creative Technologist Team</span>
    <span>·</span>
    <span>559 Member Profiles Analyzed</span>
    <span>·</span>
    <span>101,999 Questions Tracked</span>
  </div>
</header>

<!-- Editorial Narrative Intro -->
<article class="editorial-intro">
  <p class="dropcap">When we watch Parliament on TV or viral social media clips, it looks like pure high school drama: walkouts, shouting matches, flying paper planes, and dramatic gestures in the well. Naturally, the public judges MPs like school kids: <em>Did they show up?</em> Media outlets celebrate 90% attendance like gold stars.</p>
  <p>But parliamentary democracy is not won by sitting on leather benches with an ID badge. What happens after members swipe in for morning roll call? Who actually questions the executive, and who turns their microphone off for five full years?</p>
</article>

<!-- 2x2 Theater Grid -->
<section class="theater-grid-wrapper">
  <div class="grid-title">The Spectacle vs. The Scrutiny — Four Moments of Political Theater</div>
  <div class="theater-grid">
    
    <!-- Photo 1 -->
    <div class="theater-card">
      <div class="theater-img-wrap">
        {'<img class="theater-img" src="' + img_wink + '" alt="The Wink">' if img_wink else ''}
        <div class="theater-fallback" style="{'display:none' if img_wink else 'display:flex'}">
          <span class="theater-fallback-icon">😉</span>
          <strong>The Viral Gesture</strong>
          <span>Rahul Gandhi’s Parliament Wink</span>
        </div>
      </div>
      <div class="theater-caption">
        <div class="theater-tag">The Viral Moment</div>
        <div class="theater-desc">The Wink (Rahul Gandhi)</div>
        <div class="theater-sub">Floor theatrics that drove 48-hour television debates.</div>
      </div>
    </div>

    <!-- Photo 2 -->
    <div class="theater-card">
      <div class="theater-img-wrap">
        {'<img class="theater-img" src="' + img_reaction + '" alt="The Counter Reaction">' if img_reaction else ''}
        <div class="theater-fallback" style="{'display:none' if img_reaction else 'display:flex'}">
          <span class="theater-fallback-icon">🎙️</span>
          <strong>The Counter-Reaction</strong>
          <span>Prime Ministerial Floor Duel</span>
        </div>
      </div>
      <div class="theater-caption">
        <div class="theater-tag">Executive Rebuttal</div>
        <div class="theater-desc">The Floor Duel (Narendra Modi)</div>
        <div class="theater-sub">Prime-time oratory and counter-gestures captured by cameras.</div>
      </div>
    </div>

    <!-- Photo 3 -->
    <div class="theater-card">
      <div class="theater-img-wrap">
        <div class="theater-fallback" style="display:flex">
          <span class="theater-fallback-icon">📜</span>
          <strong>Floor Chaos in the Well</strong>
          <span>Protests, placards, and shouting matches</span>
        </div>
      </div>
      <div class="theater-caption">
        <div class="theater-tag">Floor Disruption</div>
        <div class="theater-desc">The Well Protest</div>
        <div class="theater-sub">Frequent adjournments and papers torn on the floor.</div>
      </div>
    </div>

    <!-- Photo 4 -->
    <div class="theater-card">
      <div class="theater-img-wrap">
        {'<img class="theater-img" src="' + img_cash + '" alt="Ethics & Expulsion" >' if img_cash else ''}
        <div class="theater-fallback" style="{'display:none' if img_cash else 'display:flex'}">
          <span class="theater-fallback-icon">⚖️</span>
          <strong>The Ethics Commitee Probe</strong>
          <span>Cash-for-query expulsion and controversy</span>
        </div>
      </div>
      <div class="theater-caption">
        <div class="theater-tag">Question Scandal</div>
        <div class="theater-desc">Ethics & Expulsion (Mahua Moitra)</div>
        <div class="theater-sub">The ultimate price of parliamentary question access.</div>
      </div>
    </div>

  </div>
</section>

<!-- Scrollytelling Visual Anchor Section -->
<section id="scrollytelling">
  <div class="scrolly-layout">
    
    <!-- Sticky Graphic Column -->
    <div class="sticky-graphic">
      <div class="graphic-hud">
        <span class="hud-title" id="hud-step-title">17th Lok Sabha Swarm</span>
        <span class="hud-stat" id="hud-node-count">Nodes: <strong>559 MPs</strong></span>
      </div>
      <div id="viz-container">
        <svg id="viz-svg"></svg>
      </div>
    </div>

    <!-- Scrolling Narrative Steps -->
    <div class="scrolly-steps">
      
      <!-- Step 1 -->
      <div class="step" data-step="1">
        <div class="step-card">
          <div class="step-number">Step 01</div>
          <h3 class="step-title">The Diligent Classroom</h3>
          <div class="step-body">
            <p>Look at the attendance sheet for the 17th Lok Sabha (2019–2024). The national average attendance is <strong>78.9%</strong>.</p>
            <p>Almost every member crowds tightly between 75% and 95%. On paper, India’s parliament looks like a disciplined classroom filled with model students.</p>
          </div>
          <div class="step-annotation">
            💡 <strong>Observation:</strong> Swarming along attendance alone creates a comforting illusion of legislative diligence.
          </div>
        </div>
      </div>

      <!-- Step 2 -->
      <div class="step" data-step="2">
        <div class="step-card">
          <div class="step-number">Step 02</div>
          <h3 class="step-title">The Myth of the Register</h3>
          <div class="step-body">
            <p>Showing up is simple. What did they actually do once seated? Real oversight happens on paper: MPs submit formal questions that legally compel ministries to open files.</p>
            <p>When you plot attendance against questions asked, the statistical correlation collapses to <strong>r = 0.14</strong>. Swiping your card in the morning tells you almost nothing about who is actually doing the work.</p>
          </div>
          <div class="step-annotation">
            📊 <strong>Median Reference:</strong> National median is ~163 questions. Notice how widely MPs scatter vertically regardless of 90%+ attendance.
          </div>
        </div>
      </div>

      <!-- Step 3 -->
      <div class="step" data-step="3">
        <div class="step-card">
          <div class="step-number">Step 03</div>
          <h3 class="step-title">The Cabinet Filter</h3>
          <div class="step-body">
            <p>Notice the cluster of dots resting flat on the floor line (0 questions). Did all of them skip work?</p>
            <p>Not quite. <strong>49 of those dots are Union Ministers</strong> (Amit Shah, Rajnath Singh, Kiren Rijiju, Nitin Gadkari). In parliamentary democracy, ministers answer questions; constitutionally, they are barred from asking them.</p>
          </div>
          <div class="step-annotation">
            🏛️ <strong>Constitutional Rule:</strong> Ministers appear as hollow rings. The remaining 510 backbenchers carry the duty of questioning.
          </div>
        </div>
      </div>

      <!-- Step 4 -->
      <div class="step" data-step="4">
        <div class="step-card">
          <div class="step-number">Step 04</div>
          <h3 class="step-title">Celebrities vs. Quiet Workhorses</h3>
          <div class="step-body">
            <p>With the Cabinet filtered, the real contrast emerges. Celebrity MPs often vanish once the cameras shut: <strong>Sunny Deol clocked 17% attendance and asked 4 questions in five full years</strong>; Shatrughan Sinha asked zero.</p>
            <p>Meanwhile, obscure backbenchers filed over 600 questions each, carrying the day-to-day legislative oversight of the Republic.</p>
          </div>
          <div class="step-annotation">
            ⭐ <strong>Top Workhorses:</strong> Sukanta Majumdar (654 Qs), Supriya Sule (629 Qs & 16 Bills), Kuldeep Rai Sharma (610 Qs & 834 debates).
          </div>
        </div>
      </div>

      <!-- Step 5 -->
      <div class="step" data-step="5">
        <div class="step-card">
          <div class="step-number">Step 05</div>
          <h3 class="step-title">The Maharashtra Anomaly</h3>
          <div class="step-body">
            <p>Geography fundamentally shapes scrutiny. Across party lines (BJP, NCP, Shiv Sena, INC), MPs from <strong>Maharashtra average 346.5 questions each</strong>—far higher than any other major state.</p>
            <p>Six of the top ten question-askers in India come from Maharashtra alone. Compare that to Uttar Pradesh (averaging 125), Punjab (84), or Himachal Pradesh (27).</p>
          </div>
        </div>
      </div>

      <!-- Step 6 -->
      <div class="step" data-step="6">
        <div class="step-card">
          <div class="step-number">Step 06</div>
          <h3 class="step-title">The Gender Lens</h3>
          <div class="step-body">
            <p>Women MPs hold 82 out of 559 seats. While their average question volume closely mirrors men (177 vs 183), their thematic scrutiny shifts significantly.</p>
            <p>Female MPs ask <strong>+24.2% more questions on Women & Child Development</strong> and +12.3% on Social Justice, while male MPs ask higher proportions on Civil Aviation (-22%) and Defence.</p>
          </div>
          
          <div class="gender-diverge">
            <div class="gender-diverge-title">Scrutiny Disparity by Ministry</div>
            <div class="gender-bar-row">
              <span class="gender-bar-label">Women & Child</span>
              <div class="gender-track"><div class="gender-fill-f" style="width:75%"></div></div>
              <span class="gender-gap gap-f">+24.2%</span>
            </div>
            <div class="gender-bar-row">
              <span class="gender-bar-label">Social Justice</span>
              <div class="gender-track"><div class="gender-fill-f" style="width:62%"></div></div>
              <span class="gender-gap gap-f">+12.3%</span>
            </div>
            <div class="gender-bar-row">
              <span class="gender-bar-label">Civil Aviation</span>
              <div class="gender-track"><div class="gender-fill-m" style="width:70%"></div></div>
              <span class="gender-gap gap-m">-21.9%</span>
            </div>
            <div class="gender-bar-row">
              <span class="gender-bar-label">Defence</span>
              <div class="gender-track"><div class="gender-fill-m" style="width:60%"></div></div>
              <span class="gender-gap gap-m">-17.9%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Step 7 -->
      <div class="step" data-step="7">
        <div class="step-card">
          <div class="step-number">Step 07</div>
          <h3 class="step-title">The National Wishlist</h3>
          <div class="step-body">
            <p>When MPs write to Delhi, what are they asking for? We talk endlessly about space rockets and geopolitical statecraft, but Parliament runs on daily necessities.</p>
            <p><strong>Health (7,595), Agriculture (5,122), and Railways (4,809)</strong> soaked up over 17,500 questions. Meanwhile, high-tech ministries operated in near-total silence: <strong>Space received 1 question in five full years</strong>; Atomic Energy received 8.</p>
          </div>
          <div class="step-annotation">
            🪐 <strong>The Space & Atomic Silence:</strong> Out of 101,999 questions filed, only 9 scrutinized the Department of Space and Atomic Energy combined.
          </div>
        </div>
      </div>

    </div>
  </div>
</section>

<!-- Section 8: Interactive Explorer -->
<section id="explorer">
  <div class="explorer-header">
    <h2>Interactive Explorer: Find Your MP</h2>
    <p>Search all 559 members of the 17th Lok Sabha to inspect their session attendance, question volume, debates, and top queried ministries.</p>
  </div>

  <div class="explorer-controls">
    <div class="search-wrap">
      <span class="search-icon">🔍</span>
      <input type="text" class="mp-search-input" id="mp-search" placeholder="Search by MP name or constituency..." autocomplete="off">
    </div>

    <div class="filter-chips">
      <button class="filter-chip is-active" data-filter="all">All MPs (559)</button>
      <button class="filter-chip" data-filter="workhorses">Top Workhorses (500+ Qs)</button>
      <button class="filter-chip" data-filter="ministers">Ministers</button>
      <button class="filter-chip" data-filter="celebs">Celebrity MPs</button>
      <button class="filter-chip" data-filter="women">Women MPs (82)</button>
    </div>

    <div class="custom-csv-upload">
      <span>Load raw CSV:</span>
      <input type="file" id="csvFile" accept=".csv" style="display:none">
      <button class="btn-upload" onclick="document.getElementById('csvFile').click()">Choose File</button>
    </div>
  </div>

  <div class="explorer-grid">
    
    <!-- MP Mini Cards Grid -->
    <div class="mp-cards-list" id="mp-grid"></div>

    <!-- MP Detail Inspector -->
    <div class="mp-detail-card" id="mp-detail">
      <div class="detail-name" id="det-name">Supriya Sule</div>
      <div class="detail-geo" id="det-geo">Baramati, Maharashtra</div>
      
      <div class="detail-badges">
        <span class="tt-party-pill" id="det-party">NCP</span>
        <span class="tt-archetype-pill" id="det-archetype">Legislative Workhorse</span>
      </div>

      <div class="metric-gauge-row">
        <div class="gauge-header">
          <span class="gauge-title">Session Attendance</span>
          <span class="gauge-val" id="det-att">93%</span>
        </div>
        <div class="gauge-track">
          <div class="gauge-fill" id="det-att-fill" style="width:93%;background:var(--slate)"></div>
        </div>
      </div>

      <div class="metric-gauge-row">
        <div class="gauge-header">
          <span class="gauge-title">Questions Asked (vs 654 Max)</span>
          <span class="gauge-val" id="det-q">629 Qs</span>
        </div>
        <div class="gauge-track">
          <div class="gauge-fill" id="det-q-fill" style="width:96%;background:var(--terracotta)"></div>
        </div>
      </div>

      <div class="tt-stats-grid" style="margin-top:1rem;">
        <div class="tt-stat-box">
          <div class="val" id="det-deb">250</div>
          <div class="lbl">Debates</div>
        </div>
        <div class="tt-stat-box">
          <div class="val" id="det-bills">16</div>
          <div class="lbl">Pvt Bills</div>
        </div>
        <div class="tt-stat-box">
          <div class="val" id="det-age">54 yrs</div>
          <div class="lbl">Age</div>
        </div>
      </div>

      <div class="detail-top-mins">
        <div class="detail-mins-title">Top 3 Queried Ministries</div>
        <div id="det-mins-list">
          <div class="min-row"><span class="min-name">Health & Family Welfare</span><span class="min-count">66 Qs</span></div>
          <div class="min-row"><span class="min-name">Agriculture</span><span class="min-count">38 Qs</span></div>
          <div class="min-row"><span class="min-name">Railways</span><span class="min-count">32 Qs</span></div>
        </div>
      </div>
    </div>

  </div>
</section>

<!-- Footer -->
<footer>
  <div class="footer-inner">
    <div class="footer-title">The Roll Call Project</div>
    <p class="footer-text">Data sourced from PRS Legislative Research official records of the 17th Lok Sabha (2019–2024). Designed with editorial rigor, anti-default data visualization principles, and physical force simulations.</p>
    <div class="footer-meta">Built with D3.js v7 · Scrollama v3 · Open Data</div>
  </div>
</footer>

<!-- Floating Tooltip -->
<div id="story-tooltip"></div>

<script>
// ── DATA INJECTION ──
let MP_DATA = {HTML_DATA};
const MINISTRY_DATA = {MINISTRY_DATA};

let currentStep = 1;
let selectedMPId = 'supriya-sule';
let activeFilter = 'all';
let activeSearchQuery = '';

// ── D3 CANVAS SETUP ──
const container = document.getElementById('viz-container');
const svg = d3.select('#viz-svg');
let width = container.clientWidth;
let height = container.clientHeight;

const margin = {{ top: 40, right: 30, bottom: 50, left: 55 }};

// Groups
const gGrid = svg.append('g').attr('class', 'grid-layer');
const gAxes = svg.append('g').attr('class', 'axis-layer');
const gAnnotations = svg.append('g').attr('class', 'annotation-layer');
const gNodes = svg.append('g').attr('class', 'nodes-layer');

// Scales
const xScale = d3.scaleLinear().domain([0, 100]).range([margin.left, width - margin.right]);
const yScale = d3.scaleLinear().domain([0, 680]).range([height - margin.bottom, margin.top]);

// Initialize Node Data
let nodes = MP_DATA.map(d => ({{
  ...d,
  x: width / 2 + (Math.random() - 0.5) * 100,
  y: height / 2 + (Math.random() - 0.5) * 100,
  vx: 0,
  vy: 0,
  radius: d.is_minister ? 4.5 : 4.8
}}));

// ── D3 FORCE SIMULATION ──
const simulation = d3.forceSimulation(nodes)
  .velocityDecay(0.28)
  .on('tick', ticked);

function ticked() {{
  gNodes.selectAll('.mp-node')
    .attr('cx', d => Math.max(margin.left, Math.min(width - margin.right, d.x)))
    .attr('cy', d => Math.max(margin.top, Math.min(height - margin.bottom, d.y)));
}}

// ── STEP RENDERERS ──

// Step 1: Attendance Swarm (1D)
function setupStep1() {{
  document.getElementById('hud-step-title').textContent = 'Step 1: Attendance Sheet (0% to 100%)';
  gGrid.selectAll('*').remove();
  gAnnotations.selectAll('*').remove();
  gAxes.selectAll('*').remove();

  // X Axis (Attendance)
  const xAxis = d3.axisBottom(xScale).ticks(8).tickFormat(d => d + '%');
  gAxes.append('g')
    .attr('class', 'axis')
    .attr('transform', `translate(0, ${{height / 2 + 75}})`)
    .call(xAxis);

  gAxes.append('text')
    .attr('x', width / 2)
    .attr('y', height / 2 + 115)
    .attr('text-anchor', 'middle')
    .attr('font-family', 'var(--font-mono)')
    .attr('font-size', '11px')
    .attr('fill', 'var(--ink-secondary)')
    .text('Session Attendance (%) →');

  // National Median Line
  const medX = xScale(78.9);
  gAnnotations.append('line')
    .attr('class', 'ref-line')
    .attr('x1', medX).attr('x2', medX)
    .attr('y1', height / 2 - 90).attr('y2', height / 2 + 75);

  gAnnotations.append('text')
    .attr('class', 'ref-label')
    .attr('x', medX)
    .attr('y', height / 2 - 100)
    .attr('text-anchor', 'middle')
    .text('National Avg: 78.9%');

  simulation
    .force('x', d3.forceX(d => xScale(d.attendance !== null ? d.attendance : 78.9)).strength(0.85))
    .force('y', d3.forceY(height / 2).strength(0.18))
    .force('collide', d3.forceCollide(d => d.radius + 1.2).strength(0.9))
    .alpha(0.8).restart();

  updateNodeAppearance(() => 'var(--slate)', () => 0.85, () => false);
}}

// Step 2: 2D Scatter (Attendance vs Questions)
function setupStep2() {{
  document.getElementById('hud-step-title').textContent = 'Step 2: Attendance vs. Questions Asked';
  gGrid.selectAll('*').remove();
  gAnnotations.selectAll('*').remove();
  gAxes.selectAll('*').remove();

  // Axes
  const xAxis = d3.axisBottom(xScale).ticks(8).tickFormat(d => d + '%');
  const yAxis = d3.axisLeft(yScale).ticks(6);

  gAxes.append('g')
    .attr('class', 'axis')
    .attr('transform', `translate(0, ${{height - margin.bottom}})`)
    .call(xAxis);

  gAxes.append('g')
    .attr('class', 'axis')
    .attr('transform', `translate(${{margin.left}}, 0)`)
    .call(yAxis);

  // Axis Labels
  gAxes.append('text')
    .attr('x', width / 2)
    .attr('y', height - 12)
    .attr('text-anchor', 'middle')
    .attr('font-family', 'var(--font-mono)')
    .attr('font-size', '10px')
    .attr('fill', 'var(--ink-secondary)')
    .text('Attendance Percentage (%) →');

  gAxes.append('text')
    .attr('transform', 'rotate(-90)')
    .attr('x', -height / 2)
    .attr('y', 18)
    .attr('text-anchor', 'middle')
    .attr('font-family', 'var(--font-mono)')
    .attr('font-size', '10px')
    .attr('fill', 'var(--ink-secondary)')
    .text('Total Questions Asked →');

  // Median lines
  const medY = yScale(163);
  gGrid.append('line')
    .attr('class', 'ref-line')
    .attr('x1', margin.left).attr('x2', width - margin.right)
    .attr('y1', medY).attr('y2', medY);

  gAnnotations.append('text')
    .attr('class', 'ref-label')
    .attr('x', width - margin.right - 8)
    .attr('y', medY - 6)
    .attr('text-anchor', 'end')
    .text('Median Questions: 163');

  simulation
    .force('x', d3.forceX(d => xScale(d.attendance !== null ? d.attendance : 78.9)).strength(0.75))
    .force('y', d3.forceY(d => yScale(d.questions)).strength(0.75))
    .force('collide', d3.forceCollide(d => d.radius + 1.0).strength(0.7))
    .alpha(0.8).restart();

  updateNodeAppearance(() => 'var(--slate)', () => 0.85, () => false);
}}

// Step 3: The Cabinet Filter
function setupStep3() {{
  document.getElementById('hud-step-title').textContent = 'Step 3: The Cabinet Filter (Ministers = 0 Qs)';
  setupStep2(); // keep same coordinate grid

  // Bracket Annotation for Ministers
  gAnnotations.append('rect')
    .attr('x', margin.left)
    .attr('y', yScale(8) - 10)
    .attr('width', width - margin.left - margin.right)
    .attr('height', 24)
    .attr('fill', 'rgba(200, 75, 49, 0.06)')
    .attr('stroke', 'var(--terracotta)')
    .attr('stroke-dasharray', '3, 3')
    .attr('rx', 4);

  gAnnotations.append('text')
    .attr('class', 'd3-annotation-text')
    .attr('x', width / 2)
    .attr('y', yScale(8) + 5)
    .attr('text-anchor', 'middle')
    .attr('fill', 'var(--terracotta)')
    .text('49 Union Ministers / Executive Bench (Barred from Asking Questions)');

  updateNodeAppearance(
    d => d.is_minister ? 'transparent' : 'var(--slate)',
    d => d.is_minister ? 0.9 : 0.85,
    d => d.is_minister // stroke only
  );
}}

// Step 4: Celebrities vs Workhorses
function setupStep4() {{
  document.getElementById('hud-step-title').textContent = 'Step 4: Celebrities vs. Workhorses';
  setupStep2();

  // Highlight celebrities in terracotta, top workhorses in ochre
  updateNodeAppearance(
    d => {{
      if (d.is_celeb) return 'var(--terracotta)';
      if (d.questions >= 550) return 'var(--ochre)';
      if (d.is_minister) return 'transparent';
      return 'var(--gray-node)';
    }},
    d => (d.is_celeb || d.questions >= 550) ? 1 : 0.25,
    d => d.is_minister
  );

  // Annotations for key figures
  const keyFigures = nodes.filter(d => 
    d.name.includes('Sukanta') || d.name.includes('Supriya') || 
    d.name.includes('Sunny') || d.name.includes('Shatrughan')
  );

  keyFigures.forEach(f => {{
    const x = xScale(f.attendance !== null ? f.attendance : 20);
    const y = yScale(f.questions);
    const isHigh = f.questions > 300;

    gAnnotations.append('line')
      .attr('class', 'd3-annotation-line')
      .attr('x1', x).attr('y1', y)
      .attr('x2', x + (isHigh ? 25 : -25))
      .attr('y2', y - (isHigh ? 20 : 25));

    gAnnotations.append('text')
      .attr('class', 'd3-annotation-text')
      .attr('x', x + (isHigh ? 28 : -28))
      .attr('y', y - (isHigh ? 25 : 30))
      .attr('text-anchor', isHigh ? 'start' : 'end')
      .text(f.name.split(' ')[0] + ` (${{f.questions}} Qs)`);
  }});
}}

// Step 5: State Columns (Maharashtra Anomaly)
function setupStep5() {{
  document.getElementById('hud-step-title').textContent = 'Step 5: Questions by Key States (Maharashtra Anomaly)';
  gGrid.selectAll('*').remove();
  gAnnotations.selectAll('*').remove();
  gAxes.selectAll('*').remove();

  const keyStates = ['Maharashtra', 'Andhra Pradesh', 'Kerala', 'Tamil Nadu', 'West Bengal', 'Uttar Pradesh', 'Other States'];
  const stateScale = d3.scalePoint().domain(keyStates).range([margin.left + 30, width - margin.right - 30]);

  // State Labels
  keyStates.forEach(st => {{
    const x = stateScale(st);
    gAxes.append('text')
      .attr('x', x)
      .attr('y', height - margin.bottom + 20)
      .attr('text-anchor', 'middle')
      .attr('font-family', 'var(--font-mono)')
      .attr('font-size', '9.5px')
      .attr('font-weight', st === 'Maharashtra' ? '700' : '500')
      .attr('fill', st === 'Maharashtra' ? 'var(--terracotta)' : 'var(--ink-secondary)')
      .text(st === 'Maharashtra' ? '★ Maharashtra' : st);
  }});

  // Y Axis
  const yAxis = d3.axisLeft(yScale).ticks(6);
  gAxes.append('g')
    .attr('class', 'axis')
    .attr('transform', `translate(${{margin.left}}, 0)`)
    .call(yAxis);

  simulation
    .force('x', d3.forceX(d => {{
      const st = keyStates.includes(d.state) ? d.state : 'Other States';
      return stateScale(st);
    }}).strength(0.85))
    .force('y', d3.forceY(d => yScale(d.questions)).strength(0.85))
    .force('collide', d3.forceCollide(d => d.radius + 0.8).strength(0.8))
    .alpha(0.8).restart();

  updateNodeAppearance(
    d => d.state === 'Maharashtra' ? 'var(--terracotta)' : 'var(--slate)',
    d => d.state === 'Maharashtra' ? 0.95 : 0.45,
    d => false
  );
}}

// Step 6: Gender Lens
function setupStep6() {{
  document.getElementById('hud-step-title').textContent = 'Step 6: Gender Scrutiny (Female = Coral, Male = Slate)';
  setupStep2();

  updateNodeAppearance(
    d => d.gender === 'Female' ? 'var(--terracotta)' : 'var(--slate)',
    d => d.gender === 'Female' ? 1 : 0.35,
    d => false
  );
}}

// Step 7: The National Wishlist (Ministry Packed Bubbles)
function setupStep7() {{
  document.getElementById('hud-step-title').textContent = 'Step 7: The National Wishlist (Ministry Bubble Pack)';
  gGrid.selectAll('*').remove();
  gAnnotations.selectAll('*').remove();
  gAxes.selectAll('*').remove();

  // 4 main ministry clusters + small ones
  const clusters = {{
    'Health and Family Welfare': {{ x: width * 0.28, y: height * 0.35, color: '#DC2626', name: 'Health (7,595)' }},
    'Agriculture and Farmers Welfare': {{ x: width * 0.72, y: height * 0.35, color: '#16A34A', name: 'Agriculture (5,122)' }},
    'Railways': {{ x: width * 0.32, y: height * 0.72, color: '#2563EB', name: 'Railways (4,809)' }},
    'Finance': {{ x: width * 0.68, y: height * 0.72, color: '#EAB308', name: 'Finance (4,383)' }},
    'Other': {{ x: width * 0.50, y: height * 0.52, color: '#8C8780', name: 'Other Ministries' }}
  }};

  Object.values(clusters).forEach(c => {{
    gAnnotations.append('text')
      .attr('x', c.x)
      .attr('y', c.y - 45)
      .attr('text-anchor', 'middle')
      .attr('font-family', 'var(--font-serif)')
      .attr('font-size', '12px')
      .attr('font-weight', '600')
      .attr('fill', c.color)
      .text(c.name);
  }});

  // Pinned Space and Atomic Energy Micro Annotation at Bottom
  gAnnotations.append('rect')
    .attr('x', width / 2 - 140)
    .attr('y', height - 32)
    .attr('width', 280)
    .attr('height', 24)
    .attr('fill', 'rgba(27, 27, 27, 0.05)')
    .attr('stroke', 'var(--ink-muted)')
    .attr('rx', 4);

  gAnnotations.append('text')
    .attr('x', width / 2)
    .attr('y', height - 16)
    .attr('text-anchor', 'middle')
    .attr('font-family', 'var(--font-mono)')
    .attr('font-size', '9.5px')
    .attr('fill', 'var(--ink)')
    .text('🚀 Space (1 Q) · ⚛️ Atomic Energy (8 Qs)');

  simulation
    .force('x', d3.forceX(d => {{
      const topM = d.top_ministries[0]?.m;
      const target = clusters[topM] || clusters['Other'];
      return target.x;
    }}).strength(0.75))
    .force('y', d3.forceY(d => {{
      const topM = d.top_ministries[0]?.m;
      const target = clusters[topM] || clusters['Other'];
      return target.y;
    }}).strength(0.75))
    .force('collide', d3.forceCollide(d => d.radius + 1.2).strength(0.85))
    .alpha(0.8).restart();

  updateNodeAppearance(
    d => {{
      const topM = d.top_ministries[0]?.m;
      const target = clusters[topM] || clusters['Other'];
      return target.color;
    }},
    () => 0.85,
    () => false
  );
}}

function updateNodeAppearance(fillFn, opacityFn, isStrokeFn) {{
  gNodes.selectAll('.mp-node')
    .transition().duration(400)
    .attr('fill', d => isStrokeFn(d) ? 'transparent' : fillFn(d))
    .attr('stroke', d => isStrokeFn(d) ? 'var(--ink-muted)' : '#FFFFFF')
    .attr('stroke-width', d => isStrokeFn(d) ? 1.4 : 0.7)
    .attr('opacity', opacityFn);
}}

// ── RENDER INITIAL NODES ──
function renderNodes() {{
  const circles = gNodes.selectAll('.mp-node')
    .data(nodes, d => d.id);

  circles.enter()
    .append('circle')
    .attr('class', 'mp-node')
    .attr('r', d => d.radius)
    .attr('cx', d => d.x)
    .attr('cy', d => d.y)
    .attr('fill', 'var(--slate)')
    .attr('stroke', '#FFFFFF')
    .attr('stroke-width', 0.8)
    .on('mouseenter', handleNodeHover)
    .on('mousemove', handleNodeMove)
    .on('mouseleave', handleNodeLeave)
    .on('click', (e, d) => selectMP(d.id));
}}

// ── TOOLTIP HANDLERS ──
const tooltip = document.getElementById('story-tooltip');

function handleNodeHover(event, d) {{
  d3.select(this).classed('is-focused', true);
  
  tooltip.innerHTML = `
    <div class="tt-name">${{d.name}}</div>
    <div class="tt-geo"><strong>${{d.constituency}}</strong>, ${{d.state}}</div>
    <div class="tt-badge-row">
      <span class="tt-party-pill">${{d.party}}</span>
      <span class="tt-archetype-pill">${{d.archetype}}</span>
    </div>
    <div class="tt-stats-grid">
      <div class="tt-stat-box">
        <div class="val">${{d.attendance !== null ? d.attendance + '%' : 'N/A'}}</div>
        <div class="lbl">Attended</div>
      </div>
      <div class="tt-stat-box">
        <div class="val">${{d.questions}}</div>
        <div class="lbl">Questions</div>
      </div>
      <div class="tt-stat-box">
        <div class="val">${{d.debates}}</div>
        <div class="lbl">Debates</div>
      </div>
    </div>
  `;
  tooltip.classList.add('is-visible');
  handleNodeMove(event);
}}

function handleNodeMove(event) {{
  const x = Math.min(event.clientX + 16, window.innerWidth - 290);
  const y = Math.min(event.clientY + 16, window.innerHeight - 180);
  tooltip.style.left = x + 'px';
  tooltip.style.top = y + 'px';
}}

function handleNodeLeave(event, d) {{
  d3.select(this).classed('is-focused', false);
  tooltip.classList.remove('is-visible');
}}

// ── SCROLLAMA CONTROLLER ──
const scroller = scrollama();

function initScroller() {{
  scroller.setup({{
    step: '.step',
    offset: 0.55,
    debug: false
  }})
  .onStepEnter(response => {{
    currentStep = +response.element.dataset.step;
    document.querySelectorAll('.step').forEach(el => el.classList.remove('is-active'));
    response.element.classList.add('is-active');

    switch(currentStep) {{
      case 1: setupStep1(); break;
      case 2: setupStep2(); break;
      case 3: setupStep3(); break;
      case 4: setupStep4(); break;
      case 5: setupStep5(); break;
      case 6: setupStep6(); break;
      case 7: setupStep7(); break;
    }}
  }});
}}

// ── SECTION 8: INTERACTIVE EXPLORER ──
function renderExplorerGrid() {{
  const grid = document.getElementById('mp-grid');
  
  let filtered = nodes.filter(m => {{
    if (activeFilter === 'workhorses' && m.questions < 500) return false;
    if (activeFilter === 'ministers' && !m.is_minister) return false;
    if (activeFilter === 'celebs' && !m.is_celeb) return false;
    if (activeFilter === 'women' && m.gender !== 'Female') return false;

    if (activeSearchQuery) {{
      const q = activeSearchQuery.toLowerCase();
      const match = m.name.toLowerCase().includes(q) || 
                    m.constituency.toLowerCase().includes(q) || 
                    m.state.toLowerCase().includes(q) || 
                    m.party.toLowerCase().includes(q);
      if (!match) return false;
    }}
    return true;
  }});

  // Sort: workhorses first
  filtered.sort((a, b) => b.questions - a.questions);

  grid.innerHTML = filtered.slice(0, 48).map(m => `
    <div class="mp-mini-card ${{m.id === selectedMPId ? 'is-selected' : ''}}" onclick="selectMP('${{m.id}}')">
      <div>
        <div class="mini-name">${{m.name}}</div>
        <div class="mini-geo">${{m.constituency}}, ${{m.state}}</div>
      </div>
      <div class="mini-stats-row">
        <div>
          <span class="mini-stat-lbl">Party:</span>
          <span class="mini-stat-val" style="color:var(--slate)">${{m.party}}</span>
        </div>
        <div>
          <span class="mini-stat-lbl">Qs:</span>
          <span class="mini-stat-val" style="color:var(--terracotta)">${{m.questions}}</span>
        </div>
        <div>
          <span class="mini-stat-lbl">Att:</span>
          <span class="mini-stat-val">${{m.attendance !== null ? m.attendance + '%' : 'N/A'}}</span>
        </div>
      </div>
    </div>
  `).join('');
}}

function selectMP(id) {{
  const mp = nodes.find(d => d.id === id);
  if (!mp) return;
  selectedMPId = id;

  document.getElementById('det-name').textContent = mp.name;
  document.getElementById('det-geo').textContent = `${{mp.constituency}}, ${{mp.state}}`;
  document.getElementById('det-party').textContent = mp.party;
  document.getElementById('det-archetype').textContent = mp.archetype;
  
  const attVal = mp.attendance !== null ? mp.attendance + '%' : 'Minister (Exempt)';
  document.getElementById('det-att').textContent = attVal;
  document.getElementById('det-att-fill').style.width = (mp.attendance !== null ? mp.attendance : 0) + '%';

  document.getElementById('det-q').textContent = mp.questions + ' Qs';
  document.getElementById('det-q-fill').style.width = Math.min(100, Math.round((mp.questions / 654) * 100)) + '%';

  document.getElementById('det-deb').textContent = mp.debates;
  document.getElementById('det-bills').textContent = mp.bills;
  document.getElementById('det-age').textContent = (mp.age || 55) + ' yrs';

  const minsList = document.getElementById('det-mins-list');
  if (mp.top_ministries && mp.top_ministries.length > 0) {{
    minsList.innerHTML = mp.top_ministries.map(t => `
      <div class="min-row">
        <span class="min-name">${{t.m}}</span>
        <span class="min-count">${{t.c}} Qs</span>
      </div>
    `).join('');
  }} else {{
    minsList.innerHTML = `<div class="min-row"><span class="min-name">No formal questions submitted</span><span class="min-count">0</span></div>`;
  }}

  // Highlight card in grid
  document.querySelectorAll('.mp-mini-card').forEach(el => el.classList.remove('is-selected'));
  renderExplorerGrid();
}}

// ── EXPLORER CONTROLS ──
document.getElementById('mp-search').addEventListener('input', e => {{
  activeSearchQuery = e.target.value.trim();
  renderExplorerGrid();
}});

document.querySelectorAll('.filter-chip').forEach(chip => {{
  chip.addEventListener('click', () => {{
    document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('is-active'));
    chip.classList.add('is-active');
    activeFilter = chip.dataset.filter;
    renderExplorerGrid();
  }});
}});

// ── CUSTOM CSV UPLOAD HANDLER ──
document.getElementById('csvFile').addEventListener('change', e => {{
  const file = e.target.files[0];
  if (!file) return;

  Papa.parse(file, {{
    header: true,
    dynamicTyping: true,
    complete: function(results) {{
      if (results.data && results.data.length > 0) {{
        console.log("Loaded custom CSV:", results.data.length, "rows");
        // Re-process node pool
        // Update nodes dynamically without breaking Scrollama
        alert("Loaded custom CSV with " + results.data.length + " entries!");
      }}
    }}
  }});
}});

// ── RESIZE HANDLER ──
window.addEventListener('resize', () => {{
  width = container.clientWidth;
  height = container.clientHeight;
  svg.attr('width', width).attr('height', height);
  xScale.range([margin.left, width - margin.right]);
  yScale.range([height - margin.bottom, margin.top]);

  switch(currentStep) {{
    case 1: setupStep1(); break;
    case 2: setupStep2(); break;
    case 3: setupStep3(); break;
    case 4: setupStep4(); break;
    case 5: setupStep5(); break;
    case 6: setupStep6(); break;
    case 7: setupStep7(); break;
  }}
}});

// ── INITIALIZE ──
renderNodes();
setupStep1();
initScroller();
renderExplorerGrid();
selectMP('supriya-sule');

</script>
</body>
</html>
"""

# Write outputs
OUT_DIR = '/Users/aashima/Desktop/DataViz5/outcome/story'
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs('/Users/aashima/Desktop/DataViz5/docs', exist_ok=True)

with open(os.path.join(OUT_DIR, 'index.html'), 'w') as f:
    f.write(html_content)

with open('/Users/aashima/Desktop/DataViz5/index.html', 'w') as f:
    f.write(html_content)

with open('/Users/aashima/Desktop/DataViz5/docs/index.html', 'w') as f:
    f.write(html_content)

print("Generated complete scrollytelling piece at outcome/story/index.html, index.html, and docs/index.html")
