import { SecurityAlert, InvestigationResult, EvaluationMetrics, FirewallRule } from './types';

// Support both dev server proxy and direct backend URL
const API_BASE = window.location.port === '5173' ? 'http://127.0.0.1:8000/api' : '/api';

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`API Error (${res.status}): ${text || res.statusText}`);
  }
  return res.json();
}

export async function checkBackendHealth(): Promise<boolean> {
  try {
    const url = window.location.port === '5173' ? 'http://127.0.0.1:8000/health' : '/health';
    const res = await fetch(url, { signal: AbortSignal.timeout(3000) });
    return res.ok;
  } catch {
    return false;
  }
}

export async function fetchAlerts(): Promise<SecurityAlert[]> {
  const res = await fetch(`${API_BASE}/alerts`);
  return handleResponse<SecurityAlert[]>(res);
}

export async function investigateAlert(alertId: string, requireHumanApproval: boolean = false): Promise<InvestigationResult> {
  const res = await fetch(`${API_BASE}/investigate/${alertId}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ require_human_approval: requireHumanApproval })
  });
  return handleResponse<InvestigationResult>(res);
}

export async function investigateAlertStep(alertId: string, sessionId?: string): Promise<any> {
  const res = await fetch(`${API_BASE}/investigate/${alertId}/step`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId })
  });
  return handleResponse<any>(res);
}

export async function triggerScenario(scenarioId: number): Promise<InvestigationResult> {
  const res = await fetch(`${API_BASE}/scenarios/trigger/${scenarioId}`, {
    method: 'POST'
  });
  return handleResponse<InvestigationResult>(res);
}

export async function injectScenario4Mfa(): Promise<any> {
  const res = await fetch(`${API_BASE}/scenarios/scenario-4-inject`, {
    method: 'POST'
  });
  return handleResponse<any>(res);
}

export async function injectEvidence(alertId: string, previousDecision: string): Promise<any> {
  const res = await fetch(`${API_BASE}/evidence/inject`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ alert_id: alertId, previous_decision: previousDecision })
  });
  return handleResponse<any>(res);
}

export async function submitHumanOverride(alertId: string, action: 'APPROVE' | 'REJECT' | 'MORE_INFO', sourceIp: string): Promise<any> {
  const res = await fetch(`${API_BASE}/human-override`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ alert_id: alertId, action, source_ip: sourceIp })
  });
  return handleResponse<any>(res);
}

export async function fetchFirewallState(): Promise<FirewallRule[]> {
  const res = await fetch(`${API_BASE}/firewall/state`);
  return handleResponse<FirewallRule[]>(res);
}

export async function fetchEvaluationMetrics(): Promise<EvaluationMetrics> {
  const res = await fetch(`${API_BASE}/evaluation/metrics`);
  return handleResponse<EvaluationMetrics>(res);
}

export async function resetDatabase(): Promise<any> {
  const res = await fetch(`${API_BASE}/reset`, { method: 'POST' });
  return handleResponse<any>(res);
}
