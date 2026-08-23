"""
CivicNexus AI — Civic Memory & Historical Intelligence Agent
Analyzes historical location records, evaluates chronic recurrence patterns,
and generates preventive infrastructure maintenance recommendations.
"""

from typing import Dict, Any, List
from tools.memory_tools import SpatialMemoryEngine


class CivicMemoryAgent:
    """Agent responsible for spatial memory, chronic failure auditing, and long-term civic insights."""

    @classmethod
    async def evaluate_memory_profile(
        cls,
        incident_context: Dict[str, Any],
        complaints_pool: List[Dict[str, Any]],
        all_incidents: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        cluster = incident_context.get("cluster", {})
        c_lat = cluster.get("center_lat", 0.0)
        c_lon = cluster.get("center_lon", 0.0)

        if c_lat == 0.0 and c_lon == 0.0:
            connected = incident_context.get("connected_reports", [])
            for c in complaints_pool:
                if c.get("report_id") in connected:
                    loc = c.get("location", {})
                    c_lat = loc.get("latitude", 0.0)
                    c_lon = loc.get("longitude", 0.0)
                    break

        memory_data = SpatialMemoryEngine.query_location_history(
            target_lat=c_lat,
            target_lon=c_lon,
            complaints_pool=complaints_pool,
            historical_incidents=all_incidents,
        )

        return memory_data


# Functional wrapper
async def evaluate_memory(incident_context: Dict[str, Any], complaints_pool: List[Dict[str, Any]], all_incidents: List[Dict[str, Any]]) -> Dict[str, Any]:
    return await CivicMemoryAgent.evaluate_memory_profile(incident_context, complaints_pool, all_incidents)
