import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
INCIDENTS_FILE = os.path.join(DATA_DIR, "incidents.json")
COMPLAINTS_FILE = os.path.join(DATA_DIR, "complaints.json")

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_hotspots():
    """Discover top active spatial incident hotspots grouped by location."""
    incidents = load_json(INCIDENTS_FILE).get("incidents", [])
    complaints = load_json(COMPLAINTS_FILE).get("reports", [])
    
    location_groups = {}
    for inc in incidents:
        ward = "Unknown Zone"
        cluster = inc.get("cluster", {})
        if "center_lat" in cluster:
            ward = f"Zone at {round(cluster['center_lat'], 3)}, {round(cluster['center_lon'], 3)}"
        
        connected = inc.get("connected_reports", [])
        for r in complaints:
            if r.get("report_id") in connected and r.get("ward"):
                ward = r["ward"]
                break
                
        if ward not in location_groups:
            location_groups[ward] = []
        location_groups[ward].append(inc)
        
    hotspots = []
    severity_map = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}
    
    for loc, loc_incidents in location_groups.items():
        count = len(loc_incidents)
        max_sev = "LOW"
        max_sev_val = 0
        
        for i in loc_incidents:
            sev = i.get("impact_score", {}).get("priority", "LOW")
            if severity_map.get(sev, 0) > max_sev_val:
                max_sev = sev
                max_sev_val = severity_map.get(sev, 0)
                
        recurring = count > 1
        
        # Hotspot score = frequency + severity score (1-4)
        score = count + max_sev_val
        if recurring:
            score += 2
            
        hotspots.append({
            "location": loc,
            "incident_count": count,
            "severity": max_sev,
            "recurring": recurring,
            "_sort_score": score
        })
        
    hotspots.sort(key=lambda x: x["_sort_score"], reverse=True)
    hotspots = hotspots[:5]
    
    for h in hotspots:
        del h["_sort_score"]
        
    return hotspots
