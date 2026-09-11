import csv

with open('/Users/aashima/Desktop/DataViz5/mp_17th_loksabha_questions_matrix.csv') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

for r in rows[:5]:
    name = r['name']
    ayush1 = r['AYUSH']
    ayush2 = r['Ayush']
    micro1 = r['Micro, Small and Medium Enterprises']
    micro2 = r['Micro']
    stats1 = r['Statistics and Programme Implementation']
    stats2 = r['Statiscs and Programme Implementation']
    consumer1 = r['Consumer Affairs, Food and Public Distribution']
    consumer2 = r['Consumer Affairs']
    heavy1 = r['Heavy Industries and Public Enterprises']
    heavy2 = r['Heavy Industries']
    print(f"{name}:")
    print(f"  AYUSH={ayush1}, Ayush={ayush2}")
    print(f"  Micro,Small={micro1}, Micro={micro2}")
    print(f"  Statistics={stats1}, Statiscs={stats2}")
    print(f"  Consumer Affairs,Food={consumer1}, Consumer Affairs={consumer2}")
    print(f"  Heavy Industries and Public={heavy1}, Heavy Industries={heavy2}")
    print()
