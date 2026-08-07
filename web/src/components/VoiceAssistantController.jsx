import React, { useState, useEffect } from 'react';
import { Mic, MicOff, Volume2, VolumeX, Sparkles } from 'lucide-react';

export const VoiceAssistantController = ({ onSpeechInput, lastAiResponse }) => {
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);

  useEffect(() => {
    // Speak automatically if new response arrives and TTS is available
    if (lastAiResponse && 'speechSynthesis' in window) {
      speakText(lastAiResponse);
    }
  }, [lastAiResponse]);

  const speakText = (text) => {
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    
    // Strip markdown formatting for cleaner speech
    const cleanText = text.replace(/[*#_`-]/g, '').trim();
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    window.speechSynthesis.speak(utterance);
  };

  const stopSpeaking = () => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
    }
  };

  const startListening = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Voice input is not supported in this browser. Please type your query.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onstart = () => setIsListening(true);
    recognition.onend = () => setIsListening(false);
    recognition.onerror = () => setIsListening(false);

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      if (transcript && onSpeechInput) {
        onSpeechInput(transcript);
      }
    };

    recognition.start();
  };

  return (
    <div className="flex items-center gap-2">
      {/* Speech-to-Text Mic Button */}
      <button
        type="button"
        onClick={isListening ? () => setIsListening(false) : startListening}
        className={`p-2.5 glass-card rounded-xl flex items-center justify-center transition-all ${
          isListening
            ? 'bg-red-500/30 border-red-500/60 text-red-400 animate-pulse shadow-lg shadow-red-500/30'
            : 'text-sky-300 hover:text-white hover:border-sky-400/50'
        }`}
        title={isListening ? "Listening..." : "Speak Question"}
      >
        {isListening ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
      </button>

      {/* Text-to-Speech Mute/Unmute Button */}
      {isSpeaking && (
        <button
          type="button"
          onClick={stopSpeaking}
          className="p-2.5 glass-card rounded-xl text-amber-400 border-amber-400/50 animate-pulse"
          title="Stop Speaking"
        >
          <VolumeX className="w-4 h-4" />
        </button>
      )}
    </div>
  );
};
