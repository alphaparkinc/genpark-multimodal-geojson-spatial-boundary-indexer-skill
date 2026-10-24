import sys, json
from client import MultimodalGeoJsonSpatialBoundaryIndexerClient
sys.stdout.reconfigure(encoding='utf-8')

def handle_mcp():
    client = MultimodalGeoJsonSpatialBoundaryIndexerClient()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps({"status": "ready", "skill": "genpark-multimodal-geojson-spatial-boundary-indexer-skill"}))
        return
    req = json.loads(sys.stdin.read() or "{}")
    lat = float(req.get("lat", 37.7749))
    lon = float(req.get("lon", -122.4194))
    zones = req.get("zones", {"type": "FeatureCollection", "features": []})
    res = client.evaluate_location_zones(lat, lon, zones)
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    handle_mcp()
