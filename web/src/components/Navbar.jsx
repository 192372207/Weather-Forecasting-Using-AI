import React, { useState } from 'react';
import { useWeather } from '../context/WeatherContext';
import { useAuth } from '../context/AuthContext';
import { Search, Sun, Moon, Bell, Sparkles, MapPin, Navigation, LogIn, UserPlus, LogOut } from 'lucide-react';
import { Link } from 'react-router-dom';

export const Navbar = () => {
  const { city, setCity, unit, setUnit, theme, toggleTheme, weather, detectGPSLocation, isGpsActive } = useWeather();
  const { user, logout } = useAuth();
  const [searchInput, setSearchInput] = useState('');
  const [showSearchDropdown, setShowSearchDropdown] = useState(false);

  const popularCities = ['London', 'New York', 'Tokyo', 'Paris', 'Sydney', 'Mumbai', 'Delhi'];

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (searchInput.trim()) {
      setCity(searchInput.trim());
      setSearchInput('');
      setShowSearchDropdown(false);
    }
  };

  const handleSelectCity = (c) => {
    setCity(c);
    setSearchInput('');
    setShowSearchDropdown(false);
  };

  return (
    <header className="sticky top-0 z-50 glass-card rounded-none border-x-0 border-t-0 px-3 sm:px-6 py-2.5 mb-4 max-w-full overflow-hidden">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-3">
        {/* Top Row: Logo & Right Controls */}
        <div className="flex items-center justify-between w-full md:w-auto gap-2">
          {/* Brand Logo */}
          <Link to="/" className="flex items-center gap-2 group flex-shrink-0">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-sky-500/30 group-hover:scale-105 transition-transform">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="font-heading font-bold text-base sm:text-lg tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-sky-400 via-indigo-200 to-white">
                SkySense <span className="text-sky-400">AI</span>
              </h1>
              <p className="text-[9px] text-sky-400/80 font-medium tracking-wider uppercase hidden sm:block">Weather Intelligence</p>
            </div>
          </Link>

          {/* Quick Actions Group for Mobile */}
          <div className="flex items-center gap-2">
            {/* °C / °F Toggle */}
            <div className="flex items-center glass-card p-0.5 rounded-lg text-xs">
              <button
                onClick={() => setUnit('C')}
                className={`px-2 py-0.5 text-[11px] font-semibold rounded-md transition-all ${
                  unit === 'C' ? 'bg-sky-500 text-white shadow' : 'text-slate-400 hover:text-white'
                }`}
              >
                °C
              </button>
              <button
                onClick={() => setUnit('F')}
                className={`px-2 py-0.5 text-[11px] font-semibold rounded-md transition-all ${
                  unit === 'F' ? 'bg-sky-500 text-white shadow' : 'text-slate-400 hover:text-white'
                }`}
              >
                °F
              </button>
            </div>

            {/* Theme Toggle */}
            <button
              onClick={toggleTheme}
              className="p-1.5 glass-card rounded-lg text-slate-300 hover:text-white transition-colors"
              title="Toggle Light/Dark Theme"
            >
              {theme === 'dark' ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-indigo-600" />}
            </button>

            {/* Notification Bell */}
            <Link
              to="/alerts"
              className="relative p-1.5 glass-card rounded-lg text-slate-300 hover:text-white transition-colors"
              title="Weather Warnings"
            >
              <Bell className="w-4 h-4 text-sky-400" />
              <span className="absolute top-0.5 right-0.5 w-1.5 h-1.5 rounded-full bg-amber-400 animate-ping"></span>
              <span className="absolute top-0.5 right-0.5 w-1.5 h-1.5 rounded-full bg-amber-400"></span>
            </Link>

            {/* User Profile / Logout */}
            {user ? (
              <div className="flex items-center gap-1.5 pl-1 border-l border-slate-700/50">
                <img
                  src={user.profile_pic}
                  alt={user.name}
                  className="w-7 h-7 rounded-full border border-sky-400/40 p-0.5 object-cover"
                />
                <button
                  onClick={logout}
                  className="p-1.5 glass-card rounded-lg text-slate-400 hover:text-red-400 transition-colors"
                  title="Logout"
                >
                  <LogOut className="w-3.5 h-3.5" />
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-1">
                <Link
                  to="/login"
                  className="px-2.5 py-1 glass-card rounded-lg text-xs font-semibold text-slate-200"
                >
                  Login
                </Link>
              </div>
            )}
          </div>
        </div>

        {/* Full-Width Responsive Search Bar for Mobile & Desktop */}
        <div className="relative w-full md:flex-1 md:max-w-md">
          <form onSubmit={handleSearchSubmit} className="flex items-center gap-1.5">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-400" />
              <input
                type="text"
                value={searchInput}
                onChange={(e) => {
                  setSearchInput(e.target.value);
                  setShowSearchDropdown(true);
                }}
                onFocus={() => setShowSearchDropdown(true)}
                placeholder="Search city (e.g. London, Tokyo)..."
                className="w-full glass-input pl-9 pr-3 py-1.5 text-xs text-slate-100 placeholder-slate-400 focus:outline-none"
              />
            </div>

            {/* GPS Auto-Detect Button */}
            <button
              type="button"
              onClick={detectGPSLocation}
              className={`p-2 glass-card rounded-xl flex items-center justify-center transition-all ${
                isGpsActive
                  ? 'bg-sky-500/30 text-sky-300 border-sky-400/60 shadow-lg shadow-sky-500/20'
                  : 'text-slate-300 hover:text-white hover:border-sky-400/50'
              }`}
              title="Use My Current GPS Location"
            >
              <Navigation className={`w-3.5 h-3.5 ${isGpsActive ? 'animate-pulse text-sky-400' : ''}`} />
            </button>
          </form>

          {/* Quick Suggestions Dropdown */}
          {showSearchDropdown && (
            <div className="absolute top-full left-0 right-0 mt-2 glass-card p-2 shadow-2xl z-50">
              <p className="text-[10px] font-semibold text-slate-400 px-2 py-1 uppercase tracking-wider">Popular Cities</p>
              <div className="grid grid-cols-2 gap-1 mt-1">
                {popularCities.map((c) => (
                  <button
                    key={c}
                    onClick={() => handleSelectCity(c)}
                    className="flex items-center gap-1.5 px-2.5 py-1.5 text-xs text-left text-slate-300 hover:text-white hover:bg-sky-500/20 rounded-lg transition-colors"
                  >
                    <MapPin className="w-3 h-3 text-sky-400" />
                    {c}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
