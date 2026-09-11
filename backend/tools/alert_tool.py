import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from data.database import get_db_connection

def get_alert(alert_id: str):
    """Retrieve security alert metadata by alert ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM security_alerts WHERE alert_id = ?", (alert_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return {"error": f"Alert {alert_id} not found."}

def get_related_alerts(ip_address: str):
    """Retrieve all related security alerts involving the given source or destination IP."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM security_alerts WHERE source_ip = ? OR destination_ip = ?", (ip_address, ip_address))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]
