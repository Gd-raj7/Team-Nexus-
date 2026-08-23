"""
CivicNexus AI -- Root Cause Investigation Agent
Walks civic_dependencies.json to find causal chains, LLM narrates the reasoning.
"""

from typing import Dict, Any, List

from tools.knowledge_tools import find_causal_chain
from services.ai_service import generate_narrative


async def investigate_root_cause(
    issue_types: List[str],
    perception_results: List[Dict[str, Any]],
    cluster_reports: List[Dict[str, Any]],
    civic_memory_data: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """
    Root Cause Investigation Agent: Walk the dependency graph to find
    the most likely causal chain connecting the observed issue types.

    Always includes the disclaimer:
    "AI-generated civic incident hypothesis. Physical inspection recommended."

    Returns root cause hypothesis with chain, confidence, and evidence.
    """
    # Walk the dependency graph
    chain_result = find_causal_chain(issue_types)
    chain = chain_result["chain"]
    confidence = chain_result["confidence"]
    evidence = chain_result["evidence"]

    # Adjust based on memory
    if civic_memory_data and civic_memory_data.get("recurring"):
        prev_interventions = civic_memory_data.get("previous_interventions", 0)
        total_incidents = civic_memory_data.get("total_incidents", 0)
        evidence.append(f"{total_incidents} previous incidents at this location")
        if prev_interventions > 0:
            evidence.append(f"{prev_interventions} previous interventions")
            evidence.append("Issue returned after previous repair")
        # Boost confidence for recurring issues
        confidence = min(0.95, confidence + 0.1)

    # Generate LLM narrative explaining the causal chain
    chain_str = " -> ".join(chain)
    evidence_str = "\n".join(f"- {e}" for e in evidence)

    report_descriptions = []
    for r in cluster_reports[:6]:
        report_descriptions.append(
            f"- {r.get('report_id', 'N/A')}: {r.get('description', '')[:120]}"
        )
    descriptions_text = "\n".join(report_descriptions)

    # Add memory context to prompt if available
    memory_context = ""
    if civic_memory_data and civic_memory_data.get("recurring"):
        memory_context = f"Civic Memory Insight: {civic_memory_data.get('insight', 'Recurring issue')}. "

    hypothesis = await generate_narrative(
        system_prompt=(
            "You are a civic infrastructure root cause analyst. "
            "Explain the causal chain connecting these civic issues in 3-4 sentences. "
            "Be specific about the mechanisms. End with a clear hypothesis statement."
        ),
        user_prompt=(
            f"Observed issue types: {', '.join(issue_types)}\n"
            f"Causal chain identified: {chain_str}\n"
            f"Chain confidence: {confidence}\n\n"
            f"Mechanisms:\n{evidence_str}\n\n"
            f"Citizen reports:\n{descriptions_text}\n\n"
            f"{memory_context}"
            "Provide a root cause hypothesis explaining how these issues are connected. "
            "Be specific about the infrastructure cascade."
        ),
        fallback_text=(
            f"{memory_context}Root cause analysis identifies a cascading infrastructure failure: {chain_str}. "
            f"The evidence suggests that {chain[0] if chain else 'the initial issue'} "
            f"triggered a chain of downstream effects through "
            f"{', '.join(evidence[:2]) if evidence else 'progressive infrastructure degradation'}. "
            f"This cascade pattern is consistent with {len(issue_types)} distinct issue types "
            f"observed within a concentrated geographic area."
        ),
    )

    disclaimer = "AI-generated civic incident hypothesis. Physical inspection recommended."

    agent_log = {
        "agent": "ROOT_CAUSE_AGENT",
        "decision": f"Causal chain: {chain_str}",
        "evidence_used": evidence + [
            f"{len(cluster_reports)} related reports analyzed",
            f"{len(issue_types)} distinct issue types identified",
        ],
        "confidence": confidence,
        "recommended_action": "Proceed to impact assessment and response planning",
    }

    return {
        "hypothesis": hypothesis,
        "chain": chain,
        "confidence": confidence,
        "evidence": evidence,
        "disclaimer": disclaimer,
        "agent_log": agent_log,
    }

