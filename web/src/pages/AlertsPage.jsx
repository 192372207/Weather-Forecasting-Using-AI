import React, { useState, useEffect } from 'react';
import { useWeather } from '../context/WeatherContext';
import { alertsApi } from '../services/api';
import { ShieldAlert, AlertTriangle, Info, BellRing, CheckCircle2 } from 'lucide-react';

export const AlertsPage = () => {
  const { city } = useWeather();
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    alertsApi.getAlerts(city).then(setAlerts);
  }, [city]);

  return (
    <div className="space-y-6">
      <div className="glass-card p-6 border-sky-400/30 flex items-center justify-between">
        <div>
          <h2 className="font-heading font-extrabold text-2xl text-white flex items-center gap-2">
            <ShieldAlert className="w-6 h-6 text-amber-400" />
            <span>Severe Weather Alerts & Warnings</span>
          </h2>
          <p className="text-xs text-slate-400">Live safety advisories for {city}</p>
        </div>
        <span className="px-3 py-1 rounded-full bg-amber-500/20 text-amber-300 text-xs font-semibold border border-amber-400/30">
          {alerts.length} Active Warnings
        </span>
      </div>

      <div className="space-y-4">
        {alerts.map((alt) => (
          <div key={alt.id} className="glass-card p-5 space-y-2 border-amber-500/30">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <AlertTriangle className="w-5 h-5 text-amber-400" />
                <h3 className="font-bold text-sm text-white">{alt.title}</h3>
              </div>
              <span className="text-[10px] text-slate-400">{alt.issued_at}</span>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed pl-7">{alt.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};
