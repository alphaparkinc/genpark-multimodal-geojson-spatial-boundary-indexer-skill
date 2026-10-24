from client import MultimodalGeoJsonSpatialBoundaryIndexerClient
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

def main():
    indexer = MultimodalGeoJsonSpatialBoundaryIndexerClient()
    print("=== MULTIMODAL GEOJSON SPATIAL BOUNDARY INDEXER ===")
    
    # Sample GeoJSON delivery geofence (Silicon Valley / SF Bay Area)
    zones = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"zone_id": "ZONE_SF_DOWNTOWN", "name": "San Francisco Metro", "tax_rate": 0.08625, "delivery_tier": "same_day_priority"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-122.52, 37.70],
                        [-122.35, 37.70],
                        [-122.35, 37.83],
                        [-122.52, 37.83],
                        [-122.52, 37.70]
                    ]]
                }
            }
        ]
    }
    
    hubs = [
        {"id": "HUB_SFO", "name": "SFO Airport Air Cargo Hub", "lat": 37.6213, "lon": -122.3790},
        {"id": "HUB_OAK", "name": "East Bay Distribution Center", "lat": 37.7212, "lon": -122.2207}
    ]
    
    # Query point: Market St, San Francisco
    res = indexer.evaluate_location_zones(37.7891, -122.4014, zones, fulfillment_hubs=hubs)
    print(f"Target: ({res['target_coordinates']['lat']}, {res['target_coordinates']['lon']})")
    print(f"Inside Geofence: {res['is_geofenced']}")
    if res['contained_zones']:
        z = res['contained_zones'][0]
        print(f"Zone: {z['zone_name']} | Tier: {z['delivery_tier']} | Tax: {z['tax_rate']*100:.2f}%")
    if res['nearest_fulfillment_hub']:
        h = res['nearest_fulfillment_hub']
        print(f"Nearest Hub: {h['hub_name']} ({h['distance_km']} km, ~{h['estimated_drive_time_mins']} mins)")

if __name__ == "__main__":
    main()
