import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Bot, Sparkles } from 'lucide-react';

export const FloatingChatButton = () => {
  const location = useLocation();
  if (location.pathname === '/ai-chat' || location.pathname === '/login' || location.pathname === '/register') {
    return null;
  }

  return (
    <Link
      to="/ai-chat"
      className="fixed bottom-16 lg:bottom-8 right-5 z-40 p-3.5 rounded-2xl bg-gradient-to-tr from-sky-500 to-indigo-600 text-white shadow-2xl shadow-sky-500/40 hover:scale-110 transition-all flex items-center gap-2 group border border-sky-400/50"
      title="Ask AI Safety Assistant"
    >
      <div className="relative">
        <Bot className="w-6 h-6" />
        <span className="absolute -top-1 -right-1 w-2.5 h-2.5 rounded-full bg-emerald-400 animate-ping"></span>
      </div>
      <span className="text-xs font-bold hidden sm:inline group-hover:inline pr-1">
        AI Safety Assistant
      </span>
    </Link>
  );
};
