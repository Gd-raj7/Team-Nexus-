import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
INCIDENTS_FILE = os.path.join(DATA_DIR, "incidents.json")

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_priority_incidents():
    """Return top incidents sorted by impact priority and score."""
    incidents = load_json(INCIDENTS_FILE).get("incidents", [])
    active_statuses = {"SUBMITTED", "UNDER_REVIEW", "ASSIGNED", "ACTION_IN_PROGRESS",
                       "AWAITING_RESOLUTION_EVIDENCE", "RESOLUTION_REVIEW"}
    
    active_incidents = [i for i in incidents if i.get("status") in active_statuses]
    
    severity_map = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}
    
    formatted_incidents = []
    for i in active_incidents:
        impact = i.get("impact_score", {})
        priority_str = impact.get("priority", "LOW")
        score_val = impact.get("score", 0)
        
        # Sort key logic: CRITICAL > HIGH > MEDIUM > LOW, then score descending
        # E.g., CRITICAL (4) * 1000 + score
        sort_score = (severity_map.get(priority_str, 0) * 1000) + score_val
        
        # Determine category (first issue type)
        classification = i.get("classification", [])
        category = classification[0] if classification else "UNKNOWN"
        
        # SLA status logic
        sla = i.get("sla", {})
        sla_status = "NORMAL"
        if sla.get("escalated"):
            sla_status = "ESCALATED"
        # Could also check deadline timestamp for "AT_RISK" but this matches requirement logic
        
        formatted_incidents.append({
            "incident_id": i.get("incident_id"),
            "category": category,
            "impact_score": score_val,
            "priority": priority_str,
            "sla_status": sla_status,
            "_sort_score": sort_score
        })
        
    formatted_incidents.sort(key=lambda x: x["_sort_score"], reverse=True)
    formatted_incidents = formatted_incidents[:10]
    
    for fi in formatted_incidents:
        del fi["_sort_score"]
        
    return formatted_incidents
