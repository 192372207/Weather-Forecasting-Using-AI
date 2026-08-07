import React from 'react';
import { useWeather } from '../context/WeatherContext';
import { BarChart3, TrendingUp, Droplets, Wind, Gauge, Sun } from 'lucide-react';

export const AnalyticsPage = () => {
  const { city, daily7, convertTemp } = useWeather();

  const maxTemp = Math.max(...daily7.map(d => d.high), 30);

  return (
    <div className="space-y-6">
      <div className="glass-card p-6 border-sky-400/30 flex items-center justify-between">
        <div>
          <h2 className="font-heading font-extrabold text-2xl text-white">Weather Analytics & Trends</h2>
          <p className="text-xs text-slate-400">7-Day telemetry decomposition for {city}</p>
        </div>
        <div className="p-3 glass-card bg-sky-500/10 border-sky-400/30 rounded-xl">
          <BarChart3 className="w-6 h-6 text-sky-400" />
        </div>
      </div>

      {/* Temperature Trend Chart */}
      <div className="glass-card p-6 space-y-4">
        <h3 className="font-heading text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
          <TrendingUp className="w-4 h-4 text-sky-400" />
          <span>Temperature High / Low Curve (°C)</span>
        </h3>

        <div className="h-48 flex items-end justify-between gap-2 pt-6 px-4 border-b border-slate-700/50">
          {daily7.map((day, idx) => {
            const highHeight = (day.high / maxTemp) * 100;
            const lowHeight = (day.low / maxTemp) * 100;
            return (
              <div key={idx} className="flex-1 flex flex-col items-center gap-2 group">
                <div className="w-full flex items-end justify-center gap-1.5 h-36">
                  {/* High Bar */}
                  <div
                    style={{ height: `${highHeight}%` }}
                    className="w-4 bg-gradient-to-t from-sky-500 to-indigo-400 rounded-t-md relative group-hover:bg-sky-400 transition-colors"
                  >
                    <span className="absolute -top-5 left-1/2 -translate-x-1/2 text-[10px] font-bold text-white">
                      {convertTemp(day.high)}°
                    </span>
                  </div>
                  {/* Low Bar */}
                  <div
                    style={{ height: `${lowHeight}%` }}
                    className="w-4 bg-slate-700/70 rounded-t-md relative"
                  >
                    <span className="absolute -top-5 left-1/2 -translate-x-1/2 text-[10px] font-bold text-slate-400">
                      {convertTemp(day.low)}°
                    </span>
                  </div>
                </div>
                <span className="text-xs font-semibold text-slate-300">{day.day}</span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Grid of Humidity & Rain Graph */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Precipitation Probabilities */}
        <div className="glass-card p-6 space-y-4">
          <h3 className="font-heading text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
            <Droplets className="w-4 h-4 text-sky-400" />
            <span>Precipitation Probability (%)</span>
          </h3>

          <div className="space-y-3">
            {daily7.map((day, idx) => (
              <div key={idx} className="space-y-1">
                <div className="flex justify-between text-xs font-medium">
                  <span className="text-slate-300">{day.day}</span>
                  <span className="text-sky-400 font-bold">{day.rain_prob}%</span>
                </div>
                <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                  <div
                    style={{ width: `${day.rain_prob}%` }}
                    className="h-full bg-gradient-to-r from-sky-500 to-cyan-400 rounded-full"
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Wind Speed Analytics */}
        <div className="glass-card p-6 space-y-4">
          <h3 className="font-heading text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
            <Wind className="w-4 h-4 text-indigo-400" />
            <span>Wind Velocity Trends (km/h)</span>
          </h3>

          <div className="space-y-3">
            {daily7.map((day, idx) => (
              <div key={idx} className="space-y-1">
                <div className="flex justify-between text-xs font-medium">
                  <span className="text-slate-300">{day.day}</span>
                  <span className="text-indigo-300 font-bold">{day.wind_speed} km/h</span>
                </div>
                <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                  <div
                    style={{ width: `${(day.wind_speed / 40) * 100}%` }}
                    className="h-full bg-gradient-to-r from-indigo-500 to-purple-400 rounded-full"
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
