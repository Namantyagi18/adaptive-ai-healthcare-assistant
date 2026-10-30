import React from 'react';
import { AlertTriangle, AlertCircle, Clock, Info, HelpCircle, PhoneCall } from 'lucide-react';
import { TriageLevel } from '../../types';

interface TriageBannerProps {
  triageLevel: TriageLevel;
  emergencyGuidance?: string | null;
  isEmergency?: boolean;
}

export const TriageBanner: React.FC<TriageBannerProps> = ({
  triageLevel,
  emergencyGuidance,
  isEmergency = false,
}) => {
  if (isEmergency || triageLevel === 'EMERGENCY_IMMEDIATE') {
    return (
      <div className="rounded-xl border border-rose-500/60 bg-gradient-to-r from-red-950/80 via-rose-900/40 to-red-950/80 p-4 shadow-lg shadow-rose-950/50 mb-3 animate-pulse">
        <div className="flex items-start gap-3">
          <div className="rounded-lg bg-rose-500/20 p-2 text-rose-400 shrink-0">
            <AlertTriangle className="w-5 h-5 text-rose-400" />
          </div>
          <div className="space-y-1.5 flex-1">
            <div className="flex items-center justify-between flex-wrap gap-2">
              <span className="text-xs font-bold uppercase tracking-wider text-rose-300 bg-rose-950/90 px-2.5 py-0.5 rounded-full border border-rose-500/40">
                Critical Emergency Immediate
              </span>
              <a
                href="tel:112"
                className="inline-flex items-center gap-1.5 text-xs font-bold bg-rose-600 hover:bg-rose-500 text-white px-3 py-1 rounded-full shadow-md transition-colors"
              >
                <PhoneCall className="w-3.5 h-3.5" />
                <span>Call 112 / 108 Now</span>
              </a>
            </div>
            <p className="text-sm font-semibold text-white">
              {emergencyGuidance ||
                'Potentially life-threatening red-flag symptoms detected. Do not wait. Call 112 / 108 or proceed immediately to the nearest Emergency Department (A&E).'}
            </p>
          </div>
        </div>
      </div>
    );
  }

  if (triageLevel === 'URGENT_CARE') {
    return (
      <div className="rounded-xl border border-amber-500/50 bg-amber-950/30 p-3.5 mb-3">
        <div className="flex items-start gap-3">
          <div className="rounded-lg bg-amber-500/20 p-1.5 text-amber-400 shrink-0">
            <AlertCircle className="w-4 h-4 text-amber-400" />
          </div>
          <div className="space-y-1 text-xs">
            <span className="font-bold uppercase tracking-wider text-amber-300">
              Urgent Clinical Assessment Recommended
            </span>
            <p className="text-slate-300">
              These symptoms warrant prompt in-person clinical assessment within 12 to 24 hours at an
              urgent care centre, outpatient clinic, or with your general practitioner.
            </p>
          </div>
        </div>
      </div>
    );
  }

  if (triageLevel === 'ROUTINE_CLINICAL') {
    return (
      <div className="rounded-xl border border-cyan-500/30 bg-cyan-950/20 p-3 mb-3">
        <div className="flex items-center gap-2.5 text-xs text-cyan-300">
          <Clock className="w-4 h-4 text-cyan-400 shrink-0" />
          <span className="font-semibold">Routine Clinical Consultation:</span>
          <span className="text-slate-300">
            Consider booking a standard appointment with a primary care physician.
          </span>
        </div>
      </div>
    );
  }

  if (triageLevel === 'UNCERTAIN_AMBIGUOUS') {
    return (
      <div className="rounded-xl border border-purple-500/30 bg-purple-950/20 p-3 mb-3">
        <div className="flex items-center gap-2.5 text-xs text-purple-300">
          <HelpCircle className="w-4 h-4 text-purple-400 shrink-0" />
          <span className="font-semibold">Clinical Ambiguity:</span>
          <span className="text-slate-300">
            Information provided is ambiguous or insufficient to safely categorize urgency.
          </span>
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-xl border border-teal-500/20 bg-teal-950/15 p-2.5 mb-3">
      <div className="flex items-center gap-2 text-xs text-teal-300">
        <Info className="w-3.5 h-3.5 text-teal-400 shrink-0" />
        <span className="font-medium">Self-Care & Health Education Context</span>
      </div>
    </div>
  );
};

