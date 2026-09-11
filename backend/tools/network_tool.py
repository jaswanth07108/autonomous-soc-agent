import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from data.database import get_db_connection

def get_network_events(source_ip: str, destination_ip: str = None):
    """Retrieve network connection events and traffic metrics for a given source/destination IP."""
    conn = get_db_connection()
    cursor = conn.cursor()
    if destination_ip:
        cursor.execute("""
        SELECT * FROM network_events 
        WHERE (source_ip = ? AND destination_ip = ?) OR (source_ip = ? AND destination_ip = ?)
        """, (source_ip, destination_ip, destination_ip, source_ip))
    else:
        cursor.execute("""
        SELECT * FROM network_events 
        WHERE source_ip = ? OR destination_ip = ?
        """, (source_ip, source_ip))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]
