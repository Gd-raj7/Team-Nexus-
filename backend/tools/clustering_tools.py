"""
CivicNexus AI — Spatio-Temporal Cluster Analysis Engine
Performs multi-dimensional temporal windowing and geo-proximity correlation.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any
from tools.geo_tools import GeoSpatialEngine


class ClusterAnalysisEngine:
    """Spatio-temporal clustering engine for municipal incident correlation."""

    DEFAULT_RADIUS_METERS: float = 180.0
    DEFAULT_TEMPORAL_WINDOW_DAYS: int = 7

    @staticmethod
    def parse_datetime(iso_string: str) -> datetime:
        try:
            return datetime.fromisoformat(iso_string)
        except (ValueError, TypeError):
            return datetime.now()

    @classmethod
    def filter_by_temporal_window(
        cls,
        anchor_timestamp: str,
        window_days: int,
        complaints_pool: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        anchor_dt = cls.parse_datetime(anchor_timestamp)
        lower_bound = anchor_dt - timedelta(days=window_days)

        matched = []
        for c in complaints_pool:
            c_dt = cls.parse_datetime(c.get("timestamp", ""))
            if lower_bound <= c_dt <= anchor_dt:
                matched.append(c)
        return matched

    @classmethod
    def build_spatio_temporal_cluster(
        cls,
        seed_report: Dict[str, Any],
        full_catalog: List[Dict[str, Any]],
        radius_threshold_m: float = DEFAULT_RADIUS_METERS,
        temporal_window_days: int = DEFAULT_TEMPORAL_WINDOW_DAYS,
    ) -> Dict[str, Any]:
        seed_loc = seed_report.get("location", {})
        s_lat = seed_loc.get("latitude", 0.0)
        s_lon = seed_loc.get("longitude", 0.0)
        s_id = seed_report.get("report_id", "")
        s_ts = seed_report.get("timestamp", "")

        anchor_dt = cls.parse_datetime(s_ts)
        w_start = anchor_dt - timedelta(days=temporal_window_days)
        w_end = anchor_dt + timedelta(days=temporal_window_days)

        time_cohort = []
        for item in full_catalog:
            item_dt = cls.parse_datetime(item.get("timestamp", ""))
            if w_start <= item_dt <= w_end and item.get("report_id") != s_id:
                time_cohort.append(item)

        proximate_cohort = GeoSpatialEngine.find_proximate_reports(
            s_lat, s_lon, radius_threshold_m, time_cohort, exclude_id=s_id
        )

        unified_group = [seed_report] + proximate_cohort
        c_lat, c_lon = GeoSpatialEngine.compute_spatial_centroid(unified_group)
        spread_m = GeoSpatialEngine.compute_bounding_radius(unified_group, c_lat, c_lon)

        return {
            "reports": proximate_cohort,
            "center_lat": c_lat,
            "center_lon": c_lon,
            "radius_m": spread_m,
            "time_window_days": temporal_window_days,
            "count": len(proximate_cohort),
            "report_ids": [r.get("report_id") for r in proximate_cohort],
        }


# ── Functional Wrappers for Complete Backward Compatibility ────────────────────

def parse_timestamp(ts: str) -> datetime:
    return ClusterAnalysisEngine.parse_datetime(ts)

def get_recent_complaints(reference_timestamp: str, window_days: int, complaints: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return ClusterAnalysisEngine.filter_by_temporal_window(reference_timestamp, window_days, complaints)

def cluster_complaints(target_report: Dict[str, Any], all_complaints: List[Dict[str, Any]], radius_m: float = 180.0, window_days: int = 7) -> Dict[str, Any]:
    return ClusterAnalysisEngine.build_spatio_temporal_cluster(target_report, all_complaints, radius_m, window_days)
