import React, { useState } from 'react';
import { EvidenceBundle } from '../types';
import { Server, ShieldAlert, FileText, Activity } from 'lucide-react';

interface EvidenceInspectorProps {
  evidence?: EvidenceBundle;
}

export const EvidenceInspector: React.FC<EvidenceInspectorProps> = ({ evidence }) => {
  const [activeSubTab, setActiveSubTab] = useState<'logs' | 'asset' | 'vulns' | 'network'>('logs');

  if (!evidence) {
    return (
      <div className="bg-[#131b2e] border border-slate-800 rounded-2xl p-8 text-center text-slate-500">
        No evidence loaded. Select an alert or scenario.
      </div>
    );
  }

  return (
    <div className="bg-[#131b2e] border border-slate-800 rounded-2xl p-5 shadow-xl space-y-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <h3 className="text-base font-bold text-white flex items-center gap-2">
          <FileText className="w-5 h-5 text-cyan-400" />
          Retrieved Evidence Inspection Panel
        </h3>

        {/* Subtab selector */}
        <div className="flex items-center gap-1 bg-[#0a0f1d] p-1 rounded-xl border border-slate-800">
          <button
            onClick={() => setActiveSubTab('logs')}
            className={`px-3 py-1 text-xs font-semibold rounded-lg transition-all ${
              activeSubTab === 'logs' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Server Logs ({evidence.server_logs?.length || 0})
          </button>
          <button
            onClick={() => setActiveSubTab('asset')}
            className={`px-3 py-1 text-xs font-semibold rounded-lg transition-all ${
              activeSubTab === 'asset' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Asset Info
          </button>
          <button
            onClick={() => setActiveSubTab('vulns')}
            className={`px-3 py-1 text-xs font-semibold rounded-lg transition-all ${
              activeSubTab === 'vulns' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Vulnerabilities ({evidence.vulnerabilities?.length || 0})
          </button>
          <button
            onClick={() => setActiveSubTab('network')}
            className={`px-3 py-1 text-xs font-semibold rounded-lg transition-all ${
              activeSubTab === 'network' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Network Events ({evidence.network_events?.length || 0})
          </button>
        </div>
      </div>

      {/* Subtab Content */}
      {activeSubTab === 'logs' && (
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-[#0a0f1d] text-slate-400 border-b border-slate-800">
              <tr>
                <th className="p-2.5">Log ID</th>
                <th className="p-2.5">Event Type</th>
                <th className="p-2.5">User</th>
                <th className="p-2.5">Action</th>
                <th className="p-2.5">Status</th>
                <th className="p-2.5">Message Details</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-slate-300">
              {evidence.server_logs?.map((log, idx) => (
                <tr key={idx} className="hover:bg-slate-800/40">
                  <td className="p-2.5 text-blue-400 font-bold">{log.log_id}</td>
                  <td className="p-2.5 text-amber-300">{log.event_type}</td>
                  <td className="p-2.5 text-white">{log.username || '-'}</td>
                  <td className="p-2.5 text-slate-300">{log.action}</td>
                  <td className="p-2.5">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                      log.status === 'SUCCESS' || log.status === 'VERIFIED_ADMIN' ? 'bg-emerald-950 text-emerald-400 border border-emerald-800/60' :
                      log.status === 'FAILED' ? 'bg-red-950 text-red-400 border border-red-800/60' :
                      'bg-slate-800 text-slate-300'
                    }`}>
                      {log.status}
                    </span>
                  </td>
                  <td className="p-2.5 text-slate-400 text-[11px] truncate max-w-md">{log.message}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {activeSubTab === 'asset' && (
        <div className="bg-[#0a0f1d] p-4 rounded-xl border border-slate-800 text-xs font-mono space-y-2">
          {evidence.asset ? (
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-slate-300">
              <div><span className="text-slate-500">Hostname:</span> <span className="font-bold text-white">{evidence.asset.hostname}</span></div>
              <div><span className="text-slate-500">IP Address:</span> <span className="text-cyan-400">{evidence.asset.ip_address}</span></div>
              <div><span className="text-slate-500">OS:</span> {evidence.asset.operating_system}</div>
              <div><span className="text-slate-500">Department:</span> {evidence.asset.owner_department}</div>
              <div><span className="text-slate-500">Criticality:</span> <span className="text-red-400 font-bold">{evidence.asset.criticality}</span></div>
              <div><span className="text-slate-500">Internet Exposed:</span> {evidence.asset.exposed_to_internet ? 'YES' : 'NO'}</div>
            </div>
          ) : (
            <p className="text-slate-400">No asset metadata found.</p>
          )}
        </div>
      )}

      {activeSubTab === 'vulns' && (
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-[#0a0f1d] text-slate-400 border-b border-slate-800">
              <tr>
                <th className="p-2.5">CVE ID</th>
                <th className="p-2.5">Service</th>
                <th className="p-2.5">Severity</th>
                <th className="p-2.5">Exploit Available</th>
                <th className="p-2.5">Patch Status</th>
                <th className="p-2.5">Description</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-slate-300">
              {evidence.vulnerabilities?.map((v, idx) => (
                <tr key={idx} className="hover:bg-slate-800/40">
                  <td className="p-2.5 text-red-400 font-bold">{v.cve_id}</td>
                  <td className="p-2.5 text-cyan-300">{v.service}</td>
                  <td className="p-2.5 font-bold text-amber-400">{v.severity}</td>
                  <td className="p-2.5">{v.exploit_available ? 'YES' : 'NO'}</td>
                  <td className="p-2.5">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                      v.patched ? 'bg-emerald-950 text-emerald-400' : 'bg-red-950 text-red-400'
                    }`}>
                      {v.patched ? 'PATCHED' : 'UNPATCHED'}
                    </span>
                  </td>
                  <td className="p-2.5 text-slate-400 text-[11px]">{v.description}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {activeSubTab === 'network' && (
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-[#0a0f1d] text-slate-400 border-b border-slate-800">
              <tr>
                <th className="p-2.5">Event ID</th>
                <th className="p-2.5">Source IP</th>
                <th className="p-2.5">Dest IP</th>
                <th className="p-2.5">Port / Proto</th>
                <th className="p-2.5">Bytes / Packets</th>
                <th className="p-2.5">Connection Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-slate-300">
              {evidence.network_events?.map((net, idx) => (
                <tr key={idx} className="hover:bg-slate-800/40">
                  <td className="p-2.5 text-blue-400 font-bold">{net.event_id}</td>
                  <td className="p-2.5">{net.source_ip}</td>
                  <td className="p-2.5">{net.destination_ip}</td>
                  <td className="p-2.5 text-amber-300">{net.port} / {net.protocol}</td>
                  <td className="p-2.5">{net.bytes?.toLocaleString()} B ({net.packets} pkts)</td>
                  <td className="p-2.5 text-cyan-400 font-bold">{net.connection_status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
