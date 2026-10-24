import math, sys
sys.stdout.reconfigure(encoding='utf-8')

class MultimodalGeoJsonSpatialBoundaryIndexerClient:
    """
    Pure Python spatial calculation engine. Computes Ray-Casting Point-in-Polygon (PIP),
    hierarchical bounding box containment, and Haversine great-circle distances.
    """
    def __init__(self):
        self.earth_radius_km = 6371.0

    def haversine_distance(self, lat1, lon1, lat2, lon2):
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        d_phi = math.radians(lat2 - lat1)
        d_lambda = math.radians(lon2 - lon1)

        a = math.sin(d_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * (math.sin(d_lambda / 2.0) ** 2)
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        return self.earth_radius_km * c

    def point_in_polygon(self, lat, lon, polygon_coords):
        # Ray casting algorithm
        # polygon_coords: list of [lon, lat] or [lat, lon] tuples
        n = len(polygon_coords)
        inside = False
        p1_lon, p1_lat = polygon_coords[0][0], polygon_coords[0][1]
        for i in range(1, n + 1):
            p2_lon, p2_lat = polygon_coords[i % n][0], polygon_coords[i % n][1]
            if lat > min(p1_lat, p2_lat):
                if lat <= max(p1_lat, p2_lat):
                    if lon <= max(p1_lon, p2_lon):
                        if p1_lat != p2_lat:
                            x_inters = (lat - p1_lat) * (p2_lon - p1_lon) / (p2_lat - p1_lat) + p1_lon
                        if p1_lon == p2_lon or lon <= x_inters:
                            inside = not inside
            p1_lon, p1_lat = p2_lon, p2_lat
        return inside

    def evaluate_location_zones(self, target_lat, target_lon, zones_geojson, fulfillment_hubs=None):
        matched_zones = []
        for feature in zones_geojson.get("features", []):
            prop = feature.get("properties", {})
            geom = feature.get("geometry", {})
            geom_type = geom.get("type", "")
            
            if geom_type == "Polygon":
                coords = geom.get("coordinates", [[]])[0]
                if self.point_in_polygon(target_lat, target_lon, coords):
                    matched_zones.append({
                        "zone_id": prop.get("zone_id", "unknown"),
                        "zone_name": prop.get("name", "Unnamed Zone"),
                        "tax_rate": prop.get("tax_rate", 0.0),
                        "delivery_tier": prop.get("delivery_tier", "standard")
                    })

        # Calculate nearest fulfillment hub
        nearest_hub = None
        min_distance = 1e9
        if fulfillment_hubs:
            for hub in fulfillment_hubs:
                dist = self.haversine_distance(target_lat, target_lon, hub["lat"], hub["lon"])
                if dist < min_distance:
                    min_distance = dist
                    nearest_hub = {
                        "hub_id": hub["id"],
                        "hub_name": hub["name"],
                        "distance_km": round(dist, 2),
                        "estimated_drive_time_mins": int(dist * 1.4 + 10)
                    }

        return {
            "status": "success",
            "target_coordinates": {"lat": target_lat, "lon": target_lon},
            "is_geofenced": len(matched_zones) > 0,
            "contained_zones": matched_zones,
            "nearest_fulfillment_hub": nearest_hub
        }
