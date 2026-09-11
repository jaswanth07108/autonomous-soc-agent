# Tech Zephyr 4.0 — Hackathon Submission Dossier
**IIT Bhubaneswar • Agentic AI Hackathon**  
**Problem Statement 9: Autonomous SOC Investigation & Response Agent**  
**Project Title**: AegisSOC — Autonomous SOC Investigation & Response Agent

---

## 📌 Deliverable 1: Problem & Solution Brief

### 1. The Problem
Modern Security Operations Centers (SOCs) face an unsustainable operational bottleneck:
* **Alert Fatigue**: Enterprise NIDS/SIEM sensors generate thousands of daily alerts, with over 70% being false positives or low-priority noise.
* **Static Rule Inflexibility**: Traditional Security Orchestration, Automation, and Response (SOAR) playbooks follow rigid if-else branches that fail when faced with novel, multi-stage, or evasive tactics.
* **The "Chatbot" Fallacy**: First-generation GenAI cybersecurity tools merely generate text summaries or advice. They cannot dynamically investigate, verify target ground truth, execute mitigation actions, or recover when tools fail.

### 2. Our Proposed Solution: AegisSOC
**AegisSOC** is a genuinely autonomous **Agentic AI SOC Investigation and Response System** operating within a safe, controlled sandbox environment. AegisSOC eliminates static playbooks and chatbot illusions by implementing a closed-loop ReAct decision trajectory:

$$\mathbf{GOAL} \longrightarrow \mathbf{OBSERVE} \longrightarrow \mathbf{HYPOTHESIZE} \longrightarrow \mathbf{PLAN\ NEXT\ TOOL} \longrightarrow \mathbf{INVESTIGATE} \longrightarrow \mathbf{DECIDE} \longrightarrow \mathbf{ACT} \longrightarrow \mathbf{VERIFY} \longrightarrow \mathbf{ADAPT}$$

* **Dynamic Evidence Planning**: The agent formulates an evolving hypothesis and dynamically picks the next best tool (e.g. terminating early after 2 tools on benign traffic, or escalating through authentication, asset criticality, CVE patch status, and exfiltration flows on breaches).
* **Closed-Loop Action Verification**: It executes simulated perimeter firewall blocks and immediately re-checks the sandbox state to verify traffic drops.
* **Real-time Contradiction Adaptation**: When contradictory evidence arrives mid-investigation (e.g. an approved Duo MFA change ticket), the agent detects the conflict, queries corporate IAM directories, lowers risk, and adapts its decision to `LEGITIMATE_ADMIN_ACTIVITY`.
* **Autonomous Failure Recovery**: If a firewall rule fails to deploy due to a communication timeout, the agent observes the error, re-plans a secondary fallback isolation route, and verifies enforcement.

---

## 🏛️ Deliverable 2: System Architecture & Workflow

```
                                  ┌────────────────────────────────────────────────────────┐
                                  │      AegisSOC Analyst Dashboard (React 18 + Vite)      │
                                  │  - Alert Dashboard      - Interactive Timeline         │
                                  │  - Topology Graph       - Step-by-Step Mode Controller │
                                  └───────────────────────────┬────────────────────────────┘
                                                              │ REST API (FastAPI)
                                                              ▼
                                  ┌────────────────────────────────────────────────────────┐
                                  │               FastAPI Gateway (backend/api)            │
                                  └───────────────────────────┬────────────────────────────┘
                                                              │
                                                              ▼
                                  ┌────────────────────────────────────────────────────────┐
                                  │         Autonomous Agent State Machine & ReAct Loop    │
                                  │       (Goal -> Hypothesis -> Plan -> Tool -> Adapt)    │
                                  └───────┬───────────────────┬───────────────────┬────────┘
                                          │                   │                   │
                                          ▼                   ▼                   ▼
                               ┌──────────────────┐┌──────────────────┐┌──────────────────┐
                               │ Dynamic Planner  ││ Decision Engine  ││ Re-Planner &     │
                               │ (backend/agent)  ││ & Risk Calculator││ Adaptation Unit  │
                               └──────────┬───────┘└──────────┬───────┘└──────────┬───────┘
                                          │                   │                   │
                                          └───────────────────┼───────────────────┘
                                                              │ Real Sandbox Tool Invocations
                                                              ▼
                                  ┌────────────────────────────────────────────────────────┐
                                  │                 Sandbox Tool Layer (9 Tools)           │
                                  │  - get_alert()            - get_server_logs()          │
                                  │  - get_asset()            - get_vulnerabilities()      │
                                  │  - get_network_events()   - verify_identity_ticket()   │
                                  │  - block_ip()             - verify_firewall()          │
                                  └───────────────────────────┬────────────────────────────┘
                                                              │
                                                              ▼
                                  ┌────────────────────────────────────────────────────────┐
                                  │          Local SQLite Sandbox (soc_sandbox.db)         │
                                  │  - security_alerts     - server_logs    - assets       │
                                  │  - vulnerabilities     - network_events - firewall_state│
                                  │  - identity_directory  - investigation_sessions        │
                                  │  - investigation_history (Audit Trail)                 │
                                  └────────────────────────────────────────────────────────┘
```

---

## 💻 Deliverable 3: Source Code & Repository Cleanliness

* **Repository Integrity**: Completely free of hardcoded API keys, passwords, bearer tokens, or cloud secrets.
* **Sandbox Safety**: All security operations, IP blocks, and vulnerability scans run strictly against a local SQLite database (`soc_sandbox.db`) without touching external production networks.
* **Modular Codebase**:
  * `backend/agent/planner.py`: Dynamic reasoning, hypothesis formulation, and next-tool planning.
  * `backend/agent/investigator.py`: Autonomous investigation cycle & interactive step-by-step engine.
  * `backend/agent/replanner.py`: Failure recovery and contradiction-aware adaptation.
  * `backend/tools/`: 9 modular, callable tools.
  * `backend/evaluation/evaluator.py`: Automated benchmark scoring module.
  * `frontend/src/`: Professional SOC Analyst dashboard in React + Tailwind.

---

## 🎥 Deliverable 4: 3–5 Minute Demo Video

▶️ **Google Drive Link**: `https://drive.google.com/your-demo-video-link-here` *(Replace with your Google Drive share link)*

> **CRITICAL**: Ensure Google Drive General Access is set to **"Anyone with the link can view"** (Viewer permission) so judges can watch without encountering permission denied screens.

### Minute-by-Minute Video Walkthrough (3:30 Total):
* **0:00 – 0:40 | Introduction & Problem**:
  * State team name, hackathon (Tech Zephyr 4.0, IIT Bhubaneswar), and Problem Statement 9.
  * Explain why traditional SOCs fail (alert fatigue, fixed playbooks, static chatbots).
* **0:40 – 1:30 | Scenario 1: Autonomous Breach Investigation & Mitigation**:
  * Show alert `ALT-1001` (SSH Brute Force).
  * Show agent dynamically pulling authentication logs, detecting 12 failures then root escalation, querying asset criticality & CVEs, blocking source IP `198.51.100.45`, and verifying firewall enforcement.
* **1:30 – 2:15 | Scenario 2: Dynamic Early Exit (False Positive)**:
  * Show alert `ALT-1002` (Port Scan).
  * Show the agent inspecting logs, observing routine Prometheus health checks (`200 OK`), and autonomously concluding `FALSE_POSITIVE` after only 2 tools without unnecessary queries.
* **2:15 – 2:50 | Scenario 4: Real-Time Contradiction Detection & Adaptation**:
  * Show initial diagnosis of suspicious out-of-hours admin session.
  * Click **"Inject Duo MFA Token Mid-Flight"**.
  * Show agent detecting contradiction, dynamically querying IAM directory for ticket `#INC-8892`, confirming authorization, and adapting decision to `LEGITIMATE_ADMIN_ACTIVITY`.
* **2:50 – 3:15 | Scenario 5: Failure Recovery**:
  * Show firewall API timeout error.
  * Show agent observing failure, re-planning fallback isolation route, and verifying rule enforcement.
* **3:15 – 3:30 | Benchmark & Conclusion**:
  * Open Evaluation Benchmark tab showing **100% accuracy, 100% false positive handling, 100% adaptation, and 100% recovery**.
  * Conclude: *"AegisSOC is not a chatbot — it is a closed-loop autonomous SOC investigator."*

---

## ⚙️ Deliverable 5: Runnable Setup Instructions

### Prerequisites
* Python 3.10+
* Node.js v18+ and npm

### Local Execution (Clean Start)
1. **Clone the repository**:
   ```bash
   git clone <YOUR_GITHUB_REPO_URL>
   cd autonomous_soc_agent
   ```
2. **Launch Backend Server**:
   ```bash
   cd backend
   py main.py
   ```
   *(Backend starts at `http://127.0.0.1:8000`)*
3. **Launch Frontend Dashboard**:
   ```bash
   cd ../frontend
   npm install
   npm run dev
   ```
   *(Open `http://localhost:5173` in your browser)*
4. **Run Benchmark Verification**:
   ```bash
   cd ../backend
   py evaluation/evaluator.py
   ```
