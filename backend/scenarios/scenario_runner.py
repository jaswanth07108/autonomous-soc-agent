import sys
import os
from datetime import datetime, timezone

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data.seed_data import seed_sandbox_data
from data.database import get_db_connection
from agent.investigator import run_autonomous_investigation
from agent.replanner import handle_evidence_contradiction
from tools.firewall_tool import set_firewall_failure_flag
from tools.log_tool import get_server_logs
from tools.alert_tool import get_alert

def inject_scenario_4_mfa_evidence():
    """Dynamically inserts contradictory Duo MFA push verification into the sandbox database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    now_str = datetime.now(timezone.utc).isoformat()
    cursor.execute("""
    INSERT INTO server_logs (log_id, timestamp, server_ip, source_ip, username, event_type, action, status, message, scenario_id)
    VALUES ('LOG-104-ADAPT', ?, '10.0.3.5', '198.51.100.99', 'alex.director', 'MFA_VERIFICATION', 'DUO_MFA_PUSH', 'VERIFIED_ADMIN', 'MFA Approved: Push token verified. Change ticket #INC-8892 (Approved Emergency Maintenance by SecOps VP)', 'SCENARIO_4')
    ON CONFLICT(log_id) DO UPDATE SET status = 'VERIFIED_ADMIN'
    """, (now_str,))
    conn.commit()
    conn.close()

def trigger_scenario(scenario_id: int):
    """
    Triggers one of the 5 official hackathon demo scenarios:
    1: Successful Attack
    2: False Positive
    3: Failed Attack
    4: Conflicting Evidence (Dynamic Adaptation Demo)
    5: Response Failure (Autonomous Recovery Demo)
    """
    seed_sandbox_data()

    if scenario_id == 1:
        # Scenario 1: Successful Attack (ALT-1001)
        res = run_autonomous_investigation("ALT-1001")
        res["scenario_name"] = "Scenario 1: Successful Attack"
        res["scenario_description"] = "SSH Brute-force -> Dynamic Planner identifies breach -> Root Escalation -> Block & Verify"
        return res

    elif scenario_id == 2:
        # Scenario 2: False Positive (ALT-1002)
        res = run_autonomous_investigation("ALT-1002")
        res["scenario_name"] = "Scenario 2: False Positive"
        res["scenario_description"] = "Suspicious Port Scan Alert -> Dynamic Planner observes benign telemetry -> Concludes early -> No Block"
        return res

    elif scenario_id == 3:
        # Scenario 3: Attack Failed (ALT-1003)
        res = run_autonomous_investigation("ALT-1003")
        res["scenario_name"] = "Scenario 3: Attack Failed"
        res["scenario_description"] = "SQL Injection Attempt -> Dynamic Planner queries WAF rejections & patched CVE -> Attack Failed -> Monitor"
        return res

    elif scenario_id == 4:
        # Scenario 4: Conflicting Evidence & Dynamic Adaptation (ALT-1004)
        # Phase 1: Initial Investigation (Suspicious Admin Access without MFA)
        initial_res = run_autonomous_investigation("ALT-1004")
        
        # Phase 2: Live Contradictory Evidence Ingestion into Sandbox DB
        inject_scenario_4_mfa_evidence()
        new_logs = get_server_logs("10.0.3.5")
        
        # Phase 3: Autonomous Agent Adaptation & IAM Ticket Verification
        adaptation_res = handle_evidence_contradiction(
            alert_id="ALT-1004",
            previous_decision=initial_res.get("decision", "ATTACK_SUCCESSFUL"),
            new_evidence={"server_logs": new_logs},
            step_index=len(initial_res.get("history", [])) + 1
        )
        
        initial_res["status"] = "ADAPTED"
        initial_res["decision"] = adaptation_res["new_decision"]
        initial_res["confidence"] = adaptation_res["confidence"]
        initial_res["action_executed"] = "NO_ACTION"
        initial_res["contradiction_adaptation"] = adaptation_res
        initial_res["scenario_name"] = "Scenario 4: Conflicting Evidence (Dynamic Adaptation Demo)"
        initial_res["scenario_description"] = "Initial Suspicious Out-of-hours Admin Login -> Duo MFA Ticket Injected -> Agent Detects Contradiction -> Queries IAM Directory -> Re-evaluates to Legitimate Admin Activity"
        return initial_res

    elif scenario_id == 5:
        # Scenario 5: Response Failure & Autonomous Recovery (ALT-1005)
        set_firewall_failure_flag("198.51.100.120", 1)

        res = run_autonomous_investigation("ALT-1005")
        res["scenario_name"] = "Scenario 5: Response Failure & Recovery"
        res["scenario_description"] = "Ransomware RCE Alert -> Initial Firewall Block Timeout -> Agent Observes Failure -> Autonomous Re-plan & Fallback Isolation -> Final Verification"
        return res

    else:
        return {"error": f"Invalid scenario ID {scenario_id}. Choose between 1 and 5."}
