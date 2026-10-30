import React from 'react';
import { useLocation, Link } from 'react-router-dom';
import { Menu, PhoneCall, AlertTriangle, Activity, Globe } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';
import { useAuth } from '../../context/AuthContext';

interface HeaderProps {
  onMobileMenuOpen: () => void;
  isSidebarCollapsed: boolean;
}

export const Header: React.FC<HeaderProps> = ({ onMobileMenuOpen, isSidebarCollapsed }) => {
  const location = useLocation();
  const { t, language } = useLanguage();
  const { isBackendHealthy } = useAuth();

  const routeTitles: Record<string, string> = {
    '/': 'Home',
    '/assistant': 'AI Health Assistant',
    '/healthcare-map': 'Healthcare Discovery Map',
    '/find-healthcare': 'Pan-India Facility Search',
    '/documents': 'Medical Document Analysis',
    '/voice-assistant': 'Multilingual Voice Assistant',
    '/community-care': 'Community Care & Schemes',
    '/safety': 'Clinical Safety Center',
    '/settings': 'Settings & Privacy',
  };

  const currentTitle = routeTitles[location.pathname] || 'ADAPT-AI';

  return (
    <header className="sticky top-0 z-20 h-14 w-full bg-slate-950/80 backdrop-blur-md border-b border-slate-800/80 px-4 sm:px-6 flex items-center justify-between">
      <div className="flex items-center gap-3">
        {/* Mobile menu trigger */}
        <button
          onClick={onMobileMenuOpen}
          className="md:hidden p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 hover:text-white hover:bg-slate-800 transition-colors"
          aria-label="Open navigation sidebar"
        >
          <Menu className="w-5 h-5" />
        </button>

        {/* Page Title & Breadcrumb */}
        <div>
          <h1 className="text-sm font-bold text-white tracking-wide flex items-center gap-2">
            <span>{currentTitle}</span>
          </h1>
        </div>
      </div>

      {/* Right Contextual Actions */}
      <div className="flex items-center gap-3">
        {/* Engine Status Indicator */}
        <div
          className={`flex items-center gap-2 px-2.5 py-1 rounded-full text-xs font-semibold border ${
            isBackendHealthy
              ? 'bg-emerald-950/50 text-emerald-300 border-emerald-500/30'
              : 'bg-amber-950/50 text-amber-300 border-amber-500/30'
          }`}
          title={
            isBackendHealthy
              ? 'Clinical AI Engine Connected (FastAPI)'
              : 'Engine connecting or standby'
          }
        >
          <span
            className={`w-2 h-2 rounded-full ${
              isBackendHealthy ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'
            }`}
          />
          <span className="hidden sm:inline">
            {isBackendHealthy ? 'Engine Active' : 'Connecting Engine'}
          </span>
        </div>

        {/* Emergency Quick Dial */}
        <a
          href="tel:112"
          className="flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-rose-600/20 text-rose-300 border border-rose-500/40 hover:bg-rose-600 hover:text-white transition-all shadow-sm"
          title="Emergency Help: 112 / 108"
        >
          <AlertTriangle className="w-3.5 h-3.5 text-rose-400" />
          <span>112 / 108</span>
        </a>

        {/* Language Quick Pill */}
        <Link
          to="/settings"
          className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800 text-slate-400 hover:text-white text-xs font-mono uppercase transition-colors"
          title="Change language"
        >
          <Globe className="w-3.5 h-3.5 text-cyan-400" />
          <span>{language}</span>
        </Link>
      </div>
    </header>
  );
};

