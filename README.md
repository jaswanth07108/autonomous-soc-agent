# AegisSOC — Autonomous SOC Investigation & Response Agent

**Tech Zephyr 4.0 — Agentic AI Hackathon, IIT Bhubaneswar**  
*Problem Statement 9: Autonomous SOC Investigation & Response Agent*

---

## 🛡️ Executive Summary

Traditional Security Operations Center (SOC) environments rely heavily on static intrusion detection system (IDS) rules, fixed playbook scripts, or simple prompt-driven LLM chatbots that merely summarize alerts without taking real actions. These legacy systems generate immense alert fatigue, miss complex multi-stage attacks, and lack the ability to dynamically gather evidence, verify mitigation outcomes, or recover from tool failures.

**AegisSOC** is a genuinely **Agentic AI SOC Investigation & Response System** operating entirely within a safe, simulated sandbox environment. Instead of producing static text responses, AegisSOC executes an autonomous closed-loop trajectory:

$$\mathbf{GOAL} \longrightarrow \mathbf{OBSERVE} \longrightarrow \mathbf{PLAN} \longrightarrow \mathbf{TOOL\ CALL} \longrightarrow \mathbf{INVESTIGATE} \longrightarrow \mathbf{DECIDE} \longrightarrow \mathbf{ACT} \longrightarrow \mathbf{VERIFY} \longrightarrow \mathbf{ADAPT/REPLAN} \longrightarrow \mathbf{FINAL\ OUTCOME}$$

---

## 🏛️ System Architecture

```
                                  ┌────────────────────────────────────────────────────────┐
                                  │           AegisSOC Analyst Dashboard (React + Vite)    │
                                  └───────────────────────────┬────────────────────────────┘
                                                              │ REST API (FastAPI)
                                                              ▼
                                  ┌────────────────────────────────────────────────────────┐
                                  │               FastAPI Gateway (backend/api)            │
                                  └───────────────────────────┬────────────────────────────┘
                                                              │
                                                              ▼
                                  ┌────────────────────────────────────────────────────────┐
                                  │            Autonomous SOC Agent State Machine          │
                                  │    (Goal -> Observe -> Plan -> Investigate -> Act)     │
                                  └───────┬───────────────────┬───────────────────┬────────┘
                                          │                   │                   │
                                          ▼                   ▼                   ▼
                               ┌──────────────────┐┌──────────────────┐┌──────────────────┐
                               │ Tool Orchestrator││ Decision Engine  ││ Re-Planner &     │
                               │ (backend/tools)  ││ & Risk Calculator││ Adaptation Unit  │
                               └──────────┬───────┘└──────────┬───────┘└──────────┬───────┘
                                          │                   │                   │
                                          └───────────────────┼───────────────────┘
                                                              │
                                                              ▼
                                  ┌────────────────────────────────────────────────────────┐
                                  │          Local SQLite Sandbox (soc_sandbox.db)         │
                                  │  - security_alerts     - server_logs    - assets       │
                                  │  - vulnerabilities     - network_events - firewall_state│
                                  │  - investigation_history (Audit Log Memory)            │
                                  └────────────────────────────────────────────────────────┘
```

---

## ⚡ Key Differentiators & Features

1. **Evidence-Driven Autonomous Investigation**: The agent does not jump to conclusions upon receiving an alert. It formulates hypotheses and dynamically selects appropriate tools (`get_alert`, `get_asset`, `get_server_logs`, `get_vulnerabilities`, `get_network_events`).
2. **Closed-Loop Mitigation Verification**: When the agent issues a perimeter block (`block_ip`), it re-checks the sandbox environment (`verify_firewall`) to ensure enforcement.
3. **Contradiction-Aware Adaptation Engine**: If new mid-investigation evidence is ingested (e.g. an approved Duo MFA ticket for an administrative session), the agent detects the contradiction, invalidates prior suspicion, lowers the risk score, and updates its conclusion.
4. **Autonomous Failure Recovery**: If a firewall tool invocation fails (e.g., simulated timeout), the agent detects the failure, logs the observation, re-plans via a secondary fallback isolation route, and verifies enforcement.
5. **Transparent Prototype SOC Risk Model**: Explicit, explainable risk scoring (0–100) combining alert severity, authentication telemetry, CVE exploitability, and target asset criticality.
6. **Human-in-the-Loop Interceptor**: Supports interactive human supervisor approval modals for high-impact perimeter actions.

---

## 📊 The 5 Hackathon Demo Scenarios

| Scenario | Incident Type | Ingested Evidence Summary | Agent Decision | Action Taken | Verification / Outcome |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Scenario 1** | Successful Attack | SSH brute force -> 12 failures -> successful login as `admin` -> root escalation | `ATTACK_SUCCESSFUL` | `BLOCK_IP` | Verified Enforced in Firewall |
| **Scenario 2** | False Positive | Port scan alert -> Internal DevOps Prometheus health check logs | `FALSE_POSITIVE` | `NO_ACTION` | Spared from Blocking |
| **Scenario 3** | Attack Failed | Web SQLi & Traversal -> WAF 403 Forbidden -> Target CVE is patched | `ATTACK_FAILED` | `MONITOR` | No Emergency Escalation |
| **Scenario 4** | Conflicting Evidence | Out-of-hours admin session -> Injected Duo MFA ticket `#INC-8892` | `LEGITIMATE_ADMIN_ACTIVITY` | `NO_ACTION` | Decision Adapted Mid-flight |
| **Scenario 5** | Response Failure | Ransomware C2 probe -> Primary firewall timeout error | `ATTACK_SUCCESSFUL` | `BLOCK_IP_RECOVERED` | Autonomous Fallback & Verified |

---

## 📈 Evaluation Benchmark Results

The built-in evaluation module (`backend/evaluation/evaluator.py`) automatically executes all 5 scenarios and generates benchmark metrics:

* **Investigation Accuracy**: `100.0%`
* **Evidence Sufficiency Rate**: `100.0%`
* **False Positive Handling**: `100.0%`
* **Adaptation Success Rate**: `100.0%`
* **Action Verification Rate**: `100.0%`
* **Tool Failure Recovery Rate**: `100.0%`

---

## 🛠️ Tech Stack

* **Backend**: Python 3.14, FastAPI, SQLite3, Pydantic, Uvicorn
* **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Lucide React Icons
* **Data Layer**: Clean local SQLite sandbox with synthetic cybersecurity datasets

---

## 🚀 Quickstart & Setup Instructions

### Prerequisites
* Python 3.10+
* Node.js v18+ and npm

### 1. Launch Backend Server
```bash
cd backend
py seed_data.py
py -m uvicorn main:app --port 8000 --reload
```
The FastAPI backend server will start at `http://127.0.0.1:8000`.

### 2. Launch Frontend Dashboard
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## 🔒 Cybersecurity Safety Statement

All security actions, IP blocking commands, server logs, asset inventories, and vulnerability checks operate strictly inside a local, isolated SQLite sandbox environment (`soc_sandbox.db`). AegisSOC does **NOT** scan external networks, attack real servers, or alter real physical firewalls.

---

## 🏆 Hackathon Submission Checklist Compliance

- [x] Autonomous Agent Workflow (Goal -> Plan -> Decide -> Act -> Verify -> Adapt)
- [x] Real Tool Calling (12 executable tools)
- [x] Failure Recovery Demonstration (Scenario 5)
- [x] Mid-Investigation Adaptation (Scenario 4)
- [x] Human-in-the-Loop Override Modal
- [x] Automated Evaluation Benchmark Module
- [x] Modern SOC Dashboard UI
