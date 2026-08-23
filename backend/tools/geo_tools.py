"""
CivicNexus AI — Geospatial Geodesic & Radius Intelligence Engine
Computes geodesic distances, spatial clusters, and incident bounding perimeters.
"""

import math
from typing import List, Dict, Any, Tuple


class GeoSpatialEngine:
    """Enterprise Geodesic computation and proximity indexing service."""
    
    EARTH_RADIUS_METERS: float = 6371000.0

    @classmethod
    def haversine_distance(cls, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculates Great-Circle geodesic distance in meters between two coordinates.
        """
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        sin_dphi = math.sin(delta_phi / 2.0)
        sin_dlam = math.sin(delta_lambda / 2.0)

        a = sin_dphi * sin_dphi + math.cos(phi1) * math.cos(phi2) * sin_dlam * sin_dlam
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

        return cls.EARTH_RADIUS_METERS * c

    @classmethod
    def find_proximate_reports(
        cls,
        origin_lat: float,
        origin_lon: float,
        threshold_radius_m: float,
        reports_pool: List[Dict[str, Any]],
        exclude_id: str = "",
    ) -> List[Dict[str, Any]]:
        """
        Discovers all incident reports falling within a spatial radial envelope.
        """
        proximate: List[Dict[str, Any]] = []
        for r in reports_pool:
            loc = r.get("location", {})
            r_lat = loc.get("latitude", 0.0)
            r_lon = loc.get("longitude", 0.0)

            if r_lat == 0.0 and r_lon == 0.0:
                continue

            dist = cls.haversine_distance(origin_lat, origin_lon, r_lat, r_lon)
            if dist <= threshold_radius_m and r.get("report_id") != exclude_id:
                cloned = dict(r)
                cloned["_distance_m"] = round(dist, 1)
                proximate.append(cloned)

        proximate.sort(key=lambda x: x["_distance_m"])
        return proximate

    @classmethod
    def compute_spatial_centroid(cls, reports: List[Dict[str, Any]]) -> Tuple[float, float]:
        """Calculates geographic center of gravity for a multi-point cluster."""
        if not reports:
            return (0.0, 0.0)

        lats = [r.get("location", {}).get("latitude", 0.0) for r in reports]
        lons = [r.get("location", {}).get("longitude", 0.0) for r in reports]

        valid_lats = [lat for lat in lats if lat != 0.0]
        valid_lons = [lon for lon in lons if lon != 0.0]

        if not valid_lats:
            return (0.0, 0.0)

        return (sum(valid_lats) / len(valid_lats), sum(valid_lons) / len(valid_lons))

    @classmethod
    def compute_bounding_radius(
        cls,
        reports: List[Dict[str, Any]],
        center_lat: float,
        center_lon: float,
    ) -> float:
        """Determines maximum spread distance from centroid to outer perimeter."""
        max_spread = 0.0
        for r in reports:
            loc = r.get("location", {})
            d = cls.haversine_distance(
                center_lat, center_lon, loc.get("latitude", 0.0), loc.get("longitude", 0.0)
            )
            if d > max_spread:
                max_spread = d
        return round(max_spread, 1)


# ── Functional Wrappers for Complete Backward Compatibility ────────────────────

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    return GeoSpatialEngine.haversine_distance(lat1, lon1, lat2, lon2)


def get_nearby_complaints(lat: float, lon: float, radius_m: float, complaints: List[Dict[str, Any]], exclude_id: str = "") -> List[Dict[str, Any]]:
    return GeoSpatialEngine.find_proximate_reports(lat, lon, radius_m, complaints, exclude_id)


def calculate_cluster_center(complaints: List[Dict[str, Any]]) -> tuple:
    return GeoSpatialEngine.compute_spatial_centroid(complaints)


def calculate_cluster_radius(complaints: List[Dict[str, Any]], center_lat: float, center_lon: float) -> float:
    return GeoSpatialEngine.compute_bounding_radius(complaints, center_lat, center_lon)
