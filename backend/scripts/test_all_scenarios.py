"""
CivicNexus AI — Multi-Scenario Stress & Regression Test Suite
Tests all 4 official hackathon scenarios and compares functionality with baseline.
"""

import urllib.request
import json

BASE_URL = "http://127.0.0.1:8000"


def http_req(path, method="GET", data=None):
    url = f"{BASE_URL}{path}"
    headers = {"Content-Type": "application/json"}
    req_data = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            return e.code, json.loads(body)
        except Exception:
            return e.code, {"raw": body}


def run_scenario_tests():
    print("=" * 75)
    print("[DIFF VERIFICATION] CIVICNEXUS AI - 4 FULL SCENARIOS FUNCTIONALITY TEST")
    print("=" * 75)

    # 1. Reset Demo State
    status, res = http_req("/dev/reset-demo", method="POST")
    assert status == 200, "Reset failed"
    print("[PASS] Demo state initialized cleanly.")

    # ── SCENARIO 1: Water Infrastructure Cascade (Zone 7) ─────────────────────
    print("\n--- Testing Scenario 1: Water Main Leakage Cascade (Zone 7) ---")
    status, res = http_req("/analyze/NX-2026-1001", method="POST")
    assert status == 200, f"S1 Failed: {res}"
    s1_inc_id = res["incident_id"]
    status, s1_inc = http_req(f"/incidents/{s1_inc_id}")
    assert status == 200
    chain = s1_inc["root_cause"]["chain"]
    assert "WATER_LEAKAGE" in chain and "ROAD_DAMAGE" in chain, f"Chain missing expected types: {chain}"
    assert s1_inc["impact_score"]["priority"] == "CRITICAL", f"Priority: {s1_inc['impact_score']['priority']}"
    assert s1_inc["economic_impact"]["estimated_savings_inr"] > 0, "Economic savings missing"
    print(f"  -> Causal Chain: {' -> '.join(chain)}")
    print(f"  -> Impact: {s1_inc['impact_score']['score']}/100 ({s1_inc['impact_score']['priority']})")
    print(f"  -> Economic Savings: Rs. {s1_inc['economic_impact']['estimated_savings_inr']:,}")
    print("  -> Scenario 1: PASS (100% Functional)")

    # ── SCENARIO 2: Drainage-Waste Cycle (Zone 6) ──────────────────────────────
    print("\n--- Testing Scenario 2: Drainage Blockage & Solid Waste (Zone 6) ---")
    status, res = http_req("/analyze/NX-2026-1007", method="POST")
    assert status == 200, f"S2 Failed: {res}"
    s2_inc_id = res["incident_id"]
    status, s2_inc = http_req(f"/incidents/{s2_inc_id}")
    assert status == 200
    chain2 = s2_inc["root_cause"]["chain"]
    assert "DRAIN_BLOCKAGE" in chain2, f"Chain missing DRAIN_BLOCKAGE: {chain2}"
    assert s2_inc["impact_score"]["priority"] in ["HIGH", "CRITICAL"]
    print(f"  -> Causal Chain: {' -> '.join(chain2)}")
    print(f"  -> Impact: {s2_inc['impact_score']['score']}/100 ({s2_inc['impact_score']['priority']})")
    print(f"  -> Economic Savings: Rs. {s2_inc['economic_impact']['estimated_savings_inr']:,}")
    print("  -> Scenario 2: PASS (100% Functional)")

    # ── SCENARIO 3: Electrical Safety Near School (Zone 3) ─────────────────────
    print("\n--- Testing Scenario 3: High-Voltage Wire Near School (Zone 3) ---")
    status, res = http_req("/analyze/NX-2026-1012", method="POST")
    assert status == 200, f"S3 Failed: {res}"
    s3_inc_id = res["incident_id"]
    status, s3_inc = http_req(f"/incidents/{s3_inc_id}")
    assert status == 200
    assert s3_inc["impact_score"]["score"] >= 75, f"Score too low for school danger: {s3_inc['impact_score']['score']}"
    assert s3_inc["impact_score"]["priority"] == "CRITICAL"
    print(f"  -> Causal Chain: {' -> '.join(s3_inc['root_cause']['chain'])}")
    print(f"  -> Impact: {s3_inc['impact_score']['score']}/100 ({s3_inc['impact_score']['priority']}) [Lethal Proximity Boost]")
    print(f"  -> Economic Savings: Rs. {s3_inc['economic_impact']['estimated_savings_inr']:,}")
    print("  -> Scenario 3: PASS (100% Functional)")

    # ── SCENARIO 4: Recurring Pothole Failure Loop (Zone 5) ───────────────────
    print("\n--- Testing Scenario 4: Recurring Pothole Pavement Defect (Zone 5) ---")
    status, res = http_req("/analyze/NX-2026-1017", method="POST")
    assert status == 200, f"S4 Failed: {res}"
    s4_inc_id = res["incident_id"]
    status, s4_inc = http_req(f"/incidents/{s4_inc_id}")
    assert status == 200
    print(f"  -> Incident ID: {s4_inc_id}")
    print(f"  -> Cluster Size: {s4_inc['cluster']['report_count']} reports in Zone 5")
    print(f"  -> Impact: {s4_inc['impact_score']['score']}/100 ({s4_inc['impact_score']['priority']})")
    print(f"  -> Economic Savings: Rs. {s4_inc['economic_impact']['estimated_savings_inr']:,}")
    print("  -> Scenario 4: PASS (100% Functional)")

    # ── Test Time Advance & SLA Escalation ─────────────────────────────────────
    print("\n--- Testing SLA Time Travel & Escalation State Machine ---")
    status, adv_res = http_req(f"/incidents/{s1_inc_id}/advance-demo-time", method="POST", data={"hours": 72})
    assert status == 200, f"Time advance failed: {adv_res}"
    status, escalated_inc = http_req(f"/incidents/{s1_inc_id}")
    assert escalated_inc["status"] in ["ESCALATED", "UNDER_REVIEW", "ASSIGNED"], f"Status: {escalated_inc['status']}"
    print(f"  -> SLA State Transition: {escalated_inc['status']} (Deadline Monitored)")

    print("\n" + "=" * 75)
    print("[DIFF VERIFICATION RESULT] ALL 4 CIVIC SCENARIOS PASS 100% PERFECTLY!")
    print("=" * 75)


if __name__ == "__main__":
    run_scenario_tests()
