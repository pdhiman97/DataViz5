import json, csv, statistics

# Read raw data
with open('/Users/aashima/Desktop/DataViz5/data/loksabha-questions/raw/mp_17th_loksabha_questions_matrix.csv') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    fieldnames = reader.fieldnames

meta_cols = {'mp_id','name','party','state','constituency','gender','age','education',
             'attendance_pct','debates_count','total_questions_prs','total_questions_parsed',
             'pvt_member_bills_count','profile_url'}
sector_cols = [c for c in fieldnames if c not in meta_cols]
merges = {
    'Ayush': 'AYUSH',
    'Micro': 'Micro, Small and Medium Enterprises',
    'Statiscs and Programme Implementation': 'Statistics and Programme Implementation',
    'Consumer Affairs': 'Consumer Affairs, Food and Public Distribution',
    'Heavy Industries': 'Heavy Industries and Public Enterprises',
}
secondary_cols = set(merges.keys())
primary_sectors = [c for c in sector_cols if c not in secondary_cols]

short_labels = {
    'Health and Family Welfare': 'Health',
    'Agriculture and Farmers Welfare': 'Agriculture',
    'Railways': 'Railways',
    'Finance': 'Finance',
    'Education': 'Education',
    'Environment, Forest and Climate Change': 'Environment',
    'Jal Shakti': 'Jal Shakti',
    'Women and Child Development': 'Women & Child',
    'Road Transport and Highways': 'Road Transport',
    'Housing and Urban Affairs': 'Housing & Urban',
    'Home Affairs': 'Home Affairs',
    'Commerce and Industry': 'Commerce',
    'Labour and Employment': 'Labour',
    'Civil Aviation': 'Civil Aviation',
    'Rural Development': 'Rural Dev.',
    'Consumer Affairs, Food and Public Distribution': 'Consumer Affairs',
    'AYUSH': 'AYUSH',
    'Communications': 'Communications',
    'Petroleum and Natural Gas': 'Petroleum & Gas',
    'Textiles': 'Textiles',
}

top12 = ['Health and Family Welfare','Agriculture and Farmers Welfare','Railways','Finance',
         'Education','Environment, Forest and Climate Change','Jal Shakti','Women and Child Development',
         'Road Transport and Highways','Home Affairs','Commerce and Industry','Labour and Employment']

mps_out = []
for r in rows:
    total = int(r['total_questions_parsed']) if r['total_questions_parsed'] else 0
    if total == 0: continue
    sc = {}
    for s in primary_sectors:
        val = int(r[s]) if r[s] else 0
        for sec, prim in merges.items():
            if prim == s and r.get(sec): val += int(r[sec])
        sc[s] = val
    shares = {s: round(sc[s]/total*100, 2) for s in top12}
    mps_out.append({
        'id': r['mp_id'],
        'name': r['name'],
        'party': r['party'],
        'state': r['state'],
        'gender': r['gender'],
        'total': total,
        's': shares,
    })

# Global averages
all_totals = {s: sum(m['s'][s] for m in mps_out) for s in top12}
n = len(mps_out)
global_avg = {s: round(all_totals[s]/n, 2) for s in top12}

# Party colors
party_colors = {
    'BJP': '#FF6B00', 'INC': '#19AAED', 'DMK': '#E31E24',
    'YSRCP': '#0F60C4', 'AITC': '#26A541', 'SS': '#FF9933',
    'JD(U)': '#3CB371', 'BJD': '#006400', 'BSP': '#1565C0',
    'BRS': '#E91E8C', 'OTHER': '#888888'
}

out = {
    'mps': mps_out,
    'sectors': top12,
    'labels': short_labels,
    'avg': global_avg,
    'party_colors': party_colors,
}

js = f"const DATA = {json.dumps(out, separators=(',',':'))};"
with open('/Users/aashima/Desktop/DataViz5/outcome/loksabha-questions/viz_inline.js', 'w') as f:
    f.write(js)

print(f"Done: {len(mps_out)} MPs, {len(js)//1024} KB")
