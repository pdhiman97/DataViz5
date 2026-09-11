import json

# Read the visualization data
with open('/Users/aashima/Desktop/DataViz5/data/loksabha-questions/curated/viz_data.json') as f:
    data = json.load(f)

# Minify the data
data_str = json.dumps(data, separators=(',', ':'))

print(f"Data size: {len(data_str):,} chars ({len(data_str)//1024} KB)")
print(f"MPs: {data['total_mps']}, States: {data['total_states']}")
