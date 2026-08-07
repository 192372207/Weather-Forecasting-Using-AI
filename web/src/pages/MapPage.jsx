import React, { useState, useEffect } from 'react';
import { useWeather } from '../context/WeatherContext';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import { MapPin, Layers, CloudRain, Wind, Thermometer, Sun } from 'lucide-react';
import L from 'leaflet';

// Fix default leaflet icon issue
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Component to dynamically re-center map when city changes
function RecenterMap({ lat, lon }) {
  const map = useMap();
  useEffect(() => {
    map.setView([lat, lon], 10);
  }, [lat, lon, map]);
  return null;
}

export const MapPage = () => {
  const { weather } = useWeather();
  const [activeLayer, setActiveLayer] = useState('temp'); // 'temp', 'rain', 'clouds', 'wind'

  const position = [weather?.lat || 51.5074, weather?.lon || -0.1278];

  return (
    <div className="space-y-4">
      {/* Top Controller Bar */}
      <div className="glass-card p-4 border-sky-400/30 flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="font-heading font-bold text-lg text-white flex items-center gap-2">
            <MapPin className="w-5 h-5 text-sky-400" />
            <span>Interactive Weather Radar - {weather?.city}</span>
          </h2>
          <p className="text-xs text-slate-400">Real-time satellite & atmospheric layers</p>
        </div>

        {/* Layer Selection Buttons */}
        <div className="flex items-center gap-2 glass-card p-1 rounded-xl">
          <button
            onClick={() => setActiveLayer('temp')}
            className={`px-3 py-1.5 text-xs font-semibold rounded-lg flex items-center gap-1.5 transition-all ${
              activeLayer === 'temp' ? 'bg-sky-500 text-white shadow-md' : 'text-slate-400 hover:text-white'
            }`}
          >
            <Thermometer className="w-3.5 h-3.5" />
            <span>Temperature</span>
          </button>
          <button
            onClick={() => setActiveLayer('rain')}
            className={`px-3 py-1.5 text-xs font-semibold rounded-lg flex items-center gap-1.5 transition-all ${
              activeLayer === 'rain' ? 'bg-sky-500 text-white shadow-md' : 'text-slate-400 hover:text-white'
            }`}
          >
            <CloudRain className="w-3.5 h-3.5" />
            <span>Rain Radar</span>
          </button>
          <button
            onClick={() => setActiveLayer('wind')}
            className={`px-3 py-1.5 text-xs font-semibold rounded-lg flex items-center gap-1.5 transition-all ${
              activeLayer === 'wind' ? 'bg-sky-500 text-white shadow-md' : 'text-slate-400 hover:text-white'
            }`}
          >
            <Wind className="w-3.5 h-3.5" />
            <span>Wind Speed</span>
          </button>
        </div>
      </div>

      {/* Map View */}
      <div className="glass-card p-2 border-sky-400/30 overflow-hidden h-[550px] relative rounded-2xl">
        <MapContainer
          center={position}
          zoom={10}
          scrollWheelZoom={true}
          style={{ height: '100%', width: '100%', borderRadius: '1rem' }}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <RecenterMap lat={position[0]} lon={position[1]} />
          <Marker position={position}>
            <Popup>
              <div className="text-slate-900 p-1">
                <p className="font-bold text-sm">{weather?.city}</p>
                <p className="text-xs">{weather?.temp}°C • {weather?.condition}</p>
              </div>
            </Popup>
          </Marker>
        </MapContainer>

        {/* Overlay Legend Badge */}
        <div className="absolute bottom-6 right-6 glass-card p-3 shadow-2xl z-[1000] border-sky-400/40 space-y-1">
          <p className="text-[11px] font-bold text-white uppercase tracking-wider">Active Radar Overlay</p>
          <div className="flex items-center gap-2 text-xs text-sky-300">
            <span className="w-2.5 h-2.5 rounded-full bg-sky-400 animate-ping"></span>
            <span>{activeLayer.toUpperCase()} Layer Active</span>
          </div>
        </div>
      </div>
    </div>
  );
};
