import csv, json, math, collections, statistics

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

# Short labels for sectors
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
    'Chemicals and Fertilizers': 'Chemicals',
    'Law and Justice': 'Law & Justice',
    'Fisheries, Animal Husbandry and Dairying': 'Fisheries',
    'Tourism': 'Tourism',
    'Electronics and Information Technology': 'Electronics & IT',
    'Micro, Small and Medium Enterprises': 'MSME',
    'Social Justice and Empowerment': 'Social Justice',
    'Culture': 'Culture',
    'Defence': 'Defence',
    'New and Renewable Energy': 'Renewable Energy',
    'Skill Development and Entrepreneurship': 'Skill Dev.',
    'External Affairs': 'External Affairs',
    'Youth Affairs and Sports': 'Youth & Sports',
    'Human Resource Development': 'HRD',
    'Power': 'Power',
    'Tribal Affairs': 'Tribal Affairs',
    'Information and Broadcasting': 'I&B',
    'Coal': 'Coal',
    'Prime Minister': "PM's Office",
    'Food Processing Industries': 'Food Processing',
    'Corporate Affairs': 'Corporate Affairs',
    'Science and Technology': 'Science & Tech',
    'Minority Affairs': 'Minority Affairs',
    'Ports, Shipping and Waterways': 'Ports & Shipping',
    'Heavy Industries and Public Enterprises': 'Heavy Industries',
    'Earth Sciences': 'Earth Sciences',
    'Panchayati Raj': 'Panchayati Raj',
    'Mines': 'Mines',
    'Steel': 'Steel',
    'Statistics and Programme Implementation': 'Statistics',
    'Cooperation': 'Cooperation',
    'Planning': 'Planning',
    'Shipping': 'Shipping',
    'Development of North Eastern Region': 'NE Development',
    'Parliamentary Affairs': 'Parliamentary Affairs',
    'Atomic Energy': 'Atomic Energy',
    'Personnel, Public Grievances and Pensions': 'Personnel',
    'Space': 'Space',
}

processed = []
for r in rows:
    total = int(r['total_questions_parsed']) if r['total_questions_parsed'] else 0
    if total == 0:
        continue
    sector_counts = {}
    for s in primary_sectors:
        val = int(r[s]) if r[s] else 0
        for sec, prim in merges.items():
            if prim == s and r.get(sec):
                val += int(r[sec])
        sector_counts[s] = val
    
    shares = {s: sector_counts[s] / total for s in primary_sectors}
    
    processed.append({
        'mp_id': r['mp_id'],
        'name': r['name'],
        'party': r['party'],
        'state': r['state'],
        'constituency': r['constituency'],
        'gender': r['gender'],
        'total_questions': total,
        'sectors': sector_counts,
        'shares': shares,
    })

# Global stats
global_counts = {s: sum(m['sectors'][s] for m in processed) for s in primary_sectors}
total_global = sum(global_counts.values())
global_shares = {s: global_counts[s] / total_global for s in primary_sectors}
top_sectors_all = sorted(global_shares, key=global_shares.get, reverse=True)
# Top 20 for viz
top20_sectors = top_sectors_all[:20]

# State data
states_with_data = {}
for state in sorted(set(m['state'] for m in processed)):
    mps = [m for m in processed if m['state'] == state]
    n = len(mps)
    if n < 2:
        continue
    avg_shares = {s: statistics.mean(m['shares'][s] for m in mps) for s in primary_sectors}
    std_shares = {s: statistics.stdev(m['shares'][s] for m in mps) for s in primary_sectors}
    avg_within_std = statistics.mean(std_shares.values())
    distinctiveness = {s: avg_shares[s] - global_shares[s] for s in primary_sectors}
    # Top distinctive sectors
    top_pos = sorted(distinctiveness.items(), key=lambda x: x[1], reverse=True)[:5]
    top_neg = sorted(distinctiveness.items(), key=lambda x: x[1])[:3]
    # Max distinctiveness score
    max_dist = max(abs(v) for v in distinctiveness.values())
    
    states_with_data[state] = {
        'n': n,
        'avg_shares': avg_shares,
        'std_shares': std_shares,
        'avg_within_std': avg_within_std,
        'distinctiveness': distinctiveness,
        'max_distinctiveness': max_dist,
        'top_sectors': [s for s,v in top_pos],
        'top_positive': [[s, round(v*100, 2)] for s, v in top_pos],
        'top_negative': [[s, round(v*100, 2)] for s, v in top_neg],
    }

# Between-state variance per sector
between_state_var = {}
for s in primary_sectors:
    state_avgs = [d['avg_shares'][s] for d in states_with_data.values()]
    between_state_var[s] = statistics.stdev(state_avgs) if len(state_avgs) > 1 else 0

# Within-state variance (avg across sectors)
within_state_avg = {state: d['avg_within_std'] for state, d in states_with_data.items()}

# Compute Jensen-Shannon divergence-like pairwise between-state distance for top 20 sectors
def cosine_dist(v1, v2):
    dot = sum(v1[i]*v2[i] for i in range(len(v1)))
    n1 = math.sqrt(sum(x**2 for x in v1))
    n2 = math.sqrt(sum(x**2 for x in v2))
    if n1 == 0 or n2 == 0:
        return 1
    return 1 - dot/(n1*n2)

state_list = sorted(states_with_data.keys())
# Pairwise distances using top20 sectors
pairwise = {}
for i, s1 in enumerate(state_list):
    for j, s2 in enumerate(state_list):
        if i >= j:
            continue
        v1 = [states_with_data[s1]['avg_shares'][s] for s in top20_sectors]
        v2 = [states_with_data[s2]['avg_shares'][s] for s in top20_sectors]
        dist = cosine_dist(v1, v2)
        pairwise[f"{s1}||{s2}"] = round(dist, 4)

# Party data
major_parties = ['BJP', 'INC', 'DMK', 'YSRCP', 'AITC', 'SS', 'JD(U)', 'BJD', 'BSP', 'BRS']
party_data = {}
for party in major_parties:
    mps = [m for m in processed if m['party'] == party]
    if len(mps) < 3:
        continue
    avg_shares = {s: statistics.mean(m['shares'][s] for m in mps) for s in primary_sectors}
    distinctiveness = {s: avg_shares[s] - global_shares[s] for s in primary_sectors}
    party_data[party] = {
        'n': len(mps),
        'avg_shares': avg_shares,
        'distinctiveness': distinctiveness,
        'top_positive': sorted([[s, round(v*100, 2)] for s, v in distinctiveness.items()], key=lambda x: x[1], reverse=True)[:5],
        'top_negative': sorted([[s, round(v*100, 2)] for s, v in distinctiveness.items()], key=lambda x: x[1])[:3],
    }

# MP-level data (simplified for viz - keep top20 sectors)
mp_viz = []
for m in processed:
    mp_viz.append({
        'mp_id': m['mp_id'],
        'name': m['name'],
        'party': m['party'],
        'state': m['state'],
        'constituency': m['constituency'],
        'gender': m['gender'],
        'total_questions': m['total_questions'],
        'shares': {s: round(m['shares'][s]*100, 2) for s in top20_sectors},
        'top_sector': max(((s, m['shares'][s]) for s in primary_sectors), key=lambda x: x[1])[0],
        'top_sector_share': round(max(m['shares'][s] for s in primary_sectors)*100, 2),
        'deviation': {s: round((m['shares'][s] - global_shares[s])*100, 2) for s in top20_sectors},
    })

# Notable MPs (extreme outliers in specific sectors)
# Find for each sector: MP with highest share
notable = {}
for s in top20_sectors:
    top_mp = max(processed, key=lambda m: m['shares'][s])
    notable[s] = {
        'name': top_mp['name'],
        'state': top_mp['state'],
        'party': top_mp['party'],
        'share': round(top_mp['shares'][s]*100, 1),
        'global_share': round(global_shares[s]*100, 1),
    }

output = {
    'mps': mp_viz,
    'sectors': primary_sectors,
    'short_labels': short_labels,
    'top20_sectors': top20_sectors,
    'global_shares': {s: round(global_shares[s]*100, 3) for s in primary_sectors},
    'state_data': {state: {
        'n': d['n'],
        'avg_shares': {s: round(d['avg_shares'][s]*100, 3) for s in primary_sectors},
        'std_shares': {s: round(d['std_shares'][s]*100, 3) for s in primary_sectors},
        'avg_within_std': round(d['avg_within_std']*100, 3),
        'distinctiveness': {s: round(d['distinctiveness'][s]*100, 3) for s in primary_sectors},
        'max_distinctiveness': round(d['max_distinctiveness']*100, 3),
        'top_positive': d['top_positive'],
        'top_negative': d['top_negative'],
        'top_sectors': d['top_sectors'],
    } for state, d in states_with_data.items()},
    'between_state_var': {s: round(between_state_var[s]*100, 3) for s in primary_sectors},
    'pairwise_distances': pairwise,
    'party_data': party_data,
    'notable_mps': notable,
    'state_list': state_list,
    'total_mps': len(processed),
    'total_states': len(states_with_data),
}

with open('/Users/aashima/Desktop/DataViz5/data/loksabha-questions/curated/viz_data.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"Done. MPs: {len(processed)}, States: {len(states_with_data)}, Sectors: {len(primary_sectors)}")
print(f"Top20 sectors: {top20_sectors}")
print(f"JSON size: {len(json.dumps(output))} chars")
