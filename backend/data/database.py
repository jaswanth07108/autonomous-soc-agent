import sqlite3
import os
import json
from typing import Dict, Any, List, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "soc_sandbox.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Security Alerts
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS security_alerts (
        alert_id TEXT PRIMARY KEY,
        timestamp TEXT NOT NULL,
        source_ip TEXT NOT NULL,
        destination_ip TEXT NOT NULL,
        source_port INTEGER,
        destination_port INTEGER,
        protocol TEXT,
        attack_type TEXT NOT NULL,
        severity TEXT NOT NULL,
        sensor TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'NEW',
        scenario_id TEXT
    )
    """)

    # 2. Server Logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS server_logs (
        log_id TEXT PRIMARY KEY,
        timestamp TEXT NOT NULL,
        server_ip TEXT NOT NULL,
        source_ip TEXT,
        username TEXT,
        event_type TEXT NOT NULL,
        action TEXT,
        status TEXT NOT NULL,
        message TEXT,
        scenario_id TEXT
    )
    """)

    # 3. Assets
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assets (
        asset_id TEXT PRIMARY KEY,
        hostname TEXT NOT NULL,
        ip_address TEXT UNIQUE NOT NULL,
        asset_type TEXT NOT NULL,
        operating_system TEXT,
        owner_department TEXT,
        criticality TEXT NOT NULL,
        exposed_to_internet INTEGER NOT NULL DEFAULT 0
    )
    """)

    # 4. Vulnerabilities
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vulnerabilities (
        vulnerability_id TEXT PRIMARY KEY,
        cve_id TEXT NOT NULL,
        asset_id TEXT NOT NULL,
        service TEXT NOT NULL,
        severity TEXT NOT NULL,
        description TEXT,
        exploit_available INTEGER NOT NULL DEFAULT 0,
        patched INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY(asset_id) REFERENCES assets(asset_id)
    )
    """)

    # 5. Network Events
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS network_events (
        event_id TEXT PRIMARY KEY,
        timestamp TEXT NOT NULL,
        source_ip TEXT NOT NULL,
        destination_ip TEXT NOT NULL,
        port INTEGER,
        protocol TEXT,
        bytes INTEGER,
        packets INTEGER,
        connection_status TEXT NOT NULL,
        scenario_id TEXT
    )
    """)

    # 6. Firewall State
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS firewall_state (
        rule_id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip_address TEXT UNIQUE NOT NULL,
        action TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        reason TEXT,
        active INTEGER NOT NULL DEFAULT 1,
        simulate_failure INTEGER NOT NULL DEFAULT 0
    )
    """)

    # 7. Identity & Access Directory (IAM & Ticket Verification)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS identity_directory (
        username TEXT PRIMARY KEY,
        full_name TEXT NOT NULL,
        department TEXT NOT NULL,
        role TEXT NOT NULL,
        has_mfa INTEGER NOT NULL DEFAULT 1,
        authorized_subnets TEXT,
        approved_tickets TEXT
    )
    """)

    # 8. Investigation History (Audit Log & Step Trajectory)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS investigation_history (
        investigation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        alert_id TEXT NOT NULL,
        step_index INTEGER NOT NULL,
        agent_action TEXT NOT NULL,
        tool_used TEXT,
        tool_input TEXT,
        evidence_found TEXT,
        decision TEXT,
        confidence REAL,
        timestamp TEXT NOT NULL
    )
    """)

    # 9. Investigation Sessions (Persistent Resumable Agent State)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS investigation_sessions (
        session_id TEXT PRIMARY KEY,
        alert_id TEXT NOT NULL,
        status TEXT NOT NULL,
        step_counter INTEGER NOT NULL DEFAULT 0,
        current_hypothesis TEXT,
        confidence REAL DEFAULT 0.0,
        evidence_bundle TEXT,
        tools_called TEXT,
        decision TEXT,
        recommended_action TEXT,
        action_executed TEXT,
        verification_result TEXT,
        reasoning TEXT,
        updated_at TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

def reset_db():
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except Exception:
            pass
    init_db()
