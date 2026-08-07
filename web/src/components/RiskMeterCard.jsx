import React from 'react';
import { ShieldCheck, AlertTriangle, ShieldAlert, Zap } from 'lucide-react';

export const RiskMeterCard = ({ riskLevel = "Green", riskScore = 20, riskTitle = "SAFE WEATHER CONDITIONS" }) => {
  const getRiskConfig = () => {
    switch (riskLevel) {
      case 'Red':
        return {
          bgColor: 'bg-red-500/20',
          borderColor: 'border-red-500/50',
          textColor: 'text-red-400',
          badgeBg: 'bg-red-500',
          gaugeColor: '#ef4444',
          icon: ShieldAlert,
          label: 'EXTREME DANGER'
        };
      case 'Orange':
        return {
          bgColor: 'bg-orange-500/20',
          borderColor: 'border-orange-500/50',
          textColor: 'text-orange-400',
          badgeBg: 'bg-orange-500',
          gaugeColor: '#f97316',
          icon: AlertTriangle,
          label: 'HIGH RISK'
        };
      case 'Yellow':
        return {
          bgColor: 'bg-amber-500/20',
          borderColor: 'border-amber-400/50',
          textColor: 'text-amber-300',
          badgeBg: 'bg-amber-500',
          gaugeColor: '#f59e0b',
          icon: Zap,
          label: 'MODERATE RISK'
        };
      case 'Green':
      default:
        return {
          bgColor: 'bg-emerald-500/20',
          borderColor: 'border-emerald-500/50',
          textColor: 'text-emerald-400',
          badgeBg: 'bg-emerald-500',
          gaugeColor: '#10b981',
          icon: ShieldCheck,
          label: 'SAFE'
        };
    }
  };

  const config = getRiskConfig();
  const Icon = config.icon;

  return (
    <div className={`glass-card p-5 space-y-4 border ${config.borderColor} transition-all`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Icon className={`w-5 h-5 ${config.textColor}`} />
          <h3 className="font-heading font-extrabold text-sm text-white uppercase tracking-wider">
            AI Weather Risk Index
          </h3>
        </div>
        <span className={`px-2.5 py-0.5 rounded-full text-[11px] font-bold text-white ${config.badgeBg}`}>
          {config.label}
        </span>
      </div>

      <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
        {/* Animated Semi-Circle Meter */}
        <div className="relative w-32 h-20 flex items-end justify-center">
          <svg className="w-32 h-32 transform -rotate-90" viewBox="0 0 36 36">
            <path
              className="text-slate-800"
              strokeWidth="4"
              stroke="currentColor"
              fill="none"
              d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
            />
            <path
              stroke={config.gaugeColor}
              strokeDasharray={`${riskScore}, 100`}
              strokeWidth="4"
              strokeLinecap="round"
              fill="none"
              d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              className="transition-all duration-1000 ease-out"
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center pt-4">
            <span className={`font-heading text-2xl font-extrabold ${config.textColor}`}>
              {riskScore}%
            </span>
            <span className="text-[9px] text-slate-400 uppercase tracking-widest">Risk Score</span>
          </div>
        </div>

        {/* Risk Status & Info */}
        <div className="flex-1 space-y-1 text-center sm:text-left">
          <p className={`font-bold text-sm ${config.textColor}`}>{riskTitle}</p>
          <p className="text-xs text-slate-300">
            {riskLevel === 'Green' && 'All weather telemetry indicates clear, safe conditions for outdoor activities and travel.'}
            {riskLevel === 'Yellow' && 'Minor atmospheric shifts detected. Keep an umbrella ready and exercise caution.'}
            {riskLevel === 'Orange' && 'High weather risk detected. Heavy rain, high AQI, or strong winds expected. Limit non-essential travel.'}
            {riskLevel === 'Red' && 'DANGER: Severe storm, flood, or cyclone risk active! Remain indoors and keep emergency services ready.'}
          </p>
        </div>
      </div>
    </div>
  );
};
