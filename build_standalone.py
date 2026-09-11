import json

with open('/Users/aashima/Desktop/DataViz5/data/loksabha-questions/curated/viz_data.json') as f:
    data = json.load(f)

data_str = json.dumps(data, separators=(',', ':'))

# Read HTML, CSS, JS
with open('/Users/aashima/Desktop/DataViz5/outcome/loksabha-questions/index.html') as f:
    html = f.read()
with open('/Users/aashima/Desktop/DataViz5/outcome/loksabha-questions/styles.css') as f:
    css = f.read()
with open('/Users/aashima/Desktop/DataViz5/outcome/loksabha-questions/script.js') as f:
    js = f.read()

# Build self-contained HTML
# Remove external font link (works online but not needed for structure check)
# Replace script references with inline content

standalone = html

# Remove the stylesheet link and inline it
standalone = standalone.replace(
    '  <link rel="stylesheet" href="styles.css">',
    f'  <style>\n{css}\n  </style>'
)

# Remove the data.js and script.js script tags, add inline data + inline script
standalone = standalone.replace(
    '''  <script src="https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"></script>
  <script src="data.js"></script>
  <script src="script.js"></script>''',
    f'''  <script src="https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"></script>
  <script>const VIZ_DATA={data_str};</script>
  <script>
{js}
  </script>'''
)

with open('/Users/aashima/Desktop/DataViz5/outcome/loksabha-questions/index.html', 'w') as f:
    f.write(standalone)

print(f"Written self-contained HTML: {len(standalone):,} chars ({len(standalone)//1024} KB)")
