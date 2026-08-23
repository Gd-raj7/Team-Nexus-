"""
CivicNexus AI — Verification Protocol & Post-Resolution Audit Engine
Enforces spatial radius geofencing, temporal validation, and post-resolution anomaly detection.
"""

from typing import List, Dict, Any
from tools.geo_tools import GeoSpatialEngine
from tools.clustering_tools import parse_timestamp


class VerificationProtocolEngine:
    """Enterprise verification service for dual-beat evidence validation."""

    DEFAULT_RADIUS_TOLERANCE_M: float = 100.0
    COMPLAINT_MONITOR_RADIUS_M: float = 200.0

    @classmethod
    def validate_spatial_proximity(
        cls,
        origin_lat: float,
        origin_lon: float,
        proof_lat: float,
        proof_lon: float,
        tolerance_m: float = DEFAULT_RADIUS_TOLERANCE_M,
    ) -> Dict[str, Any]:
        dist = GeoSpatialEngine.haversine_distance(origin_lat, origin_lon, proof_lat, proof_lon)
        return {
            "distance_m": round(dist, 1),
            "within_threshold": dist <= tolerance_m,
            "threshold_m": tolerance_m,
        }

    @classmethod
    def audit_post_resolution_signals(
        cls,
        site_lat: float,
        site_lon: float,
        timestamp_boundary: str,
        complaints_pool: List[Dict[str, Any]],
        radius_m: float = COMPLAINT_MONITOR_RADIUS_M,
    ) -> List[Dict[str, Any]]:
        threshold_dt = parse_timestamp(timestamp_boundary)
        anomalies = []

        for c in complaints_pool:
            c_dt = parse_timestamp(c.get("timestamp", ""))
            if c_dt <= threshold_dt:
                continue

            loc = c.get("location", {})
            d = GeoSpatialEngine.haversine_distance(
                site_lat, site_lon, loc.get("latitude", 0.0), loc.get("longitude", 0.0)
            )
            if d <= radius_m:
                anomaly = dict(c)
                anomaly["_distance_m"] = round(d, 1)
                anomalies.append(anomaly)

        return anomalies

    @classmethod
    def evaluate_resolution_protocol(
        cls,
        incident_context: Dict[str, Any],
        complaints_pool: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        resolution = incident_context.get("resolution", {})
        after_gps = resolution.get("after_gps", {})

        cluster = incident_context.get("cluster", {})
        ref_lat = cluster.get("center_lat", 0.0)
        ref_lon = cluster.get("center_lon", 0.0)

        if ref_lat == 0.0 and ref_lon == 0.0:
            connected = incident_context.get("connected_reports", [])
            for c in complaints_pool:
                if c.get("report_id") in connected:
                    loc = c.get("location", {})
                    ref_lat = loc.get("latitude", 0.0)
                    ref_lon = loc.get("longitude", 0.0)
                    break

        proof_lat = after_gps.get("latitude", 0.0)
        proof_lon = after_gps.get("longitude", 0.0)

        spatial_eval = cls.validate_spatial_proximity(ref_lat, ref_lon, proof_lat, proof_lon)

        if not spatial_eval["within_threshold"]:
            return {
                "verification_result": "LOCATION_MISMATCH",
                "verification_details": (
                    f"Resolution evidence location is {spatial_eval['distance_m']}m "
                    f"from the incident site (threshold: {spatial_eval['threshold_m']}m). "
                    "The submitted photo does not appear to be from the correct location. "
                    "Please submit evidence from the actual incident site. "
                    "DO NOT CLOSE this incident."
                ),
                "confidence": 0.15,
                "location_check": spatial_eval,
                "new_complaints": [],
            }

        submitted_at = resolution.get("submitted_at", "")
        recurrence = []
        if submitted_at:
            recurrence = cls.audit_post_resolution_signals(
                ref_lat, ref_lon, submitted_at, complaints_pool
            )

        if recurrence:
            return {
                "verification_result": "POSSIBLE_FAILED_RESOLUTION",
                "verification_details": (
                    f"Location verified (within {spatial_eval['distance_m']}m), "
                    f"but {len(recurrence)} new complaint(s) have been filed "
                    f"near this location since the resolution was submitted. "
                    "This may indicate the issue has not been fully resolved. "
                    "Physical inspection recommended before closing."
                ),
                "confidence": 0.45,
                "location_check": spatial_eval,
                "new_complaints": [c.get("report_id") for c in recurrence],
            }

        return {
            "verification_result": "RESOLUTION_VERIFIED",
            "verification_details": (
                f"Resolution evidence verified. Location match confirmed "
                f"(within {spatial_eval['distance_m']}m of incident site). "
                "No new complaints detected post-resolution. "
                "Issue appears to be resolved."
            ),
            "confidence": 0.88,
            "location_check": spatial_eval,
            "new_complaints": [],
        }


# ── Functional Wrappers for Complete Backward Compatibility ────────────────────

def verify_location(before_lat: float, before_lon: float, after_lat: float, after_lon: float, threshold_m: float = 100.0) -> Dict[str, Any]:
    return VerificationProtocolEngine.validate_spatial_proximity(before_lat, before_lon, after_lat, after_lon, threshold_m)

def check_new_complaints(lat: float, lon: float, since_timestamp: str, complaints: List[Dict[str, Any]], radius_m: float = 200.0) -> List[Dict[str, Any]]:
    return VerificationProtocolEngine.audit_post_resolution_signals(lat, lon, since_timestamp, complaints, radius_m)

def verify_resolution_evidence(incident: Dict[str, Any], complaints: List[Dict[str, Any]]) -> Dict[str, Any]:
    return VerificationProtocolEngine.evaluate_resolution_protocol(incident, complaints)
