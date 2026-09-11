import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tools.firewall_tool import get_firewall_state

def verify_firewall(ip_address: str):
    """Verify that a firewall block rule is actively enforcing in the sandbox environment."""
    state = get_firewall_state(ip_address)
    if isinstance(state, dict) and state.get("active") == 1 and state.get("action") == "BLOCKED":
        return {
            "verified": True,
            "ip_address": ip_address,
            "status": "ENFORCING",
            "message": f"Firewall rule verified active for {ip_address}. Inbound & outbound traffic dropped."
        }
    return {
        "verified": False,
        "ip_address": ip_address,
        "status": "NOT_ENFORCING",
        "message": f"Verification failed. No active blocking rule found in firewall state for {ip_address}."
    }
