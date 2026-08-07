import React, { useState, useEffect } from 'react';
import { weatherApi } from '../services/api';
import { GitCompare, Plus, Trash2, CloudSun, Wind, Droplets, Gauge } from 'lucide-react';

export const ComparisonPage = () => {
  const [city1, setCity1] = useState('London');
  const [city2, setCity2] = useState('Tokyo');
  const [data1, setData1] = useState(null);
  const [data2, setData2] = useState(null);

  useEffect(() => {
    weatherApi.getCurrent(city1).then(setData1);
  }, [city1]);

  useEffect(() => {
    weatherApi.getCurrent(city2).then(setData2);
  }, [city2]);

  return (
    <div className="space-y-6">
      <div className="glass-card p-6 border-sky-400/30">
        <h2 className="font-heading font-extrabold text-2xl text-white flex items-center gap-2">
          <GitCompare className="w-6 h-6 text-sky-400" />
          <span>Multi-City Weather Comparison</span>
        </h2>
        <p className="text-xs text-slate-400">Side-by-side weather telemetry matrix</p>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {/* City 1 */}
        <div className="glass-card p-6 space-y-4 border-sky-400/20">
          <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block">City 1</label>
          <select
            value={city1}
            onChange={(e) => setCity1(e.target.value)}
            className="w-full glass-input px-3 py-2 text-sm text-white"
          >
            <option value="London" className="bg-slate-900">London</option>
            <option value="New York" className="bg-slate-900">New York</option>
            <option value="Tokyo" className="bg-slate-900">Tokyo</option>
            <option value="Paris" className="bg-slate-900">Paris</option>
            <option value="Sydney" className="bg-slate-900">Sydney</option>
          </select>

          {data1 && (
            <div className="space-y-4 pt-2">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-3xl font-extrabold text-white font-heading">{data1.temp}°C</p>
                  <p className="text-xs text-sky-300 font-semibold">{data1.condition}</p>
                </div>
                <CloudSun className="w-12 h-12 text-amber-400" />
              </div>

              <div className="space-y-2 text-xs divide-y divide-slate-700/50">
                <div className="py-2 flex justify-between">
                  <span className="text-slate-400">Humidity</span>
                  <span className="font-bold text-white">{data1.humidity}%</span>
                </div>
                <div className="py-2 flex justify-between">
                  <span className="text-slate-400">Wind Speed</span>
                  <span className="font-bold text-white">{data1.wind_speed} km/h</span>
                </div>
                <div className="py-2 flex justify-between">
                  <span className="text-slate-400">Pressure</span>
                  <span className="font-bold text-white">{data1.pressure} hPa</span>
                </div>
                <div className="py-2 flex justify-between">
                  <span className="text-slate-400">Air Quality</span>
                  <span className="font-bold text-emerald-400">{data1.aqi} AQI</span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* City 2 */}
        <div className="glass-card p-6 space-y-4 border-indigo-400/20">
          <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block">City 2</label>
          <select
            value={city2}
            onChange={(e) => setCity2(e.target.value)}
            className="w-full glass-input px-3 py-2 text-sm text-white"
          >
            <option value="Tokyo" className="bg-slate-900">Tokyo</option>
            <option value="London" className="bg-slate-900">London</option>
            <option value="New York" className="bg-slate-900">New York</option>
            <option value="Paris" className="bg-slate-900">Paris</option>
            <option value="Sydney" className="bg-slate-900">Sydney</option>
          </select>

          {data2 && (
            <div className="space-y-4 pt-2">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-3xl font-extrabold text-white font-heading">{data2.temp}°C</p>
                  <p className="text-xs text-sky-300 font-semibold">{data2.condition}</p>
                </div>
                <CloudSun className="w-12 h-12 text-sky-400" />
              </div>

              <div className="space-y-2 text-xs divide-y divide-slate-700/50">
                <div className="py-2 flex justify-between">
                  <span className="text-slate-400">Humidity</span>
                  <span className="font-bold text-white">{data2.humidity}%</span>
                </div>
                <div className="py-2 flex justify-between">
                  <span className="text-slate-400">Wind Speed</span>
                  <span className="font-bold text-white">{data2.wind_speed} km/h</span>
                </div>
                <div className="py-2 flex justify-between">
                  <span className="text-slate-400">Pressure</span>
                  <span className="font-bold text-white">{data2.pressure} hPa</span>
                </div>
                <div className="py-2 flex justify-between">
                  <span className="text-slate-400">Air Quality</span>
                  <span className="font-bold text-emerald-400">{data2.aqi} AQI</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
