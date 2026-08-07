import React, { useState, useEffect } from 'react';
import { useWeather } from '../context/WeatherContext';
import { safetyApi } from '../services/api';
import { RiskMeterCard } from '../components/RiskMeterCard';
import { WeatherHealthCard } from '../components/WeatherHealthCard';
import {
  Sun,
  CloudSun,
  CloudRain,
  Wind,
  Droplets,
  Gauge,
  Sparkles,
  ChevronRight,
  ShieldAlert,
  Calendar,
  HeartPulse,
  PhoneCall
} from 'lucide-react';
import { Link } from 'react-router-dom';

export const DashboardPage = () => {
  const { city, weather, hourly, daily7, daily15, loading, convertTemp, unit } = useWeather();
  const [activeTab, setActiveTab] = useState('7day');
  const [safetyData, setSafetyData] = useState(null);

  useEffect(() => {
    if (city) {
      safetyApi.getAssessment(city).then(setSafetyData);
    }
  }, [city]);

  if (loading || !weather) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[500px] space-y-4">
        <div className="w-12 h-12 border-4 border-sky-400 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-sm font-medium text-slate-300">Fetching live weather telemetry for {city}...</p>
      </div>
    );
  }

  const forecastDays = activeTab === '7day' ? daily7 : daily15;

  return (
    <div className="space-y-6">
      {/* Current Weather Hero Card */}
      <div className="relative overflow-hidden glass-card p-6 md:p-8 border-sky-400/30">
        <div className="ambient-glow bg-sky-500/15 w-80 h-80 -top-10 -right-10"></div>
        
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 relative z-10">
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <h2 className="font-heading font-extrabold text-3xl md:text-4xl text-white tracking-tight">
                {weather.city}
              </h2>
              <span className="px-2.5 py-0.5 text-xs font-semibold bg-sky-500/20 text-sky-300 border border-sky-400/30 rounded-lg">
                {weather.country}
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Coordinates: {weather.lat}° N, {weather.lon}° E • Live Open-Meteo Feed
            </p>
          </div>

          <div className="flex items-center gap-6">
            <div className="p-3 glass-card rounded-2xl bg-sky-500/10 border-sky-400/40 animate-pulse-slow">
              {weather.condition.toLowerCase().includes('rain') ? (
                <CloudRain className="w-16 h-16 text-sky-400" />
              ) : (
                <CloudSun className="w-16 h-16 text-amber-400" />
              )}
            </div>

            <div className="space-y-1">
              <div className="flex items-baseline gap-2">
                <span className="font-heading text-5xl md:text-6xl font-extrabold text-white">
                  {convertTemp(weather.temp)}°
                </span>
                <span className="text-lg text-sky-400 font-semibold">{unit}</span>
              </div>
              <p className="text-sm font-semibold text-sky-300">{weather.condition}</p>
              <p className="text-xs text-slate-400">
                Feels like {convertTemp(weather.feels_like)}° • H: {convertTemp(weather.high)}° L: {convertTemp(weather.low)}°
              </p>
            </div>
          </div>
        </div>

        {/* Daily Safety Summary Card Header */}
        <div className="mt-6 pt-4 border-t border-slate-700/50 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <Sparkles className="w-5 h-5 text-sky-400 flex-shrink-0" />
            <p className="text-xs text-slate-300">
              <span className="font-semibold text-sky-300">Daily Safety Summary:</span> {safetyData?.daily_summary || `Temp ${weather.temp}°C, Rain chance ${weather.rain_probability}%.`}
            </p>
          </div>

          <div className="flex items-center gap-2">
            <Link
              to="/emergency"
              className="px-3 py-1.5 rounded-xl bg-red-600/80 hover:bg-red-600 text-white font-semibold text-xs flex items-center gap-1 shadow-md shadow-red-500/20"
            >
              <PhoneCall className="w-3.5 h-3.5" />
              <span>Emergency</span>
            </Link>
            <Link
              to="/ai-chat"
              className="px-3 py-1.5 glass-card text-xs font-semibold text-sky-400 hover:text-sky-300 flex items-center gap-1"
            >
              <span>Ask AI</span>
              <ChevronRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </div>

      {/* AI Weather Risk Meter Gauge */}
      {safetyData && (
        <RiskMeterCard
          riskLevel={safetyData.risk_level}
          riskScore={safetyData.risk_score}
          riskTitle={safetyData.risk_title}
        />
      )}

      {/* Weather Health & Precautions Card */}
      {safetyData && (
        <WeatherHealthCard
          weather={weather}
          precautions={safetyData.precautions}
        />
      )}

      {/* 24-Hour Hourly Forecast Carousel */}
      <div className="glass-card p-5 space-y-3">
        <h3 className="font-heading text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
          <Sun className="w-4 h-4 text-amber-400" />
          <span>24-Hour Forecast</span>
        </h3>

        <div className="flex items-center gap-3 overflow-x-auto pb-2">
          {hourly.map((item, idx) => (
            <div
              key={idx}
              className="flex-shrink-0 w-20 glass-card p-3 text-center space-y-2 glass-card-hover border-slate-700/50"
            >
              <p className="text-xs text-slate-400 font-medium">{item.time}</p>
              <CloudSun className="w-6 h-6 mx-auto text-sky-300" />
              <p className="text-sm font-bold text-white">{convertTemp(item.temp)}°</p>
              <p className="text-[10px] text-sky-400 font-semibold">{item.pop}% Rain</p>
            </div>
          ))}
        </div>
      </div>

      {/* Weather Metrics Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {/* Wind */}
        <div className="glass-card p-4 space-y-2">
          <div className="flex items-center gap-2 text-slate-400 text-xs font-semibold">
            <Wind className="w-4 h-4 text-sky-400" />
            <span>WIND & GUSTS</span>
          </div>
          <p className="text-2xl font-bold text-white font-heading">{weather.wind_speed} <span className="text-xs font-normal text-slate-400">km/h</span></p>
          <p className="text-[11px] text-slate-400">Direction: {weather.wind_direction}° S/SW</p>
        </div>

        {/* Humidity */}
        <div className="glass-card p-4 space-y-2">
          <div className="flex items-center gap-2 text-slate-400 text-xs font-semibold">
            <Droplets className="w-4 h-4 text-sky-400" />
            <span>HUMIDITY</span>
          </div>
          <p className="text-2xl font-bold text-white font-heading">{weather.humidity}%</p>
          <p className="text-[11px] text-slate-400">Dew point is 14°C right now</p>
        </div>

        {/* Pressure */}
        <div className="glass-card p-4 space-y-2">
          <div className="flex items-center gap-2 text-slate-400 text-xs font-semibold">
            <Gauge className="w-4 h-4 text-indigo-400" />
            <span>PRESSURE</span>
          </div>
          <p className="text-2xl font-bold text-white font-heading">{weather.pressure} <span className="text-xs font-normal text-slate-400">hPa</span></p>
          <p className="text-[11px] text-emerald-400">Stable atmospheric pressure</p>
        </div>

        {/* AQI */}
        <div className="glass-card p-4 space-y-2">
          <div className="flex items-center gap-2 text-slate-400 text-xs font-semibold">
            <Sun className="w-4 h-4 text-emerald-400" />
            <span>AIR QUALITY (AQI)</span>
          </div>
          <p className="text-2xl font-bold text-emerald-400 font-heading">{weather.aqi}</p>
          <p className="text-[11px] text-slate-400">{weather.aqi_description}</p>
        </div>
      </div>

      {/* Extended Daily Forecast */}
      <div className="glass-card p-5 space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="font-heading text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
            <Calendar className="w-4 h-4 text-sky-400" />
            <span>Extended Forecast</span>
          </h3>
          
          <div className="flex items-center glass-card p-1 rounded-xl">
            <button
              onClick={() => setActiveTab('7day')}
              className={`px-3 py-1 text-xs font-semibold rounded-lg transition-all ${
                activeTab === '7day' ? 'bg-sky-500 text-white shadow-md' : 'text-slate-400 hover:text-white'
              }`}
            >
              7 Days
            </button>
            <button
              onClick={() => setActiveTab('15day')}
              className={`px-3 py-1 text-xs font-semibold rounded-lg transition-all ${
                activeTab === '15day' ? 'bg-sky-500 text-white shadow-md' : 'text-slate-400 hover:text-white'
              }`}
            >
              15 Days
            </button>
          </div>
        </div>

        <div className="divide-y divide-slate-700/50">
          {forecastDays.map((day, idx) => (
            <div key={idx} className="py-3 flex items-center justify-between text-xs hover:bg-white/5 px-2 rounded-xl transition-colors">
              <span className="w-20 font-semibold text-slate-200">{day.day} ({day.date.slice(5)})</span>
              <div className="flex items-center gap-2 w-32">
                <CloudSun className="w-4 h-4 text-sky-400" />
                <span className="text-slate-300">{day.condition}</span>
              </div>
              <span className="text-sky-400 font-semibold w-16">{day.rain_prob}% Rain</span>
              <div className="flex items-center gap-3 font-semibold">
                <span className="text-white">{convertTemp(day.high)}°</span>
                <div className="w-16 h-1.5 rounded-full bg-gradient-to-r from-sky-500 to-amber-400"></div>
                <span className="text-slate-400">{convertTemp(day.low)}°</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
