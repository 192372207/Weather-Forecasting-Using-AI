import React, { useState, useEffect } from 'react';
import { useWeather } from '../context/WeatherContext';
import { Navigation, MapPin, Sparkles, Check, X } from 'lucide-react';

export const LocationPermissionModal = () => {
  const { detectGPSLocation, isGpsActive } = useWeather();
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    const hasPrompted = localStorage.getItem('skysense_loc_prompted');
    if (!hasPrompted) {
      setShowModal(true);
    }
  }, []);

  const handleAllow = () => {
    localStorage.setItem('skysense_loc_prompted', 'true');
    setShowModal(false);
    detectGPSLocation();
  };

  const handleDismiss = () => {
    localStorage.setItem('skysense_loc_prompted', 'true');
    setShowModal(false);
  };

  if (!showModal) return null;

  return (
    <div className="fixed inset-0 z-[100] bg-black/75 backdrop-blur-md flex items-center justify-center p-4">
      <div className="glass-card p-6 max-w-sm w-full border-sky-400/50 space-y-5 text-center shadow-2xl animate-float">
        {/* Icon Header */}
        <div className="w-14 h-14 rounded-2xl bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center mx-auto shadow-lg shadow-sky-500/40">
          <Navigation className="w-7 h-7 text-white animate-pulse" />
        </div>

        <div className="space-y-2">
          <h3 className="font-heading font-extrabold text-xl text-white">Enable Precise Location</h3>
          <p className="text-xs text-slate-300 leading-relaxed">
            Allow <span className="text-sky-300 font-semibold">SkySense AI</span> to access your device location to deliver real-time weather forecasts, AQI tracking, and severe weather warnings for your exact position.
          </p>
        </div>

        <div className="flex flex-col gap-2 pt-1">
          <button
            onClick={handleAllow}
            className="w-full py-3 rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 text-white font-semibold text-xs shadow-lg shadow-sky-500/30 flex items-center justify-center gap-2 hover:scale-[1.02] transition-transform"
          >
            <Check className="w-4 h-4" />
            <span>Allow Location Access</span>
          </button>
          <button
            onClick={handleDismiss}
            className="w-full py-2.5 rounded-xl glass-card text-xs text-slate-400 hover:text-white transition-colors"
          >
            Maybe Later (Use Default City)
          </button>
        </div>
      </div>
    </div>
  );
};
