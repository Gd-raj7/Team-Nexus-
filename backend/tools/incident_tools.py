"""
CivicNexus AI — Incident State Machine & Multi-Report Classification Matrix
Validates incident lifecycle transitions and categorizes clustered signals.
"""

from typing import List, Dict, Any, Set


class IncidentStateMatrix:
    """Finite State Machine (FSM) and cluster categorizer for municipal tickets."""

    VALID_TRANSITIONS: Dict[str, Set[str]] = {
        "SUBMITTED": {"UNDER_REVIEW"},
        "UNDER_REVIEW": {"ASSIGNED", "SUBMITTED"},
        "ASSIGNED": {"ACTION_IN_PROGRESS", "UNDER_REVIEW"},
        "ACTION_IN_PROGRESS": {"AWAITING_RESOLUTION_EVIDENCE", "ESCALATED"},
        "AWAITING_RESOLUTION_EVIDENCE": {"RESOLUTION_REVIEW", "ESCALATED"},
        "RESOLUTION_REVIEW": {"RESOLVED", "REOPENED", "AWAITING_RESOLUTION_EVIDENCE"},
        "RESOLVED": {"REOPENED"},
        "REOPENED": {"UNDER_REVIEW", "ESCALATED"},
        "ESCALATED": {"UNDER_REVIEW", "ASSIGNED"},
    }

    @classmethod
    def is_transition_permissible(cls, source_state: str, target_state: str) -> bool:
        allowed = cls.VALID_TRANSITIONS.get(source_state, set())
        return target_state in allowed

    @classmethod
    def evaluate_cluster_topology(
        cls,
        total_reports: int,
        distinct_issue_types_count: int,
        primary_category_frequency: int,
    ) -> str:
        if total_reports <= 1:
            return "INDEPENDENT_COMPLAINTS"

        if distinct_issue_types_count == 1 and primary_category_frequency > 1:
            return "DUPLICATE_REPORTS"

        if distinct_issue_types_count >= 4 or total_reports >= 5:
            return "HIGH_CONFIDENCE_CONNECTED_INCIDENT"

        if distinct_issue_types_count >= 2:
            return "POSSIBLE_CONNECTED_INCIDENT"

        return "DUPLICATE_REPORTS"

    @classmethod
    def extract_distinct_categories(cls, perception_data: List[Dict[str, Any]]) -> List[str]:
        return list(set(p.get("issue_type", "") for p in perception_data if p.get("issue_type")))


# ── Functional Wrappers for Complete Backward Compatibility ────────────────────

STATUS_TRANSITIONS = {k: list(v) for k, v in IncidentStateMatrix.VALID_TRANSITIONS.items()}

def can_transition(current_status: str, new_status: str) -> bool:
    return IncidentStateMatrix.is_transition_permissible(current_status, new_status)

def classify_cluster(report_count: int, unique_issue_types: int, same_type_count: int) -> str:
    return IncidentStateMatrix.evaluate_cluster_topology(report_count, unique_issue_types, same_type_count)

def get_unique_issue_types(perception_results: List[Dict]) -> List[str]:
    return IncidentStateMatrix.extract_distinct_categories(perception_results)
