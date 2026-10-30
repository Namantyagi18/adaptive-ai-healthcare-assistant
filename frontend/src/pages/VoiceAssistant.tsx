import React, { useState, useEffect, useRef } from 'react';
import {
  Mic,
  MicOff,
  Volume2,
  VolumeX,
  Languages,
  Sparkles,
  AlertTriangle,
  RotateCcw,
  Sliders,
  Send,
  X,
  Edit3,
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { apiService } from '../services/api';
import { VoiceWaveform } from '../components/voice/VoiceWaveform';
import { MessageBubble } from '../components/chat/MessageBubble';
import { ChatMessage, QuestionResponse } from '../types';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';

export const VoiceAssistant: React.FC = () => {
  const { t, language, setLanguage, supportedLanguages, isRTL } = useLanguage();

  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [speechRate, setSpeechRate] = useState(1.0);
  const [voiceEnabled, setVoiceEnabled] = useState(true);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isSupported, setIsSupported] = useState(true);
  const [statusText, setStatusText] = useState('Click "Start Voice Assistant" to begin speaking.');

  const recognitionRef = useRef<any>(null);

  // Initialize Speech Recognition
  useEffect(() => {
    const SpeechRecognition =
      (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = true;

      const langMap: Record<string, string> = {
        en: 'en-IN',
        hi: 'hi-IN',
        'hi-en': 'hi-IN',
        pa: 'pa-IN',
        ur: 'ur-IN',
        bn: 'bn-IN',
        ta: 'ta-IN',
        te: 'te-IN',
        mr: 'mr-IN',
      };
      recognition.lang = langMap[language] || 'en-IN';

      recognition.onstart = () => {
        setIsListening(true);
        setStatusText('Listening... Speak your healthcare query.');
      };

      recognition.onresult = (event: any) => {
        let currentTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; ++i) {
          currentTranscript += event.results[i][0].transcript;
        }
        setTranscript(currentTranscript);
      };

      recognition.onerror = (event: any) => {
        console.warn('Speech recognition error:', event.error);
        setIsListening(false);
        if (event.error === 'not-allowed') {
          setStatusText('Microphone access denied. You can type your question in the text box below.');
        } else {
          setStatusText(`Microphone status: ${event.error}. You can also type below.`);
        }
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognitionRef.current = recognition;
    } else {
      setIsSupported(false);
      setStatusText('Browser speech recognition not supported in this browser. Please use Chrome or type your query below.');
    }

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.abort();
      }
    };
  }, [language]);

  const toggleListening = () => {
    if (!isSupported) {
      alert('Speech Recognition is not supported by your current browser. You can type your query in the box below.');
      return;
    }

    if (isListening) {
      recognitionRef.current?.stop();
      setIsListening(false);
      setStatusText('Listening stopped. You can edit the transcript and submit.');
    } else {
      setTranscript('');
      try {
        recognitionRef.current?.start();
      } catch (err) {
        console.error('Speech start error:', err);
      }
    }
  };

  const handleCancel = () => {
    if (isListening) {
      recognitionRef.current?.abort();
      setIsListening(false);
    }
    setTranscript('');
    setStatusText('Cancelled. Click to speak again or type below.');
  };

  const speakText = (text: string) => {
    if (!voiceEnabled || !window.speechSynthesis) return;

    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = speechRate;

    const langMap: Record<string, string> = {
      en: 'en-IN',
      hi: 'hi-IN',
      'hi-en': 'hi-IN',
      pa: 'pa-IN',
      ur: 'ur-IN',
    };
    utterance.lang = langMap[language] || 'en-IN';

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    window.speechSynthesis.speak(utterance);
  };

  const submitTranscript = async (queryText?: string) => {
    const textToSubmit = (queryText || transcript).trim();
    if (!textToSubmit || isLoading) return;

    if (isListening) {
      recognitionRef.current?.stop();
      setIsListening(false);
    }

    setIsLoading(true);
    setStatusText('Processing clinical inquiry with verified guidelines...');

    const userMessage: ChatMessage = {
      id: 'voice-usr-' + Date.now(),
      role: 'user',
      content: textToSubmit,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMessage]);

    try {
      const res: QuestionResponse = await apiService.askQuestion({
        question: textToSubmit,
        language_hint: language === 'hi' ? 'hi' : language === 'pa' ? 'pa' : 'en',
        country_code: 'IN',
      });

      const assistantMessage: ChatMessage = {
        id: 'voice-asst-' + Date.now(),
        role: 'assistant',
        content: res.answer,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        triageLevel: res.triage_level,
        isEmergency: res.is_emergency,
        emergencyGuidance: res.emergency_guidance,
        citations: res.citations,
        evidenceSufficiency: res.evidence_sufficiency,
        uncertaintyStatement: res.uncertainty_statement,
        followUpQuestions: res.follow_up_questions,
        latencyMs: res.latency_ms,
        modelUsed: res.model_used,
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setStatusText('Guideline synthesis ready.');
      setTranscript('');

      // Voice read-out
      speakText(res.answer);
    } catch (err: any) {
      setStatusText(`Error: ${err.message || 'Failed to query assistant.'}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={`max-w-4xl mx-auto space-y-8 ${isRTL ? 'rtl' : 'ltr'}`}>
      {/* Header */}
      <div className="text-center max-w-2xl mx-auto space-y-2">
        <Badge variant="cyan" className="mx-auto">
          Speech AI Engine
        </Badge>
        <h1 className="text-3xl font-black text-white tracking-tight">
          {t('voice.title') || 'Hands-Free Multilingual Voice Assistant'}
        </h1>
        <p className="text-xs sm:text-sm text-slate-400">
          Speak naturally in English, Hindi, Hinglish, Punjabi, or Urdu with real-time speech synthesis.
        </p>
      </div>

      {/* Voice Visualizer Control Panel */}
      <Card className="p-6 sm:p-8 border-cyan-500/40 bg-slate-900/90 text-center space-y-6">
        {/* Animated Waveform */}
        <VoiceWaveform isActive={isListening || isSpeaking} barsCount={24} />

        {/* Live Status Text */}
        <div className="text-xs font-semibold text-cyan-300 min-h-6">
          {statusText}
        </div>

        {/* Editable Transcript Area */}
        <div className="max-w-xl mx-auto space-y-2 text-left">
          <label className="block text-[11px] font-bold uppercase tracking-wider text-slate-400 flex items-center justify-between">
            <span className="flex items-center gap-1.5">
              <Edit3 className="w-3.5 h-3.5 text-cyan-400" />
              <span>Voice Transcript (Editable)</span>
            </span>
            {transcript && (
              <button
                onClick={() => setTranscript('')}
                className="text-slate-500 hover:text-slate-300 text-[10px] normal-case"
              >
                Clear text
              </button>
            )}
          </label>
          <div className="relative">
            <textarea
              rows={2}
              value={transcript}
              onChange={(e) => setTranscript(e.target.value)}
              placeholder="Your spoken words appear here. You can also edit before submitting..."
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500"
            />
            {transcript.trim() && (
              <Button
                size="sm"
                onClick={() => submitTranscript()}
                isLoading={isLoading}
                icon={<Send className="w-3 h-3 text-slate-950" />}
                className="absolute right-2 bottom-3"
              >
                Submit
              </Button>
            )}
          </div>
        </div>

        {/* Microphone Big Trigger & Cancel */}
        <div className="flex items-center justify-center gap-4">
          <button
            onClick={toggleListening}
            className={`relative flex items-center justify-center h-20 w-20 rounded-full transition-all shadow-2xl focus:outline-none ${
              isListening
                ? 'bg-rose-600 text-white animate-pulse ring-8 ring-rose-500/30 shadow-rose-600/50'
                : 'bg-gradient-to-tr from-cyan-500 to-teal-500 text-slate-950 hover:scale-105 shadow-cyan-500/30'
            }`}
            title={isListening ? 'Click to stop' : 'Click to start speaking'}
          >
            {isListening ? <MicOff className="w-8 h-8" /> : <Mic className="w-8 h-8" />}
          </button>

          {isListening && (
            <button
              onClick={handleCancel}
              className="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs text-slate-300 flex items-center gap-1 transition-colors"
            >
              <X className="w-3.5 h-3.5" />
              <span>Cancel</span>
            </button>
          )}
        </div>

        {/* Voice Setting Controls */}
        <div className="flex flex-wrap items-center justify-center gap-6 pt-4 border-t border-slate-800 text-xs text-slate-400">
          {/* Language selector */}
          <div className="flex items-center gap-2">
            <Languages className="w-4 h-4 text-cyan-400" />
            <span>Voice Language:</span>
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="bg-slate-950 border border-slate-800 rounded-lg px-2.5 py-1 text-slate-200 focus:outline-none focus:border-cyan-500"
            >
              {supportedLanguages.map((l) => (
                <option key={l.code} value={l.code}>
                  {l.flag} {l.nativeName} ({l.name})
                </option>
              ))}
            </select>
          </div>

          {/* Voice rate slider */}
          <div className="flex items-center gap-2">
            <Sliders className="w-4 h-4 text-teal-400" />
            <span>Speech Speed:</span>
            <input
              type="range"
              min={0.7}
              max={1.4}
              step={0.1}
              value={speechRate}
              onChange={(e) => setSpeechRate(Number(e.target.value))}
              className="w-20 accent-cyan-500 h-1 bg-slate-800 rounded"
            />
            <span className="font-mono text-cyan-400 font-bold">{speechRate}x</span>
          </div>

          {/* Audio Output Mute Toggle */}
          <button
            onClick={() => {
              if (isSpeaking) window.speechSynthesis?.cancel();
              setVoiceEnabled(!voiceEnabled);
            }}
            className="flex items-center gap-1.5 px-3 py-1 rounded-lg bg-slate-800 text-slate-300 hover:text-white"
          >
            {voiceEnabled ? (
              <>
                <Volume2 className="w-3.5 h-3.5 text-emerald-400" />
                <span>Audio Readout: ON</span>
              </>
            ) : (
              <>
                <VolumeX className="w-3.5 h-3.5 text-rose-400" />
                <span>Audio Readout: OFF</span>
              </>
            )}
          </button>
        </div>
      </Card>

      {/* Voice Messages Conversation Transcript */}
      {messages.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Voice Conversation
          </h3>
          <div className="space-y-4">
            {messages.map((msg) => (
              <MessageBubble key={msg.id} message={msg} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
