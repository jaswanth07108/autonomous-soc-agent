import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from data.database import get_db_connection

def get_server_logs(ip_address: str, limit: int = 50):
    """Retrieve server logs for a given server or source IP."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM server_logs 
    WHERE server_ip = ? OR source_ip = ?
    ORDER BY timestamp ASC
    LIMIT ?
    """, (ip_address, ip_address, limit))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]
