import React from 'react';
import { SecurityAlert } from '../types';
import { Network, Server, Shield, Lock, AlertTriangle, ArrowRight } from 'lucide-react';

interface NetworkTopologyProps {
  alert?: SecurityAlert;
  asset?: any;
  firewallActive?: boolean;
}

export const NetworkTopology: React.FC<NetworkTopologyProps> = ({ alert, asset, firewallActive }) => {
  return (
    <div className="bg-[#131b2e] border border-slate-800 rounded-2xl p-5 shadow-xl space-y-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2">
          <Network className="w-5 h-5 text-blue-400" />
          <h3 className="text-base font-bold text-white">Network Attack Topology & Relationship Graph</h3>
        </div>
        <span className="text-xs text-slate-400 font-mono">Dynamic Path Visualization</span>
      </div>

      {/* Topology Nodes Flow Diagram */}
      <div className="bg-[#0a0f1d] p-6 rounded-xl border border-slate-800 flex flex-col md:flex-row items-center justify-around gap-6 relative">
        
        {/* Node 1: External Source IP */}
        <div className="flex flex-col items-center text-center space-y-2 group">
          <div className={`p-4 rounded-2xl border-2 shadow-lg transition-all ${
            alert ? 'bg-red-950/80 border-red-500 text-red-400 shadow-red-500/20' : 'bg-slate-900 border-slate-700 text-slate-400'
          }`}>
            <AlertTriangle className="w-8 h-8 animate-bounce" />
          </div>
          <div>
            <span className="text-[10px] text-slate-500 font-semibold uppercase">Source Entity</span>
            <div className="font-mono text-xs font-bold text-red-400">{alert?.source_ip || '198.51.100.45'}</div>
            <div className="text-[11px] text-slate-400">{alert?.attack_type || 'External Threat'}</div>
          </div>
        </div>

        {/* Link Arrow 1 */}
        <div className="flex flex-col items-center text-slate-600">
          <span className="text-[10px] font-mono text-amber-400 mb-1">{alert?.protocol || 'TCP'} Port {alert?.destination_port || 22}</span>
          <ArrowRight className="w-6 h-6 animate-pulse text-amber-500" />
        </div>

        {/* Node 2: Perimeter Firewall / WAF */}
        <div className="flex flex-col items-center text-center space-y-2">
          <div className={`p-4 rounded-2xl border-2 shadow-lg transition-all ${
            firewallActive ? 'bg-emerald-950/90 border-emerald-400 text-emerald-400 shadow-emerald-500/30' : 'bg-slate-900 border-slate-700 text-slate-400'
          }`}>
            {firewallActive ? <Lock className="w-8 h-8 text-emerald-400" /> : <Shield className="w-8 h-8 text-slate-400" />}
          </div>
          <div>
            <span className="text-[10px] text-slate-500 font-semibold uppercase">Perimeter Guard</span>
            <div className="font-mono text-xs font-bold text-white">Simulated Firewall</div>
            <div className={`text-[11px] font-semibold ${firewallActive ? 'text-emerald-400' : 'text-slate-400'}`}>
              {firewallActive ? 'RULE ENFORCED (BLOCKED)' : 'MONITORING PASS-THROUGH'}
            </div>
          </div>
        </div>

        {/* Link Arrow 2 */}
        <div className="flex flex-col items-center text-slate-600">
          <ArrowRight className="w-6 h-6 text-slate-600" />
        </div>

        {/* Node 3: Target Server Asset */}
        <div className="flex flex-col items-center text-center space-y-2">
          <div className="p-4 bg-cyan-950/80 border-2 border-cyan-500 text-cyan-400 rounded-2xl shadow-lg shadow-cyan-500/20">
            <Server className="w-8 h-8" />
          </div>
          <div>
            <span className="text-[10px] text-slate-500 font-semibold uppercase">Target Asset</span>
            <div className="font-mono text-xs font-bold text-cyan-400">{asset?.hostname || 'db-prod-01'}</div>
            <div className="text-[11px] text-slate-300">{asset?.ip_address || alert?.destination_ip || '10.0.4.15'}</div>
            <div className="text-[10px] text-red-400 font-semibold mt-0.5">Criticality: {asset?.criticality || 'CRITICAL'}</div>
          </div>
        </div>

      </div>
    </div>
  );
};
