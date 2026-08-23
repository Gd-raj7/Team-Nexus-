import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
CIVIC_MEMORY_FILE = os.path.join(DATA_DIR, "civic_memory.json")
INCIDENTS_FILE = os.path.join(DATA_DIR, "incidents.json")
COMPLAINTS_FILE = os.path.join(DATA_DIR, "complaints.json")

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def calculate_location_memory(location_id: str) -> dict:
    incidents_data = load_json(INCIDENTS_FILE).get("incidents", [])
    complaints_data = load_json(COMPLAINTS_FILE).get("reports", [])

    # Filter incidents related to this location (ward)
    # Incidents don't always have ward directly, so we check connected_reports
    # or just use reports for basic counts
    location_reports = [r for r in complaints_data if r.get("ward") == location_id or r.get("location", {}).get("ward") == location_id]
    report_ids = {r["report_id"] for r in location_reports}
    
    location_incidents = []
    for inc in incidents_data:
        # If any of the incident's connected reports belong to this location
        connected = inc.get("connected_reports", [])
        if any(rid in report_ids for rid in connected):
            location_incidents.append(inc)

    total_incidents = len(location_incidents)
    
    resolved_incidents = 0
    previous_interventions = 0
    last_intervention_date = None
    issues_count = {}

    for inc in location_incidents:
        status = inc.get("status", "")
        if status == "RESOLVED":
            resolved_incidents += 1
            
        plan = inc.get("response_plan", {})
        if plan.get("approved"):
            previous_interventions += 1
            approved_at = plan.get("approved_at")
            if approved_at:
                if not last_intervention_date or approved_at > last_intervention_date:
                    last_intervention_date = approved_at
                    
        # Track issues
        cause = inc.get("root_cause", {}).get("hypothesis", "")
        if cause:
            issues_count[cause] = issues_count.get(cause, 0) + 1

    for r in location_reports:
        issue = r.get("description", "").lower()
        key = "Water leakage" if "leak" in issue or "water" in issue else "Pothole" if "pothole" in issue else "Drainage issue"
        issues_count[key] = issues_count.get(key, 0) + 1

    common_issue = max(issues_count, key=issues_count.get) if issues_count else "General Infrastructure"
    
    recurrence_rate = resolved_incidents / total_incidents if total_incidents > 0 else 0.0
    recurring = total_incidents > 1 and previous_interventions > 0

    if recurring and recurrence_rate < 1.0:
        insight = "Recurring infrastructure problem"
    elif total_incidents > 0:
        insight = "Historical reports exist in this area."
    else:
        insight = "No significant prior history."

    # Format the date properly if possible
    if last_intervention_date:
        try:
            # Try parsing ISO 8601
            dt = datetime.fromisoformat(last_intervention_date.replace('Z', '+00:00'))
            last_intervention_date = dt.strftime("%Y-%m-%d")
        except:
            last_intervention_date = last_intervention_date[:10] # fallback

    memory_data = {
        "location": location_id,
        "total_incidents": total_incidents,
        "previous_interventions": previous_interventions,
        "resolved_incidents": resolved_incidents,
        "recurring": recurring,
        "recurrence_rate": round(recurrence_rate, 2),
        "last_intervention": last_intervention_date or "None",
        "common_issue": common_issue,
        "insight": insight
    }

    # Save to civic_memory.json
    db = load_json(CIVIC_MEMORY_FILE)
    if "memories" not in db:
        db["memories"] = {}
    db["memories"][location_id] = memory_data
    save_json(CIVIC_MEMORY_FILE, db)

    return memory_data

def get_civic_memory(location_id: str) -> dict:
    db = load_json(CIVIC_MEMORY_FILE)
    memories = db.get("memories", {})
    if location_id in memories:
        # Recalculate anyway to ensure freshness
        return calculate_location_memory(location_id)
    return calculate_location_memory(location_id)
