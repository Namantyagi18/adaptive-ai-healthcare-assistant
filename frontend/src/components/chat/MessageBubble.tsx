import React, { useState } from 'react';
import {
  User,
  Bot,
  ShieldCheck,
  AlertCircle,
  Copy,
  Check,
  CheckCircle2,
  Clock,
} from 'lucide-react';
import { ChatMessage } from '../../types';
import { TriageBanner } from './TriageBanner';
import { CitationCard } from './CitationCard';
import { FollowUpChips } from './FollowUpChips';

interface MessageBubbleProps {
  message: ChatMessage;
  onSelectFollowUp?: (question: string) => void;
  onRetry?: () => void;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({
  message,
  onSelectFollowUp,
}) => {
  const isUser = message.role === 'user';
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(message.content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Fallback
    }
  };

  if (isUser) {
    return (
      <div className="flex items-start justify-end gap-3 my-4">
        <div className="max-w-2xl rounded-2xl rounded-tr-none bg-gradient-to-r from-cyan-600 to-teal-600 px-5 py-3.5 text-white shadow-md shadow-cyan-950/20">
          <p className="text-sm leading-relaxed whitespace-pre-wrap font-medium">{message.content}</p>
          <span className="block text-[10px] text-cyan-200/80 text-right mt-1 font-mono">
            {message.timestamp}
          </span>
        </div>
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-slate-800 border border-slate-700 text-slate-300">
          <User className="w-4 h-4" />
        </div>
      </div>
    );
  }

  // Assistant Message
  return (
    <div className="flex items-start gap-3 my-5">
      <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-gradient-to-tr from-cyan-500 to-teal-500 text-slate-950 shadow-md shadow-cyan-500/20 mt-1">
        <Bot className="w-4 h-4 stroke-[2.5]" />
      </div>

      <div className="max-w-3xl flex-1 rounded-2xl rounded-tl-none bg-slate-900/90 border border-slate-800 p-5 shadow-xl">
        {/* Triage Banner if present */}
        {message.triageLevel && (
          <TriageBanner
            triageLevel={message.triageLevel}
            emergencyGuidance={message.emergencyGuidance}
            isEmergency={message.isEmergency}
          />
        )}

        {/* Evidence Status Pill */}
        {message.evidenceSufficiency && (
          <div className="flex items-center justify-between mb-3">
            <span
              className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-semibold border ${
                message.evidenceSufficiency === 'SUFFICIENT'
                  ? 'bg-emerald-950/60 text-emerald-400 border-emerald-500/30'
                  : message.evidenceSufficiency === 'INSUFFICIENT'
                  ? 'bg-amber-950/60 text-amber-400 border-amber-500/30'
                  : 'bg-rose-950/60 text-rose-400 border-rose-500/30'
              }`}
            >
              <CheckCircle2 className="w-3 h-3" />
              <span>
                Evidence Grounding:{' '}
                {message.evidenceSufficiency === 'SUFFICIENT'
                  ? 'Verified in Guidelines'
                  : message.evidenceSufficiency === 'INSUFFICIENT'
                  ? 'Limited/Insufficient Guidance'
                  : 'Contradictory Evidence'}
              </span>
            </span>

            {/* Copy Button */}
            <button
              onClick={handleCopy}
              className="flex items-center gap-1 text-[11px] text-slate-400 hover:text-cyan-400 transition-colors p-1 rounded"
              title="Copy response to clipboard"
            >
              {copied ? (
                <>
                  <Check className="w-3.5 h-3.5 text-emerald-400" />
                  <span className="text-emerald-400 font-semibold">Copied!</span>
                </>
              ) : (
                <>
                  <Copy className="w-3.5 h-3.5" />
                  <span>Copy</span>
                </>
              )}
            </button>
          </div>
        )}

        {/* Clinical Answer text */}
        <div className="text-sm text-slate-200 leading-relaxed whitespace-pre-wrap font-sans space-y-2">
          {message.content}
        </div>

        {/* Clinical Uncertainty Note */}
        {message.uncertaintyStatement && (
          <div className="mt-3.5 rounded-xl bg-slate-950/70 border border-amber-500/30 p-3 text-xs text-amber-300/90 flex items-start gap-2">
            <AlertCircle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
            <div>
              <strong className="font-semibold block text-amber-300">Clinical Boundary:</strong>
              <span>{message.uncertaintyStatement}</span>
            </div>
          </div>
        )}

        {/* Guideline Citations */}
        {message.citations && message.citations.length > 0 && (
          <div className="mt-4 pt-3 border-t border-slate-800/80 space-y-2">
            <div className="flex items-center justify-between text-xs font-semibold text-slate-400 mb-1">
              <span className="flex items-center gap-1.5 text-cyan-400">
                <ShieldCheck className="w-3.5 h-3.5" />
                <span>Verified Guideline Sources ({message.citations.length})</span>
              </span>
              <span className="text-[10px] text-slate-500">Peer-Reviewed Publications</span>
            </div>
            <div className="grid grid-cols-1 gap-2">
              {message.citations.map((c, i) => (
                <CitationCard key={c.chunk_id || i} citation={c} index={i} />
              ))}
            </div>
          </div>
        )}

        {/* Suggested Follow-ups */}
        {message.followUpQuestions && onSelectFollowUp && (
          <FollowUpChips
            questions={message.followUpQuestions}
            onSelect={onSelectFollowUp}
          />
        )}

        {/* Footer info: Timestamp & disclaimer reminder */}
        <div className="mt-4 pt-3 border-t border-slate-800/60 flex items-center justify-between text-[10px] text-slate-500">
          <span>Always seek in-person professional physician guidance.</span>
          <span className="font-mono">{message.timestamp}</span>
        </div>
      </div>
    </div>
  );
};
