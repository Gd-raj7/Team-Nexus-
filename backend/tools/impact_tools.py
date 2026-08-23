"""
CivicNexus AI — Civic Threat Matrix & Public Severity Scoring System
Evaluates systemic risks, population exposure, critical infrastructure proximity,
and compounding secondary cascading hazards into a 0-100 severity index.
"""

from typing import Dict, Any, List


class CivicThreatMatrix:
    """Multi-dimensional public infrastructure risk assessment engine."""

    FACTOR_WEIGHTS: Dict[str, float] = {
        "severity": 0.30,
        "infrastructure_proximity": 0.20,
        "people_affected": 0.15,
        "duration": 0.10,
        "repeat_reports": 0.10,
        "secondary_risk": 0.15,
    }

    SEVERITY_BENCHMARKS: Dict[str, float] = {
        "CRITICAL": 100.0,
        "HIGH": 80.0,
        "MEDIUM": 50.0,
        "LOW": 25.0,
    }

    CRITICAL_ANCHOR_KEYWORDS: List[str] = [
        "school", "hospital", "temple", "church", "mosque", "station",
        "bus stop", "metro", "market", "playground", "college", "university",
    ]

    SECONDARY_HAZARD_RATING: Dict[str, float] = {
        "EXPOSED_WIRES": 95.0,
        "SEWAGE_OVERFLOW": 80.0,
        "WATERLOGGING": 65.0,
        "WATER_LEAKAGE": 55.0,
        "POTHOLE": 60.0,
        "ROAD_DAMAGE": 50.0,
        "DRAIN_BLOCKAGE": 55.0,
        "DRAINAGE_PROBLEM": 50.0,
        "GARBAGE_OVERFLOW": 45.0,
        "BROKEN_STREETLIGHT": 40.0,
    }

    @classmethod
    def evaluate_severity_subscore(cls, perception_data: List[Dict[str, Any]]) -> float:
        if not perception_data:
            return 0.0
        peak = "LOW"
        for p in perception_data:
            val = p.get("severity", "LOW")
            if cls.SEVERITY_BENCHMARKS.get(val, 0.0) > cls.SEVERITY_BENCHMARKS.get(peak, 0.0):
                peak = val
        return cls.SEVERITY_BENCHMARKS.get(peak, 25.0)

    @classmethod
    def evaluate_proximity_subscore(cls, reports: List[Dict[str, Any]]) -> float:
        baseline = 30.0
        for r in reports:
            text = (r.get("description", "") + " " + r.get("location", {}).get("address", "")).lower()
            for anchor in cls.CRITICAL_ANCHOR_KEYWORDS:
                if anchor in text:
                    baseline = max(baseline, 85.0)
                    break
        return min(baseline, 100.0)

    @classmethod
    def evaluate_exposure_subscore(cls, count: int, text_corpus: List[str]) -> float:
        base = min(count * 15.0, 60.0)
        density_terms = ["pedestrian", "commuter", "resident", "children", "elderly", "bus", "traffic", "market", "colony", "society", "building"]
        boost = 0.0
        for doc in text_corpus:
            d_low = doc.lower()
            for t in density_terms:
                if t in d_low:
                    boost = max(boost, 30.0)
                    break
        return min(base + boost, 100.0)

    @classmethod
    def evaluate_duration_subscore(cls, days: float) -> float:
        if days <= 1.0:
            return 20.0
        if days <= 3.0:
            return 50.0
        if days <= 7.0:
            return 70.0
        if days <= 14.0:
            return 85.0
        return 100.0

    @classmethod
    def evaluate_recurrence_subscore(cls, count: int) -> float:
        if count <= 1:
            return 10.0
        if count <= 2:
            return 30.0
        if count <= 4:
            return 60.0
        if count <= 6:
            return 80.0
        return 100.0

    @classmethod
    def evaluate_secondary_hazard_subscore(cls, issues: List[str]) -> float:
        if not issues:
            return 0.0
        peak_hazard = max((cls.SECONDARY_HAZARD_RATING.get(i, 25.0) for i in issues), default=0.0)
        cascade_multi = min(len(set(issues)) * 5.0, 20.0)
        return min(peak_hazard + cascade_multi, 100.0)

    @classmethod
    def compute_composite_impact(
        cls,
        perception_results: List[Dict[str, Any]],
        reports: List[Dict[str, Any]],
        time_span_days: float = 3.0,
    ) -> Dict[str, Any]:
        texts = [r.get("description", "") for r in reports]
        issue_set = [p.get("issue_type", "") for p in perception_results]

        s_score = cls.evaluate_severity_subscore(perception_results)
        p_score = cls.evaluate_proximity_subscore(reports)
        e_score = cls.evaluate_exposure_subscore(len(reports), texts)
        d_score = cls.evaluate_duration_subscore(time_span_days)
        r_score = cls.evaluate_recurrence_subscore(len(reports))
        h_score = cls.evaluate_secondary_hazard_subscore(issue_set)

        composite = (
            s_score * cls.FACTOR_WEIGHTS["severity"] +
            p_score * cls.FACTOR_WEIGHTS["infrastructure_proximity"] +
            e_score * cls.FACTOR_WEIGHTS["people_affected"] +
            d_score * cls.FACTOR_WEIGHTS["duration"] +
            r_score * cls.FACTOR_WEIGHTS["repeat_reports"] +
            h_score * cls.FACTOR_WEIGHTS["secondary_risk"]
        )
        composite = round(composite, 1)

        if composite >= 76.0:
            priority = "CRITICAL"
        elif composite >= 51.0:
            priority = "HIGH"
        elif composite >= 26.0:
            priority = "MEDIUM"
        else:
            priority = "LOW"

        return {
            "score": composite,
            "priority": priority,
            "breakdown": {
                "severity_score": round(s_score, 1),
                "infrastructure_proximity": round(p_score, 1),
                "people_affected": round(e_score, 1),
                "duration": round(d_score, 1),
                "repeat_reports": round(r_score, 1),
                "secondary_risk": round(h_score, 1),
            },
        }


# ── Functional Wrappers for Complete Backward Compatibility ────────────────────

WEIGHTS = CivicThreatMatrix.FACTOR_WEIGHTS
SEVERITY_SCORES = CivicThreatMatrix.SEVERITY_BENCHMARKS
HIGH_PROXIMITY_KEYWORDS = CivicThreatMatrix.CRITICAL_ANCHOR_KEYWORDS
SECONDARY_RISK_MAP = CivicThreatMatrix.SECONDARY_HAZARD_RATING

def calculate_severity_score(perception_results: List[Dict]) -> float:
    return CivicThreatMatrix.evaluate_severity_subscore(perception_results)

def calculate_infrastructure_proximity(reports: List[Dict]) -> float:
    return CivicThreatMatrix.evaluate_proximity_subscore(reports)

def calculate_people_affected(report_count: int, descriptions: List[str]) -> float:
    return CivicThreatMatrix.evaluate_exposure_subscore(report_count, descriptions)

def calculate_duration_score(time_span_days: float) -> float:
    return CivicThreatMatrix.evaluate_duration_subscore(time_span_days)

def calculate_repeat_reports_score(report_count: int) -> float:
    return CivicThreatMatrix.evaluate_recurrence_subscore(report_count)

def calculate_secondary_risk(issue_types: List[str]) -> float:
    return CivicThreatMatrix.evaluate_secondary_hazard_subscore(issue_types)

def calculate_impact_score(perception_results: List[Dict], reports: List[Dict], time_span_days: float = 3.0) -> Dict[str, Any]:
    return CivicThreatMatrix.compute_composite_impact(perception_results, reports, time_span_days)
