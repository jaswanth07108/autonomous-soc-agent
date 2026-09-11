import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { DashboardOverview } from './components/DashboardOverview';
import { TimelineView } from './components/TimelineView';
import { EvidenceInspector } from './components/EvidenceInspector';
import { NetworkTopology } from './components/NetworkTopology';
import { ScenarioControl } from './components/ScenarioControl';
import { HumanApprovalModal } from './components/HumanApprovalModal';
import { EvaluationMetricsView } from './components/EvaluationMetrics';
import { AlertTriangle, RefreshCw, Zap } from 'lucide-react';

import {
  SecurityAlert,
  InvestigationResult,
  EvaluationMetrics,
  FirewallRule
} from './types';

import {
  fetchAlerts,
  investigateAlert,
  investigateAlertStep,
  triggerScenario,
  injectScenario4Mfa,
  fetchFirewallState,
  fetchEvaluationMetrics,
  submitHumanOverride,
  resetDatabase,
  checkBackendHealth
} from './api';

export function App() {
  const [activeTab, setActiveTab] = useState<string>('dashboard');
  const [alerts, setAlerts] = useState<SecurityAlert[]>([]);
  const [firewallRules, setFirewallRules] = useState<FirewallRule[]>([]);
  const [activeResult, setActiveResult] = useState<InvestigationResult | null>(null);
  const [evaluationMetrics, setEvaluationMetrics] = useState<EvaluationMetrics | null>(null);
  
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isResetting, setIsResetting] = useState<boolean>(false);
  const [isBackendConnected, setIsBackendConnected] = useState<boolean>(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [pendingApproval, setPendingApproval] = useState<InvestigationResult | null>(null);

  // Step-by-Step Mode State
  const [isStepMode, setIsStepMode] = useState<boolean>(false);
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);
  const [activeAlertId, setActiveAlertId] = useState<string | null>(null);
  const [isStepComplete, setIsStepComplete] = useState<boolean>(false);

  // Load initial data
  const loadData = async () => {
    try {
      const isHealthy = await checkBackendHealth();
      setIsBackendConnected(isHealthy);
      if (!isHealthy) {
        setErrorMessage("Backend server is not reachable at http://127.0.0.1:8000. Please start the backend service.");
        return;
      }
      setErrorMessage(null);

      const [alertsData, fwData] = await Promise.all([
        fetchAlerts(),
        fetchFirewallState()
      ]);
      setAlerts(alertsData);
      setFirewallRules(fwData);
    } catch (err: any) {
      console.error("Error loading dashboard data:", err);
      setIsBackendConnected(false);
      setErrorMessage(`Connection Error: ${err.message || "Failed to communicate with AegisSOC backend."}`);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleInvestigateAlert = async (alertId: string) => {
    setIsLoading(true);
    setErrorMessage(null);
    try {
      if (isStepMode) {
        // Initialize step session
        const stepRes = await investigateAlertStep(alertId);
        setActiveSessionId(stepRes.session_id);
        setActiveAlertId(alertId);
        setIsStepComplete(stepRes.is_complete || false);
        setActiveResult({
          status: 'IN_PROGRESS',
          alert_id: alertId,
          history: stepRes.history || []
        });
      } else {
        const res = await investigateAlert(alertId, false);
        setActiveResult(res);
      }
      setActiveTab('workspace');
      await loadData();
    } catch (err: any) {
      setErrorMessage(`Investigation Failed: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNextStep = async () => {
    if (!activeAlertId) return;
    setIsLoading(true);
    setErrorMessage(null);
    try {
      const stepRes = await investigateAlertStep(activeAlertId, activeSessionId || undefined);
      setIsStepComplete(stepRes.is_complete || false);
      if (stepRes.is_complete) {
        setActiveResult(stepRes);
      } else {
        setActiveResult(prev => ({
          ...(prev || { status: 'IN_PROGRESS', alert_id: activeAlertId }),
          status: 'IN_PROGRESS',
          history: stepRes.history || prev?.history || []
        }));
      }
      await loadData();
    } catch (err: any) {
      setErrorMessage(`Step Execution Failed: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleTriggerScenario = async (scenarioId: number) => {
    setIsLoading(true);
    setErrorMessage(null);
    try {
      if (isStepMode) {
        const alertMap: Record<number, string> = {
          1: 'ALT-1001',
          2: 'ALT-1002',
          3: 'ALT-1003',
          4: 'ALT-1004',
          5: 'ALT-1005'
        };
        const alertId = alertMap[scenarioId] || 'ALT-1001';
        await handleInvestigateAlert(alertId);
      } else {
        const res = await triggerScenario(scenarioId);
        setActiveResult(res);
        setActiveTab('workspace');
      }
      await loadData();
    } catch (err: any) {
      setErrorMessage(`Scenario Trigger Failed: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleInjectMfa = async () => {
    setIsLoading(true);
    setErrorMessage(null);
    try {
      const res = await injectScenario4Mfa();
      setActiveResult(prev => ({
        ...(prev || { status: 'ADAPTED', alert_id: 'ALT-1004' }),
        status: 'ADAPTED',
        decision: res.new_decision,
        confidence: res.confidence,
        reasoning: res.reasoning,
        history: res.history || prev?.history || []
      }));
      setActiveTab('workspace');
      await loadData();
    } catch (err: any) {
      setErrorMessage(`MFA Injection Failed: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRunEvaluation = async () => {
    setIsLoading(true);
    setErrorMessage(null);
    try {
      const metrics = await fetchEvaluationMetrics();
      setEvaluationMetrics(metrics);
      setActiveTab('evaluation');
    } catch (err: any) {
      setErrorMessage(`Evaluation Benchmark Failed: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = async () => {
    setIsResetting(true);
    setErrorMessage(null);
    try {
      await resetDatabase();
      setActiveResult(null);
      setActiveSessionId(null);
      setActiveAlertId(null);
      setIsStepComplete(false);
      await loadData();
    } catch (err: any) {
      setErrorMessage(`Reset Sandbox Failed: ${err.message}`);
    } finally {
      setIsResetting(false);
    }
  };

  const handleHumanApprove = async (alertId: string, sourceIp: string) => {
    try {
      await submitHumanOverride(alertId, 'APPROVE', sourceIp);
      setPendingApproval(null);
      await loadData();
    } catch (err: any) {
      setErrorMessage(`Approval Error: ${err.message}`);
    }
  };

  const handleHumanReject = async (alertId: string, sourceIp: string) => {
    try {
      await submitHumanOverride(alertId, 'REJECT', sourceIp);
      setPendingApproval(null);
      await loadData();
    } catch (err: any) {
      setErrorMessage(`Rejection Error: ${err.message}`);
    }
  };

  return (
    <div className="min-h-screen bg-[#0a0f1d] text-slate-100 flex flex-col font-sans">
      
      {/* Top Navbar */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onReset={handleReset}
        isResetting={isResetting}
        isBackendConnected={isBackendConnected}
      />

      {/* Disconnection / Error Banner */}
      {!isBackendConnected && (
        <div className="bg-red-950/90 border-b border-red-800 p-3 text-center text-xs text-red-200 flex items-center justify-center gap-2">
          <AlertTriangle className="w-4 h-4 text-red-400 animate-bounce" />
          <span>Backend Server Unreachable at <code className="bg-red-900/60 px-1 py-0.5 rounded font-mono">http://127.0.0.1:8000</code>. Ensure Python backend is running (`py main.py`).</span>
          <button onClick={loadData} className="ml-2 px-2 py-0.5 bg-red-800 hover:bg-red-700 text-white text-[11px] rounded font-bold transition-all">
            Retry Connection
          </button>
        </div>
      )}

      {errorMessage && isBackendConnected && (
        <div className="bg-amber-950/90 border-b border-amber-800 p-2.5 text-center text-xs text-amber-200 flex items-center justify-center gap-2">
          <AlertTriangle className="w-4 h-4 text-amber-400" />
          <span>{errorMessage}</span>
          <button onClick={() => setErrorMessage(null)} className="ml-2 text-amber-400 hover:underline font-bold">Dismiss</button>
        </div>
      )}

      {/* Loading Overlay */}
      {isLoading && (
        <div className="fixed inset-0 z-30 bg-black/60 backdrop-blur-xs flex flex-col items-center justify-center gap-3">
          <div className="p-4 bg-[#131b2e] border border-blue-500/50 rounded-2xl flex flex-col items-center gap-3 shadow-2xl">
            <RefreshCw className="w-8 h-8 text-blue-400 animate-spin" />
            <div className="text-center">
              <h4 className="text-sm font-bold text-white">Agent Execution In Progress</h4>
              <p className="text-xs text-slate-400">Dynamic planning, tool invocation, and verification...</p>
            </div>
          </div>
        </div>
      )}

      {/* Main Content View */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-6 space-y-6">
        
        {/* Tab 1: Dashboard Overview */}
        {activeTab === 'dashboard' && (
          <DashboardOverview
            alerts={alerts}
            firewallRules={firewallRules}
            onInvestigate={handleInvestigateAlert}
            onSelectScenario={handleTriggerScenario}
          />
        )}

        {/* Tab 2: Agent Workspace */}
        {activeTab === 'workspace' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            {/* Left Col (2/3): Agent Trajectory & Timeline */}
            <div className="lg:col-span-2 space-y-6">
              <TimelineView
                history={activeResult?.history || []}
                result={activeResult}
                onNextStep={handleNextStep}
                isStepMode={isStepMode}
                isStepComplete={isStepComplete}
                isLoading={isLoading}
              />

              <EvidenceInspector
                evidence={activeResult?.evidence}
              />
            </div>

            {/* Right Col (1/3): Network Topology & Incident Summary */}
            <div className="space-y-6">
              <NetworkTopology
                alert={activeResult?.evidence?.alert}
                asset={activeResult?.evidence?.asset}
                firewallActive={activeResult?.verification_result?.verified}
              />

              {/* Reasoning Summary Card */}
              {activeResult && (
                <div className="bg-[#131b2e] border border-slate-800 p-5 rounded-2xl space-y-3 shadow-xl">
                  <div className="flex items-center justify-between">
                    <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">Agent Reasoning</h4>
                    {activeResult.tools_called_count && (
                      <span className="px-2 py-0.5 bg-blue-950 text-blue-400 border border-blue-800/60 rounded text-[10px] font-mono font-bold">
                        {activeResult.tools_called_count} tools invoked
                      </span>
                    )}
                  </div>
                  <p className="text-xs text-slate-300 leading-relaxed bg-[#0a0f1d] p-3 rounded-xl border border-slate-800">
                    {activeResult.reasoning || 'No reasoning summary available.'}
                  </p>
                  
                  {activeResult.risk_info && (
                    <div className="bg-[#0a0f1d] p-3 rounded-xl border border-slate-800 space-y-2">
                      <div className="flex items-center justify-between text-xs">
                        <span className="text-slate-400 font-semibold">Prototype Risk Score:</span>
                        <span className="font-bold text-red-400">{activeResult.risk_info.score} / 100</span>
                      </div>
                      <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
                        <div
                          className="bg-gradient-to-r from-yellow-500 to-red-500 h-full transition-all duration-500"
                          style={{ width: `${activeResult.risk_info.score}%` }}
                        />
                      </div>
                      <div className="text-[10px] text-slate-400 pt-1">
                        <span className="font-semibold text-slate-300">Factors: </span>
                        {activeResult.risk_info.factor_breakdown?.join(', ')}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>

          </div>
        )}

        {/* Tab 3: Demo Scenarios Studio */}
        {activeTab === 'scenarios' && (
          <ScenarioControl
            onTriggerScenario={handleTriggerScenario}
            onInjectEvidence={handleInjectMfa}
            isStepMode={isStepMode}
            setIsStepMode={setIsStepMode}
            isLoading={isLoading}
          />
        )}

        {/* Tab 4: Evaluation Metrics Benchmark */}
        {activeTab === 'evaluation' && (
          <EvaluationMetricsView
            metrics={evaluationMetrics}
            onRefresh={handleRunEvaluation}
            isLoading={isLoading}
          />
        )}

      </main>

      {/* Human Approval Interceptor Modal */}
      <HumanApprovalModal
        pendingResult={pendingApproval}
        onApprove={handleHumanApprove}
        onReject={handleHumanReject}
        onClose={() => setPendingApproval(null)}
      />

    </div>
  );
}

export default App;
