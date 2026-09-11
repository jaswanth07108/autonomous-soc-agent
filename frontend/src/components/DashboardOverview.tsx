import React from 'react';
import { SecurityAlert, FirewallRule } from '../types';
import { ShieldAlert, AlertTriangle, CheckCircle, ShieldCheck, Play, Radio, Lock } from 'lucide-react';

interface DashboardOverviewProps {
  alerts: SecurityAlert[];
  firewallRules: FirewallRule[];
  onInvestigate: (alertId: string) => void;
  onSelectScenario: (scenarioId: number) => void;
}

export const DashboardOverview: React.FC<DashboardOverviewProps> = ({
  alerts,
  firewallRules,
  onInvestigate,
  onSelectScenario
}) => {
  const criticalCount = alerts.filter(a => a.severity === 'CRITICAL').length;
  const highCount = alerts.filter(a => a.severity === 'HIGH').length;
  const activeBlocks = firewallRules.filter(r => r.active === 1).length;

  return (
    <div className="space-y-6">
      
      {/* Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        
        <div className="bg-[#131b2e] border border-slate-800 p-5 rounded-2xl relative overflow-hidden shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs text-slate-400 font-medium uppercase tracking-wider">Active Ingested Alerts</p>
              <h3 className="text-3xl font-bold text-white mt-1">{alerts.length}</h3>
            </div>
            <div className="p-3 bg-blue-500/10 border border-blue-500/20 text-blue-400 rounded-xl">
              <Radio className="w-6 h-6 animate-pulse" />
            </div>
          </div>
          <div className="mt-3 text-xs text-slate-400 flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-blue-400" />
            <span>NIDS / Suricata / WAF Stream</span>
          </div>
        </div>

        <div className="bg-[#131b2e] border border-red-900/40 p-5 rounded-2xl relative overflow-hidden shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs text-red-400 font-medium uppercase tracking-wider">Critical Severity</p>
              <h3 className="text-3xl font-bold text-red-400 mt-1">{criticalCount}</h3>
            </div>
            <div className="p-3 bg-red-500/10 border border-red-500/20 text-red-400 rounded-xl">
              <ShieldAlert className="w-6 h-6" />
            </div>
          </div>
          <div className="mt-3 text-xs text-slate-400 flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-red-500" />
            <span>High Risk Target Compromise</span>
          </div>
        </div>

        <div className="bg-[#131b2e] border border-amber-900/40 p-5 rounded-2xl relative overflow-hidden shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs text-amber-400 font-medium uppercase tracking-wider">High Severity</p>
              <h3 className="text-3xl font-bold text-amber-400 mt-1">{highCount}</h3>
            </div>
            <div className="p-3 bg-amber-500/10 border border-amber-500/20 text-amber-400 rounded-xl">
              <AlertTriangle className="w-6 h-6" />
            </div>
          </div>
          <div className="mt-3 text-xs text-slate-400 flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-amber-400" />
            <span>Exploit Probes & Scans</span>
          </div>
        </div>

        <div className="bg-[#131b2e] border border-emerald-900/40 p-5 rounded-2xl relative overflow-hidden shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs text-emerald-400 font-medium uppercase tracking-wider">Active Firewall Rules</p>
              <h3 className="text-3xl font-bold text-emerald-400 mt-1">{activeBlocks}</h3>
            </div>
            <div className="p-3 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 rounded-xl">
              <Lock className="w-6 h-6" />
            </div>
          </div>
          <div className="mt-3 text-xs text-slate-400 flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
            <span>Verified Perimeter Enforcements</span>
          </div>
        </div>

      </div>

      {/* Quick Demo Scenario Trigger Bar */}
      <div className="bg-[#131b2e] border border-blue-900/40 p-4 rounded-2xl flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-cyan-500/20 border border-cyan-500/40 text-cyan-400 rounded-lg">
            <Play className="w-5 h-5" />
          </div>
          <div>
            <h4 className="text-sm font-semibold text-white">Hackathon Demo Launcher</h4>
            <p className="text-xs text-slate-400">Launch any of the 5 official problem scenarios in 1-click</p>
          </div>
        </div>

        <div className="flex items-center gap-2 flex-wrap">
          <button
            onClick={() => onSelectScenario(1)}
            className="px-3 py-1.5 bg-red-950/80 hover:bg-red-900 border border-red-700/60 text-red-300 text-xs font-semibold rounded-xl transition-all shadow"
          >
            1. Successful Attack
          </button>
          <button
            onClick={() => onSelectScenario(2)}
            className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 border border-slate-600 text-slate-200 text-xs font-semibold rounded-xl transition-all shadow"
          >
            2. False Positive
          </button>
          <button
            onClick={() => onSelectScenario(3)}
            className="px-3 py-1.5 bg-amber-950/80 hover:bg-amber-900 border border-amber-700/60 text-amber-300 text-xs font-semibold rounded-xl transition-all shadow"
          >
            3. Attack Failed
          </button>
          <button
            onClick={() => onSelectScenario(4)}
            className="px-3 py-1.5 bg-cyan-950/80 hover:bg-cyan-900 border border-cyan-700/60 text-cyan-300 text-xs font-semibold rounded-xl transition-all shadow"
          >
            4. Adaptation (MFA)
          </button>
          <button
            onClick={() => onSelectScenario(5)}
            className="px-3 py-1.5 bg-purple-950/80 hover:bg-purple-900 border border-purple-700/60 text-purple-300 text-xs font-semibold rounded-xl transition-all shadow"
          >
            5. Failure Recovery
          </button>
        </div>
      </div>

      {/* Security Alerts Queue */}
      <div className="bg-[#131b2e] border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
        <div className="p-5 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <ShieldAlert className="w-5 h-5 text-blue-400" />
            <h3 className="text-base font-semibold text-white">Ingested Security Alert Queue</h3>
          </div>
          <span className="text-xs text-slate-400 font-mono">Live Sandbox Stream</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-[#0a0f1d] text-slate-400 uppercase tracking-wider border-b border-slate-800 font-semibold">
              <tr>
                <th className="py-3 px-4">Alert ID</th>
                <th className="py-3 px-4">Timestamp</th>
                <th className="py-3 px-4">Attack Type</th>
                <th className="py-3 px-4">Source IP</th>
                <th className="py-3 px-4">Destination IP</th>
                <th className="py-3 px-4">Severity</th>
                <th className="py-3 px-4">Sensor</th>
                <th className="py-3 px-4 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-slate-300">
              {alerts.map((alert) => (
                <tr key={alert.alert_id} className="hover:bg-slate-800/40 transition-colors">
                  <td className="py-3.5 px-4 font-mono font-bold text-blue-400">{alert.alert_id}</td>
                  <td className="py-3.5 px-4 text-slate-400">{new Date(alert.timestamp).toLocaleTimeString()}</td>
                  <td className="py-3.5 px-4 font-medium text-white">{alert.attack_type}</td>
                  <td className="py-3.5 px-4 font-mono text-slate-300">{alert.source_ip}</td>
                  <td className="py-3.5 px-4 font-mono text-slate-300">{alert.destination_ip}</td>
                  <td className="py-3.5 px-4">
                    <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold ${
                      alert.severity === 'CRITICAL' ? 'bg-red-950 text-red-400 border border-red-800/60' :
                      alert.severity === 'HIGH' ? 'bg-amber-950 text-amber-400 border border-amber-800/60' :
                      'bg-slate-800 text-slate-300'
                    }`}>
                      {alert.severity}
                    </span>
                  </td>
                  <td className="py-3.5 px-4 text-slate-400">{alert.sensor}</td>
                  <td className="py-3.5 px-4 text-right">
                    <button
                      onClick={() => onInvestigate(alert.alert_id)}
                      className="px-3.5 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-semibold transition-all shadow-md shadow-blue-600/20 flex items-center gap-1.5 ml-auto"
                    >
                      <Play className="w-3.5 h-3.5" />
                      Autonomous Investigate
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
};
