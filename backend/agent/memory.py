import sys
import os
import json
from datetime import datetime, timezone
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from data.database import get_db_connection

def record_step(alert_id: str, step_index: int, agent_action: str, tool_used: str, tool_input: dict, evidence_found: dict, decision: str = None, confidence: float = 0.0):
    conn = get_db_connection()
    cursor = conn.cursor()
    now_str = datetime.now(timezone.utc).isoformat()
    cursor.execute("""
    INSERT INTO investigation_history (alert_id, step_index, agent_action, tool_used, tool_input, evidence_found, decision, confidence, timestamp)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        alert_id,
        step_index,
        agent_action,
        tool_used,
        json.dumps(tool_input),
        json.dumps(evidence_found),
        decision,
        confidence,
        now_str
    ))
    conn.commit()
    conn.close()

def get_investigation_history(alert_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM investigation_history
    WHERE alert_id = ?
    ORDER BY step_index ASC
    """, (alert_id,))
    rows = cursor.fetchall()
    conn.close()
    
    result = []
    for r in rows:
        item = dict(r)
        try:
            item["tool_input"] = json.loads(item["tool_input"])
        except:
            pass
        try:
            item["evidence_found"] = json.loads(item["evidence_found"])
        except:
            pass
        result.append(item)
    return result

def clear_investigation_history(alert_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM investigation_history WHERE alert_id = ?", (alert_id,))
    conn.commit()
    conn.close()
