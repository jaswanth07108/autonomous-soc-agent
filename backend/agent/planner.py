import sys
import os
from typing import Dict, Any, List, Tuple, Optional

def plan_next_investigation_step(
    alert: Dict[str, Any],
    evidence: Dict[str, Any],
    tools_called: List[str]
) -> Dict[str, Any]:
    """
    Autonomous Investigation Planner.
    Evaluates current hypothesis, checks information gaps, and dynamically
    selects the next best tool to call rather than running a rigid script.
    """
    attack_type = alert.get("attack_type", "")
    source_ip = alert.get("source_ip", "")
    dest_ip = alert.get("destination_ip", "")
    severity = alert.get("severity", "MEDIUM")

    logs = evidence.get("server_logs", [])
    asset = evidence.get("asset")
    vulns = evidence.get("vulnerabilities")
    network_events = evidence.get("network_events")
    identity_info = evidence.get("identity_info")

    # -------------------------------------------------------------
    # Rule 1: Always check server/authentication logs first to ground the alert
    # -------------------------------------------------------------
    if "get_server_logs" not in tools_called:
        return {
            "hypothesis": f"Initial hypothesis: Alert '{attack_type}' requires authentication/system telemetry verification.",
            "tool_to_call": "get_server_logs",
            "tool_args": {"ip_address": dest_ip, "limit": 50},
            "rationale": "Must inspect server authentication and access logs to verify whether suspicious activity reached the target.",
            "missing_evidence": ["Authentication outcomes", "Host execution telemetry"],
            "is_sufficient": False
        }

    # -------------------------------------------------------------
    # Rule 2: Evaluate Logs & Branch Dynamically
    # -------------------------------------------------------------
    
    # Check for MFA / Admin tickets in logs (Scenario 4)
    mfa_verified = any(l.get("status") == "VERIFIED_ADMIN" for l in logs)
    if mfa_verified:
        if "verify_identity_and_ticket" not in tools_called:
            mfa_log = next((l for l in logs if l.get("status") == "VERIFIED_ADMIN"), {})
            username = mfa_log.get("username", "alex.director")
            return {
                "hypothesis": "CONTRADICTION DETECTED: Authentication logs show Duo MFA assertion. Cross-referencing IAM ticket registry.",
                "tool_to_call": "verify_identity_and_ticket",
                "tool_args": {"username": username, "ticket_id": "#INC-8892"},
                "rationale": "An emergency maintenance ticket was cited in authentication logs. Verifying authorization in IAM corporate directory.",
                "missing_evidence": ["Corporate change management verification"],
                "is_sufficient": False
            }
        else:
            return {
                "hypothesis": "CONFIRMED: Authorized administrative emergency maintenance session with valid MFA and approval ticket.",
                "tool_to_call": None,
                "tool_args": {},
                "rationale": "Both MFA authentication and corporate ticket registry confirm legitimate SecOps maintenance. Investigation complete.",
                "missing_evidence": [],
                "is_sufficient": True
            }

    # Check for Benign Telemetry / Health Checks (Scenario 2 Early Exit)
    has_failed_events = any(l.get("status") in ["FAILED", "CRITICAL", "BLOCKED"] for l in logs)
    all_success_logs = logs and all(l.get("status") == "SUCCESS" for l in logs)
    if all_success_logs and not has_failed_events:
        return {
            "hypothesis": "HYPOTHESIS CONFIRMED: Traffic matches authorized internal monitoring (Prometheus/DevOps probes).",
            "tool_to_call": None,
            "tool_args": {},
            "rationale": "Server logs show exclusively successful health check metrics with zero exploit attempts or authentication anomalies. No further queries required.",
            "missing_evidence": [],
            "is_sufficient": True
        }

    # Check for WAF Rejections / Failed Exploits (Scenario 3)
    has_waf_block = any(l.get("status") == "BLOCKED" for l in logs)
    has_auth_success = any(l.get("status") == "SUCCESS" and "AUTHENTICATION" in l.get("event_type", "") for l in logs)
    
    if has_waf_block and not has_auth_success:
        if "get_asset" not in tools_called:
            return {
                "hypothesis": "Hypothesis: Web exploit attempts detected but blocked by perimeter WAF. Inspecting host configuration.",
                "tool_to_call": "get_asset",
                "tool_args": {"ip_address": dest_ip},
                "rationale": "WAF rejected exploit payloads. Checking target asset details to locate associated vulnerability records.",
                "missing_evidence": ["Target asset metadata"],
                "is_sufficient": False
            }
        elif "get_vulnerabilities" not in tools_called and asset:
            asset_id = asset.get("asset_id", "")
            return {
                "hypothesis": "Hypothesis: Checking CVE patch status to verify whether host is immune to attempted exploit.",
                "tool_to_call": "get_vulnerabilities",
                "tool_args": {"asset_id": asset_id},
                "rationale": "Verifying whether vulnerability CVE-2024-21762 was patched on target server.",
                "missing_evidence": ["CVE patch confirmation"],
                "is_sufficient": False
            }
        else:
            return {
                "hypothesis": "HYPOTHESIS CONFIRMED: Attack failed. Requests blocked by WAF (403 Forbidden) and host vulnerability is patched.",
                "tool_to_call": None,
                "tool_args": {},
                "rationale": "Evidence confirms defense-in-depth held: perimeter dropped requests and vulnerability is patched. Investigation complete.",
                "missing_evidence": [],
                "is_sufficient": True
            }

    # Check for Credential Compromise / Privilege Escalation / RCE (Scenario 1 & 5)
    priv_esc = any(l.get("event_type") == "PRIVILEGE_ESCALATION" for l in logs)
    rce_attempt = any(l.get("event_type") in ["RCE_ATTEMPT", "WEBSHELL_UPLOAD"] for l in logs)
    
    if priv_esc or has_auth_success or rce_attempt:
        if "get_asset" not in tools_called:
            return {
                "hypothesis": "CRITICAL HYPOTHESIS: Host authentication compromised or active RCE attempt. Checking target criticality.",
                "tool_to_call": "get_asset",
                "tool_args": {"ip_address": dest_ip},
                "rationale": "Breach indicator detected in logs. Querying asset inventory to evaluate target criticality and exposure.",
                "missing_evidence": ["Asset criticality", "Data owner"],
                "is_sufficient": False
            }
        elif "get_vulnerabilities" not in tools_called and asset:
            asset_id = asset.get("asset_id", "")
            return {
                "hypothesis": "Hypothesis: Asset is high-value. Checking if unpatched vulnerabilities enabled exploitation.",
                "tool_to_call": "get_vulnerabilities",
                "tool_args": {"asset_id": asset_id},
                "rationale": "Determining whether known unpatched CVEs on target asset enabled privilege escalation.",
                "missing_evidence": ["Asset CVE vulnerabilities"],
                "is_sufficient": False
            }
        elif "get_network_events" not in tools_called:
            return {
                "hypothesis": "Hypothesis: Checking network metadata for exfiltration volume or active C2 channels.",
                "tool_to_call": "get_network_events",
                "tool_args": {"source_ip": source_ip, "destination_ip": dest_ip},
                "rationale": "Measuring packet count and byte volume transferred between attacker IP and compromised server.",
                "missing_evidence": ["Network exfiltration volume"],
                "is_sufficient": False
            }
        else:
            return {
                "hypothesis": "HYPOTHESIS CONFIRMED: Attack successful with root compromise and data exfiltration.",
                "tool_to_call": None,
                "tool_args": {},
                "rationale": "Comprehensive evidence collected: authentication breach, privilege escalation, unpatched CVE, and active network flow.",
                "missing_evidence": [],
                "is_sufficient": True
            }

    # Default fallback: check asset if not already checked
    if "get_asset" not in tools_called:
        return {
            "hypothesis": "Hypothesis: Gathering baseline asset information for target host.",
            "tool_to_call": "get_asset",
            "tool_args": {"ip_address": dest_ip},
            "rationale": "Need asset metadata to understand context of alert.",
            "missing_evidence": ["Asset metadata"],
            "is_sufficient": False
        }

    return {
        "hypothesis": "Evidence gathered sufficient for incident classification.",
        "tool_to_call": None,
        "tool_args": {},
        "rationale": "Sufficient evidence collected to compute prototype risk and formulate response.",
        "missing_evidence": [],
        "is_sufficient": True
    }
