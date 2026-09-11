import json, math

def simplify_points(pts, tol=0.015):
    if len(pts) <= 3:
        return pts
    # Simple radial / Douglas-Peucker approximation
    simplified = [pts[0]]
    for i in range(1, len(pts)-1):
        prev = simplified[-1]
        curr = pts[i]
        dist = math.hypot(curr[0]-prev[0], curr[1]-prev[1])
        if dist > tol:
            simplified.append(curr)
    simplified.append(pts[-1])
    return simplified

def simplify_geom(geom, tol=0.015):
    gtype = geom.get('type')
    coords = geom.get('coordinates', [])
    if gtype == 'Polygon':
        new_coords = [simplify_points(ring, tol) for ring in coords]
        return {'type': gtype, 'coordinates': new_coords}
    elif gtype == 'MultiPolygon':
        new_coords = [[simplify_points(ring, tol) for ring in poly] for poly in coords]
        return {'type': gtype, 'coordinates': new_coords}
    return geom

with open('/Users/aashima/Desktop/DataViz5/data/loksabha-questions/curated/india_states.geojson') as f:
    data = json.load(f)

simplified_features = []
for feat in data.get('features', []):
    state_name = feat.get('properties', {}).get('NAME_1') or feat.get('properties', {}).get('st_nm') or 'State'
    geom = feat.get('geometry')
    if geom:
        sim_geom = simplify_geom(geom, tol=0.02)
        simplified_features.append({
            'type': 'Feature',
            'properties': {'name': state_name},
            'geometry': sim_geom
        })

simplified_geojson = {
    'type': 'FeatureCollection',
    'features': simplified_features
}

with open('/Users/aashima/Desktop/DataViz5/data/loksabha-questions/curated/india_states_simplified.json', 'w') as f:
    json.dump(simplified_geojson, f, separators=(',', ':'))

orig_size = len(json.dumps(data))
new_size = len(json.dumps(simplified_geojson, separators=(',', ':')))
print(f"Original GeoJSON: {orig_size//1024} KB -> Simplified: {new_size//1024} KB")
