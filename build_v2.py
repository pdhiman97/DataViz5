import json

# Load data
with open('/Users/aashima/Desktop/DataViz5/data/loksabha-questions/curated/viz_data_v2.json') as f:
    data = json.load(f)

# Load images
with open('/Users/aashima/Desktop/DataViz5/data/loksabha-questions/curated/mp_images.json') as f:
    imgs = json.load(f)

# Filter out None values
imgs_clean = {k: v for k, v in imgs.items() if v}
print(f"MPs: {len(data['mps'])}, Images: {len(imgs_clean)}")

# Read template
with open('/Users/aashima/Desktop/DataViz5/outcome/loksabha-questions/viz_template.html') as f:
    template = f.read()

# Inject data
data_str = json.dumps(data, separators=(',', ':'))
imgs_str = json.dumps(imgs_clean, separators=(',', ':'))

html = template.replace('__DATA_PLACEHOLDER__', f'const DATA = {data_str};')
html = html.replace('__IMGS_PLACEHOLDER__', imgs_str)

with open('/Users/aashima/Desktop/DataViz5/outcome/loksabha-questions/viz_v2.html', 'w') as f:
    f.write(html)

print(f"Written viz_v2.html: {len(html)//1024} KB")
