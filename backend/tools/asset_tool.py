import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from data.database import get_db_connection

def get_asset(ip_address: str):
    """Retrieve target asset information by IP address."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM assets WHERE ip_address = ?", (ip_address,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return {"warning": f"No asset metadata registered for IP {ip_address}. Operating as external target or unmanaged host."}
