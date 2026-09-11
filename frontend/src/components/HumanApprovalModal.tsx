import React from 'react';
import { InvestigationResult } from '../types';
import { ShieldAlert, CheckCircle, XCircle, AlertTriangle } from 'lucide-react';

interface HumanApprovalModalProps {
  pendingResult: InvestigationResult | null;
  onApprove: (alertId: string, sourceIp: string) => void;
  onReject: (alertId: string, sourceIp: string) => void;
  onClose: () => void;
}

export const HumanApprovalModal: React.FC<HumanApprovalModalProps> = ({
  pendingResult,
  onApprove,
  onReject,
  onClose
}) => {
  if (!pendingResult || pendingResult.status !== 'WAITING_FOR_HUMAN_APPROVAL') {
    return null;
  }

  const alert = pendingResult.evidence?.alert;
  const sourceIp = alert?.source_ip || '';

  return (
    <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-[#131b2e] border border-red-500/60 rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-5 animate-in fade-in zoom-in duration-200">
        
        {/* Header */}
        <div className="flex items-center gap-3 border-b border-slate-800 pb-4">
          <div className="p-3 bg-red-500/20 border border-red-500/40 text-red-400 rounded-xl">
            <ShieldAlert className="w-6 h-6 animate-pulse" />
          </div>
          <div>
            <h3 className="text-base font-bold text-white">Human-in-the-Loop Approval Interceptor</h3>
            <p className="text-xs text-red-400">High-Impact Response Action Requires Authorization</p>
          </div>
        </div>

        {/* Reasoning Details */}
        <div className="bg-[#0a0f1d] p-4 rounded-xl border border-slate-800 space-y-3 text-xs">
          <div>
            <span className="text-slate-500 font-semibold">Recommended Action:</span>
            <div className="font-mono text-sm font-bold text-red-400 mt-0.5">BLOCK_IP ({sourceIp})</div>
          </div>

          <div>
            <span className="text-slate-500 font-semibold">Incident Classification:</span>
            <div className="font-bold text-white mt-0.5">{pendingResult.decision} (Confidence: {((pendingResult.confidence || 0) * 100).toFixed(0)}%)</div>
          </div>

          <div>
            <span className="text-slate-500 font-semibold">Agent Reasoning Summary:</span>
            <p className="text-slate-300 mt-1 leading-relaxed">{pendingResult.reasoning}</p>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="grid grid-cols-2 gap-3 pt-2">
          <button
            onClick={() => onReject(pendingResult.alert_id, sourceIp)}
            className="py-2.5 px-4 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl font-bold text-xs transition-all flex items-center justify-center gap-2"
          >
            <XCircle className="w-4 h-4 text-slate-400" />
            Reject Action
          </button>

          <button
            onClick={() => onApprove(pendingResult.alert_id, sourceIp)}
            className="py-2.5 px-4 bg-red-600 hover:bg-red-500 text-white rounded-xl font-bold text-xs transition-all shadow-lg shadow-red-600/30 flex items-center justify-center gap-2"
          >
            <CheckCircle className="w-4 h-4" />
            Approve & Block IP
          </button>
        </div>

      </div>
    </div>
  );
};
