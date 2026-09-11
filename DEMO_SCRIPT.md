# AegisSOC — Judge Demo Script (60-Second Walkthrough)

**Tech Zephyr 4.0 — Agentic AI Hackathon, IIT Bhubaneswar**

---

## 🎯 Demo Goal
Demonstrate to judges in 60 seconds that **AegisSOC** is NOT a static LLM prompt or chatbot, but a closed-loop autonomous SOC investigator that observes, calls tools, decides, acts, verifies, and adapts when the environment changes.

---

## ⏱️ Step-by-Step Demo Flow

### 1. Alert Ingestion (0:00 - 0:10)
* **Action**: Open `http://localhost:5173`. Show the **Alert Dashboard**.
* **Talking Point**: *"We start at the AegisSOC Alert Queue. Here we have simulated NIDS and Suricata alerts. Rather than blindly outputting text, our agent independently decides what evidence it needs."*

### 2. Scenario 1 — Successful Attack & Closed-Loop Verification (0:10 - 0:25)
* **Action**: Click **"1. Successful Attack"** on the quick launcher bar. Switch to **Agent Workspace**.
* **Talking Point**: *"Watch the agent trajectory live. First, the agent formulates its goal. It queries asset details (`get_asset`), authentication logs (`get_server_logs`), CVE vulnerabilities (`get_vulnerabilities`), and packet flows (`get_network_events`). It identifies 12 failed logins followed by a root privilege escalation. It calculates a 98% risk score, classifies the attack as `ATTACK_SUCCESSFUL`, executes a simulated firewall block (`block_ip`), and re-checks the sandbox to verify rule enforcement (`verify_firewall`)."*

### 3. Scenario 4 — Mid-Investigation Adaptation (0:25 - 0:40)
* **Action**: Click **"4. Adaptation (MFA)"** on the Scenario Studio.
* **Talking Point**: *"Now observe agentic adaptation. Initially, an out-of-hours root login was flagged as suspicious. However, when a Duo MFA push token is ingested mid-flight, AegisSOC detects the contradiction with its previous hypothesis, invalidates the breach alert, lowers the risk score, and adapts its decision to Legitimate Admin Activity."*

### 4. Scenario 5 — Response Failure & Autonomous Recovery (0:40 - 0:50)
* **Action**: Click **"5. Failure Recovery"** on the Scenario Studio.
* **Talking Point**: *"Here, a ransomware C2 probe requires immediate containment. When the primary firewall tool returns a communication timeout error, AegisSOC doesn't stall or fail. It observes the failure, re-plans a fallback isolation pathway, executes the secondary block, and verifies enforcement."*

### 5. Evaluation Benchmark (0:50 - 1:00)
* **Action**: Click **Evaluation Benchmark** tab and click **"Run Benchmark Test"**.
* **Talking Point**: *"Finally, our automated evaluation module runs all 5 scenarios, achieving 100% investigation accuracy, 100% false positive handling, 100% adaptation success, and 100% tool failure recovery."*
