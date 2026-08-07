import React, { useState, useEffect } from 'react';
import { useWeather } from '../context/WeatherContext';
import { alertsApi } from '../services/api';
import { History, ShieldAlert, Calendar, Clock, AlertTriangle } from 'lucide-react';

export const AlertHistoryPage = () => {
  const { city } = useWeather();
  const [history, setHistory] = useState([]);

  useEffect(() => {
    alertsApi.getAlerts(city).then(data => {
      // Simulate history timeline entries
      const logs = [
        ...data,
        {
          id: "hist_001",
          type: "Heavy Precipitation Notice",
          severity: "Warning",
          city: city,
          title: `Heavy Rain Alert Logged for ${city}`,
          description: "Waterlogging detected in low-lying roads. Citizens advised to take alternative routes.",
          issued_at: "Yesterday at 16:45"
        },
        {
          id: "hist_002",
          type: "Heatwave Advisory",
          severity: "Caution",
          city: city,
          title: "High UV & Temperature Peak",
          description: "Midday temperature exceeded 34°C with UV index > 7. Hydration advisories issued.",
          issued_at: "3 days ago"
        }
      ];
      setHistory(logs);
    });
  }, [city]);

  return (
    <div className="space-y-6">
      <div className="glass-card p-6 border-sky-400/30 flex items-center justify-between">
        <div>
          <h2 className="font-heading font-extrabold text-2xl text-white flex items-center gap-2">
            <History className="w-6 h-6 text-sky-400" />
            <span>Weather Alert History & Logs</span>
          </h2>
          <p className="text-xs text-slate-400">Archived severe advisories and risk logs for {city}</p>
        </div>
        <span className="px-3 py-1 rounded-full bg-sky-500/20 text-sky-300 text-xs font-semibold border border-sky-400/30">
          {history.length} Logs Saved
        </span>
      </div>

      <div className="space-y-4">
        {history.map((item, idx) => (
          <div key={idx} className="glass-card p-5 space-y-2 border-slate-700/50 glass-card-hover">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <ShieldAlert className="w-4 h-4 text-amber-400" />
                <h4 className="font-bold text-sm text-white">{item.title}</h4>
              </div>
              <span className="text-[10px] text-slate-400 flex items-center gap-1">
                <Clock className="w-3 h-3 text-sky-400" />
                {item.issued_at}
              </span>
            </div>

            <p className="text-xs text-slate-300 leading-relaxed pl-6">{item.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};
