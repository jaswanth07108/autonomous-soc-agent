export interface SecurityAlert {
  alert_id: string;
  timestamp: string;
  source_ip: string;
  destination_ip: string;
  source_port: number;
  destination_port: number;
  protocol: string;
  attack_type: string;
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  sensor: string;
  status: string;
  scenario_id?: string;
}

export interface InvestigationStep {
  investigation_id?: number;
  alert_id: string;
  step_index: number;
  agent_action: string;
  tool_used?: string;
  tool_input?: any;
  evidence_found?: any;
  decision?: string;
  confidence?: number;
  timestamp: string;
}

export interface RiskInfo {
  score: number;
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  label: string;
  factor_breakdown: string[];
}

export interface EvidenceBundle {
  alert: SecurityAlert;
  asset: any;
  server_logs: any[];
  vulnerabilities: any[];
  network_events: any[];
  identity_info?: any;
}

export interface InvestigationResult {
  status: 'IN_PROGRESS' | 'COMPLETED' | 'WAITING_FOR_HUMAN_APPROVAL' | 'ADAPTED' | 'ERROR';
  alert_id: string;
  goal?: string;
  decision?: string;
  confidence?: number;
  risk_info?: RiskInfo;
  recommended_action?: string;
  action_executed?: string;
  verification_result?: any;
  reasoning?: string;
  evidence?: EvidenceBundle;
  history?: InvestigationStep[];
  recovery_info?: any;
  contradiction_adaptation?: any;
  scenario_name?: string;
  scenario_description?: string;
  tools_called_count?: number;
}

export interface EvaluationMetrics {
  benchmark_summary: {
    total_scenarios: number;
    passed_scenarios: number;
    investigation_accuracy: string;
    evidence_sufficiency_rate: string;
    false_positive_handling: string;
    adaptation_success_rate: string;
    action_verification_rate: string;
    tool_failure_recovery_rate: string;
  };
  scenario_results: Array<{
    scenario: number;
    passed: boolean;
    decision?: string;
    action?: string;
    status?: string;
    verified?: boolean;
  }>;
}

export interface FirewallRule {
  rule_id: number;
  ip_address: string;
  action: string;
  timestamp: string;
  reason: string;
  active: number;
  simulate_failure: number;
}
