import json
import sqlite3
import os
import sys
from datetime import datetime, timedelta, timezone

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data.database import get_db_connection, reset_db

def seed_sandbox_data():
    reset_db()
    conn = get_db_connection()
    cursor = conn.cursor()

    now = datetime.now(timezone.utc)

    # -------------------------------------------------------------
    # 1. ASSETS
    # -------------------------------------------------------------
    assets = [
        ("AST-01", "db-prod-01", "10.0.4.15", "Database Server", "Ubuntu 22.04 LTS", "Data Engineering", "CRITICAL", 0),
        ("AST-02", "api-internal-01", "10.0.1.50", "App Server", "Debian 11", "Backend Engineering", "MEDIUM", 0),
        ("AST-03", "web-prod-01", "10.0.2.10", "Web Gateway", "Alpine Linux", "Frontend Operations", "HIGH", 1),
        ("AST-04", "auth-prod-01", "10.0.3.5", "Identity Server", "RHEL 9", "SecOps", "CRITICAL", 1),
        ("AST-05", "pay-prod-01", "10.0.1.20", "Payment Microservice", "Ubuntu 24.04 LTS", "FinTech Core", "CRITICAL", 1)
    ]
    cursor.executemany("""
    INSERT INTO assets (asset_id, hostname, ip_address, asset_type, operating_system, owner_department, criticality, exposed_to_internet)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, assets)

    # -------------------------------------------------------------
    # 2. VULNERABILITIES
    # -------------------------------------------------------------
    vulnerabilities = [
        ("VULN-101", "CVE-2023-38606", "AST-01", "OpenSSH Sudo", "CRITICAL", "Privilege escalation vulnerability in OpenSSH helper module", 1, 0),
        ("VULN-102", "CVE-2024-21762", "AST-03", "Nginx WAF", "HIGH", "SQL injection vector in web routing service", 1, 1), # Patched
        ("VULN-103", "CVE-2024-3094", "AST-05", "XZ Utils / SSH", "CRITICAL", "Malicious backdoor in XZ compression library", 1, 0)
    ]
    cursor.executemany("""
    INSERT INTO vulnerabilities (vulnerability_id, cve_id, asset_id, service, severity, description, exploit_available, patched)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, vulnerabilities)

    # -------------------------------------------------------------
    # 3. IDENTITY DIRECTORY (IAM & Tickets)
    # -------------------------------------------------------------
    identities = [
        ("alex.director", "Alex Vance", "SecOps Core", "Director of SecOps", 1, "198.51.100.0/24,10.0.0.0/8", json.dumps([
            {"ticket_id": "#INC-8892", "type": "EMERGENCY_MAINTENANCE", "approved_by": "VP SecOps", "description": "Emergency Identity Node Patching"}
        ])),
        ("devops_service", "Prometheus Agent", "DevOps Infrastructure", "Service Account", 0, "192.168.1.0/24", json.dumps([])),
        ("admin", "Default Local Admin", "IT Operations", "Local SysAdmin", 0, "10.0.0.0/8", json.dumps([]))
    ]
    cursor.executemany("""
    INSERT INTO identity_directory (username, full_name, department, role, has_mfa, authorized_subnets, approved_tickets)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, identities)

    # -------------------------------------------------------------
    # 4. SECURITY ALERTS (The 5 Scenarios)
    # -------------------------------------------------------------
    alerts = [
        ("ALT-1001", (now - timedelta(minutes=10)).isoformat(), "198.51.100.45", "10.0.4.15", 48210, 22, "TCP", "SSH Brute Force & Privilege Escalation", "HIGH", "Snort-NIDS-Node01", "NEW", "SCENARIO_1"),
        ("ALT-1002", (now - timedelta(minutes=8)).isoformat(), "192.168.1.105", "10.0.1.50", 52104, 8080, "TCP", "Suspicious Port Scan / Anomaly", "MEDIUM", "Suricata-Internal-Sensor", "NEW", "SCENARIO_2"),
        ("ALT-1003", (now - timedelta(minutes=6)).isoformat(), "203.0.113.88", "10.0.2.10", 39100, 443, "TCP", "SQL Injection & Directory Traversal Attempt", "HIGH", "Cloudflare-WAF-Edge", "NEW", "SCENARIO_3"),
        ("ALT-1004", (now - timedelta(minutes=4)).isoformat(), "198.51.100.99", "10.0.3.5", 61002, 22, "TCP", "Unauthorized High-Privilege Account Access", "CRITICAL", "Guacamole-PAM-Audit", "NEW", "SCENARIO_4"),
        ("ALT-1005", (now - timedelta(minutes=2)).isoformat(), "198.51.100.120", "10.0.1.20", 44312, 8443, "TCP", "Ransomware C2 Probe & Remote Code Execution", "CRITICAL", "CrowdStrike-Falcon-Sim", "NEW", "SCENARIO_5")
    ]
    cursor.executemany("""
    INSERT INTO security_alerts (alert_id, timestamp, source_ip, destination_ip, source_port, destination_port, protocol, attack_type, severity, sensor, status, scenario_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, alerts)

    # -------------------------------------------------------------
    # 5. SERVER LOGS
    # -------------------------------------------------------------
    logs = []
    
    # Scenario 1 logs
    t1 = now - timedelta(minutes=12)
    for i in range(12):
        logs.append((
            f"LOG-101-{i}", (t1 + timedelta(seconds=i*5)).isoformat(), "10.0.4.15", "198.51.100.45", "root",
            "AUTHENTICATION_FAILURE", "SSH_LOGIN", "FAILED", "Invalid password for user root from 198.51.100.45", "SCENARIO_1"
        ))
    logs.append((
        "LOG-101-SUCCESS", (t1 + timedelta(seconds=70)).isoformat(), "10.0.4.15", "198.51.100.45", "admin",
        "AUTHENTICATION_SUCCESS", "SSH_LOGIN", "SUCCESS", "Accepted password for admin from 198.51.100.45 port 48210 ssh2", "SCENARIO_1"
    ))
    logs.append((
        "LOG-101-ESC", (t1 + timedelta(seconds=85)).isoformat(), "10.0.4.15", "198.51.100.45", "admin",
        "PRIVILEGE_ESCALATION", "SUDO_EXEC", "SUCCESS", "admin : TTY=pts/0 ; PWD=/home/admin ; USER=root ; COMMAND=/bin/bash", "SCENARIO_1"
    ))

    # Scenario 2 logs (benign health check)
    t2 = now - timedelta(minutes=9)
    logs.append((
        "LOG-102-1", t2.isoformat(), "10.0.1.50", "192.168.1.105", "devops_service",
        "HEALTH_CHECK", "HTTP_GET", "SUCCESS", "GET /api/v1/health HTTP/1.1 200 OK User-Agent: Prometheus/2.45.0", "SCENARIO_2"
    ))
    logs.append((
        "LOG-102-2", (t2 + timedelta(seconds=2)).isoformat(), "10.0.1.50", "192.168.1.105", "devops_service",
        "METRICS_COLLECTION", "HTTP_GET", "SUCCESS", "GET /api/v1/metrics HTTP/1.1 200 OK User-Agent: Prometheus/2.45.0", "SCENARIO_2"
    ))

    # Scenario 3 logs (WAF blocks)
    t3 = now - timedelta(minutes=7)
    logs.append((
        "LOG-103-1", t3.isoformat(), "10.0.2.10", "203.0.113.88", "anonymous",
        "EXPLOIT_ATTEMPT", "HTTP_POST", "BLOCKED", "POST /login?user=' OR 1=1-- HTTP/1.1 403 Forbidden (Blocked by WAF Rule SQLi-04)", "SCENARIO_3"
    ))
    logs.append((
        "LOG-103-2", (t3 + timedelta(seconds=5)).isoformat(), "10.0.2.10", "203.0.113.88", "anonymous",
        "PATH_TRAVERSAL", "HTTP_GET", "BLOCKED", "GET /../../etc/passwd HTTP/1.1 400 Bad Request", "SCENARIO_3"
    ))

    # Scenario 4 logs: initial suspicious PAM session
    t4 = now - timedelta(minutes=5)
    logs.append((
        "LOG-104-1", t4.isoformat(), "10.0.3.5", "198.51.100.99", "alex.director",
        "REMOTE_ACCESS_ALERT", "PAM_SESSION", "SUSPICIOUS", "Interactive PAM session opened for alex.director from external IP 198.51.100.99 without active MFA assertion", "SCENARIO_4"
    ))

    # Scenario 5 logs
    t5 = now - timedelta(minutes=3)
    logs.append((
        "LOG-105-1", t5.isoformat(), "10.0.1.20", "198.51.100.120", "system",
        "RCE_ATTEMPT", "WEBSHELL_UPLOAD", "CRITICAL", "Detected attempt to invoke deserialization payload on /api/payment/process", "SCENARIO_5"
    ))

    cursor.executemany("""
    INSERT INTO server_logs (log_id, timestamp, server_ip, source_ip, username, event_type, action, status, message, scenario_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, logs)

    # -------------------------------------------------------------
    # 6. NETWORK EVENTS
    # -------------------------------------------------------------
    network_events = [
        ("NET-101", (now - timedelta(minutes=10)).isoformat(), "198.51.100.45", "10.0.4.15", 22, "TCP", 4500000, 3200, "ESTABLISHED", "SCENARIO_1"),
        ("NET-102", (now - timedelta(minutes=8)).isoformat(), "192.168.1.105", "10.0.1.50", 8080, "TCP", 12500, 42, "CLOSED", "SCENARIO_2"),
        ("NET-103", (now - timedelta(minutes=6)).isoformat(), "203.0.113.88", "10.0.2.10", 443, "TCP", 3400, 12, "RESET", "SCENARIO_3"),
        ("NET-104", (now - timedelta(minutes=4)).isoformat(), "198.51.100.99", "10.0.3.5", 22, "TCP", 89000, 210, "ESTABLISHED", "SCENARIO_4"),
        ("NET-105", (now - timedelta(minutes=2)).isoformat(), "198.51.100.120", "10.0.1.20", 8443, "TCP", 980000, 1500, "ACTIVE_PROBE", "SCENARIO_5")
    ]
    cursor.executemany("""
    INSERT INTO network_events (event_id, timestamp, source_ip, destination_ip, port, protocol, bytes, packets, connection_status, scenario_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, network_events)

    # -------------------------------------------------------------
    # 7. FIREWALL INITIAL STATE
    # -------------------------------------------------------------
    firewall_rules = [
        ("198.51.100.120", "PENDING_BLOCK", (now - timedelta(minutes=2)).isoformat(), "Pre-seeded for response recovery test", 0, 1)
    ]
    cursor.executemany("""
    INSERT INTO firewall_state (ip_address, action, timestamp, reason, active, simulate_failure)
    VALUES (?, ?, ?, ?, ?, ?)
    """, firewall_rules)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    seed_sandbox_data()
    print("Database sandbox successfully seeded with extended IAM & IAM ticket directories!")
