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
    'Home Affairs': 'Home Affairs',
    'Commerce and Industry': 'Commerce & Industry',
    'Labour and Employment': 'Labour',
    'Civil Aviation': 'Civil Aviation',
    'Rural Development': 'Rural Dev.',
    'Consumer Affairs, Food and Public Distribution': 'Consumer Affairs',
    'AYUSH': 'AYUSH',
    'Communications': 'Communications',
    'Petroleum and Natural Gas': 'Petroleum & Gas',
    'Textiles': 'Textiles',
    'Housing and Urban Affairs': 'Housing & Urban',
    'Micro, Small and Medium Enterprises': 'MSME',
    'Social Justice and Empowerment': 'Social Justice',
    'External Affairs': 'External Affairs',
    'Defence': 'Defence',
    'New and Renewable Energy': 'Renewable Energy',
}

top16 = [
    'Health and Family Welfare','Agriculture and Farmers Welfare','Railways','Finance',
    'Education','Environment, Forest and Climate Change','Jal Shakti','Women and Child Development',
    'Road Transport and Highways','Home Affairs','Commerce and Industry','Labour and Employment',
    'Civil Aviation','Rural Development','Consumer Affairs, Food and Public Distribution','AYUSH',
]

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
    shares = {s: round(sc[s]/total*100, 3) for s in top16}
    mps_out.append({
        'id': r['mp_id'],
        'name': r['name'],
        'party': r['party'],
        'state': r['state'],
        'constituency': r['constituency'],
        'gender': r['gender'],
        'total': total,
        's': shares,
        'img': None,  # to be filled
    })

# Global averages
n = len(mps_out)
global_avg = {s: round(sum(m['s'][s] for m in mps_out)/n, 3) for s in top16}

# Ranges for each sector
sector_stats = {}
for s in top16:
    vals = [m['s'][s] for m in mps_out]
    sector_stats[s] = {
        'avg': round(statistics.mean(vals), 2),
        'max': round(max(vals), 1),
        'min': round(min(vals), 1),
    }

out = {
    'mps': mps_out,
    'sectors': top16,
    'labels': short_labels,
    'avg': global_avg,
    'sector_stats': sector_stats,
    'total_mps': n,
}

with open('/Users/aashima/Desktop/DataViz5/data/loksabha-questions/curated/viz_data_v2.json', 'w') as f:
    json.dump(out, f, separators=(',',':'))

print(f"Done: {n} MPs, {len(top16)} sectors")
print(f"Sector stats sample - Health: {sector_stats['Health and Family Welfare']}")
print(f"JSON size: {len(json.dumps(out, separators=(',',':')))//1024} KB")
