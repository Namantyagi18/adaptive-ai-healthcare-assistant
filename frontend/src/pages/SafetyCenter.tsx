import React from 'react';
import {
  ShieldAlert,
  AlertTriangle,
  HeartPulse,
  Brain,
  Activity,
  PhoneCall,
  CheckCircle,
  XCircle,
  HelpCircle,
  Clock,
  ShieldCheck,
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { Card } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';

export const SafetyCenter: React.FC = () => {
  const { t } = useLanguage();

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-10">
      {/* Page Header */}
      <div className="text-center max-w-3xl mx-auto space-y-3">
        <Badge variant="emergency" className="mx-auto" pulse>
          Zero Compromise on Patient Safety
        </Badge>
        <h1 className="text-3xl sm:text-4xl font-black text-white tracking-tight">
          {t('safety.title')}
        </h1>
        <p className="text-xs sm:text-sm text-slate-400 leading-relaxed">
          {t('safety.subtitle')} ADAPT-AI incorporates deterministic red-flag triage filters, clinical
          regulatory guardrails, and rapid emergency escalation.
        </p>
      </div>

      {/* Emergency Call Box */}
      <div className="rounded-2xl border border-rose-500/60 bg-gradient-to-r from-red-950/80 via-rose-900/40 to-red-950/80 p-6 shadow-2xl">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="space-y-1 text-center sm:text-left">
            <h2 className="text-lg font-bold text-white flex items-center justify-center sm:justify-start gap-2">
              <AlertTriangle className="w-5 h-5 text-rose-400" />
              <span>Immediate Life-Threatening Emergency?</span>
            </h2>
            <p className="text-xs text-rose-200">
              Do not use an AI app if you or someone near you has acute chest pain, sudden paralysis,
              difficulty breathing, or severe blood loss. Call emergency services immediately.
            </p>
          </div>
          <div className="flex items-center gap-3">
            <a
              href="tel:112"
              className="flex items-center gap-2 bg-rose-600 hover:bg-rose-500 text-white font-bold px-5 py-3 rounded-xl shadow-lg transition-colors text-sm"
            >
              <PhoneCall className="w-4 h-4" />
              <span>Call 112 (India)</span>
            </a>
            <a
              href="tel:108"
              className="flex items-center gap-2 bg-slate-900 hover:bg-slate-800 text-rose-300 font-bold px-4 py-3 rounded-xl border border-rose-500/40 transition-colors text-sm"
            >
              <span>108 Ambulance</span>
            </a>
          </div>
        </div>
      </div>

      {/* FAST Stroke Protocol */}
      <div className="space-y-4">
        <div className="flex items-center gap-2">
          <Brain className="w-5 h-5 text-cyan-400" />
          <h2 className="text-xl font-bold text-white">{t('safety.fastProtocol')}</h2>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
          <Card className="p-5 border-cyan-500/30 bg-slate-900/80 text-center space-y-2">
            <div className="text-2xl font-black text-cyan-400">F</div>
            <h3 className="text-sm font-bold text-white">Face Drooping</h3>
            <p className="text-xs text-slate-300">
              Does one side of the face droop or is it numb? Ask the person to smile. Is the smile uneven?
            </p>
          </Card>

          <Card className="p-5 border-cyan-500/30 bg-slate-900/80 text-center space-y-2">
            <div className="text-2xl font-black text-cyan-400">A</div>
            <h3 className="text-sm font-bold text-white">Arm Weakness</h3>
            <p className="text-xs text-slate-300">
              Is one arm weak or numb? Ask the person to raise both arms. Does one arm drift downward?
            </p>
          </Card>

          <Card className="p-5 border-cyan-500/30 bg-slate-900/80 text-center space-y-2">
            <div className="text-2xl font-black text-cyan-400">S</div>
            <h3 className="text-sm font-bold text-white">Speech Difficulty</h3>
            <p className="text-xs text-slate-300">
              Is speech slurred? Is the person unable to speak or hard to understand? Ask them to repeat a simple sentence.
            </p>
          </Card>

          <Card className="p-5 border-rose-500/40 bg-red-950/40 text-center space-y-2">
            <div className="text-2xl font-black text-rose-400">T</div>
            <h3 className="text-sm font-bold text-white">Time to Call 112</h3>
            <p className="text-xs text-slate-300">
              If the person shows ANY of these symptoms, call 112 or 108 immediately. Note the time symptoms first appeared.
            </p>
          </Card>
        </div>
      </div>

      {/* Heart Attack Red Flags */}
      <Card className="p-6 border-red-500/30 bg-slate-900/80 space-y-4">
        <div className="flex items-center gap-2 text-rose-400">
          <HeartPulse className="w-5 h-5" />
          <h2 className="text-lg font-bold text-white">{t('safety.miProtocol')}</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs text-slate-300">
          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-1">
            <strong className="text-white block font-semibold">1. Chest Discomfort</strong>
            <span>
              Pressure, fullness, squeezing, or crushing pain in the centre of the chest lasting more than a few minutes or going away and returning.
            </span>
          </div>
          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-1">
            <strong className="text-white block font-semibold">2. Radiating Pain</strong>
            <span>
              Pain radiating to the left arm, shoulders, neck, jaw, back, or upper stomach.
            </span>
          </div>
          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-1">
            <strong className="text-white block font-semibold">3. Associated Signs</strong>
            <span>
              Cold sweats, unexplained dizziness, extreme shortness of breath, nausea, or lightheadedness.
            </span>
          </div>
        </div>
      </Card>

      {/* Clinical Guardrails Boundary Explanation */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* What ADAPT-AI Does */}
        <Card className="p-6 border-emerald-500/30 bg-slate-900/70 space-y-4">
          <div className="flex items-center gap-2 text-emerald-400">
            <CheckCircle className="w-5 h-5" />
            <h3 className="text-base font-bold text-white">What ADAPT-AI Provides</h3>
          </div>
          <ul className="space-y-2.5 text-xs text-slate-300">
            <li className="flex items-start gap-2">
              <span className="text-emerald-400 font-bold">✓</span>
              <span>Evidence-based guidance retrieved verbatim from peer-reviewed clinical guidelines.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-emerald-400 font-bold">✓</span>
              <span>Exact citations with relevance percentages and source document IDs.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-emerald-400 font-bold">✓</span>
              <span>Transparent disclosure when guidelines lack evidence (zero hallucination).</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-emerald-400 font-bold">✓</span>
              <span>Immediate geo-navigation to emergency facilities and blood centres across India.</span>
            </li>
          </ul>
        </Card>

        {/* What ADAPT-AI Refuses */}
        <Card className="p-6 border-rose-500/30 bg-slate-900/70 space-y-4">
          <div className="flex items-center gap-2 text-rose-400">
            <XCircle className="w-5 h-5" />
            <h3 className="text-base font-bold text-white">What ADAPT-AI Refuses</h3>
          </div>
          <ul className="space-y-2.5 text-xs text-slate-300">
            <li className="flex items-start gap-2">
              <span className="text-rose-400 font-bold">✗</span>
              <span>Will NEVER prescribe pharmaceutical drug dosages or generate prescriptions.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-rose-400 font-bold">✗</span>
              <span>Will NEVER make a definitive clinical diagnosis based solely on user chat messages.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-rose-400 font-bold">✗</span>
              <span>Will NEVER fabricate fake citations, study names, or clinical guidelines.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-rose-400 font-bold">✗</span>
              <span>Will NEVER delay red-flag emergency advice behind conversation loops.</span>
            </li>
          </ul>
        </Card>
      </div>
    </div>
  );
};

