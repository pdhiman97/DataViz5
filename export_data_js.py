import json

with open('/Users/aashima/Desktop/DataViz5/data/loksabha-questions/curated/viz_data.json') as f:
    data = json.load(f)

data_str = json.dumps(data, separators=(',', ':'))

js_data = f"const VIZ_DATA = {data_str};"

with open('/Users/aashima/Desktop/DataViz5/outcome/loksabha-questions/data.js', 'w') as f:
    f.write(js_data)

print(f"Written data.js: {len(js_data):,} chars")
