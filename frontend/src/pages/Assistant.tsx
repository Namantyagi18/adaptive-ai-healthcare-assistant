import React, { useState, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import {
  Send,
  Trash2,
  AlertTriangle,
  Sparkles,
  ShieldCheck,
  RotateCcw,
  Bot,
  HelpCircle,
  Copy,
  Info,
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { useAuth } from '../context/AuthContext';
import { apiService } from '../services/api';
import { ChatMessage, QuestionResponse } from '../types';
import { MessageBubble } from '../components/chat/MessageBubble';
import { TypingIndicator } from '../components/chat/TypingIndicator';
import { Button } from '../components/ui/Button';

const SAMPLE_PROMPTS = [
  'What are the common symptoms of vitamin D deficiency?',
  'What are the common symptoms of iron deficiency anemia?',
  'Severe crushing chest pressure radiating down my left arm',
  'Sudden facial drooping and slurred speech in my father',
  'What are the warning signs of heat exhaustion?',
  'What is normal fasting blood glucose level?',
];

export const Assistant: React.FC = () => {
  const location = useLocation();
  const { t, language } = useLanguage();
  const { isBackendHealthy } = useAuth();

  const [messages, setMessages] = useState<ChatMessage[]>(() => {
    return [
      {
        id: 'welcome',
        role: 'assistant',
        content:
          'Hello, I am your ADAPT-AI Health Assistant. I retrieve evidence-based clinical guidance from authoritative medical bodies including NICE, WHO, CDC, and AIIMS.\n\nDescribe any symptoms you are experiencing or select an inquiry below to begin.',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      },
    ];
  });

  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string>(() => {
    return 'session-' + Math.random().toString(36).substring(2, 9);
  });
  const [lastSubmittedQuery, setLastSubmittedQuery] = useState<string>('');
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const messagesEndRef = useRef<HTMLDivElement | null>(null);
  const inputRef = useRef<HTMLTextAreaElement | null>(null);
  const initialQuestionProcessed = useRef(false);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  // Handle incoming question from Home page navigation
  useEffect(() => {
    const initQuestion = (location.state as any)?.initialQuestion;
    if (initQuestion && !initialQuestionProcessed.current) {
      initialQuestionProcessed.current = true;
      handleSend(initQuestion);
    }
  }, [location.state]);

  const handleSend = async (queryText?: string) => {
    const question = (queryText || input).trim();
    if (!question || isLoading) return;

    setErrorMsg(null);
    setInput('');
    setLastSubmittedQuery(question);

    const userMessage: ChatMessage = {
      id: 'usr-' + Date.now(),
      role: 'user',
      content: question,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response: QuestionResponse = await apiService.askQuestion({
        question,
        session_id: sessionId,
        include_citations: true,
        language_hint: language === 'hi' ? 'hi' : language === 'pa' ? 'pa' : 'en',
        country_code: 'IN',
      });

      const assistantMessage: ChatMessage = {
        id: 'asst-' + Date.now(),
        role: 'assistant',
        content: response.answer,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        triageLevel: response.triage_level,
        isEmergency: response.is_emergency,
        emergencyGuidance: response.emergency_guidance,
        citations: response.citations,
        evidenceSufficiency: response.evidence_sufficiency,
        uncertaintyStatement: response.uncertainty_statement,
        followUpQuestions: response.follow_up_questions,
        latencyMs: response.latency_ms,
        modelUsed: response.model_used,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err: any) {
      const msg = err.message || '';
      if (msg.includes('429')) {
        setErrorMsg('The clinical AI service is receiving high demand. Please wait a moment and click Retry.');
      } else if (msg.includes('401')) {
        setErrorMsg('Authentication session refreshed. Please click Retry.');
      } else if (msg.includes('timeout') || msg.includes('Failed to fetch')) {
        setErrorMsg('Communication timeout. Please verify backend server connectivity and try again.');
      } else {
        setErrorMsg(msg || 'An unexpected error occurred while communicating with the health assistant.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleRetry = () => {
    if (lastSubmittedQuery) {
      handleSend(lastSubmittedQuery);
    }
  };

  const handleClearSession = async () => {
    try {
      await apiService.clearSession(sessionId);
    } catch {
      // Clear locally regardless
    }
    const newSession = 'session-' + Math.random().toString(36).substring(2, 9);
    setSessionId(newSession);
    setMessages([
      {
        id: 'welcome-new',
        role: 'assistant',
        content: 'Conversation history reset. How may I help you today?',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      },
    ]);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-7.5rem)] max-w-5xl mx-auto space-y-4">
      {/* Top Session & Emergency Header */}
      <div className="flex items-center justify-between gap-4 pb-3 border-b border-slate-800 shrink-0">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-tr from-cyan-500 to-teal-500 text-slate-950 shadow-md">
            <Bot className="w-5 h-5 stroke-[2.5]" />
          </div>
          <div>
            <h1 className="text-base font-bold text-white flex items-center gap-2">
              <span>{t('nav.assistant')}</span>
              <span className="text-[10px] font-mono text-cyan-400 bg-cyan-950/80 px-2 py-0.5 rounded-full border border-cyan-800">
                Session Active
              </span>
            </h1>
            <p className="text-xs text-slate-400">
              Grounded in peer-reviewed clinical guidelines • Deterministic triage
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Button
            variant="ghost"
            size="sm"
            onClick={handleClearSession}
            icon={<Trash2 className="w-3.5 h-3.5 text-slate-400" />}
            title="Reset conversation"
          >
            Clear Chat
          </Button>
        </div>
      </div>

      {/* Backend Engine Reconnecting Notice */}
      {!isBackendHealthy && (
        <div className="p-3 rounded-xl bg-amber-950/40 border border-amber-500/40 text-xs text-amber-300 flex items-center gap-2 shrink-0">
          <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />
          <span>
            Connecting to ADAPT-AI healthcare engine at <code>localhost:8000</code>. Queries will
            dispatch as soon as connected.
          </span>
        </div>
      )}

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto pr-1 space-y-4">
        {messages.map((msg) => (
          <MessageBubble
            key={msg.id}
            message={msg}
            onSelectFollowUp={(q) => handleSend(q)}
          />
        ))}

        {isLoading && <TypingIndicator />}

        {errorMsg && (
          <div className="p-4 rounded-xl bg-red-950/50 border border-red-500/50 text-xs text-rose-300 space-y-2.5">
            <div className="flex items-center gap-2 font-bold text-red-200">
              <AlertTriangle className="w-4 h-4 text-red-400" />
              <span>Service Notification</span>
            </div>
            <p>{errorMsg}</p>
            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={handleRetry}
                icon={<RotateCcw className="w-3.5 h-3.5" />}
              >
                Retry Last Inquiry
              </Button>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Sample Inquiries Carousel */}
      {messages.length <= 2 && (
        <div className="shrink-0 pt-1 pb-2">
          <span className="text-[11px] font-semibold text-slate-400 block mb-2">
            Suggested clinical questions to ask:
          </span>
          <div className="flex flex-wrap gap-2">
            {SAMPLE_PROMPTS.map((prompt, i) => (
              <button
                key={i}
                onClick={() => handleSend(prompt)}
                className="text-xs px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-cyan-950/40 text-slate-300 hover:text-cyan-300 border border-slate-800 hover:border-cyan-500/40 transition-all text-left"
              >
                {prompt}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input Composer Area */}
      <div className="shrink-0 pt-2 border-t border-slate-800">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="relative rounded-2xl bg-slate-900 border border-slate-800 focus-within:border-cyan-500/60 focus-within:ring-1 focus-within:ring-cyan-500/50 transition-all shadow-xl"
        >
          <textarea
            ref={inputRef}
            rows={2}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={t('chat.placeholder') || 'Describe your symptoms or ask a health question...'}
            className="w-full bg-transparent px-4 pt-3 pb-12 text-xs sm:text-sm text-slate-100 placeholder-slate-500 focus:outline-none resize-none"
          />

          <div className="absolute bottom-2.5 left-3 right-3 flex items-center justify-between">
            <span className="text-[10px] text-slate-500 hidden sm:inline">
              Press <kbd className="bg-slate-800 px-1 py-0.5 rounded text-slate-400 font-mono">Enter</kbd> to submit, <kbd className="bg-slate-800 px-1 py-0.5 rounded text-slate-400 font-mono">Shift+Enter</kbd> for new line
            </span>

            <div className="flex items-center gap-2 ml-auto">
              <Button
                type="submit"
                size="sm"
                disabled={!input.trim() || isLoading}
                isLoading={isLoading}
                icon={<Send className="w-3.5 h-3.5 text-slate-950" />}
              >
                {t('chat.send') || 'Send'}
              </Button>
            </div>
          </div>
        </form>

        <p className="text-[10px] text-slate-500 text-center mt-2">
          {t('chat.disclaimer') || 'ADAPT-AI is an informational clinical decision support tool. It does not replace professional medical diagnosis or prescription.'}
        </p>
      </div>
    </div>
  );
};
