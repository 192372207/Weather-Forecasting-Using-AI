import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Bot,
  Map,
  BarChart3,
  Users,
  GitCompare,
  ShieldAlert,
  ShieldCheck,
  Home,
  PhoneCall,
  History,
  LogIn,
  UserPlus
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const Sidebar = () => {
  const { user } = useAuth();

  const navItems = [
    { path: '/', label: 'Landing Page', icon: Home },
    { path: '/dashboard', label: 'Weather Hub', icon: LayoutDashboard },
    { path: '/ai-chat', label: 'AI Safety Assistant', icon: Bot, badge: 'Groq' },
    { path: '/emergency', label: 'Emergency Mode', icon: PhoneCall, badge: 'Alert' },
    { path: '/alert-history', label: 'Alert History', icon: History },
    { path: '/map', label: 'Interactive Map', icon: Map },
    { path: '/analytics', label: 'Weather Analytics', icon: BarChart3 },
    { path: '/community', label: 'Community Feed', icon: Users },
    { path: '/comparison', label: 'City Comparison', icon: GitCompare },
    { path: '/alerts', label: 'Weather Warnings', icon: ShieldAlert },
    { path: '/admin', label: 'Admin Dashboard', icon: ShieldCheck, badge: 'Admin' },
  ];

  if (!user) {
    navItems.push(
      { path: '/login', label: 'Login', icon: LogIn },
      { path: '/register', label: 'Register', icon: UserPlus }
    );
  }

  return (
    <aside className="w-64 glass-card p-4 hidden lg:block sticky top-24 h-[calc(100vh-7rem)] flex flex-col justify-between">
      <div className="space-y-1 overflow-y-auto pr-1">
        <p className="px-3 py-2 text-[10px] font-bold text-sky-400 uppercase tracking-widest">
          Main Navigation
        </p>
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center justify-between px-3 py-2 rounded-xl text-xs font-medium transition-all ${
                  isActive
                    ? 'bg-gradient-to-r from-sky-500/20 to-indigo-500/20 text-sky-300 border border-sky-400/30 shadow-md shadow-sky-500/10'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'
                }`
              }
            >
              <div className="flex items-center gap-2.5">
                <Icon className="w-4 h-4 text-sky-400" />
                <span>{item.label}</span>
              </div>
              {item.badge && (
                <span className={`px-1.5 py-0.5 text-[9px] font-semibold border rounded-md ${
                  item.badge === 'Alert' ? 'bg-red-500/20 text-red-300 border-red-400/30' : 'bg-sky-500/20 text-sky-300 border-sky-400/30'
                }`}>
                  {item.badge}
                </span>
              )}
            </NavLink>
          );
        })}
      </div>

      {/* Powered by Open-Meteo & Groq */}
      <div className="p-3 glass-card bg-sky-950/40 border border-sky-500/20 rounded-xl space-y-1 text-center mt-2">
        <p className="text-[11px] font-semibold text-slate-200">SkySense Safety Engine</p>
        <p className="text-[10px] text-slate-400">Groq AI + Live Open-Meteo Telemetry</p>
      </div>
    </aside>
  );
};
