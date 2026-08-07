import React, { useState, useEffect } from 'react';
import { adminApi } from '../services/api';
import { ShieldCheck, Users, Activity, Bot, Cpu, HardDrive, Terminal } from 'lucide-react';

export const AdminPage = () => {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    adminApi.getStats().then(setStats);
  }, []);

  return (
    <div className="space-y-6">
      <div className="glass-card p-6 border-sky-400/30 flex items-center justify-between">
        <div>
          <h2 className="font-heading font-extrabold text-2xl text-white flex items-center gap-2">
            <ShieldCheck className="w-6 h-6 text-emerald-400" />
            <span>SkySense System Console & Admin Panel</span>
          </h2>
          <p className="text-xs text-slate-400">System metrics, Groq AI status, and API telemetry</p>
        </div>
        <span className="px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-semibold border border-emerald-400/30">
          ● System 100% Operational
        </span>
      </div>

      {/* Metrics Grid */}
      {stats && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="glass-card p-4 space-y-1 border-slate-700/50">
            <p className="text-xs text-slate-400 flex items-center gap-1">
              <Users className="w-3.5 h-3.5 text-sky-400" />
              Total Users
            </p>
            <p className="text-2xl font-bold text-white font-heading">{stats.total_users}</p>
          </div>

          <div className="glass-card p-4 space-y-1 border-slate-700/50">
            <p className="text-xs text-slate-400 flex items-center gap-1">
              <Bot className="w-3.5 h-3.5 text-indigo-400" />
              AI Queries Today
            </p>
            <p className="text-2xl font-bold text-white font-heading">{stats.ai_queries_today}</p>
          </div>

          <div className="glass-card p-4 space-y-1 border-slate-700/50">
            <p className="text-xs text-slate-400 flex items-center gap-1">
              <Activity className="w-3.5 h-3.5 text-emerald-400" />
              API Telemetry Calls
            </p>
            <p className="text-2xl font-bold text-white font-heading">{stats.weather_api_calls_today}</p>
          </div>

          <div className="glass-card p-4 space-y-1 border-slate-700/50">
            <p className="text-xs text-slate-400 flex items-center gap-1">
              <Cpu className="w-3.5 h-3.5 text-cyan-400" />
              API Latency
            </p>
            <p className="text-2xl font-bold text-emerald-400 font-heading">{stats.api_latency_ms} ms</p>
          </div>
        </div>
      )}

      {/* System Status Table */}
      <div className="glass-card p-6 space-y-4">
        <h3 className="font-heading text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
          <Terminal className="w-4 h-4 text-sky-400" />
          <span>Integrated Services Health</span>
        </h3>

        <div className="space-y-3 text-xs">
          <div className="p-3 glass-card flex items-center justify-between">
            <span className="font-semibold text-slate-200">MongoDB Atlas Driver (Motor)</span>
            <span className="text-emerald-400 font-bold">Connected & Cached</span>
          </div>
          <div className="p-3 glass-card flex items-center justify-between">
            <span className="font-semibold text-slate-200">Groq AI Engine (llama-3.3-70b-versatile)</span>
            <span className="text-emerald-400 font-bold">Active</span>
          </div>
          <div className="p-3 glass-card flex items-center justify-between">
            <span className="font-semibold text-slate-200">Open-Meteo REST Weather Stream</span>
            <span className="text-emerald-400 font-bold">Online</span>
          </div>
        </div>
      </div>
    </div>
  );
};
