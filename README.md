# CivicNexus AI — Autonomous Urban Incident Intelligence Matrix

> **Team:** Team Nexus  
> **Tagline:** *"Decoding Fragmented Citizen Signals into Unified Urban Intelligence."*  
> **Framing Line:** *"Cities don't suffer from a lack of civic complaints. They suffer from isolated incident silos that mask compounding systemic infrastructure failures."*

CivicNexus AI is an autonomous, multi-agent civic incident intelligence system built for municipal operators and citizens. By correlating geographical and temporal proximity of independent citizen reports, CivicNexus identifies cascading root-cause failures (e.g., pressurized water main burst weakening a road foundation to form potholes that pool water into traffic-blocking waterlogging), projects municipal tax savings from preventative coordinated repairs, automatically sequences department work orders, and enforces dual-beat GPS and photographic resolution verification.

---

## 🛠️ Multi-Agent Architecture

CivicNexus operates via a coordinated pipeline of eleven specialized autonomous agents:

| Agent | Responsibility | Core Logic |
| :--- | :--- | :--- |
| **Perception Agent** | Analyzes photos and citizen text to detect category, severity, and visual markers. | Gemini Multimodal Vision + Deterministic image lookup + descriptive evidence synthesis. |
| **Geo-Temporal Clustering Agent** | Finds geographically and temporally related reports. | Pure Python Haversine distance (<180m) and temporal window (<7 days) math. |
| **Incident Detection Agent** | Analyzes the cluster to determine classification. | Rules: `INDEPENDENT` / `DUPLICATE` / `POSSIBLE_CONNECTED` / `HIGH_CONFIDENCE_CONNECTED` + LLM narrative reasoning. |
| **Root-Cause Agent** | Traces causal connections across multiple civic issues. | Directed dependency graph traversal (`civic_dependencies.json`) + LLM cascade hypothesis. |
| **Civic Impact Agent** | Scores real-world public threat severity (0-100). | Weighted formula (Severity 30%, Proximity 20%, Impacted 15%, Duration 10%, Repeats 10%, Risks 15%) + LLM explanation. |
| **Economic Optimization Agent** | Calculates municipal tax savings and prevented road re-digging cycles. | Preventative root fix ROI calculation vs compounding 4-week neglected damage. |
| **Response Orchestration Agent** | Designates multi-department resolution work orders. | Topological sort matching department roles and execution dependencies (`departments.json`). |
| **Municipal Dispatch Agent** | Generates formal, traceable municipal dispatch tickets. | Generates `MUNI-NEXUS-[INC_ID]` work orders with automated tracking. |
| **Escalation Agent** | Tracks SLA deadlines and alerts senior management. | State machine transitioner checking deadlines + simulated demo time-traveler. |
| **Verification Agent** | Validates resolution claims via photographic/GPS proof. | Dual-beat verification (GPS <100m + visual evidence validation + incoming complaints monitor). |
| **Central Orchestrator** | Coordinates state transitions of `IncidentContext`. | Writes and persists updates to shared atomic state `incidents.json`. |

---

## 🚀 Setup & Execution

### Prerequisites
- Python 3.10+
- Node.js 18+

### 1. Backend Setup
```bash
cd backend
python -m venv venv

# On Windows
.\venv\Scripts\activate

pip install -r requirements.txt
```

Generate seed data:
```bash
python -m backend.scripts.seed_data
```

Start the FastAPI server:
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### 2. Frontend Setup
Open a separate terminal window:
```bash
cd frontend
npm install
npm run dev
```
Navigate to `http://localhost:5173`.

---

## 🎯 Rehearsed Live Demo Script

Follow this script step-by-step for a seamless live demonstration:

1. **Submit Initial Report**: Go to the **Citizen Portal** (`/report`). Select the seed image **`leak_01.jpg`** (Tech Junction Hub, Zone 7 Sector A). Click **Submit Complaint Report**.
2. **Launch Agent Analysis**: Click **Go to Dashboard and Analyze**.
3. **Analyze Pipeline**: On the Dashboard, find `NX-2026-1001` in the *Citizen Reports Feed*. Click **Run Agentic AI**. The live *Agent Pipeline* animates through perception, clustering (finding 6 related complaints), detection, root cause, impact, economic optimization, response, and municipal dispatch.
4. **Inspect Root Cause, Economic Savings & Priority**:
   - The **Economic Optimization Card** displays estimated municipal tax savings (e.g. ₹8,40,000 saved) and prevented road re-digging cycles.
   - The Root Cause card displays the cascade hypothesis with the required physical inspection disclaimer.
   - The Civic Impact gauge displays **CRITICAL** (86/100) priority.
5. **Approve Multi-Department Plan**: Scroll down to the *Response Plan*. Inspect the sequenced steps (Water Board first, then Drainage, and Roads Department last). Click **Approve Multi-Department Plan** to transition status to `ACTION_IN_PROGRESS`.
6. **Submit Mismatched Resolution (Beat 1)**: In the *Resolution Verification* card, select **`resolved_leak_wrong.jpg`** (garbage image) and click **Submit and Verify**. The Verification Agent returns **`LOCATION_MISMATCH`** with a low confidence score, refusing to close the ticket.
7. **Submit Correct Resolution (Beat 2)**: Select **`resolved_leak_correct.jpg`** (dry patched road at Tech Junction) and click **Submit and Verify**. The Verification Agent confirms **`RESOLUTION_VERIFIED`** and transitions status to **RESOLVED**, reducing impact level to **LOW**.
8. **Advance SLA Escalation**: Advance simulated time by clicking **Advance Time (+3 Days)** to trigger the SLA monitor. Notice the incident status changing to **ESCALATED** with a detailed SLA breach notification.

---

*Built with pride by Team Nexus.*
