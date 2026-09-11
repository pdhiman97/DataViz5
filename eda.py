import csv, json, math, collections
import statistics

with open('/Users/aashima/Desktop/DataViz5/mp_17th_loksabha_questions_matrix.csv') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    fieldnames = reader.fieldnames

meta_cols = {'mp_id','name','party','state','constituency','gender','age','education',
             'attendance_pct','debates_count','total_questions_prs','total_questions_parsed',
             'pvt_member_bills_count','profile_url'}
sector_cols = [c for c in fieldnames if c not in meta_cols]

# Merge the duplicate/secondary columns into the primary ones
# 'Ayush' -> 'AYUSH', 'Micro' -> 'Micro, Small and Medium Enterprises',
# 'Statiscs and Programme Implementation' -> 'Statistics and Programme Implementation'
# 'Consumer Affairs' -> 'Consumer Affairs, Food and Public Distribution'
# 'Heavy Industries' -> 'Heavy Industries and Public Enterprises'

# Define merges: secondary -> primary
merges = {
    'Ayush': 'AYUSH',
    'Micro': 'Micro, Small and Medium Enterprises',
    'Statiscs and Programme Implementation': 'Statistics and Programme Implementation',
    'Consumer Affairs': 'Consumer Affairs, Food and Public Distribution',
    'Heavy Industries': 'Heavy Industries and Public Enterprises',
}
secondary_cols = set(merges.keys())

# Build final sector list (primary only)
primary_sectors = [c for c in sector_cols if c not in secondary_cols]

# Process each row: merge secondary into primary, compute sector shares
processed = []
for r in rows:
    mp = {
        'mp_id': r['mp_id'],
        'name': r['name'],
        'party': r['party'],
        'state': r['state'],
        'constituency': r['constituency'],
        'gender': r['gender'],
        'total_questions': int(r['total_questions_parsed']) if r['total_questions_parsed'] else 0
    }
    sector_counts = {}
    for s in primary_sectors:
        val = int(r[s]) if r[s] else 0
        # Add secondary if exists
        for sec, prim in merges.items():
            if prim == s and r.get(sec):
                val += int(r[sec])
        sector_counts[s] = val
    mp['sectors'] = sector_counts
    processed.append(mp)

# Filter MPs with at least 1 question
processed = [m for m in processed if m['total_questions'] > 0]
print(f"MPs with questions: {len(processed)}")

# Compute shares for each MP
for m in processed:
    total = m['total_questions']
    m['shares'] = {s: m['sectors'][s] / total for s in primary_sectors}

# === 1. Global sector distribution ===
global_counts = {s: sum(m['sectors'][s] for m in processed) for s in primary_sectors}
total_global = sum(global_counts.values())
global_shares = {s: global_counts[s] / total_global for s in primary_sectors}
top_sectors = sorted(global_shares, key=global_shares.get, reverse=True)[:15]
print("\nTop 15 sectors globally:")
for s in top_sectors:
    print(f"  {s}: {global_shares[s]*100:.1f}%")

# === 2. State-level sector profiles ===
states = sorted(set(m['state'] for m in processed))
state_data = {}
for state in states:
    mps = [m for m in processed if m['state'] == state]
    n = len(mps)
    if n < 2:
        continue
    # Average share per sector
    avg_shares = {s: statistics.mean(m['shares'][s] for m in mps) for s in primary_sectors}
    # Std dev per sector
    std_shares = {s: statistics.stdev(m['shares'][s] for m in mps) if n > 1 else 0 for s in primary_sectors}
    # Within-state variance (avg of stds across sectors)
    avg_within_std = statistics.mean(std_shares.values())
    # Distinctiveness: deviation from global average
    distinctiveness = {s: avg_shares[s] - global_shares[s] for s in primary_sectors}
    state_data[state] = {
        'n': n,
        'avg_shares': avg_shares,
        'std_shares': std_shares,
        'avg_within_std': avg_within_std,
        'distinctiveness': distinctiveness,
        'mps': mps
    }

print(f"\nStates with 2+ MPs: {len(state_data)}")

# === 3. Which states are most cohesive vs diverse? ===
print("\nState cohesion (lower avg_within_std = more cohesive):")
cohesion_rank = sorted(state_data.items(), key=lambda x: x[1]['avg_within_std'])
for state, d in cohesion_rank[:10]:
    print(f"  {state} (n={d['n']}): avg_within_std={d['avg_within_std']*100:.2f}%")
print("  ...")
for state, d in cohesion_rank[-5:]:
    print(f"  {state} (n={d['n']}): avg_within_std={d['avg_within_std']*100:.2f}%")

# === 4. Most distinctive states (biggest deviation from national average) ===
print("\nMost distinctive states (max absolute distinctiveness):")
for state, d in sorted(state_data.items(), key=lambda x: max(abs(v) for v in x[1]['distinctiveness'].values()), reverse=True)[:10]:
    top_dist = sorted(d['distinctiveness'].items(), key=lambda x: abs(x[1]), reverse=True)[:3]
    print(f"  {state}: {[(s[:25], f'{v*100:+.1f}%') for s, v in top_dist]}")

# === 5. Between-state variance for each sector ===
print("\nSectors with highest between-state variation:")
between_state_var = {}
for s in primary_sectors:
    state_avgs = [d['avg_shares'][s] for d in state_data.values()]
    between_state_var[s] = statistics.stdev(state_avgs) if len(state_avgs) > 1 else 0

for s in sorted(between_state_var, key=between_state_var.get, reverse=True)[:10]:
    print(f"  {s}: std={between_state_var[s]*100:.2f}%")

# === 6. Party patterns ===
parties_major = ['BJP', 'INC', 'DMK', 'YSRCP', 'AITC', 'SS', 'JD(U)', 'BJD', 'BSP']
print("\nParty sector profiles (top distinctive sectors):")
for party in parties_major:
    mps = [m for m in processed if m['party'] == party]
    if len(mps) < 3:
        continue
    avg_shares = {s: statistics.mean(m['shares'][s] for m in mps) for s in primary_sectors}
    distinctiveness = {s: avg_shares[s] - global_shares[s] for s in primary_sectors}
    top3 = sorted(distinctiveness.items(), key=lambda x: x[1], reverse=True)[:3]
    bot3 = sorted(distinctiveness.items(), key=lambda x: x[1])[:2]
    print(f"  {party} (n={len(mps)}): high={[(s[:20], f'{v*100:+.1f}%') for s,v in top3]} low={[(s[:20], f'{v*100:+.1f}%') for s,v in bot3]}")

# Save processed data for visualization
output = {
    'mps': processed,
    'sectors': primary_sectors,
    'global_shares': global_shares,
    'state_data': {state: {
        'n': d['n'],
        'avg_shares': d['avg_shares'],
        'std_shares': d['std_shares'],
        'avg_within_std': d['avg_within_std'],
        'distinctiveness': d['distinctiveness'],
    } for state, d in state_data.items()},
    'between_state_var': between_state_var,
    'top_sectors': top_sectors,
}

with open('/Users/aashima/Desktop/DataViz5/data/curated_analysis.json', 'w') as f:
    json.dump(output, f, indent=2)
print("\nSaved curated_analysis.json")
