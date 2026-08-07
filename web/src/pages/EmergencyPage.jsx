import React, { useState, useEffect } from 'react';
import { useWeather } from '../context/WeatherContext';
import { safetyApi } from '../services/api';
import { ShieldAlert, AlertTriangle, PhoneCall, MapPin, Navigation, Building2, Shield, Flame, LifeBuoy, Volume2 } from 'lucide-react';

export const EmergencyPage = () => {
  const { city, weather } = useWeather();
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    safetyApi.getEmergencyServices(city).then(data => {
      setServices(data);
      setLoading(false);
    });

    if ('vibrate' in navigator) {
      navigator.vibrate([200, 100, 200, 100, 300]);
    }
  }, [city]);

  const emergencyHelplines = [
    { name: "Emergency Response", number: "112", icon: PhoneCall, color: "bg-red-600" },
    { name: "Ambulance Medical", number: "108", icon: Building2, color: "bg-rose-600" },
    { name: "Disaster Helpline", number: "1078", icon: LifeBuoy, color: "bg-orange-600" },
    { name: "Police Headquarters", number: "100", icon: Shield, color: "bg-blue-600" },
    { name: "Fire & Rescue", number: "101", icon: Flame, color: "bg-amber-600" },
  ];

  return (
    <div className="space-y-6">
      {/* Emergency Mode Red Header Banner */}
      <div className="glass-card p-6 border-red-500/50 bg-red-950/40 space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-2xl bg-red-600 flex items-center justify-center shadow-lg shadow-red-500/40 animate-pulse">
              <ShieldAlert className="w-7 h-7 text-white" />
            </div>
            <div>
              <h2 className="font-heading font-extrabold text-2xl text-white">
                EMERGENCY MODE & HAZARD NAVIGATION
              </h2>
              <p className="text-xs text-red-300">Live response protocols for {city}</p>
            </div>
          </div>
          <span className="px-3 py-1 rounded-full bg-red-600 text-white text-xs font-bold uppercase tracking-wider animate-bounce">
            ● RED ALERT
          </span>
        </div>

        <p className="text-xs text-slate-200 leading-relaxed pt-2 border-t border-red-500/30">
          If you encounter localized flooding, severe thunderstorms, cyclone wind gusts, or medical distress, use one-tap emergency calling below.
        </p>
      </div>

      {/* Emergency Hotline Buttons */}
      <div className="space-y-3">
        <h3 className="font-heading text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
          <PhoneCall className="w-4 h-4 text-red-400" />
          <span>One-Tap Emergency Hotlines</span>
        </h3>

        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
          {emergencyHelplines.map((item, idx) => {
            const Icon = item.icon;
            return (
              <a
                key={idx}
                href={`tel:${item.number}`}
                className={`p-4 rounded-2xl ${item.color} text-white space-y-2 shadow-lg hover:scale-[1.03] transition-transform block`}
              >
                <div className="flex items-center justify-between">
                  <Icon className="w-5 h-5" />
                  <span className="font-heading font-extrabold text-xl">{item.number}</span>
                </div>
                <p className="text-xs font-semibold leading-tight">{item.name}</p>
              </a>
            );
          })}
        </div>
      </div>

      {/* Nearby Emergency Services List */}
      <div className="glass-card p-6 space-y-4 border-slate-700/50">
        <h3 className="font-heading text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
          <Building2 className="w-4 h-4 text-sky-400" />
          <span>Nearby Hospitals, Police Stations & Shelters</span>
        </h3>

        {loading ? (
          <div className="text-center py-6 text-xs text-slate-400">Locating nearby emergency infrastructure...</div>
        ) : (
          <div className="grid md:grid-cols-2 gap-4">
            {services.map((s) => (
              <div key={s.id} className="p-4 glass-card border-slate-700/60 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-sm text-white">{s.name}</span>
                  <span className="px-2 py-0.5 text-[10px] font-bold bg-sky-500/20 text-sky-300 border border-sky-400/30 rounded">
                    {s.category}
                  </span>
                </div>

                <p className="text-xs text-slate-400 flex items-center gap-1">
                  <MapPin className="w-3.5 h-3.5 text-sky-400" />
                  {s.address} ({s.distance})
                </p>

                <div className="pt-2 flex items-center gap-2">
                  <a
                    href={`tel:${s.phone}`}
                    className="flex-1 py-1.5 rounded-xl bg-sky-600 text-white text-xs font-semibold text-center flex items-center justify-center gap-1"
                  >
                    <PhoneCall className="w-3.5 h-3.5" />
                    <span>Call {s.phone}</span>
                  </a>

                  <a
                    href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(s.name + ' ' + city)}`}
                    target="_blank"
                    rel="noreferrer"
                    className="py-1.5 px-3 rounded-xl glass-card text-xs font-semibold text-sky-300 flex items-center gap-1 hover:bg-sky-500/20"
                  >
                    <Navigation className="w-3.5 h-3.5" />
                    <span>Directions</span>
                  </a>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
