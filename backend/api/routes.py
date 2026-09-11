from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any, Optional

from data.database import get_db_connection, reset_db
from data.seed_data import seed_sandbox_data
from agent.investigator import run_autonomous_investigation, step_autonomous_investigation
from agent.memory import get_investigation_history
from agent.replanner import handle_evidence_contradiction
from scenarios.scenario_runner import trigger_scenario, inject_scenario_4_mfa_evidence
from evaluation.evaluator import run_evaluation_benchmark
from tools.firewall_tool import get_firewall_state, block_ip
from tools.verification_tool import verify_firewall

router = APIRouter(prefix="/api")

@router.get("/alerts")
def list_alerts():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM security_alerts ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

@router.get("/alerts/{alert_id}")
def get_alert_detail(alert_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM security_alerts WHERE alert_id = ?", (alert_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Alert not found")
    return dict(row)

@router.post("/investigate/{alert_id}")
def investigate_alert(alert_id: str, payload: Optional[Dict[str, Any]] = Body(None)):
    require_approval = payload.get("require_human_approval", False) if payload else False
    result = run_autonomous_investigation(alert_id, require_human_approval=require_approval)
    return result

@router.post("/investigate/{alert_id}/step")
def investigate_alert_step(alert_id: str, payload: Optional[Dict[str, Any]] = Body(None)):
    session_id = payload.get("session_id") if payload else None
    return step_autonomous_investigation(alert_id, session_id=session_id)

@router.get("/investigation/{alert_id}/history")
def fetch_history(alert_id: str):
    return get_investigation_history(alert_id)

@router.post("/scenarios/trigger/{scenario_id}")
def trigger_scenario_endpoint(scenario_id: int):
    if scenario_id < 1 or scenario_id > 5:
        raise HTTPException(status_code=400, detail="Scenario ID must be between 1 and 5")
    return trigger_scenario(scenario_id)

@router.post("/scenarios/scenario-4-inject")
def inject_mfa_and_adapt():
    """Live injection of MFA push verification and corporate ticket into Scenario 4."""
    inject_scenario_4_mfa_evidence()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM server_logs WHERE server_ip = '10.0.3.5'")
    new_logs = [dict(r) for r in cursor.fetchall()]
    conn.close()

    history = get_investigation_history("ALT-1004")
    prev_decision = history[-1]["decision"] if history else "ATTACK_SUCCESSFUL"

    res = handle_evidence_contradiction(
        alert_id="ALT-1004",
        previous_decision=prev_decision,
        new_evidence={"server_logs": new_logs},
        step_index=len(history) + 1
    )
    res["history"] = get_investigation_history("ALT-1004")
    return res

@router.post("/evidence/inject")
def inject_evidence(payload: Dict[str, Any] = Body(...)):
    alert_id = payload.get("alert_id", "ALT-1004")
    previous_decision = payload.get("previous_decision", "ATTACK_SUCCESSFUL")
    new_log = payload.get("new_log", {
        "log_id": "LOG-104-ADAPT",
        "username": "alex.director",
        "event_type": "MFA_VERIFICATION",
        "status": "VERIFIED_ADMIN",
        "message": "MFA Approved: Push token verified. Change ticket #INC-8892 (Approved Emergency Maintenance by SecOps VP)"
    })
    
    inject_scenario_4_mfa_evidence()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM server_logs WHERE server_ip = '10.0.3.5'")
    new_logs = [dict(r) for r in cursor.fetchall()]
    conn.close()

    history = get_investigation_history(alert_id)

    res = handle_evidence_contradiction(
        alert_id=alert_id,
        previous_decision=previous_decision,
        new_evidence={"server_logs": new_logs},
        step_index=len(history) + 1
    )
    res["history"] = get_investigation_history(alert_id)
    return res

@router.post("/human-override")
def human_override(payload: Dict[str, Any] = Body(...)):
    alert_id = payload.get("alert_id")
    action = payload.get("action")  # APPROVE, REJECT, MORE_INFO
    source_ip = payload.get("source_ip")

    if action == "APPROVE":
        block_res = block_ip(source_ip, reason="Human Approved SOC Mitigation")
        v_res = verify_firewall(source_ip)
        return {
            "status": "APPROVED",
            "message": f"Human supervisor approved firewall block on {source_ip}.",
            "firewall_result": block_res,
            "verification": v_res
        }
    elif action == "REJECT":
        return {
            "status": "REJECTED",
            "message": f"Human supervisor rejected firewall block on {source_ip}. Action cancelled.",
            "rule_active": False
        }
    else:
        return {
            "status": "PENDING_INVESTIGATION",
            "message": "Additional evidence requested by human supervisor."
        }

@router.get("/firewall/state")
def firewall_state(ip_address: Optional[str] = None):
    return get_firewall_state(ip_address)

@router.get("/evaluation/metrics")
def evaluation_metrics():
    return run_evaluation_benchmark()

@router.post("/reset")
def reset_database():
    seed_sandbox_data()
    return {"status": "SUCCESS", "message": "Database sandbox successfully reset with fresh seed data."}
