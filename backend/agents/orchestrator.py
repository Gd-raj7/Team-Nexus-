"""
CivicIQ -- Orchestrator
Central pipeline controller. Sole writer of IncidentContext to disk.

Pipeline: OBSERVE -> UNDERSTAND -> CONNECT -> INVESTIGATE -> PRIORITIZE ->
          PLAN -> ACT/RECOMMEND -> TRACK -> VERIFY -> REPLAN/ESCALATE
"""

import json
import os
from typing import Dict, Any, List
from datetime import datetime, timezone, timedelta

from agents.perception import analyze_report
from agents.clustering import find_cluster
from agents.incident import detect_incident
from agents.root_cause import investigate_root_cause
from agents.impact import assess_impact
from agents.response import create_response_plan
from agents.filing import file_complaint

IST = timezone(timedelta(hours=5, minutes=30))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


def _now_ist() -> str:
    return datetime.now(IST).isoformat()


def _load_json(filename: str) -> dict:
    path = os.path.join(DATA_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_json(filename: str, data: dict):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _append_agent_log(entry: dict):
    """Append an agent log entry to the centralized log."""
    entry["timestamp"] = _now_ist()
    logs = _load_json("agent_logs.json")
    if "logs" not in logs:
        logs["logs"] = []
    logs["logs"].append(entry)
    logs["total"] = len(logs["logs"])
    _save_json("agent_logs.json", logs)


def _next_incident_id() -> str:
    data = _load_json("incidents.json")
    incidents = data.get("incidents", [])
    if not incidents:
        return "INC-2026-001"
    max_num = 0
    for inc in incidents:
        try:
            num = int(inc["incident_id"].split("-")[-1])
            if num > max_num:
                max_num = num
        except (ValueError, IndexError):
            pass
    return f"INC-2026-{max_num + 1:03d}"


async def run_full_pipeline(report: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run the full agent pipeline on a new report.

    Pipeline stages:
    1. PERCEPTION: Analyze the report image/description
    2. CLUSTERING: Find nearby related reports
    3. PERCEPTION (batch): Analyze all clustered reports
    4. INCIDENT DETECTION: Classify the cluster
    5. ROOT CAUSE: Find causal chain
    6. IMPACT: Score civic impact
    7. RESPONSE: Create department response plan
    8. FILING: Create formal complaint record

    Returns the complete pipeline result with all agent outputs.
    """
    report_id = report.get("report_id", "")
    pipeline_result = {
        "report_id": report_id,
        "stages": {},
        "agent_logs": [],
        "incident_id": None,
    }

    # ── Stage 1: PERCEPTION ──────────────────────────────────────────────
    perception_result = await analyze_report(report)
    _append_agent_log(perception_result["agent_log"])
    pipeline_result["stages"]["perception"] = {
        "status": "complete",
        "result": {
            "report_id": perception_result["report_id"],
            "issue_type": perception_result["issue_type"],
            "severity": perception_result["severity"],
            "confidence": perception_result["confidence"],
            "evidence_text": perception_result["evidence_text"],
            "visual_evidence": perception_result.get("visual_evidence", []),
        },
    }
    pipeline_result["agent_logs"].append(perception_result["agent_log"])

    # ── Stage 2: CLUSTERING ──────────────────────────────────────────────
    cluster_result = await find_cluster(report)
    _append_agent_log(cluster_result["agent_log"])
    cluster = cluster_result["cluster"]
    pipeline_result["stages"]["clustering"] = {
        "status": "complete",
        "result": {
            "cluster_size": cluster["count"],
            "radius_m": cluster["radius_m"],
            "report_ids": cluster["report_ids"],
            "reasoning": cluster_result["reasoning"],
        },
    }
    pipeline_result["agent_logs"].append(cluster_result["agent_log"])

    # ── Stage 3: BATCH PERCEPTION (for clustered reports) ────────────────
    all_perception_results = [perception_result]
    cluster_reports = [report]  # Include target report

    for clustered_report in cluster["reports"]:
        p_result = await analyze_report(clustered_report)
        all_perception_results.append(p_result)
        cluster_reports.append(clustered_report)

    pipeline_result["stages"]["batch_perception"] = {
        "status": "complete",
        "result": {
            "analyzed_count": len(all_perception_results),
            "issue_types": list(set(p["issue_type"] for p in all_perception_results)),
        },
    }

    # ── Stage 4: INCIDENT DETECTION ──────────────────────────────────────
    detection_result = await detect_incident(
        report=report,
        perception_result=perception_result,
        cluster=cluster,
        all_perception_results=all_perception_results,
    )
    _append_agent_log(detection_result["agent_log"])
    pipeline_result["stages"]["incident_detection"] = {
        "status": "complete",
        "result": {
            "classification": detection_result["classification"],
            "issue_types": detection_result["issue_types"],
            "reasoning": detection_result["reasoning"],
            "confidence": detection_result["confidence"],
        },
    }
    pipeline_result["agent_logs"].append(detection_result["agent_log"])

    # Only create a full incident if connected reports detected
    if "CONNECTED" not in detection_result["classification"]:
        # Update report status
        _update_report_status(report_id, "UNDER_REVIEW")
        pipeline_result["stages"]["summary"] = {
            "status": "complete",
            "classification": detection_result["classification"],
            "message": "Report classified as independent or duplicate. No incident created.",
        }
        return pipeline_result

    # ── Create Incident ──────────────────────────────────────────────────
    incident_id = _next_incident_id()
    pipeline_result["incident_id"] = incident_id

    connected_report_ids = [report_id] + cluster["report_ids"]

    # Initialize incident context
    incident = {
        "incident_id": incident_id,
        "status": "UNDER_REVIEW",
        "classification": detection_result["classification"],
        "created_at": _now_ist(),
        "updated_at": _now_ist(),
        "connected_reports": connected_report_ids,
        "cluster": {
            "radius_m": cluster["radius_m"],
            "time_window_days": cluster["time_window_days"],
            "center_lat": cluster["center_lat"],
            "center_lon": cluster["center_lon"],
            "report_count": len(connected_report_ids),
        },
        "perception_results": [
            {
                "report_id": p["report_id"],
                "issue_type": p["issue_type"],
                "severity": p["severity"],
                "confidence": p["confidence"],
                "evidence_text": p["evidence_text"],
                "image_filename": p.get("image_filename", ""),
                "visual_evidence": p.get("visual_evidence", []),
            }
            for p in all_perception_results
        ],
        "root_cause": {},
        "impact_score": {},
        "response_plan": {},
        "resolution": {},
        "sla": {},
        "agent_log": [],
    }

    # ── Stage 5: ROOT CAUSE ──────────────────────────────────────────────
    root_cause_result = await investigate_root_cause(
        issue_types=detection_result["issue_types"],
        perception_results=all_perception_results,
        cluster_reports=cluster_reports,
    )
    _append_agent_log(root_cause_result["agent_log"])
    incident["root_cause"] = {
        "hypothesis": root_cause_result["hypothesis"],
        "confidence": root_cause_result["confidence"],
        "evidence": root_cause_result["evidence"],
        "chain": root_cause_result["chain"],
        "disclaimer": root_cause_result["disclaimer"],
    }
    pipeline_result["stages"]["root_cause"] = {
        "status": "complete",
        "result": {
            "chain": root_cause_result["chain"],
            "confidence": root_cause_result["confidence"],
            "hypothesis": root_cause_result["hypothesis"],
            "disclaimer": root_cause_result["disclaimer"],
        },
    }
    pipeline_result["agent_logs"].append(root_cause_result["agent_log"])

    # ── Stage 6: IMPACT ──────────────────────────────────────────────────
    impact_result = await assess_impact(
        perception_results=all_perception_results,
        cluster_reports=cluster_reports,
        root_cause=root_cause_result,
    )
    _append_agent_log(impact_result["agent_log"])
    incident["impact_score"] = {
        "score": impact_result["score"],
        "priority": impact_result["priority"],
        "breakdown": impact_result["breakdown"],
        "explanation": impact_result["explanation"],
    }
    pipeline_result["stages"]["impact"] = {
        "status": "complete",
        "result": {
            "score": impact_result["score"],
            "priority": impact_result["priority"],
            "breakdown": impact_result["breakdown"],
            "explanation": impact_result["explanation"],
        },
    }
    pipeline_result["agent_logs"].append(impact_result["agent_log"])

    # ── Stage 7: RESPONSE PLAN ───────────────────────────────────────────
    response_result = await create_response_plan(
        issue_types=detection_result["issue_types"],
        impact_score=impact_result,
        root_cause=root_cause_result,
        cluster_reports=cluster_reports,
    )
    _append_agent_log(response_result["agent_log"])
    incident["response_plan"] = {
        "steps": response_result["steps"],
        "rationale": response_result["rationale"],
        "approved": False,
        "approved_by": "",
        "approved_at": "",
    }
    pipeline_result["stages"]["response"] = {
        "status": "complete",
        "result": {
            "steps": response_result["steps"],
            "rationale": response_result["rationale"],
            "approved": False,
        },
    }
    pipeline_result["agent_logs"].append(response_result["agent_log"])

    # ── Stage 8: FILING ──────────────────────────────────────────────────
    filing_result = await file_complaint(
        incident=incident,
        perception_results=all_perception_results,
        impact=impact_result,
    )
    _append_agent_log(filing_result["agent_log"])
    pipeline_result["stages"]["filing"] = {
        "status": "complete",
        "result": filing_result["filing"],
    }
    pipeline_result["agent_logs"].append(filing_result["agent_log"])

    # ── Set SLA deadline ─────────────────────────────────────────────────
    SLA_HOURS = {"CRITICAL": 12, "HIGH": 24, "MEDIUM": 48, "LOW": 72}
    sla_hours = SLA_HOURS.get(impact_result["priority"], 48)
    created_dt = datetime.now(IST)
    deadline_dt = created_dt + timedelta(hours=sla_hours)
    incident["sla"] = {
        "deadline": deadline_dt.isoformat(),
        "reminders_sent": 0,
        "escalated": False,
        "escalation_reason": "",
        "original_deadline": deadline_dt.isoformat(),
    }

    # ── Write incident to disk (Orchestrator is sole writer) ─────────────
    incidents_data = _load_json("incidents.json")
    incidents_data["incidents"].append(incident)
    incidents_data["total"] = len(incidents_data["incidents"])
    _save_json("incidents.json", incidents_data)

    # ── Update linked report statuses ────────────────────────────────────
    for rid in connected_report_ids:
        _update_report_status(rid, "LINKED_TO_INCIDENT", incident_id)

    pipeline_result["stages"]["summary"] = {
        "status": "complete",
        "incident_id": incident_id,
        "classification": detection_result["classification"],
        "impact_score": impact_result["score"],
        "priority": impact_result["priority"],
        "response_steps": len(response_result["steps"]),
        "message": f"Incident {incident_id} created with {len(connected_report_ids)} connected reports.",
    }

    return pipeline_result


async def analyze_existing_incident(incident: Dict[str, Any]) -> Dict[str, Any]:
    """Re-analyze an existing incident (for updates)."""
    # This is a simplified version for re-analysis
    return {
        "incident_id": incident["incident_id"],
        "status": incident["status"],
        "message": "Incident analysis refreshed.",
    }


def _update_report_status(
    report_id: str,
    status: str,
    incident_id: str = None,
):
    """Update a report's status and linked incident."""
    data = _load_json("complaints.json")
    for r in data.get("reports", []):
        if r["report_id"] == report_id:
            r["status"] = status
            if incident_id:
                r["linked_incident_id"] = incident_id
            break
    _save_json("complaints.json", data)
