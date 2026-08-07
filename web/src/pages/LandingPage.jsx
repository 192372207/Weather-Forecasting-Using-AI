import React from 'react';
import { Link } from 'react-router-dom';
import { Sparkles, Sun, CloudRain, ShieldCheck, Zap, ArrowRight, Activity, Globe, Compass, CheckCircle2 } from 'lucide-react';

export const LandingPage = () => {
  return (
    <div className="space-y-16 py-4">
      {/* Hero Section */}
      <section className="relative overflow-hidden glass-card p-8 md:p-14 text-center space-y-6">
        <div className="ambient-glow bg-sky-500/20 w-96 h-96 -top-20 -left-20"></div>
        <div className="ambient-glow bg-indigo-500/20 w-96 h-96 -bottom-20 -right-20"></div>

        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-sky-500/10 border border-sky-400/30 text-sky-300 text-xs font-semibold">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Next-Generation AI Weather Intelligence Engine</span>
        </div>

        <h1 className="font-heading font-extrabold text-4xl sm:text-5xl md:text-6xl tracking-tight text-white max-w-4xl mx-auto leading-tight">
          Hyper-Local Weather Insights Driven by <span className="text-transparent bg-clip-text bg-gradient-to-r from-sky-400 via-indigo-300 to-cyan-300">Groq AI</span>
        </h1>

        <p className="text-slate-300 text-base md:text-lg max-w-2xl mx-auto font-normal leading-relaxed">
          Experience ultra-accurate 15-day weather forecasts, real-time AQI tracking, interactive radar maps, and personal AI weather advisories—designed with Apple Weather elegance.
        </p>

        <div className="flex flex-wrap items-center justify-center gap-4 pt-4">
          <Link
            to="/dashboard"
            className="inline-flex items-center gap-2 px-6 py-3.5 rounded-2xl bg-gradient-to-r from-sky-500 to-indigo-600 text-white font-semibold text-sm shadow-xl shadow-sky-500/25 hover:scale-105 transition-transform"
          >
            <span>Launch Live Weather Hub</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
          <Link
            to="/ai-chat"
            className="inline-flex items-center gap-2 px-6 py-3.5 rounded-2xl glass-card text-sky-300 font-semibold text-sm border-sky-400/40 hover:bg-white/10 transition-colors"
          >
            <Sparkles className="w-4 h-4 text-sky-400" />
            <span>Try AI Weather Assistant</span>
          </Link>
        </div>

        {/* Live Weather Preview Widget */}
        <div className="pt-10 max-w-3xl mx-auto">
          <div className="glass-card p-6 border-sky-400/30 grid grid-cols-2 md:grid-cols-4 gap-4 text-left">
            <div className="space-y-1">
              <p className="text-xs text-slate-400">Current Temp</p>
              <p className="text-2xl font-bold text-white font-heading">24.5°C</p>
              <p className="text-[11px] text-sky-400">Feels like 25°C</p>
            </div>
            <div className="space-y-1">
              <p className="text-xs text-slate-400">Air Quality</p>
              <p className="text-2xl font-bold text-emerald-400 font-heading">32 AQI</p>
              <p className="text-[11px] text-emerald-400/80">Optimal Air Quality</p>
            </div>
            <div className="space-y-1">
              <p className="text-xs text-slate-400">Precipitation</p>
              <p className="text-2xl font-bold text-white font-heading">15%</p>
              <p className="text-[11px] text-slate-400">Low rain chance</p>
            </div>
            <div className="space-y-1">
              <p className="text-xs text-slate-400">Groq AI Advice</p>
              <p className="text-xs text-sky-300 font-medium line-clamp-2">"Great day for outdoor sports & driving!"</p>
            </div>
          </div>
        </div>
      </section>

      {/* Feature Highlights Grid */}
      <section className="space-y-8">
        <div className="text-center space-y-2">
          <h2 className="font-heading text-2xl md:text-3xl font-bold text-white">
            Built for Modern Weather Precision
          </h2>
          <p className="text-slate-400 text-sm">Comprehensive weather intelligence tailored for travel, agriculture, and daily decisions.</p>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          <div className="glass-card p-6 space-y-3 glass-card-hover border-sky-500/20">
            <div className="w-10 h-10 rounded-xl bg-sky-500/20 flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-sky-400" />
            </div>
            <h3 className="font-heading font-semibold text-lg text-white">Groq AI Weather Companion</h3>
            <p className="text-slate-400 text-xs leading-relaxed">
              Ask natural questions like "Should I carry an umbrella?" or "Is today good for farming?" to get instant markdown insights.
            </p>
          </div>

          <div className="glass-card p-6 space-y-3 glass-card-hover border-sky-500/20">
            <div className="w-10 h-10 rounded-xl bg-indigo-500/20 flex items-center justify-center">
              <Globe className="w-5 h-5 text-indigo-400" />
            </div>
            <h3 className="font-heading font-semibold text-lg text-white">Interactive Leaflet Radar Maps</h3>
            <p className="text-slate-400 text-xs leading-relaxed">
              Visualize real-time precipitation, cloud velocity, temperature heatmaps, and wind direction over global cities.
            </p>
          </div>

          <div className="glass-card p-6 space-y-3 glass-card-hover border-sky-500/20">
            <div className="w-10 h-10 rounded-xl bg-cyan-500/20 flex items-center justify-center">
              <Activity className="w-5 h-5 text-cyan-400" />
            </div>
            <h3 className="font-heading font-semibold text-lg text-white">Crowd-Sourced Reports</h3>
            <p className="text-slate-400 text-xs leading-relaxed">
              Community members upload live ground reports with photos of heavy rain, floods, or severe storms with instant voting.
            </p>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="glass-card p-8 space-y-6">
        <h2 className="font-heading text-2xl font-bold text-center text-white">Trusted by Weather Enthusiasts</h2>
        <div className="grid md:grid-cols-2 gap-6">
          <div className="glass-card p-4 space-y-2 border-slate-700/50">
            <p className="text-xs text-slate-300 italic">"SkySense AI's travel advice saved our weekend trip to Paris. The Groq AI suggestions are spot on!"</p>
            <div className="flex items-center gap-3 pt-2">
              <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=SarahP" alt="Sarah" className="w-8 h-8 rounded-full" />
              <div>
                <p className="text-xs font-semibold text-white">Sarah Jenkins</p>
                <p className="text-[10px] text-slate-400">Travel Blogger</p>
              </div>
            </div>
          </div>

          <div className="glass-card p-4 space-y-2 border-slate-700/50">
            <p className="text-xs text-slate-300 italic">"The UI is gorgeous—feels just like Apple Weather with Tesla dashboard smoothness. Highly recommended!"</p>
            <div className="flex items-center gap-3 pt-2">
              <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=DavidK" alt="David" className="w-8 h-8 rounded-full" />
              <div>
                <p className="text-xs font-semibold text-white">David K.</p>
                <p className="text-[10px] text-slate-400">Agronomist & Pilot</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};
