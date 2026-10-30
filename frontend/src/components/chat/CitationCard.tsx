import React, { useState } from 'react';
import { BookOpen, ChevronDown, ChevronUp } from 'lucide-react';
import { EvidenceReference } from '../../types';

interface CitationCardProps {
  citation: EvidenceReference;
  index: number;
}

export const CitationCard: React.FC<CitationCardProps> = ({ citation, index }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const matchPercentage = Math.round(citation.relevance_score * 100);

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-3 transition-all hover:border-slate-700">
      <div className="flex items-start justify-between gap-2">
        <div className="flex items-start gap-2.5">
          <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-md bg-cyan-500/20 text-[10px] font-bold text-cyan-400">
            [{index + 1}]
          </span>
          <div>
            <h4 className="text-xs font-semibold text-slate-200 line-clamp-1">{citation.title}</h4>
            <div className="flex items-center gap-2 mt-0.5 text-[11px] text-slate-400">
              <span className="text-cyan-400 font-semibold">{citation.source}</span>
              <span>•</span>
              <span className="text-slate-500">Verified Clinical Guideline</span>
            </div>
          </div>
        </div>

        {/* Confidence Match Badge */}
        <div className="flex items-center gap-1.5 shrink-0">
          <span
            className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${
              citation.relevance_score >= 0.7
                ? 'bg-emerald-950/80 text-emerald-300 border-emerald-500/40'
                : citation.relevance_score >= 0.5
                ? 'bg-cyan-950/80 text-cyan-300 border-cyan-500/40'
                : 'bg-slate-800 text-slate-300 border-slate-700'
            }`}
          >
            {matchPercentage}% Confidence
          </span>
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="rounded p-1 text-slate-400 hover:text-white transition-colors"
            title={isExpanded ? 'Hide passage' : 'Read source passage'}
            aria-label={isExpanded ? 'Hide source passage' : 'Read source passage'}
          >
            {isExpanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
          </button>
        </div>
      </div>

      {/* Expanded Guideline Passage */}
      {isExpanded && (
        <div className="mt-3 pt-2.5 border-t border-slate-800/80 text-xs text-slate-300 bg-slate-950/70 rounded-lg p-3 leading-relaxed">
          <div className="flex items-center gap-1.5 text-[10px] text-cyan-400 font-semibold mb-1.5">
            <BookOpen className="w-3.5 h-3.5" />
            <span>ORIGINAL CLINICAL PASSAGE:</span>
          </div>
          <p className="whitespace-pre-wrap font-sans text-slate-300">{citation.excerpt}</p>
        </div>
      )}
    </div>
  );
};
