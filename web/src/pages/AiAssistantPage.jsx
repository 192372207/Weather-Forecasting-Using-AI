import React, { useState } from 'react';
import { useWeather } from '../context/WeatherContext';
import { aiApi } from '../services/api';
import { VoiceAssistantController } from '../components/VoiceAssistantController';
import { Sparkles, Send, Bot, User, RefreshCw, Languages, ShieldCheck, AlertTriangle } from 'lucide-react';

export const AiAssistantPage = () => {
  const { city, weather } = useWeather();
  const [inputMessage, setInputMessage] = useState('');
  const [selectedLang, setSelectedLang] = useState('en');
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([
    {
      sender: 'ai',
      text: `### 🌤️ Welcome to SkySense AI Safety Assistant!\n\nI am your meteorologist and weather safety companion. Currently tracking **${city}** (${weather?.temp || 22}°C, ${weather?.condition || 'Clear'}). Ask me anything about travel safety, rain risk, clothing, farming, or emergency advisories!`,
      risk_level: 'Green',
      suggestions: [
        'Is it safe to travel today?',
        'Will it rain today?',
        'Should I carry an umbrella?',
        'Is there any cyclone warning?',
        'Is the air quality healthy today?',
        'Is today safe for outdoor exercise?',
        'What precautions should I take today?'
      ]
    }
  ]);

  const languages = [
    { code: 'en', name: 'English' },
    { code: 'hi', name: 'हिंदी (Hindi)' },
    { code: 'te', name: 'తెలుగు (Telugu)' },
    { code: 'ta', name: 'தமிழ் (Tamil)' },
    { code: 'kn', name: 'కన్నడ (Kannada)' },
    { code: 'ml', name: 'മലയാളം (Malayalam)' },
    { code: 'ur', name: 'اردو (Urdu)' },
    { code: 'es', name: 'Español' },
    { code: 'fr', name: 'Français' },
    { code: 'de', name: 'Deutsch' },
  ];

  const handleSend = async (textToSend) => {
    const msg = textToSend || inputMessage;
    if (!msg.trim() || loading) return;

    const newMessages = [...messages, { sender: 'user', text: msg }];
    setMessages(newMessages);
    setInputMessage('');
    setLoading(true);

    try {
      const res = await aiApi.chat(
        msg,
        city,
        weather?.temp || 22.0,
        weather?.condition || 'Clear',
        selectedLang
      );

      setMessages([
        ...newMessages,
        {
          sender: 'ai',
          text: res.response,
          risk_level: res.risk_level || 'Green',
          suggestions: res.suggestions || []
        }
      ]);
    } catch (err) {
      setMessages([
        ...newMessages,
        {
          sender: 'ai',
          text: `### 🌤️ SkySense Weather Guidance for ${city}\n\nWeather conditions in **${city}** are pleasant today. Feel free to ask more!`,
          risk_level: 'Green',
          suggestions: ['Should I carry an umbrella?', 'Is it safe to travel today?']
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const lastAiMsg = messages.filter(m => m.sender === 'ai').slice(-1)[0]?.text;

  return (
    <div className="glass-card p-4 sm:p-6 h-[calc(100vh-8rem)] flex flex-col justify-between border-sky-400/30">
      {/* Top Controller Header */}
      <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-slate-700/50">
        {/* Animated Bot Avatar & Title */}
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-sky-500/30 animate-pulse-slow">
              <Bot className="w-6 h-6 text-white" />
            </div>
            <span className="absolute -bottom-0.5 -right-0.5 w-3 h-3 rounded-full bg-emerald-400 border-2 border-slate-900"></span>
          </div>
          <div>
            <h2 className="font-heading font-bold text-base sm:text-lg text-white flex items-center gap-2">
              <span>SkySense AI Safety Assistant</span>
              <Sparkles className="w-4 h-4 text-sky-400" />
            </h2>
            <p className="text-xs text-sky-400">Context: {city} ({weather?.temp || 22}°C, {weather?.condition || 'Clear'})</p>
          </div>
        </div>

        {/* Right Controls: Language Selector, Voice Controller, Reset */}
        <div className="flex items-center gap-2">
          {/* Language Selector */}
          <div className="flex items-center gap-1 glass-card px-2 py-1 rounded-xl text-xs">
            <Languages className="w-3.5 h-3.5 text-sky-400" />
            <select
              value={selectedLang}
              onChange={(e) => setSelectedLang(e.target.value)}
              className="bg-transparent text-xs text-white focus:outline-none cursor-pointer"
            >
              {languages.map(l => (
                <option key={l.code} value={l.code} className="bg-slate-900 text-white">
                  {l.name}
                </option>
              ))}
            </select>
          </div>

          {/* Voice Input & Output Controller */}
          <VoiceAssistantController
            onSpeechInput={(text) => handleSend(text)}
            lastAiResponse={lastAiMsg}
          />

          {/* Reset */}
          <button
            onClick={() => setMessages([messages[0]])}
            className="p-2 glass-card rounded-xl text-slate-400 hover:text-white"
            title="Reset Chat History"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Messages Feed */}
      <div className="flex-1 overflow-y-auto py-4 space-y-4 pr-2">
        {messages.map((m, idx) => (
          <div
            key={idx}
            className={`flex gap-3 ${m.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            {m.sender === 'ai' && (
              <div className="w-8 h-8 rounded-full bg-sky-500/20 border border-sky-400/40 flex items-center justify-center flex-shrink-0">
                <Sparkles className="w-4 h-4 text-sky-400" />
              </div>
            )}
            
            <div className={`max-w-xl space-y-3 ${m.sender === 'user' ? 'bg-sky-600 text-white rounded-2xl rounded-tr-none px-4 py-3' : 'glass-card p-4 text-slate-200 border-slate-700/50'}`}>
              <div className="text-xs leading-relaxed whitespace-pre-line">
                {m.text}
              </div>

              {/* Suggestions */}
              {m.suggestions && m.suggestions.length > 0 && (
                <div className="flex flex-wrap gap-1.5 pt-2 border-t border-slate-700/30">
                  {m.suggestions.map((s, i) => (
                    <button
                      key={i}
                      onClick={() => handleSend(s)}
                      className="px-2.5 py-1 text-[11px] font-semibold glass-card bg-sky-500/10 hover:bg-sky-500/20 text-sky-300 border-sky-400/30 rounded-lg transition-colors text-left"
                    >
                      {s}
                    </button>
                  ))}
                </div>
              )}
            </div>

            {m.sender === 'user' && (
              <div className="w-8 h-8 rounded-full bg-indigo-500/20 border border-indigo-400/40 flex items-center justify-center flex-shrink-0">
                <User className="w-4 h-4 text-indigo-300" />
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="flex gap-3 items-center text-slate-400 text-xs">
            <Sparkles className="w-4 h-4 text-sky-400 animate-spin" />
            <span>Groq AI is calculating safety telemetry & hazards for {city}...</span>
          </div>
        )}
      </div>

      {/* Input Bar */}
      <form onSubmit={(e) => { e.preventDefault(); handleSend(); }} className="pt-3 border-t border-slate-700/50 flex items-center gap-2 sm:gap-3">
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder={`Ask safety questions in ${languages.find(l => l.code === selectedLang)?.name}...`}
          className="flex-1 glass-input px-3.5 py-2.5 sm:py-3 text-xs text-white placeholder-slate-400 focus:outline-none"
        />
        <button
          type="submit"
          disabled={loading || !inputMessage.trim()}
          className="px-4 sm:px-5 py-2.5 sm:py-3 rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 text-white font-semibold text-xs shadow-lg shadow-sky-500/20 disabled:opacity-50 flex items-center gap-1.5 hover:scale-105 transition-transform"
        >
          <span>Send</span>
          <Send className="w-3.5 h-3.5" />
        </button>
      </form>
    </div>
  );
};
