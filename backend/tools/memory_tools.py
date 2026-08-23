"""
CivicNexus AI — Spatial Memory & Chronic Recurrence Intelligence Engine
Analyzes multi-month historical complaint logs, past municipal interventions,
and identifies chronic urban infrastructure vulnerability hotspots.
"""

from typing import List, Dict, Any, Tuple
from tools.geo_tools import GeoSpatialEngine
from tools.clustering_tools import parse_timestamp
from datetime import datetime, timedelta


class SpatialMemoryEngine:
    """Historical spatial memory and chronic recurrence analysis engine."""

    RECURRENCE_RADIUS_METERS: float = 250.0

    @classmethod
    def query_location_history(
        cls,
        target_lat: float,
        target_lon: float,
        complaints_pool: List[Dict[str, Any]],
        historical_incidents: List[Dict[str, Any]],
        radius_m: float = RECURRENCE_RADIUS_METERS,
    ) -> Dict[str, Any]:
        """
        Retrieves all past citizen complaints and incidents within radial vicinity.
        """
        nearby_complaints = []
        for c in complaints_pool:
            loc = c.get("location", {})
            c_lat = loc.get("latitude", 0.0)
            c_lon = loc.get("longitude", 0.0)
            dist = GeoSpatialEngine.haversine_distance(target_lat, target_lon, c_lat, c_lon)
            if dist <= radius_m:
                item = dict(c)
                item["_distance_m"] = round(dist, 1)
                nearby_complaints.append(item)

        # Sort chronologically
        nearby_complaints.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

        # Identify linked or historical incidents
        nearby_incidents = []
        for inc in historical_incidents:
            c_info = inc.get("cluster", {})
            c_lat = c_info.get("center_lat", 0.0)
            c_lon = c_info.get("center_lon", 0.0)
            if c_lat != 0.0 and c_lon != 0.0:
                dist = GeoSpatialEngine.haversine_distance(target_lat, target_lon, c_lat, c_lon)
                if dist <= radius_m:
                    nearby_incidents.append({
                        "incident_id": inc.get("incident_id"),
                        "status": inc.get("status"),
                        "created_at": inc.get("created_at"),
                        "root_cause": inc.get("root_cause", {}).get("hypothesis", ""),
                        "distance_m": round(dist, 1)
                    })

        # Calculate recurrence index (0 to 100)
        recurrence_count = len(nearby_complaints)
        recurrence_score = min(recurrence_count * 12.5, 100.0)

        # Extract past interventions
        past_interventions = []
        for inc in historical_incidents:
            plan = inc.get("response_plan", {})
            if plan.get("approved"):
                for step in plan.get("steps", []):
                    past_interventions.append({
                        "incident_id": inc.get("incident_id"),
                        "department": step.get("department_name", step.get("department")),
                        "action": step.get("action"),
                        "approved_at": plan.get("approved_at", inc.get("created_at")),
                        "status": inc.get("status"),
                    })

        # Synthesize civic memory insight
        category_counts: Dict[str, int] = {}
        for c in nearby_complaints:
            # Check description keywords for categories
            desc = c.get("description", "").lower()
            if "leak" in desc or "water" in desc:
                category_counts["Water Infrastructure"] = category_counts.get("Water Infrastructure", 0) + 1
            if "pothole" in desc or "road" in desc:
                category_counts["Pavement Integrity"] = category_counts.get("Pavement Integrity", 0) + 1
            if "drain" in desc or "flood" in desc:
                category_counts["Storm Drainage"] = category_counts.get("Storm Drainage", 0) + 1
            if "wire" in desc or "electric" in desc:
                category_counts["Power Grid"] = category_counts.get("Power Grid", 0) + 1

        top_issue = max(category_counts, key=category_counts.get) if category_counts else "General Infrastructure"

        if recurrence_count >= 5:
            insight = (
                f"Chronic infrastructure stress detected: {recurrence_count} complaints registered in this 250m radius. "
                f"Predominant issue: {top_issue}. High probability of sub-surface foundation decay. "
                "Recommend capital infrastructure overhaul rather than isolated surface repairs."
            )
        elif recurrence_count >= 2:
            insight = (
                f"Moderate cluster activity: {recurrence_count} related historical reports recorded. "
                "Multi-department synchronization required to prevent recurring failure cycles."
            )
        else:
            insight = "First recorded incident occurrence at this coordinate. Baseline standard response recommended."

        return {
            "target_coordinates": {"latitude": target_lat, "longitude": target_lon},
            "radius_m": radius_m,
            "total_historical_reports": recurrence_count,
            "chronic_recurrence_score": recurrence_score,
            "nearby_complaints": nearby_complaints[:10],
            "historical_incidents": nearby_incidents,
            "past_interventions": past_interventions[:5],
            "civic_memory_insight": insight,
            "primary_vulnerability": top_issue,
        }

    @classmethod
    def discover_citywide_hotspots(
        cls,
        complaints_pool: List[Dict[str, Any]],
        incidents_pool: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Clusters citywide complaints to discover top active incident hotspots.
        """
        zone_groups: Dict[str, List[Dict[str, Any]]] = {}
        for c in complaints_pool:
            ward = c.get("ward") or c.get("location", {}).get("ward", "Unassigned Zone")
            zone_groups.setdefault(ward, []).append(c)

        hotspots = []
        for zone_name, group in zone_groups.items():
            if not group:
                continue

            center_lat, center_lon = GeoSpatialEngine.compute_spatial_centroid(group)
            count = len(group)

            # Determine risk tier
            if count >= 8:
                risk = "CRITICAL"
            elif count >= 4:
                risk = "HIGH"
            elif count >= 2:
                risk = "MODERATE"
            else:
                risk = "LOW"

            # Check if any active incidents exist in this zone
            zone_incidents = [
                i for i in incidents_pool
                if any(c_id in [r.get("report_id") for r in group] for c_id in i.get("connected_reports", []))
            ]

            hotspots.append({
                "zone": zone_name,
                "center_lat": round(center_lat, 4),
                "center_lon": round(center_lon, 4),
                "active_reports_count": count,
                "risk_tier": risk,
                "active_incidents_count": len(zone_incidents),
                "sample_address": group[0].get("location", {}).get("address", zone_name),
            })

        hotspots.sort(key=lambda x: x["active_reports_count"], reverse=True)
        return hotspots
