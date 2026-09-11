def calculate_risk(evidence: dict) -> dict:
    """
    Calculate evidence-backed Prototype SOC Risk Score (0-100).
    Explicit heuristic breakdown for hackathon transparency.
    """
    factors = []
    base_score = 0.0

    alert = evidence.get("alert") or {}
    severity = alert.get("severity", "MEDIUM").upper()
    if severity == "CRITICAL":
        base_score += 40
        factors.append("Critical alert severity (+40)")
    elif severity == "HIGH":
        base_score += 30
        factors.append("High alert severity (+30)")
    elif severity == "MEDIUM":
        base_score += 15
        factors.append("Medium alert severity (+15)")
    else:
        base_score += 5
        factors.append("Low alert severity (+5)")

    # 1. Authentication & System Logs Factor
    logs = evidence.get("server_logs") or []
    has_success_auth = any(l.get("status") == "SUCCESS" and "AUTHENTICATION" in l.get("event_type", "") for l in logs)
    has_priv_esc = any(l.get("event_type") == "PRIVILEGE_ESCALATION" for l in logs)
    has_mfa_approved = any(l.get("status") == "VERIFIED_ADMIN" for l in logs)

    if has_mfa_approved:
        base_score -= 30
        factors.append("Legitimate MFA-verified admin session (-30)")
    elif has_priv_esc:
        base_score += 35
        factors.append("Successful privilege escalation confirmed (+35)")
    elif has_success_auth:
        base_score += 25
        factors.append("Successful authentication after probe (+25)")
    else:
        all_blocked = logs and all(l.get("status") in ["BLOCKED", "FAILED"] for l in logs)
        if all_blocked:
            base_score -= 15
            factors.append("All exploit/auth attempts blocked by host (-15)")

    # 2. Vulnerability & Exploitability Factor
    vulnerabilities = evidence.get("vulnerabilities") or []
    unpatched_critical = any(v.get("severity") == "CRITICAL" and v.get("patched") == 0 for v in vulnerabilities)
    if unpatched_critical:
        base_score += 20
        factors.append("Target asset has unpatched critical CVE (+20)")
    elif vulnerabilities:
        patched_count = sum(1 for v in vulnerabilities if v.get("patched") == 1)
        if patched_count > 0:
            base_score -= 10
            factors.append(f"Target vulnerabilities actively patched ({patched_count}) (-10)")

    # 3. Asset Criticality Multiplier
    asset = evidence.get("asset") or {}
    criticality = asset.get("criticality", "MEDIUM").upper() if isinstance(asset, dict) else "MEDIUM"
    multiplier = 1.0
    if criticality == "CRITICAL":
        multiplier = 1.4
        factors.append("Critical Asset Multiplier (x1.4)")
    elif criticality == "HIGH":
        multiplier = 1.2
        factors.append("High Asset Multiplier (x1.2)")

    final_score = min(100.0, max(0.0, base_score * multiplier))

    risk_level = "LOW"
    if final_score >= 75:
        risk_level = "CRITICAL"
    elif final_score >= 50:
        risk_level = "HIGH"
    elif final_score >= 25:
        risk_level = "MEDIUM"

    return {
        "score": round(final_score, 1),
        "risk_level": risk_level,
        "label": "Prototype SOC Risk Score",
        "factor_breakdown": factors
    }
