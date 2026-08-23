"""
CivicNexus AI — Economic Savings & Resource Optimization Agent
Quantifies municipal budget preservation and citizen asset protection.
"""

from typing import Dict, Any, List
from tools.economic_tools import calculate_economic_savings
from services.ai_service import generate_narrative


async def evaluate_economic_impact(
    issue_types: List[str],
    impact_score: Dict[str, Any],
    cluster_reports: List[Dict[str, Any]],
    root_cause: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Evaluates fiscal impact and resource efficiency.
    Returns:
        EconomicImpact dict + AgentLogEntry.
    """
    score_val = impact_score.get("score", 50.0)
    report_count = len(cluster_reports)

    econ_data = calculate_economic_savings(
        issue_types=issue_types,
        impact_score=score_val,
        report_count=report_count,
    )

    savings_inr = econ_data["estimated_savings_inr"]
    cycles = econ_data["prevented_road_redigging_cycles"]

    narrative = await generate_narrative(
        system_prompt=(
            "You are a municipal fiscal analyst and urban economist. "
            "Summarize the economic advantage of root-cause civic resolution in 2 crisp sentences."
        ),
        user_prompt=(
            f"Issues: {', '.join(issue_types)}\n"
            f"Estimated Net Savings: ₹{savings_inr:,}\n"
            f"Prevented road re-digging cycles: {cycles}\n"
            f"Longevity boost: {econ_data['infrastructure_longevity_boost']}\n\n"
            "Provide a concise fiscal statement."
        ),
        fallback_text=econ_data["cost_benefit_summary"],
    )

    econ_data["cost_benefit_summary"] = narrative

    agent_log = {
        "agent": "ECONOMIC_OPTIMIZATION_AGENT",
        "decision": f"Projected Municipal Savings: ₹{savings_inr:,}",
        "evidence_used": [
            f"Coordinated Root Repair: ₹{econ_data['root_cause_fix_cost_inr']:,}",
            f"Projected 4-Week Cascade Damage: ₹{econ_data['estimated_damage_if_neglected_inr']:,}",
            f"Prevented Repetitive Excavation: {cycles} cycle(s)",
        ],
        "confidence": 0.92,
        "recommended_action": "Prioritize combined work order to optimize municipal capital allocation",
    }

    return {
        "economic_impact": econ_data,
        "agent_log": agent_log,
    }
