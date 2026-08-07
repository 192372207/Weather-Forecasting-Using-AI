import React, { useState, useEffect } from 'react';
import { communityApi } from '../services/api';
import { Users, ThumbsUp, MessageSquare, Plus, Image as ImageIcon, MapPin, AlertTriangle } from 'lucide-react';

export const CommunityPage = () => {
  const [reports, setReports] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [eventType, setEventType] = useState('Heavy Rain');
  const [city, setCity] = useState('Paris');
  const [description, setDescription] = useState('');

  useEffect(() => {
    loadReports();
  }, []);

  const loadReports = async () => {
    const data = await communityApi.getReports();
    setReports(data);
  };

  const handleLike = async (id) => {
    try {
      await communityApi.likeReport(id);
      setReports(reports.map(r => r.id === id ? { ...r, likes: r.likes + 1 } : r));
    } catch (err) {
      // ignore
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!description.trim()) return;

    const formData = new FormData();
    formData.append('event_type', eventType);
    formData.append('city', city);
    formData.append('description', description);

    try {
      const newRep = await communityApi.createReport(formData);
      setReports([newRep, ...reports]);
      setShowModal(false);
      setDescription('');
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="glass-card p-6 border-sky-400/30 flex items-center justify-between">
        <div>
          <h2 className="font-heading font-extrabold text-2xl text-white">Community Weather Radar Feed</h2>
          <p className="text-xs text-slate-400">Crowd-sourced weather observations from citizens worldwide</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 text-white font-semibold text-xs shadow-lg shadow-sky-500/20 hover:scale-105 transition-transform"
        >
          <Plus className="w-4 h-4" />
          <span>Report Weather Event</span>
        </button>
      </div>

      {/* Reports Feed Grid */}
      <div className="grid md:grid-cols-2 gap-6">
        {reports.map((item) => (
          <div key={item.id} className="glass-card p-5 space-y-4 border-slate-700/50 glass-card-hover">
            {/* User Info Header */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <img src={item.user_avatar} alt={item.user_name} className="w-9 h-9 rounded-full border border-sky-400/40 p-0.5 object-cover" />
                <div>
                  <h4 className="font-bold text-xs text-white">{item.user_name}</h4>
                  <p className="text-[10px] text-slate-400 flex items-center gap-1">
                    <MapPin className="w-3 h-3 text-sky-400" />
                    {item.city} • {item.timestamp}
                  </p>
                </div>
              </div>
              <span className="px-2.5 py-1 text-[11px] font-bold bg-amber-500/20 text-amber-300 border border-amber-400/30 rounded-lg">
                {item.event_type}
              </span>
            </div>

            {/* Description */}
            <p className="text-xs text-slate-300 leading-relaxed">{item.description}</p>

            {/* Attached Photo */}
            {item.image_url && (
              <div className="rounded-xl overflow-hidden h-48 bg-slate-900 border border-slate-700/50">
                <img src={item.image_url} alt={item.event_type} className="w-full h-full object-cover" />
              </div>
            )}

            {/* Footer Action Buttons */}
            <div className="pt-3 border-t border-slate-700/50 flex items-center justify-between text-xs text-slate-400">
              <button
                onClick={() => handleLike(item.id)}
                className="flex items-center gap-1.5 hover:text-sky-400 transition-colors"
              >
                <ThumbsUp className="w-4 h-4 text-sky-400" />
                <span className="font-semibold">{item.likes} Likes</span>
              </button>
              <div className="flex items-center gap-1.5">
                <MessageSquare className="w-4 h-4 text-slate-400" />
                <span>{item.comments_count} Comments</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Modal Form */}
      {showModal && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-md flex items-center justify-center p-4">
          <div className="glass-card p-6 max-w-md w-full border-sky-400/40 space-y-4">
            <h3 className="font-heading font-bold text-lg text-white">Report Severe Weather Event</h3>
            
            <form onSubmit={handleSubmit} className="space-y-3">
              <div>
                <label className="text-xs font-semibold text-slate-300 block mb-1">Event Type</label>
                <select
                  value={eventType}
                  onChange={(e) => setEventType(e.target.value)}
                  className="w-full glass-input px-3 py-2 text-xs text-white"
                >
                  <option value="Heavy Rain" className="bg-slate-900">Heavy Rain</option>
                  <option value="Flood" className="bg-slate-900">Flood</option>
                  <option value="Storm" className="bg-slate-900">Storm</option>
                  <option value="Heatwave" className="bg-slate-900">Heatwave</option>
                  <option value="Heavy Fog" className="bg-slate-900">Heavy Fog</option>
                </select>
              </div>

              <div>
                <label className="text-xs font-semibold text-slate-300 block mb-1">City Location</label>
                <input
                  type="text"
                  value={city}
                  onChange={(e) => setCity(e.target.value)}
                  placeholder="e.g. Paris, London, Sydney..."
                  className="w-full glass-input px-3 py-2 text-xs text-white"
                  required
                />
              </div>

              <div>
                <label className="text-xs font-semibold text-slate-300 block mb-1">Observation Details</label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Describe weather severity, road conditions..."
                  className="w-full glass-input px-3 py-2 text-xs text-white h-24"
                  required
                ></textarea>
              </div>

              <div className="flex gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="flex-1 py-2 rounded-xl glass-card text-xs text-slate-400 hover:text-white"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 py-2 rounded-xl bg-sky-500 text-white font-semibold text-xs shadow-md shadow-sky-500/30"
                >
                  Publish Report
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
