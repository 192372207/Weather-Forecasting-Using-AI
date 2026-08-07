import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Bot, PhoneCall, Map, BarChart3, ShieldAlert } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const MobileBottomNav = () => {
  const { user } = useAuth();
  if (!user) return null;

  const items = [
    { path: '/dashboard', label: 'Weather', icon: LayoutDashboard },
    { path: '/ai-chat', label: 'AI Safety', icon: Bot },
    { path: '/emergency', label: 'Emergency', icon: PhoneCall, isEmergency: true },
    { path: '/map', label: 'Radar Map', icon: Map },
    { path: '/alerts', label: 'Alerts', icon: ShieldAlert },
  ];

  return (
    <div className="lg:hidden fixed bottom-0 left-0 right-0 z-50 glass-card rounded-none border-x-0 border-b-0 px-2 py-1.5 backdrop-blur-xl bg-slate-950/95 border-slate-800">
      <div className="flex items-center justify-around">
        {items.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex flex-col items-center gap-0.5 px-2 py-1 rounded-xl transition-all ${
                  item.isEmergency
                    ? 'text-red-400 font-bold animate-pulse'
                    : isActive
                    ? 'text-sky-400 font-bold scale-105'
                    : 'text-slate-400 hover:text-slate-200'
                }`
              }
            >
              <Icon className="w-5 h-5" />
              <span className="text-[10px] tracking-tight">{item.label}</span>
            </NavLink>
          );
        })}
      </div>
    </div>
  );
};
