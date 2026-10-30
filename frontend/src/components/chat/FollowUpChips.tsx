import React from 'react';
import { HelpCircle, ArrowRight } from 'lucide-react';

interface FollowUpChipsProps {
  questions: string[];
  onSelect: (question: string) => void;
}

export const FollowUpChips: React.FC<FollowUpChipsProps> = ({ questions, onSelect }) => {
  if (!questions || questions.length === 0) return null;

  return (
    <div className="mt-3 pt-3 border-t border-slate-800/60">
      <div className="flex items-center gap-1.5 text-[11px] font-semibold text-cyan-400 mb-2">
        <HelpCircle className="w-3.5 h-3.5" />
        <span>SUGGESTED FOLLOW-UP QUESTIONS:</span>
      </div>
      <div className="flex flex-wrap gap-2">
        {questions.map((q, idx) => (
          <button
            key={idx}
            onClick={() => onSelect(q)}
            className="group flex items-center gap-1.5 text-xs text-left px-3 py-1.5 rounded-xl bg-slate-950/70 hover:bg-cyan-950/40 text-slate-300 hover:text-cyan-300 border border-slate-800 hover:border-cyan-500/40 transition-all shadow-sm"
          >
            <span>{q}</span>
            <ArrowRight className="w-3 h-3 text-slate-500 group-hover:text-cyan-400 group-hover:translate-x-0.5 transition-all shrink-0" />
          </button>
        ))}
      </div>
    </div>
  );
};

