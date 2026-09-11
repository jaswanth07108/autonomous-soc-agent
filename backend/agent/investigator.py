import sys
import os
import json
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.alert_tool import get_alert, get_related_alerts
from tools.asset_tool import get_asset
from tools.log_tool import get_server_logs
from tools.vulnerability_tool import get_vulnerabilities
from tools.network_tool import get_network_events
from tools.firewall_tool import block_ip
from tools.verification_tool import verify_firewall
from tools.risk_tool import calculate_risk
from tools.identity_tool import verify_identity_and_ticket

from agent.planner import plan_next_investigation_step
from agent.decision_engine import evaluate_incident_decision
from agent.memory import record_step, clear_investigation_history, get_investigation_history
from agent.replanner import handle_firewall_failure_recovery, handle_evidence_contradiction
from data.database import get_db_connection

def execute_tool_by_name(tool_name: str, tool_args: Dict[str, Any]) -> Any:
    """Invokes real sandbox tools dynamically by name with arguments."""
    if tool_name == "get_alert":
        return get_alert(tool_args.get("alert_id"))
    elif tool_name == "get_server_logs":
        return get_server_logs(tool_args.get("ip_address"), tool_args.get("limit", 50))
    elif tool_name == "get_asset":
        return get_asset(tool_args.get("ip_address"))
    elif tool_name == "get_vulnerabilities":
        return get_vulnerabilities(tool_args.get("asset_id"))
    elif tool_name == "get_network_events":
        return get_network_events(tool_args.get("source_ip"), tool_args.get("destination_ip"))
    elif tool_name == "verify_identity_and_ticket":
        return verify_identity_and_ticket(tool_args.get("username"), tool_args.get("ticket_id"))
    elif tool_name == "get_related_alerts":
        return get_related_alerts(tool_args.get("ip_address"))
    elif tool_name == "block_ip":
        return block_ip(tool_args.get("ip_address"), tool_args.get("reason", "Automated mitigation"))
    elif tool_name == "verify_firewall":
        return verify_firewall(tool_args.get("ip_address"))
    else:
        return {"error": f"Unknown tool: {tool_name}"}

def run_autonomous_investigation(alert_id: str, require_human_approval: bool = False) -> Dict[str, Any]:
    """
    Executes a fully autonomous, dynamic SOC investigation cycle:
    GOAL -> OBSERVE -> DYNAMIC PLAN -> EXECUTE TOOLS -> DECIDE -> ACT -> VERIFY -> REPLAN
    """
    clear_investigation_history(alert_id)
    step_counter = 1
    tools_called = []

    # -------------------------------------------------------------
    # Step 1: Goal Formulation & Alert Ingestion
    # -------------------------------------------------------------
    goal = f"Investigate alert {alert_id} dynamically: form hypothesis, gather evidence, decide outcome, and mitigate if verified."
    alert_data = get_alert(alert_id)
    
    if "error" in alert_data:
        return {"status": "ERROR", "message": alert_data["error"]}

    source_ip = alert_data.get("source_ip", "")
    dest_ip = alert_data.get("destination_ip", "")

    record_step(
        alert_id=alert_id,
        step_index=step_counter,
        agent_action="GOAL_FORMULATION_AND_ALERT_INGESTION",
        tool_used="get_alert",
        tool_input={"alert_id": alert_id},
        evidence_found={
            "alert": alert_data,
            "rationale": "Initial trigger received. Parsing attack signature and targets to establish investigation objective."
        },
        decision="INITIALIZING_DYNAMIC_PLANNER"
    )
    step_counter += 1
    tools_called.append("get_alert")

    evidence_bundle = {
        "alert": alert_data,
        "asset": None,
        "server_logs": [],
        "vulnerabilities": [],
        "network_events": [],
        "identity_info": None
    }

    # -------------------------------------------------------------
    # Dynamic Planning Loop
    # -------------------------------------------------------------
    max_steps = 10
    final_hypothesis = ""
    
    while step_counter <= max_steps:
        plan = plan_next_investigation_step(alert_data, evidence_bundle, tools_called)
        final_hypothesis = plan.get("hypothesis", "")
        
        if plan.get("is_sufficient") or not plan.get("tool_to_call"):
            break

        tool_name = plan["tool_to_call"]
        tool_args = plan["tool_args"]
        rationale = plan["rationale"]
        hypothesis = plan["hypothesis"]

        # Real tool call execution against sandbox
        tool_result = execute_tool_by_name(tool_name, tool_args)
        tools_called.append(tool_name)

        # Update evidence bundle
        if tool_name == "get_server_logs":
            evidence_bundle["server_logs"] = tool_result
            evidence_summary = {"logs_retrieved": len(tool_result), "sample": tool_result[:3]}
        elif tool_name == "get_asset":
            evidence_bundle["asset"] = tool_result
            evidence_summary = {"asset": tool_result}
        elif tool_name == "get_vulnerabilities":
            evidence_bundle["vulnerabilities"] = tool_result
            evidence_summary = {"vulnerabilities": tool_result}
        elif tool_name == "get_network_events":
            evidence_bundle["network_events"] = tool_result
            evidence_summary = {"network_events": tool_result}
        elif tool_name == "verify_identity_and_ticket":
            evidence_bundle["identity_info"] = tool_result
            evidence_summary = {"identity": tool_result}
        else:
            evidence_summary = {"result": tool_result}

        evidence_summary["rationale"] = rationale
        evidence_summary["hypothesis"] = hypothesis

        record_step(
            alert_id=alert_id,
            step_index=step_counter,
            agent_action=f"DYNAMIC_TOOL_CALL:{tool_name.upper()}",
            tool_used=tool_name,
            tool_input=tool_args,
            evidence_found=evidence_summary,
            decision="INVESTIGATING",
            confidence=0.5
        )
        step_counter += 1

    # -------------------------------------------------------------
    # Risk Calculation & Decision Formulation
    # -------------------------------------------------------------
    risk_info = calculate_risk(evidence_bundle)
    record_step(
        alert_id=alert_id,
        step_index=step_counter,
        agent_action="CALCULATE_RISK_SCORE",
        tool_used="calculate_risk",
        tool_input={},
        evidence_found={"risk": risk_info, "hypothesis": final_hypothesis},
        decision="EVALUATING_RISK"
    )
    step_counter += 1

    decision, confidence, rec_action, reasoning = evaluate_incident_decision(evidence_bundle, risk_info)

    record_step(
        alert_id=alert_id,
        step_index=step_counter,
        agent_action="FORMULATE_DECISION",
        tool_used="evaluate_incident_decision",
        tool_input={},
        evidence_found={
            "reasoning": reasoning,
            "recommended_action": rec_action,
            "final_hypothesis": final_hypothesis
        },
        decision=decision,
        confidence=confidence
    )
    step_counter += 1

    # Check for Human Override requirement
    if require_human_approval and rec_action.startswith("BLOCK_IP"):
        return {
            "status": "WAITING_FOR_HUMAN_APPROVAL",
            "alert_id": alert_id,
            "decision": decision,
            "confidence": confidence,
            "risk_info": risk_info,
            "recommended_action": rec_action,
            "reasoning": reasoning,
            "evidence": evidence_bundle,
            "history": get_investigation_history(alert_id)
        }

    # -------------------------------------------------------------
    # Response Execution & Closed-Loop Verification
    # -------------------------------------------------------------
    action_executed = "NO_ACTION"
    verification_result = None
    recovery_info = None

    if rec_action.startswith("BLOCK_IP"):
        action_res = block_ip(source_ip, reason=f"Automated AegisSOC Mitigation: {decision}")
        
        if action_res.get("status") == "FAILED":
            recovery_info = handle_firewall_failure_recovery(
                alert_id=alert_id,
                ip_address=source_ip,
                step_index=step_counter,
                error_message=action_res.get("message", "Rule deployment failed")
            )
            step_counter += 2
            action_executed = "BLOCK_IP_RECOVERED"
            verification_result = recovery_info.get("verification")
        else:
            action_executed = "BLOCK_IP"
            verification_result = verify_firewall(source_ip)
            record_step(
                alert_id=alert_id,
                step_index=step_counter,
                agent_action="EXECUTE_AND_VERIFY_RESPONSE",
                tool_used="block_ip & verify_firewall",
                tool_input={"source_ip": source_ip},
                evidence_found={"firewall_action": action_res, "verification": verification_result},
                decision=decision,
                confidence=confidence
            )
            step_counter += 1

    final_history = get_investigation_history(alert_id)

    return {
        "status": "COMPLETED",
        "alert_id": alert_id,
        "goal": goal,
        "decision": decision,
        "confidence": confidence,
        "risk_info": risk_info,
        "recommended_action": rec_action,
        "action_executed": action_executed,
        "verification_result": verification_result,
        "reasoning": reasoning,
        "evidence": evidence_bundle,
        "history": final_history,
        "recovery_info": recovery_info,
        "tools_called_count": len(tools_called)
    }

def step_autonomous_investigation(alert_id: str, session_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Executes a single dynamic step in an interactive investigation session.
    Allows judges and analysts to inspect the agent's thought process step-by-step.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    if not session_id:
        session_id = f"SES-{uuid.uuid4().hex[:8]}"
        clear_investigation_history(alert_id)
        
        # Step 1: Alert Ingestion
        alert_data = get_alert(alert_id)
        evidence_bundle = {
            "alert": alert_data,
            "asset": None,
            "server_logs": [],
            "vulnerabilities": [],
            "network_events": [],
            "identity_info": None
        }
        tools_called = ["get_alert"]
        
        record_step(
            alert_id=alert_id,
            step_index=1,
            agent_action="GOAL_FORMULATION_AND_ALERT_INGESTION",
            tool_used="get_alert",
            tool_input={"alert_id": alert_id},
            evidence_found={"alert": alert_data},
            decision="INITIALIZING_SESSION"
        )

        plan = plan_next_investigation_step(alert_data, evidence_bundle, tools_called)

        now_str = datetime.now(timezone.utc).isoformat()
        cursor.execute("""
        INSERT INTO investigation_sessions 
        (session_id, alert_id, status, step_counter, current_hypothesis, confidence, evidence_bundle, tools_called, decision, recommended_action, action_executed, verification_result, reasoning, updated_at)
        VALUES (?, ?, 'IN_PROGRESS', 1, ?, 0.5, ?, ?, NULL, NULL, NULL, NULL, NULL, ?)
        """, (session_id, alert_id, plan.get("hypothesis", ""), json.dumps(evidence_bundle), json.dumps(tools_called), now_str))
        conn.commit()
        conn.close()

        return {
            "session_id": session_id,
            "alert_id": alert_id,
            "status": "IN_PROGRESS",
            "step": 1,
            "hypothesis": plan.get("hypothesis"),
            "next_planned_tool": plan.get("tool_to_call"),
            "next_planned_rationale": plan.get("rationale"),
            "is_complete": False,
            "history": get_investigation_history(alert_id)
        }

    # Retrieve existing session
    cursor.execute("SELECT * FROM investigation_sessions WHERE session_id = ?", (session_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return {"error": f"Session {session_id} not found."}

    session = dict(row)
    evidence_bundle = json.loads(session["evidence_bundle"])
    tools_called = json.loads(session["tools_called"])
    step_counter = session["step_counter"] + 1
    alert_data = evidence_bundle.get("alert", {})

    plan = plan_next_investigation_step(alert_data, evidence_bundle, tools_called)

    if plan.get("is_sufficient") or not plan.get("tool_to_call"):
        # Investigation reached conclusion, calculate risk and action
        risk_info = calculate_risk(evidence_bundle)
        decision, confidence, rec_action, reasoning = evaluate_incident_decision(evidence_bundle, risk_info)
        
        action_executed = "NO_ACTION"
        verification_result = None
        source_ip = alert_data.get("source_ip", "")

        if rec_action.startswith("BLOCK_IP"):
            action_res = block_ip(source_ip, reason=f"Automated Mitigation: {decision}")
            if action_res.get("status") == "FAILED":
                rec = handle_firewall_failure_recovery(alert_id, source_ip, step_counter, "Timeout")
                action_executed = "BLOCK_IP_RECOVERED"
                verification_result = rec.get("verification")
            else:
                action_executed = "BLOCK_IP"
                verification_result = verify_firewall(source_ip)

        record_step(
            alert_id=alert_id,
            step_index=step_counter,
            agent_action="FORMULATE_FINAL_DECISION",
            tool_used="decision_engine",
            tool_input={},
            evidence_found={"reasoning": reasoning, "action": action_executed, "verification": verification_result},
            decision=decision,
            confidence=confidence
        )

        now_str = datetime.now(timezone.utc).isoformat()
        cursor.execute("""
        UPDATE investigation_sessions
        SET status = 'COMPLETED', step_counter = ?, decision = ?, recommended_action = ?, action_executed = ?, 
            verification_result = ?, reasoning = ?, updated_at = ?
        WHERE session_id = ?
        """, (step_counter, decision, rec_action, action_executed, json.dumps(verification_result), reasoning, now_str, session_id))
        conn.commit()
        conn.close()

        return {
            "session_id": session_id,
            "alert_id": alert_id,
            "status": "COMPLETED",
            "step": step_counter,
            "decision": decision,
            "confidence": confidence,
            "recommended_action": rec_action,
            "action_executed": action_executed,
            "verification_result": verification_result,
            "reasoning": reasoning,
            "is_complete": True,
            "history": get_investigation_history(alert_id)
        }

    # Execute next planned tool
    tool_name = plan["tool_to_call"]
    tool_args = plan["tool_args"]
    tool_result = execute_tool_by_name(tool_name, tool_args)
    tools_called.append(tool_name)

    if tool_name == "get_server_logs":
        evidence_bundle["server_logs"] = tool_result
    elif tool_name == "get_asset":
        evidence_bundle["asset"] = tool_result
    elif tool_name == "get_vulnerabilities":
        evidence_bundle["vulnerabilities"] = tool_result
    elif tool_name == "get_network_events":
        evidence_bundle["network_events"] = tool_result
    elif tool_name == "verify_identity_and_ticket":
        evidence_bundle["identity_info"] = tool_result

    record_step(
        alert_id=alert_id,
        step_index=step_counter,
        agent_action=f"STEP:{tool_name.upper()}",
        tool_used=tool_name,
        tool_input=tool_args,
        evidence_found={"result": tool_result, "rationale": plan.get("rationale")},
        decision="INVESTIGATING",
        confidence=0.5
    )

    next_plan = plan_next_investigation_step(alert_data, evidence_bundle, tools_called)

    now_str = datetime.now(timezone.utc).isoformat()
    cursor.execute("""
    UPDATE investigation_sessions
    SET step_counter = ?, current_hypothesis = ?, evidence_bundle = ?, tools_called = ?, updated_at = ?
    WHERE session_id = ?
    """, (step_counter, next_plan.get("hypothesis", ""), json.dumps(evidence_bundle), json.dumps(tools_called), now_str, session_id))
    conn.commit()
    conn.close()

    return {
        "session_id": session_id,
        "alert_id": alert_id,
        "status": "IN_PROGRESS",
        "step": step_counter,
        "tool_executed": tool_name,
        "observation": tool_result,
        "hypothesis": next_plan.get("hypothesis"),
        "next_planned_tool": next_plan.get("tool_to_call"),
        "next_planned_rationale": next_plan.get("rationale"),
        "is_complete": next_plan.get("is_sufficient", False),
        "history": get_investigation_history(alert_id)
    }
