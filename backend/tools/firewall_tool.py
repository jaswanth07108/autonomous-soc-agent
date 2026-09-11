import sys
import os
from datetime import datetime, timezone
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from data.database import get_db_connection

def block_ip(ip_address: str, reason: str = "Automated SOC Block Response"):
    """Execute simulated firewall rule block on source IP."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if simulate_failure is active for this IP
    cursor.execute("SELECT simulate_failure FROM firewall_state WHERE ip_address = ?", (ip_address,))
    row = cursor.fetchone()
    
    if row and row['simulate_failure'] == 1:
        conn.close()
        return {
            "status": "FAILED",
            "action": "BLOCK_IP",
            "ip_address": ip_address,
            "error_code": "FIREWALL_RULE_DEPLOYMENT_TIMEOUT",
            "message": f"ERROR_FIREWALL_COMMUNICATION_TIMEOUT: Gateway interface rejected rule for {ip_address}. Subsystem unreachable."
        }

    now_str = datetime.now(timezone.utc).isoformat()
    cursor.execute("""
    INSERT INTO firewall_state (ip_address, action, timestamp, reason, active, simulate_failure)
    VALUES (?, 'BLOCKED', ?, ?, 1, 0)
    ON CONFLICT(ip_address) DO UPDATE SET
    action = 'BLOCKED',
    timestamp = excluded.timestamp,
    reason = excluded.reason,
    active = 1
    """, (ip_address, now_str, reason))
    conn.commit()
    conn.close()

    return {
        "status": "SUCCESS",
        "action": "BLOCK_IP",
        "ip_address": ip_address,
        "reason": reason,
        "timestamp": now_str,
        "rule_active": True
    }

def unblock_ip(ip_address: str):
    """Remove simulated firewall block rule for IP."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM firewall_state WHERE ip_address = ?", (ip_address,))
    conn.commit()
    conn.close()
    return {"status": "SUCCESS", "action": "UNBLOCK_IP", "ip_address": ip_address}

def get_firewall_state(ip_address: str = None):
    """Retrieve active firewall rules."""
    conn = get_db_connection()
    cursor = conn.cursor()
    if ip_address:
        cursor.execute("SELECT * FROM firewall_state WHERE ip_address = ?", (ip_address,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else {"ip_address": ip_address, "active": 0, "action": "NONE"}
    else:
        cursor.execute("SELECT * FROM firewall_state WHERE active = 1")
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

def set_firewall_failure_flag(ip_address: str, simulate_failure: int):
    """Toggle failure flag for failure recovery demo."""
    conn = get_db_connection()
    cursor = conn.cursor()
    now_str = datetime.now(timezone.utc).isoformat()
    cursor.execute("""
    INSERT INTO firewall_state (ip_address, action, timestamp, reason, active, simulate_failure)
    VALUES (?, 'PENDING', ?, 'Demo failure injection', 0, ?)
    ON CONFLICT(ip_address) DO UPDATE SET simulate_failure = ?
    """, (ip_address, now_str, simulate_failure, simulate_failure))
    conn.commit()
    conn.close()
