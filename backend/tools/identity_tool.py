import sys
import os
import json
from typing import Optional, Dict, Any

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from data.database import get_db_connection

def verify_identity_and_ticket(username: str, ticket_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Verify user identity, roles, MFA status, and approved change management / maintenance tickets.
    Queries the sandbox identity_directory table.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM identity_directory WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return {
            "verified": False,
            "username": username,
            "status": "UNKNOWN_IDENTITY",
            "message": f"User '{username}' is not registered in corporate IAM directory."
        }

    data = dict(row)
    approved_tickets = []
    try:
        approved_tickets = json.loads(data.get("approved_tickets") or "[]")
    except:
        pass

    matching_ticket = None
    if ticket_id:
        matching_ticket = next((t for t in approved_tickets if t.get("ticket_id") == ticket_id), None)
    elif approved_tickets:
        matching_ticket = approved_tickets[0]

    return {
        "verified": True,
        "username": username,
        "full_name": data.get("full_name"),
        "department": data.get("department"),
        "role": data.get("role"),
        "has_mfa": bool(data.get("has_mfa")),
        "authorized_subnets": data.get("authorized_subnets"),
        "ticket_verified": matching_ticket is not None,
        "matched_ticket": matching_ticket,
        "all_tickets": approved_tickets
    }

def get_identity_info(username: str) -> Dict[str, Any]:
    return verify_identity_and_ticket(username)
