import React from 'react';
import { Play, Zap, RefreshCw, AlertTriangle, ShieldCheck, Cpu, GitCommit, Layers, ArrowRight } from 'lucide-react';

interface ScenarioControlProps {
  onTriggerScenario: (scenarioId: number) => void;
  onInjectEvidence: () => void;
  isStepMode: boolean;
  setIsStepMode: (val: boolean) => void;
  isLoading: boolean;
}

export const ScenarioControl: React.FC<ScenarioControlProps> = ({
  onTriggerScenario,
  onInjectEvidence,
  isStepMode,
  setIsStepMode,
  isLoading
}) => {
  return (
    <div className="space-y-6">
      
      {/* Studio Banner & Mode Selector */}
      <div className="bg-[#131b2e] border border-slate-800 p-6 rounded-2xl shadow-xl space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-blue-600/20 border border-blue-500/40 text-blue-400 rounded-xl">
              <Cpu className="w-6 h-6" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-white">Hackathon Demo Scenario Control Studio</h3>
              <p className="text-xs text-slate-400">
                Interactive testbed proving autonomous goal-formulation, dynamic tool planning, failure recovery, and real-time adaptation to judges.
              </p>
            </div>
          </div>

          {/* Mode Switcher */}
          <div className="flex items-center gap-2 bg-[#0a0f1d] p-1.5 rounded-xl border border-slate-800">
            <span className="text-xs font-semibold text-slate-400 pl-2">Execution Mode:</span>
            <button
              onClick={() => setIsStepMode(false)}
              className={`px-3 py-1.5 text-xs font-bold rounded-lg transition-all ${
                !isStepMode ? 'bg-blue-600 text-white shadow' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Autonomous Auto-Run
            </button>
            <button
              onClick={() => setIsStepMode(true)}
              className={`px-3 py-1.5 text-xs font-bold rounded-lg transition-all flex items-center gap-1.5 ${
                isStepMode ? 'bg-indigo-600 text-white shadow' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <GitCommit className="w-3.5 h-3.5" />
              Interactive Step-by-Step
            </button>
          </div>
        </div>

        {isStepMode && (
          <div className="bg-indigo-950/40 border border-indigo-700/50 p-3 rounded-xl text-xs text-indigo-300 flex items-center gap-2">
            <Layers className="w-4 h-4 text-indigo-400 shrink-0" />
            <span>
              <strong>Step-by-Step Mode Active:</strong> Clicking any scenario will initialize the investigation session. You can then advance each tool decision individually in the Agent Workspace tab to inspect the agent's internal hypothesis and tool selection rationale.
            </span>
          </div>
        )}
      </div>

      {/* Scenarios Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        
        {/* Scenario 1 */}
        <div className="bg-[#131b2e] border border-red-900/50 p-5 rounded-2xl flex flex-col justify-between space-y-4 hover:border-red-500/60 transition-all shadow-lg">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="px-2.5 py-1 text-[10px] font-bold text-red-400 bg-red-950 border border-red-800/60 rounded-md">
                SCENARIO 1
              </span>
              <span className="text-xs font-mono text-slate-400">ALT-1001</span>
            </div>
            <h4 className="text-base font-bold text-white">Successful Attack</h4>
            <p className="text-xs text-slate-400 mt-1">
              SSH brute force leads to valid login & root privilege escalation on unpatched database server.
            </p>
            <div className="mt-3 text-[11px] text-red-400 font-mono">
              Expected: ATTACK_SUCCESSFUL → BLOCK_IP → VERIFIED
            </div>
          </div>
          <button
            onClick={() => onTriggerScenario(1)}
            disabled={isLoading}
            className="w-full py-2.5 bg-red-600 hover:bg-red-500 text-white rounded-xl text-xs font-bold transition-all shadow flex items-center justify-center gap-2"
          >
            <Play className="w-4 h-4" />
            Run Scenario 1
          </button>
        </div>

        {/* Scenario 2 */}
        <div className="bg-[#131b2e] border border-slate-800 p-5 rounded-2xl flex flex-col justify-between space-y-4 hover:border-slate-600 transition-all shadow-lg">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="px-2.5 py-1 text-[10px] font-bold text-slate-300 bg-slate-800 rounded-md">
                SCENARIO 2
              </span>
              <span className="text-xs font-mono text-slate-400">ALT-1002</span>
            </div>
            <h4 className="text-base font-bold text-white">False Positive & Early Exit</h4>
            <p className="text-xs text-slate-400 mt-1">
              Port scan alert. Dynamic planner observes benign Prometheus health telemetry and concludes early without running unnecessary invasive queries.
            </p>
            <div className="mt-3 text-[11px] text-emerald-400 font-mono">
              Expected: FALSE_POSITIVE → NO BLOCK
            </div>
          </div>
          <button
            onClick={() => onTriggerScenario(2)}
            disabled={isLoading}
            className="w-full py-2.5 bg-slate-700 hover:bg-slate-600 text-white rounded-xl text-xs font-bold transition-all shadow flex items-center justify-center gap-2"
          >
            <Play className="w-4 h-4" />
            Run Scenario 2
          </button>
        </div>

        {/* Scenario 3 */}
        <div className="bg-[#131b2e] border border-amber-900/50 p-5 rounded-2xl flex flex-col justify-between space-y-4 hover:border-amber-500/60 transition-all shadow-lg">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="px-2.5 py-1 text-[10px] font-bold text-amber-400 bg-amber-950 border border-amber-800/60 rounded-md">
                SCENARIO 3
              </span>
              <span className="text-xs font-mono text-slate-400">ALT-1003</span>
            </div>
            <h4 className="text-base font-bold text-white">Attack Failed</h4>
            <p className="text-xs text-slate-400 mt-1">
              External SQL injection attempt rejected by WAF (403 Forbidden). Planner verifies patched CVE on target server.
            </p>
            <div className="mt-3 text-[11px] text-amber-400 font-mono">
              Expected: ATTACK_FAILED → MONITORING
            </div>
          </div>
          <button
            onClick={() => onTriggerScenario(3)}
            disabled={isLoading}
            className="w-full py-2.5 bg-amber-600 hover:bg-amber-500 text-white rounded-xl text-xs font-bold transition-all shadow flex items-center justify-center gap-2"
          >
            <Play className="w-4 h-4" />
            Run Scenario 3
          </button>
        </div>

        {/* Scenario 4: Adaptation */}
        <div className="bg-[#131b2e] border border-cyan-900/50 p-5 rounded-2xl flex flex-col justify-between space-y-4 hover:border-cyan-500/60 transition-all shadow-lg col-span-1 md:col-span-1 lg:col-span-1">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="px-2.5 py-1 text-[10px] font-bold text-cyan-400 bg-cyan-950 border border-cyan-800/60 rounded-md">
                SCENARIO 4
              </span>
              <span className="text-xs font-mono text-slate-400">ALT-1004</span>
            </div>
            <h4 className="text-base font-bold text-white">Conflicting Evidence & Adaptation</h4>
            <p className="text-xs text-slate-400 mt-1">
              Initial suspicious out-of-hours admin session. When contradictory Duo MFA ticket is injected, agent actively re-opens hypothesis, calls IAM verification tool, and adapts decision.
            </p>
            <div className="mt-3 text-[11px] text-cyan-400 font-mono">
              Demonstrates Contradiction Detection & Real-time Adaptation
            </div>
          </div>
          <div className="space-y-2">
            <button
              onClick={() => onTriggerScenario(4)}
              disabled={isLoading}
              className="w-full py-2.5 bg-cyan-600 hover:bg-cyan-500 text-white rounded-xl text-xs font-bold transition-all shadow flex items-center justify-center gap-2"
            >
              <Zap className="w-4 h-4 text-yellow-300" />
              Run Full Adaptation Demo
            </button>
            <button
              onClick={onInjectEvidence}
              disabled={isLoading}
              className="w-full py-2 bg-[#0a0f1d] hover:bg-cyan-950/60 border border-cyan-700/60 text-cyan-300 rounded-xl text-[11px] font-semibold transition-all flex items-center justify-center gap-1.5"
            >
              <ArrowRight className="w-3.5 h-3.5 text-cyan-400" />
              Inject Duo MFA Token Mid-Flight
            </button>
          </div>
        </div>

        {/* Scenario 5: Failure Recovery */}
        <div className="bg-[#131b2e] border border-purple-900/50 p-5 rounded-2xl flex flex-col justify-between space-y-4 hover:border-purple-500/60 transition-all shadow-lg col-span-1 md:col-span-1 lg:col-span-2">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="px-2.5 py-1 text-[10px] font-bold text-purple-400 bg-purple-950 border border-purple-800/60 rounded-md">
                SCENARIO 5
              </span>
              <span className="text-xs font-mono text-slate-400">ALT-1005</span>
            </div>
            <h4 className="text-base font-bold text-white">Response Failure & Autonomous Recovery</h4>
            <p className="text-xs text-slate-400 mt-1">
              Ransomware C2 probe requires perimeter block. Primary firewall returns communication timeout. Agent observes failure, re-plans fallback isolation route via secondary interface, and verifies final enforcement.
            </p>
            <div className="mt-3 text-[11px] text-purple-400 font-mono">
              Demonstrates Autonomous Failure Recovery & Verification Loop
            </div>
          </div>
          <button
            onClick={() => onTriggerScenario(5)}
            disabled={isLoading}
            className="w-full py-2.5 bg-purple-600 hover:bg-purple-500 text-white rounded-xl text-xs font-bold transition-all shadow flex items-center justify-center gap-2"
          >
            <RefreshCw className="w-4 h-4" />
            Run Failure Recovery Demo
          </button>
        </div>

      </div>

    </div>
  );
};
