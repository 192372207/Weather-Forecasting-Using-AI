import React from 'react';
import { HeartPulse, Sun, Droplets, Shield, Umbrella, Shirt, Car, Wind } from 'lucide-react';

export const WeatherHealthCard = ({ weather, precautions = [] }) => {
  if (!weather) return null;

  const aqiVal = weather.aqi || 30;
  const uvVal = weather.uv_index || 4.5;
  const temp = weather.temp || 22;

  const getAqiColor = (val) => {
    if (val <= 50) return 'text-emerald-400 border-emerald-500/40 bg-emerald-500/10';
    if (val <= 100) return 'text-amber-400 border-amber-500/40 bg-amber-500/10';
    return 'text-red-400 border-red-500/40 bg-red-500/10';
  };

  const getUvColor = (val) => {
    if (val <= 3) return 'text-emerald-400';
    if (val <= 6) return 'text-amber-400';
    return 'text-orange-400';
  };

  return (
    <div className="glass-card p-5 space-y-4 border-sky-400/30">
      <div className="flex items-center justify-between">
        <h3 className="font-heading font-extrabold text-sm text-white uppercase tracking-wider flex items-center gap-2">
          <HeartPulse className="w-5 h-5 text-sky-400" />
          <span>Weather Health & Safety Guidance</span>
        </h3>
        <span className="text-[10px] text-sky-300 font-semibold px-2 py-0.5 rounded bg-sky-500/20 border border-sky-400/30">
          AI Telemetry
        </span>
      </div>

      {/* Health Metrics Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {/* AQI Health Box */}
        <div className={`p-3 rounded-xl border ${getAqiColor(aqiVal)} space-y-1`}>
          <div className="flex items-center gap-1.5 text-xs font-semibold">
            <Wind className="w-4 h-4" />
            <span>AIR QUALITY</span>
          </div>
          <p className="text-xl font-extrabold font-heading">{aqiVal} <span className="text-[10px] font-normal">AQI</span></p>
          <p className="text-[10px] opacity-80">{weather.aqi_description || 'Good'}</p>
        </div>

        {/* UV Index Box */}
        <div className="p-3 glass-card rounded-xl border-slate-700/50 space-y-1">
          <div className="flex items-center gap-1.5 text-xs font-semibold text-amber-400">
            <Sun className="w-4 h-4" />
            <span>UV INDEX</span>
          </div>
          <p className={`text-xl font-extrabold font-heading ${getUvColor(uvVal)}`}>{uvVal}</p>
          <p className="text-[10px] text-slate-400">{uvVal > 6 ? 'Sunscreen Required' : 'Moderate Sun'}</p>
        </div>

        {/* Hydration Goal */}
        <div className="p-3 glass-card rounded-xl border-slate-700/50 space-y-1">
          <div className="flex items-center gap-1.5 text-xs font-semibold text-cyan-400">
            <Droplets className="w-4 h-4" />
            <span>HYDRATION</span>
          </div>
          <p className="text-xl font-extrabold text-white font-heading">{temp > 30 ? '3.5L' : '2.5L'}</p>
          <p className="text-[10px] text-slate-400">Daily Water Goal</p>
        </div>

        {/* Vulnerable Groups */}
        <div className="p-3 glass-card rounded-xl border-slate-700/50 space-y-1">
          <div className="flex items-center gap-1.5 text-xs font-semibold text-indigo-400">
            <Shield className="w-4 h-4" />
            <span>SENSITIVE GROUPS</span>
          </div>
          <p className="text-sm font-bold text-white leading-snug">
            {aqiVal > 80 ? 'Mask Needed' : 'Safe Outdoors'}
          </p>
          <p className="text-[10px] text-slate-400">Elderly & Children Advice</p>
        </div>
      </div>

      {/* Safety Precautions List */}
      {precautions.length > 0 && (
        <div className="space-y-2 pt-2 border-t border-slate-700/50">
          <p className="text-xs font-bold text-slate-300 uppercase tracking-wider">AI Safety Action Items</p>
          <div className="grid gap-2">
            {precautions.map((item, idx) => (
              <div key={idx} className="p-2.5 glass-card bg-sky-950/30 border-sky-400/20 text-xs text-slate-200 rounded-xl flex items-center gap-2">
                <span className="text-sm">{item}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
