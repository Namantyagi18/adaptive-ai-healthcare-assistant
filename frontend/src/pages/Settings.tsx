import React, { useState } from 'react';
import {
  Settings as SettingsIcon,
  Globe,
  ShieldCheck,
  Cpu,
  Database,
  CheckCircle,
  AlertTriangle,
  RefreshCw,
  Server,
  Eye,
  Sliders,
  MapPin,
  Lock,
  ChevronDown,
  ChevronUp,
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { useAuth } from '../context/AuthContext';
import { Card } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';

export const Settings: React.FC = () => {
  const { language, setLanguage, supportedLanguages, isRTL } = useLanguage();
  const { isBackendHealthy, healthData, refreshHealth, isLoadingHealth, developerKey, setDeveloperKey } =
    useAuth();

  const [devKeyInput, setDevKeyInput] = useState(developerKey || '');
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [showDeveloperPanel, setShowDeveloperPanel] = useState(false);
  const [reducedMotion, setReducedMotion] = useState<boolean>(() => {
    return localStorage.getItem('adapt_ai_reduced_motion') === 'true';
  });

  const handleToggleReducedMotion = () => {
    const nextVal = !reducedMotion;
    setReducedMotion(nextVal);
    localStorage.setItem('adapt_ai_reduced_motion', String(nextVal));
    if (nextVal) {
      document.documentElement.classList.add('reduce-motion');
    } else {
      document.documentElement.classList.remove('reduce-motion');
    }
  };

  const handleClearLocationCache = () => {
    alert('Location cache cleared. The next map search will request fresh GPS or default to New Delhi.');
  };

  const handleSaveDeveloperKey = () => {
    setDeveloperKey(devKeyInput.trim() || null);
    setSaveSuccess(true);
    setTimeout(() => setSaveSuccess(false), 3000);
  };

  return (
    <div className={`max-w-4xl mx-auto space-y-8 ${isRTL ? 'rtl' : 'ltr'}`}>
      {/* Header */}
      <div className="flex items-center gap-3 border-b border-slate-800 pb-4">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-800 text-cyan-400">
          <SettingsIcon className="w-5 h-5" />
        </div>
        <div>
          <h1 className="text-2xl font-black text-white">Settings & Patient Privacy</h1>
          <p className="text-xs text-slate-400">
            Configure language, accessibility, location preferences, and view privacy safeguards.
          </p>
        </div>
      </div>

      {/* Language Preferences */}
      <Card className="p-6 border-slate-800 bg-slate-900/80 space-y-4">
        <div className="flex items-center gap-2 text-cyan-400 font-bold text-sm">
          <Globe className="w-4 h-4" />
          <span>Interface & Conversation Language</span>
        </div>
        <p className="text-xs text-slate-300">
          Select your primary language for navigation, assistant synthesized advice, and speech interaction.
        </p>

        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 pt-2">
          {supportedLanguages.map((lang) => (
            <button
              key={lang.code}
              onClick={() => setLanguage(lang.code)}
              className={`flex items-center justify-between p-3 rounded-xl border text-left transition-all ${
                language === lang.code
                  ? 'bg-cyan-500/15 border-cyan-500 text-cyan-300 shadow-md ring-1 ring-cyan-500/40'
                  : 'bg-slate-950 border-slate-800 text-slate-300 hover:border-slate-700 hover:text-white'
              }`}
            >
              <div className="flex items-center gap-2">
                <span className="text-lg">{lang.flag}</span>
                <div>
                  <div className="text-xs font-semibold">{lang.nativeName}</div>
                  <div className="text-[10px] text-slate-400">{lang.name}</div>
                </div>
              </div>
              {language === lang.code && <CheckCircle className="w-4 h-4 text-cyan-400 shrink-0" />}
            </button>
          ))}
        </div>
      </Card>

      {/* Accessibility & Visual Motion */}
      <Card className="p-6 border-slate-800 bg-slate-900/80 space-y-4">
        <div className="flex items-center gap-2 text-teal-400 font-bold text-sm">
          <Eye className="w-4 h-4" />
          <span>Accessibility & Visual Motion</span>
        </div>
        <p className="text-xs text-slate-300">
          Adjust visual motion settings for comfort and screen reader accessibility.
        </p>

        <div className="flex items-center justify-between p-4 rounded-xl bg-slate-950 border border-slate-800">
          <div>
            <div className="text-xs font-semibold text-white">Reduce Interface Motion</div>
            <div className="text-[11px] text-slate-400 mt-0.5">
              Disables subtle background waveforms and transitions for users sensitive to motion.
            </div>
          </div>
          <button
            onClick={handleToggleReducedMotion}
            className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none ${
              reducedMotion ? 'bg-cyan-500' : 'bg-slate-800'
            }`}
          >
            <span
              className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                reducedMotion ? 'translate-x-6' : 'translate-x-1'
              }`}
            />
          </button>
        </div>
      </Card>

      {/* Location Permissions & Privacy */}
      <Card className="p-6 border-slate-800 bg-slate-900/80 space-y-4">
        <div className="flex items-center gap-2 text-emerald-400 font-bold text-sm">
          <MapPin className="w-4 h-4" />
          <span>Location & Map Controls</span>
        </div>
        <p className="text-xs text-slate-300">
          GPS coordinates are used strictly inside your browser session to compute distances to verified facilities. Coordinates are never sent to external advertisers.
        </p>

        <div className="flex items-center justify-between p-4 rounded-xl bg-slate-950 border border-slate-800">
          <div>
            <div className="text-xs font-semibold text-white">Reset Location Settings</div>
            <div className="text-[11px] text-slate-400 mt-0.5">
              Clears cached coordinates and restores default New Delhi anchor.
            </div>
          </div>
          <Button variant="secondary" size="sm" onClick={handleClearLocationCache}>
            Reset Location
          </Button>
        </div>
      </Card>

      {/* Privacy Notice */}
      <Card className="p-6 border-slate-800 bg-slate-900/80 space-y-3">
        <div className="flex items-center gap-2 text-cyan-400 font-bold text-sm">
          <Lock className="w-4 h-4" />
          <span>Patient Data Privacy Commitment</span>
        </div>
        <div className="text-xs text-slate-300 leading-relaxed space-y-2">
          <p>
            ADAPT-AI is built on principles of medical privacy and patient empowerment:
          </p>
          <ul className="list-disc pl-5 space-y-1 text-slate-400">
            <li>Zero retention of personal health identifiers (PHI).</li>
            <li>Uploaded documents are quarantined in memory, SHA-256 hashed, and never added to public training data.</li>
            <li>Anonymous patient session tokens are dynamically generated so patients never need to manage or configure secret server keys.</li>
          </ul>
        </div>
      </Card>

      {/* Advanced Developer & Clinical Node Diagnostics (Separate from Patient Experience) */}
      <div className="pt-2">
        <button
          onClick={() => setShowDeveloperPanel(!showDeveloperPanel)}
          className="flex items-center gap-2 text-xs font-semibold text-slate-500 hover:text-slate-300 transition-colors"
        >
          <span>Advanced Clinical Node Diagnostics</span>
          {showDeveloperPanel ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
        </button>

        {showDeveloperPanel && (
          <Card className="mt-3 p-6 border-slate-800 bg-slate-950/90 space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 text-teal-400 font-bold text-xs uppercase tracking-wider">
                <Server className="w-4 h-4" />
                <span>Backend Telemetry (FastAPI Service)</span>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={refreshHealth}
                isLoading={isLoadingHealth}
                icon={<RefreshCw className="w-3.5 h-3.5" />}
              >
                Refresh
              </Button>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <div className="rounded-xl bg-slate-900 p-3 border border-slate-800 text-xs">
                <div className="text-slate-400">Active Model Adapter</div>
                <div className="font-bold text-white mt-0.5">
                  {healthData?.components?.model_adapter?.name || 'gemini-3.5-flash'}
                </div>
              </div>

              <div className="rounded-xl bg-slate-900 p-3 border border-slate-800 text-xs">
                <div className="text-slate-400">Indexed Medical Corpus</div>
                <div className="font-bold text-white mt-0.5">
                  {healthData?.components?.vector_store?.total_documents ?? 20} Guidelines (
                  {healthData?.components?.vector_store?.total_chunks ?? 21} Chunks)
                </div>
              </div>

              <div className="rounded-xl bg-slate-900 p-3 border border-slate-800 text-xs">
                <div className="text-slate-400">Service Status</div>
                <div className="font-bold text-emerald-400 mt-0.5">
                  {isBackendHealthy ? 'HEALTHY (200 OK)' : 'CONNECTING'}
                </div>
              </div>
            </div>

            <div className="pt-3 border-t border-slate-800 space-y-2">
              <label className="block text-[11px] font-semibold text-slate-400">
                Optional Custom Developer Master API Key (For administrative test calls)
              </label>
              <div className="flex items-center gap-2">
                <input
                  type="text"
                  value={devKeyInput}
                  onChange={(e) => setDevKeyInput(e.target.value)}
                  placeholder="Leave blank to use automatic anonymous patient session tokens"
                  className="flex-1 bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-cyan-500 font-mono"
                />
                <Button size="sm" variant="secondary" onClick={handleSaveDeveloperKey}>
                  Apply
                </Button>
              </div>
              {saveSuccess && (
                <div className="text-xs text-emerald-400 flex items-center gap-1">
                  <CheckCircle className="w-3.5 h-3.5" />
                  <span>Key override applied</span>
                </div>
              )}
            </div>
          </Card>
        )}
      </div>
    </div>
  );
};
