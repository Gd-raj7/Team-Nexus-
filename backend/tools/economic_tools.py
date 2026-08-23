"""
CivicNexus AI — Economic & Resource Optimization Tools
Calculates ROI, municipal tax savings, and infrastructure longevity gained
by fixing root-cause civic cascades rather than repeatedly patching symptoms.
"""

from typing import Dict, Any, List

# Estimated unit cost of recurring emergency patches vs preventative root cause interventions (INR)
COST_BENCHMARKS_INR = {
    "WATER_LEAKAGE": {"root_fix": 45000, "consequential_damage_per_week": 180000},
    "ROAD_DAMAGE": {"root_fix": 75000, "consequential_damage_per_week": 120000},
    "POTHOLE": {"root_fix": 15000, "consequential_damage_per_week": 60000},
    "WATERLOGGING": {"root_fix": 35000, "consequential_damage_per_week": 150000},
    "EXPOSED_WIRES": {"root_fix": 20000, "consequential_damage_per_week": 350000},
    "DRAIN_BLOCKAGE": {"root_fix": 25000, "consequential_damage_per_week": 110000},
    "SEWAGE_OVERFLOW": {"root_fix": 40000, "consequential_damage_per_week": 220000},
    "BROKEN_STREETLIGHT": {"root_fix": 8000, "consequential_damage_per_week": 30000},
    "GARBAGE_OVERFLOW": {"root_fix": 12000, "consequential_damage_per_week": 45000},
}


def calculate_economic_savings(
    issue_types: List[str],
    impact_score: float,
    report_count: int,
) -> Dict[str, Any]:
    """
    Computes real-time economic cost-benefit projection:
    1. Single root-cause coordinated dispatch cost.
    2. Consequential damage cost if neglected for 4 weeks.
    3. Net savings and prevented re-digging cycles.
    """
    total_root_fix = 0
    total_damage_if_neglected = 0

    for it in issue_types:
        bench = COST_BENCHMARKS_INR.get(it, {"root_fix": 20000, "consequential_damage_per_week": 80000})
        total_root_fix += bench["root_fix"]
        total_damage_if_neglected += bench["consequential_damage_per_week"] * 4

    # Scale with impact severity and report cluster density
    severity_multiplier = max(1.0, impact_score / 50.0)
    density_multiplier = max(1.0, 1.0 + (report_count * 0.1))

    total_damage = int(total_damage_if_neglected * severity_multiplier * density_multiplier)
    coordinated_fix = int(total_root_fix * 1.15)  # Coordinated multi-dept logistics overhead
    estimated_savings = max(0, total_damage - coordinated_fix)

    # Prevented re-digging cycles (repairing road without fixing pipe underneath)
    prevented_cycles = max(1, len(issue_types) - 1) if "WATER_LEAKAGE" in issue_types or "DRAIN_BLOCKAGE" in issue_types else 1

    return {
        "estimated_damage_if_neglected_inr": total_damage,
        "root_cause_fix_cost_inr": coordinated_fix,
        "estimated_savings_inr": estimated_savings,
        "prevented_road_redigging_cycles": prevented_cycles,
        "infrastructure_longevity_boost": "4.2x Extended Pavement Life" if prevented_cycles > 1 else "2.1x Extended Asset Life",
        "cost_benefit_summary": (
            f"By executing a unified multi-department response instead of isolated ad-hoc repairs, "
            f"the municipality saves an estimated ₹{estimated_savings:,} and prevents {prevented_cycles} wasteful road re-excavation cycles."
        ),
    }
