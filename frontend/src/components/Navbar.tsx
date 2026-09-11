import React from 'react';
import { Shield, Activity, RefreshCw, Cpu, CheckCircle2, Award, Wifi, WifiOff } from 'lucide-react';

interface NavbarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  onReset: () => void;
  isResetting: boolean;
  isBackendConnected: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({
  activeTab,
  setActiveTab,
  onReset,
  isResetting,
  isBackendConnected
}) => {
  return (
    <header className="bg-[#131b2e] border-b border-slate-800 sticky top-0 z-40 px-6 py-3.5 shadow-xl">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="p-2 bg-blue-600/20 border border-blue-500/40 rounded-lg text-blue-400">
            <Shield className="w-6 h-6 animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold tracking-tight text-white">Aegis<span className="text-blue-500">SOC</span></h1>
              <span className="px-2 py-0.5 text-[10px] font-semibold tracking-wider text-cyan-300 bg-cyan-950/80 border border-cyan-700/50 rounded-full">
                AGENTIC AI
              </span>
            </div>
            <p className="text-xs text-slate-400">Autonomous SOC Investigation & Response Agent • IIT Bhubaneswar Demo</p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="flex items-center gap-1 bg-[#0a0f1d] p-1 rounded-xl border border-slate-800">
          <button
            onClick={() => setActiveTab('dashboard')}
            className={`px-4 py-2 text-xs font-medium rounded-lg transition-all flex items-center gap-2 ${
              activeTab === 'dashboard'
                ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/30'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
            }`}
          >
            <Activity className="w-3.5 h-3.5" />
            Alert Dashboard
          </button>
          
          <button
            onClick={() => setActiveTab('workspace')}
            className={`px-4 py-2 text-xs font-medium rounded-lg transition-all flex items-center gap-2 ${
              activeTab === 'workspace'
                ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/30'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
            }`}
          >
            <Cpu className="w-3.5 h-3.5" />
            Agent Workspace
          </button>

          <button
            onClick={() => setActiveTab('scenarios')}
            className={`px-4 py-2 text-xs font-medium rounded-lg transition-all flex items-center gap-2 ${
              activeTab === 'scenarios'
                ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/30'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
            }`}
          >
            <CheckCircle2 className="w-3.5 h-3.5 text-cyan-400" />
            Demo Scenarios (5)
          </button>

          <button
            onClick={() => setActiveTab('evaluation')}
            className={`px-4 py-2 text-xs font-medium rounded-lg transition-all flex items-center gap-2 ${
              activeTab === 'evaluation'
                ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/30'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
            }`}
          >
            <Award className="w-3.5 h-3.5 text-yellow-400" />
            Evaluation Benchmark
          </button>
        </nav>

        {/* System Controls & Health */}
        <div className="flex items-center gap-3">
          {isBackendConnected ? (
            <div className="flex items-center gap-1.5 px-3 py-1 bg-emerald-950/80 border border-emerald-700/60 rounded-lg text-emerald-400 text-xs font-semibold">
              <Wifi className="w-3.5 h-3.5 text-emerald-400 animate-pulse" />
              <span>API Online</span>
            </div>
          ) : (
            <div className="flex items-center gap-1.5 px-3 py-1 bg-red-950/80 border border-red-700/60 rounded-lg text-red-400 text-xs font-semibold animate-pulse">
              <WifiOff className="w-3.5 h-3.5 text-red-400" />
              <span>Backend Disconnected</span>
            </div>
          )}

          <button
            onClick={onReset}
            disabled={isResetting}
            className="p-2 text-slate-400 hover:text-white bg-slate-800/60 hover:bg-slate-800 border border-slate-700/60 rounded-lg transition-all"
            title="Reset Sandbox Database"
          >
            <RefreshCw className={`w-4 h-4 ${isResetting ? 'animate-spin text-blue-400' : ''}`} />
          </button>
        </div>

      </div>
    </header>
  );
};
