"""
CivicNexus AI — Municipal Filing & Dispatch Agent
Synthesizes official municipal work order tickets with automated traceability.
"""

from typing import Dict, Any
from datetime import datetime, timezone, timedelta

IST = timezone(timedelta(hours=5, minutes=30))


async def file_complaint(
    incident: Dict[str, Any],
    perception_results: list,
    impact: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Municipal Filing Agent: Generate formal multi-department tracking work order.
    """
    incident_id = incident.get("incident_id", "")
    connected = incident.get("connected_reports", [])
    priority = impact.get("priority", "MEDIUM")
    score = impact.get("score", 0)

    issue_types = list(set(p.get("issue_type", "") for p in perception_results))

    filing = {
        "filing_id": f"MUNI-NEXUS-{incident_id}",
        "incident_id": incident_id,
        "filed_at": datetime.now(IST).isoformat(),
        "status": "DISPATCHED_SIMULATED",
        "disclaimer": "Simulated municipal filing order for demonstration purposes.",
        "priority": priority,
        "impact_score": score,
        "issue_types": issue_types,
        "connected_reports": connected,
        "report_count": len(connected),
        "summary": (
            f"CivicNexus incident {incident_id} involving {len(issue_types)} issue types "
            f"({', '.join(issue_types)}) across {len(connected)} citizen reports. "
            f"Priority: {priority} (Impact Score: {score}/100)."
        ),
    }

    agent_log = {
        "agent": "MUNICIPAL_DISPATCH_AGENT",
        "decision": f"Municipal Dispatch Work Order generated: {filing['filing_id']}",
        "evidence_used": [
            f"Incident: {incident_id}",
            f"Reports: {len(connected)}",
            f"Priority: {priority}",
        ],
        "confidence": 1.0,
        "recommended_action": "Track resolution through SLA monitoring",
    }

    return {
        "filing": filing,
        "agent_log": agent_log,
    }
