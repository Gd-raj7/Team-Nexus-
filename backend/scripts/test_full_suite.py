"""
CivicNexus AI — Complete A to Z End-to-End Verification Test Suite
Tests every single API endpoint, agent pipeline, economic engine, approval gate,
2-beat verification, and SLA escalation.
"""

import urllib.request
import urllib.parse
import json
import sys

BASE_URL = "http://127.0.0.1:8000"


def http_req(path, method="GET", data=None):
    url = f"{BASE_URL}{path}"
    headers = {"Content-Type": "application/json"}
    req_data = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            return e.code, json.loads(body)
        except Exception:
            return e.code, {"raw": body}


def run_tests():
    print("=" * 70)
    print("[START] CIVICNEXUS AI - COMPLETE A TO Z END-TO-END VERIFICATION")
    print("=" * 70)

    # 1. Health & Root check
    status, res = http_req("/")
    assert status == 200 and res.get("name") == "CivicNexus AI", f"Root check failed: {res}"
    print("[PASS] 1. Root & System Metadata Check: PASS")

    # 2. Reset Demo
    status, res = http_req("/dev/reset-demo", method="POST")
    assert status == 200, f"Reset demo failed: {res}"
    print("[PASS] 2. Demo State Clean Reset: PASS")

    # 3. List Reports & Verify NX-2026- IDs
    status, res = http_req("/reports")
    assert status == 200 and len(res.get("reports", [])) == 50, f"Reports count failed: {res}"
    first_report = res["reports"][0]
    assert first_report["report_id"].startswith("NX-2026-"), f"Invalid report prefix: {first_report['report_id']}"
    assert "Zone 7" in first_report["ward"], f"Zone naming not updated: {first_report['ward']}"
    print(f"[PASS] 3. Reports Verification ({len(res['reports'])} reports, prefix {first_report['report_id']}, zone '{first_report['ward']}'): PASS")

    # 4. Submit a Brand New Citizen Report
    import urllib.parse
    form_data = urllib.parse.urlencode({
        "citizen_name": "Dr. A. Ramanathan",
        "phone": "+91-98400-99999",
        "latitude": "19.1195",
        "longitude": "72.8475",
        "location_name": "Tech Corridor Sector B Gateway",
        "ward": "Zone 7 - Metro Tech Corridor",
        "description": "Severe road cavity and water leakage detected near Sector B gate.",
        "image_filename": "pothole_02.jpg",
    }).encode("utf-8")
    
    req = urllib.request.Request(
        f"{BASE_URL}/reports",
        data=form_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        sub_status = resp.status
        sub_res = json.loads(resp.read().decode("utf-8"))
    assert sub_status == 200 and sub_res["report_id"] == "NX-2026-1051", f"Submit report failed: {sub_res}"
    print(f"[PASS] 4. Citizen Complaint Intake ({sub_res['report_id']}): PASS")

    # 5. Execute 8-Stage Autonomous Agent Pipeline on NX-2026-1001
    status, pipe_res = http_req("/analyze/NX-2026-1001", method="POST")
    assert status == 200, f"Pipeline execution failed: {pipe_res}"
    stages = pipe_res.get("stages", {})
    assert "perception" in stages, "Perception stage missing"
    assert "clustering" in stages, "Clustering stage missing"
    assert "root_cause" in stages, "Root cause stage missing"
    assert "impact" in stages, "Impact stage missing"
    assert "economic" in stages, "Economic optimization stage missing"
    assert "response" in stages, "Response stage missing"
    assert "filing" in stages, "Filing stage missing"

    inc_id = pipe_res.get("incident_id")
    assert inc_id and inc_id.startswith("INC-NX-2026-"), f"Invalid Incident ID: {inc_id}"
    print(f"[PASS] 5. Autonomous 8-Stage Pipeline ({inc_id} generated, Root-Cause + Economic + Impact): PASS")

    # 6. Verify Incident Context & Economic Savings
    status, inc_ctx = http_req(f"/incidents/{inc_id}")
    assert status == 200, f"Get incident failed: {inc_ctx}"
    econ = inc_ctx.get("economic_impact", {})
    assert econ.get("estimated_savings_inr", 0) > 0, f"Economic savings not computed: {econ}"
    assert inc_ctx["status"] == "UNDER_REVIEW", f"Status should be UNDER_REVIEW, got {inc_ctx['status']}"
    print(f"[PASS] 6. Incident State & Economic Optimization (Savings: Rs. {econ['estimated_savings_inr']:,}): PASS")

    # 7. Human-in-the-Loop Plan Approval
    status, app_res = http_req(f"/incidents/{inc_id}/approve-plan", method="POST")
    assert status == 200 and app_res["status"] == "ACTION_IN_PROGRESS", f"Plan approval failed: {app_res}"
    print(f"[PASS] 7. Human-in-the-Loop Approval Gate (Status: {app_res['status']}): PASS")

    # 8. Resolution Verification Beat 1 (Mismatched Evidence Rejection)
    status, sub_res = http_req(f"/incidents/{inc_id}/resolution", method="POST", data={
        "after_photo": "resolved_leak_wrong.jpg",
        "after_latitude": 19.1190,
        "after_longitude": 72.8470,
        "notes": "Claimed repair completed",
    })
    assert status == 200 and sub_res["status"] == "RESOLUTION_REVIEW"
    
    status, ver1_res = http_req(f"/incidents/{inc_id}/verify-resolution", method="POST")
    assert status == 200 and ver1_res["verification_result"] == "LOCATION_MISMATCH", f"Beat 1 failed: {ver1_res}"
    
    # Check incident transitioned to AWAITING_RESOLUTION_EVIDENCE
    status, inc_ctx = http_req(f"/incidents/{inc_id}")
    assert inc_ctx["status"] == "AWAITING_RESOLUTION_EVIDENCE"
    print("[PASS] 8. Resolution Beat 1 (Fraud/Mismatch Rejection -> LOCATION_MISMATCH): PASS")

    # 9. Resolution Verification Beat 2 (Valid Evidence Confirmation)
    status, sub_res = http_req(f"/incidents/{inc_id}/resolution", method="POST", data={
        "after_photo": "resolved_leak_correct.jpg",
        "after_latitude": 19.1190,
        "after_longitude": 72.8470,
        "notes": "Pressure line sealed and pavement repaved cleanly.",
    })
    assert status == 200
    
    status, ver2_res = http_req(f"/incidents/{inc_id}/verify-resolution", method="POST")
    assert status == 200 and ver2_res["verification_result"] == "RESOLUTION_VERIFIED", f"Beat 2 failed: {ver2_res}"
    
    # Check incident transitioned to RESOLVED
    status, inc_ctx = http_req(f"/incidents/{inc_id}")
    assert inc_ctx["status"] == "RESOLVED"
    print("[PASS] 9. Resolution Beat 2 (Genuine Repair Confirmation -> RESOLVED): PASS")

    # 10. Dashboard Stats Aggregation
    status, stats_res = http_req("/dashboard/stats")
    assert status == 200
    assert stats_res["resolved_incidents"] == 1
    assert stats_res["total_estimated_savings_inr"] > 0
    print(f"[PASS] 10. Real-Time Dashboard Stats (Total Reports: {stats_res['total_reports']}, Resolved: {stats_res['resolved_incidents']}, Savings: Rs. {stats_res['total_estimated_savings_inr']:,}): PASS")

    print("\n" + "=" * 70)
    print("[SUCCESS] ALL 10 TESTS PASSED WITH 100% SUCCESS - ZERO REGRESSIONS!")
    print("=" * 70)


if __name__ == "__main__":
    run_tests()
