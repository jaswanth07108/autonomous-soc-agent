import React from 'react';
import { InvestigationStep, InvestigationResult } from '../types';
import { CheckCircle2, AlertOctagon, Terminal, ShieldAlert, Cpu, RefreshCw, Zap, Compass, HelpCircle, Eye } from 'lucide-react';

interface TimelineViewProps {
  history: InvestigationStep[];
  result: InvestigationResult | null;
  onInjectEvidence?: () => void;
  onNextStep?: () => void;
  isStepMode?: boolean;
  isStepComplete?: boolean;
  isLoading?: boolean;
}

export const TimelineView: React.FC<TimelineViewProps> = ({
  history,
  result,
  onInjectEvidence,
  onNextStep,
  isStepMode,
  isStepComplete,
  isLoading
}) => {
  if (!history || history.length === 0) {
    return (
      <div className="bg-[#131b2e] border border-slate-800 rounded-2xl p-12 text-center text-slate-400 shadow-xl">
        <Cpu className="w-12 h-12 text-slate-600 mx-auto mb-3 animate-pulse" />
        <h4 className="text-base font-semibold text-slate-200">No Active Agent Trajectory</h4>
        <p className="text-xs text-slate-400 mt-1 max-w-sm mx-auto">
          Select an alert or click a demo scenario to see the autonomous agent dynamically hypothesize, select tools, and verify mitigation.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      
      {/* Agent Trajectory Header */}
      <div className="bg-[#131b2e] border border-slate-800 p-5 rounded-2xl flex flex-wrap items-center justify-between gap-4 shadow-xl">
        <div>
          <div className="flex items-center gap-2">
            <h3 className="text-base font-bold text-white">Dynamic Agent Investigation Trajectory</h3>
            <span className="px-2.5 py-0.5 text-[10px] font-bold text-cyan-400 bg-cyan-950 border border-cyan-800/60 rounded-full flex items-center gap-1">
              <Compass className="w-3 h-3" />
              DYNAMIC REACT PLANNER
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-0.5">
            GOAL → OBSERVE → HYPOTHESIZE → PLAN NEXT TOOL → INVESTIGATE → DECIDE → ACT → VERIFY → ADAPT
          </p>
        </div>

        {/* Action Controls in Header */}
        <div className="flex items-center gap-3">
          {isStepMode && !isStepComplete && onNextStep && (
            <button
              onClick={onNextStep}
              disabled={isLoading}
              className="px-4 py-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white rounded-xl text-xs font-bold transition-all shadow-lg flex items-center gap-2"
            >
              <Zap className="w-4 h-4 text-yellow-300" />
              Execute Next Agent Step
            </button>
          )}

          {result && (
            <div className="flex items-center gap-3">
              {result.decision && (
                <div className="px-4 py-2 bg-[#0a0f1d] border border-slate-700 rounded-xl flex items-center gap-2">
                  <ShieldAlert className={`w-4 h-4 ${
                    result.decision === 'ATTACK_SUCCESSFUL' ? 'text-red-400' :
                    result.decision === 'ATTACK_FAILED' ? 'text-amber-400' :
                    'text-emerald-400'
                  }`} />
                  <div>
                    <div className="text-[10px] text-slate-400 font-semibold uppercase">Decision</div>
                    <div className="text-xs font-bold text-white">{result.decision}</div>
                  </div>
                </div>
              )}

              {result.confidence !== undefined && (
                <div className="px-4 py-2 bg-[#0a0f1d] border border-slate-700 rounded-xl">
                  <div className="text-[10px] text-slate-400 font-semibold uppercase">Confidence</div>
                  <div className="text-xs font-bold text-cyan-400">{(result.confidence * 100).toFixed(0)}%</div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Interactive Step Timeline */}
      <div className="relative border-l-2 border-slate-800 ml-4 space-y-6">
        {history.map((step, idx) => {
          const isLast = idx === history.length - 1;
          const evidence = step.evidence_found || {};
          const hypothesis = evidence.hypothesis;
          const rationale = evidence.rationale;
          
          return (
            <div key={idx} className="relative pl-6">
              
              {/* Timeline Icon Marker */}
              <div className={`absolute -left-3.5 top-1.5 w-7 h-7 rounded-full border-2 flex items-center justify-center text-xs font-bold ${
                step.agent_action.includes('ADAPT') ? 'bg-cyan-950 border-cyan-400 text-cyan-300' :
                step.agent_action.includes('FAILURE') || step.agent_action.includes('RECOVER') ? 'bg-purple-950 border-purple-400 text-purple-300' :
                step.agent_action.includes('DECISION') ? 'bg-emerald-950 border-emerald-400 text-emerald-300' :
                'bg-blue-950 border-blue-500 text-blue-300'
              }`}>
                {step.step_index}
              </div>

              {/* Step Card */}
              <div className={`bg-[#131b2e] border rounded-2xl p-4 shadow-lg transition-all ${
                isLast ? 'border-blue-500/60 ring-1 ring-blue-500/30' : 'border-slate-800'
              }`}>
                
                <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800/80 pb-2.5 mb-3">
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-xs font-bold text-blue-400">{step.agent_action}</span>
                    {step.tool_used && (
                      <span className="px-2 py-0.5 text-[10px] font-mono text-amber-300 bg-amber-950/60 border border-amber-800/40 rounded-md flex items-center gap-1">
                        <Terminal className="w-3 h-3 text-amber-400" />
                        tool: {step.tool_used}
                      </span>
                    )}
                  </div>
                  <span className="text-[11px] text-slate-500 font-mono">
                    {new Date(step.timestamp).toLocaleTimeString()}
                  </span>
                </div>

                {/* Agent Dynamic Reasoning Block (Hypothesis & Rationale) */}
                {(hypothesis || rationale) && (
                  <div className="mb-3 p-3 bg-[#0a0f1d] rounded-xl border border-blue-900/40 space-y-1.5 text-xs">
                    {hypothesis && (
                      <div className="flex items-start gap-2">
                        <span className="px-1.5 py-0.5 rounded bg-blue-950 text-[10px] font-bold text-cyan-400 border border-blue-800/60 shrink-0">
                          HYPOTHESIS
                        </span>
                        <span className="text-slate-200 font-medium">{hypothesis}</span>
                      </div>
                    )}
                    {rationale && (
                      <div className="flex items-start gap-2 text-slate-400 text-[11px]">
                        <span className="px-1.5 py-0.5 rounded bg-slate-900 text-[10px] font-bold text-amber-300 border border-slate-700 shrink-0">
                          RATIONALE
                        </span>
                        <span>{rationale}</span>
                      </div>
                    )}
                  </div>
                )}

                {/* Tool Input / Parameters */}
                {step.tool_input && Object.keys(step.tool_input).length > 0 && (
                  <div className="mb-3 bg-[#0a0f1d] p-2.5 rounded-xl border border-slate-800 font-mono text-[11px] text-slate-300">
                    <span className="text-slate-500">Inputs: </span>
                    <span>{JSON.stringify(step.tool_input)}</span>
                  </div>
                )}

                {/* Evidence Found Output */}
                {step.evidence_found && (
                  <div className="bg-[#0a0f1d] p-3 rounded-xl border border-slate-800/80 text-xs space-y-2">
                    <div className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                      <Eye className="w-3.5 h-3.5 text-blue-400" />
                      Observed Evidence
                    </div>
                    <pre className="font-mono text-[11px] text-slate-300 whitespace-pre-wrap overflow-x-auto max-h-40">
                      {JSON.stringify(step.evidence_found, null, 2)}
                    </pre>
                  </div>
                )}

                {/* Decision / Reasoning Banner inside step if present */}
                {step.decision && (
                  <div className="mt-3 p-2.5 bg-blue-950/40 border border-blue-800/50 rounded-xl flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Zap className="w-4 h-4 text-yellow-400" />
                      <span className="text-xs font-bold text-white">Agent Decision: {step.decision}</span>
                    </div>
                    {step.confidence ? (
                      <span className="text-xs font-semibold text-cyan-400">Confidence: {(step.confidence * 100).toFixed(0)}%</span>
                    ) : null}
                  </div>
                )}

              </div>

            </div>
          );
        })}
      </div>

    </div>
  );
};
