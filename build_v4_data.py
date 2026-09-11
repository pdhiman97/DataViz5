import json, csv, statistics

with open('/Users/aashima/Desktop/DataViz5/data/loksabha-questions/raw/mp_17th_loksabha_questions_matrix.csv') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    fieldnames = reader.fieldnames

meta_cols = {'mp_id','name','party','state','constituency','gender','age','education',
             'attendance_pct','debates_count','total_questions_prs','total_questions_parsed',
             'pvt_member_bills_count','profile_url'}
sector_cols = [c for c in fieldnames if c not in meta_cols]
merges = {'Ayush':'AYUSH','Micro':'Micro, Small and Medium Enterprises',
          'Statiscs and Programme Implementation':'Statistics and Programme Implementation',
          'Consumer Affairs':'Consumer Affairs, Food and Public Distribution',
          'Heavy Industries':'Heavy Industries and Public Enterprises'}
secondary_cols = set(merges.keys())
primary_sectors = [c for c in sector_cols if c not in secondary_cols]

short_labels = {
    'Health and Family Welfare':'Health',
    'Agriculture and Farmers Welfare':'Agriculture',
    'Railways':'Railways',
    'Finance':'Finance',
    'Education':'Education',
    'Environment, Forest and Climate Change':'Environment',
    'Jal Shakti':'Jal Shakti',
    'Women and Child Development':'Women & Child',
    'Road Transport and Highways':'Road Transport',
    'Home Affairs':'Home Affairs',
    'Commerce and Industry':'Commerce',
    'Labour and Employment':'Labour',
    'Civil Aviation':'Civil Aviation',
    'Rural Development':'Rural Dev.',
    'Consumer Affairs, Food and Public Distribution':'Consumer Affairs',
    'AYUSH':'AYUSH',
    'Communications':'Communications',
    'Petroleum and Natural Gas':'Petroleum & Gas',
    'Textiles':'Textiles',
    'Housing and Urban Affairs':'Housing',
    'Micro, Small and Medium Enterprises':'MSME',
    'Social Justice and Empowerment':'Social Justice',
    'External Affairs':'External Affairs',
    'Defence':'Defence',
    'New and Renewable Energy':'Renewables',
    'Tribal Affairs':'Tribal Affairs',
    'Fisheries, Animal Husbandry and Dairying':'Fisheries',
    'Science and Technology':'Science & Tech',
    'Minority Affairs':'Minority Affairs',
    'Skill Development and Entrepreneurship':'Skill Dev.',
    'Information and Broadcasting':'Info & Broadcast',
    'Coal':'Coal',
    'Power':'Power',
    'Steel':'Steel',
    'Mines':'Mines',
    'Tourism':'Tourism',
}

top20 = [
    'Health and Family Welfare','Agriculture and Farmers Welfare','Railways','Finance','Education',
    'Environment, Forest and Climate Change','Jal Shakti','Women and Child Development',
    'Road Transport and Highways','Home Affairs','Commerce and Industry','Labour and Employment',
    'Civil Aviation','Rural Development','Consumer Affairs, Food and Public Distribution','AYUSH',
    'Communications','Petroleum and Natural Gas','Textiles','Housing and Urban Affairs',
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
    shares = {s: round(sc[s]/total*100, 2) for s in top20}
    mps_out.append({
        'id': r['mp_id'],
        'name': r['name'],
        'party': r['party'],
        'state': r['state'],
        'constituency': r['constituency'],
        'gender': r['gender'],
        'total': total,
        's': shares,
    })

# Sort by total questions descending — assign rank
mps_out.sort(key=lambda m: -m['total'])
for i, m in enumerate(mps_out):
    m['rank'] = i + 1  # 1 = most active

n = len(mps_out)
global_avg = {s: round(sum(m['s'][s] for m in mps_out)/n, 2) for s in top20}

out = {
    'mps': mps_out,
    'sectors': top20,
    'labels': short_labels,
    'avg': global_avg,
    'total_mps': n,
    'max_q': mps_out[0]['total'],
    'min_q': mps_out[-1]['total'],
    'states': sorted(set(m['state'] for m in mps_out)),
    'parties': [p for p,_ in sorted(
        {p: sum(1 for m in mps_out if m['party']==p) for p in set(m['party'] for m in mps_out)}.items(),
        key=lambda x: -x[1]
    )[:12]],
}

with open('/Users/aashima/Desktop/DataViz5/data/loksabha-questions/curated/viz_v4_data.json','w') as f:
    json.dump(out, f, separators=(',',':'))

sz = len(json.dumps(out, separators=(',',':')))
print(f"MPs: {n}, max_q: {out['max_q']}, min_q: {out['min_q']}")
print(f"Top MP: {mps_out[0]['name']} ({mps_out[0]['total']} questions)")
print(f"Sectors: {len(top20)}, States: {len(out['states'])}")
print(f"JSON: {sz//1024} KB")
