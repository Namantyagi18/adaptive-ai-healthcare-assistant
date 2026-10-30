import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Home,
  Activity,
  Bot,
  MapPin,
  Compass,
  FileText,
  Mic,
  HeartHandshake,
  ShieldAlert,
  Settings,
  ChevronLeft,
  ChevronRight,
  Globe,
  PhoneCall,
  Sparkles,
  X,
  ExternalLink,
} from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';
import { useAuth } from '../../context/AuthContext';

interface SidebarProps {
  isMobileOpen: boolean;
  onMobileClose: () => void;
  isCollapsed: boolean;
  onToggleCollapse: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  isMobileOpen,
  onMobileClose,
  isCollapsed,
  onToggleCollapse,
}) => {
  const location = useLocation();
  const { language, setLanguage, t, supportedLanguages } = useLanguage();
  const { isBackendHealthy } = useAuth();
  const [isLangMenuOpen, setIsLangMenuOpen] = useState(false);

  const navItems = [
    { path: '/', label: t('nav.home') || 'Home', icon: Home },
    { path: '/assistant', label: t('nav.assistant') || 'AI Health Assistant', icon: Bot, badge: 'AI' },
    { path: '/healthcare-map', label: t('nav.map') || 'Healthcare Map', icon: MapPin },
    { path: '/find-healthcare', label: t('nav.find') || 'Find Healthcare', icon: Compass },
    { path: '/documents', label: t('nav.documents') || 'Medical Documents', icon: FileText },
    { path: '/voice-assistant', label: t('nav.voice') || 'Voice Assistant', icon: Mic },
    { path: '/community-care', label: t('nav.community') || 'Community Care', icon: HeartHandshake },
    { path: '/safety', label: t('nav.safety') || 'Safety Center', icon: ShieldAlert, alert: true },
  ];

  const currentLang = supportedLanguages.find((l) => l.code === language) || supportedLanguages[0];

  const sidebarContent = (
    <div className="flex flex-col h-full bg-slate-950 border-r border-slate-800/80 text-slate-300 select-none">
      {/* Brand Header */}
      <div className="flex items-center justify-between h-16 px-4 border-b border-slate-800/80 shrink-0">
        <Link
          to="/"
          onClick={onMobileClose}
          className="flex items-center gap-3 overflow-hidden group"
          title="ADAPT-AI Healthcare Intelligence"
        >
          <div className="relative flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-teal-500 text-slate-950 shadow-lg shadow-cyan-500/20 group-hover:scale-105 transition-transform shrink-0">
            <Activity className="w-5 h-5 stroke-[2.5]" />
            <span className="absolute -top-0.5 -right-0.5 flex h-2.5 w-2.5">
              <span
                className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${
                  isBackendHealthy ? 'bg-cyan-400' : 'bg-amber-400'
                }`}
              />
              <span
                className={`relative inline-flex rounded-full h-2.5 w-2.5 ${
                  isBackendHealthy ? 'bg-teal-400' : 'bg-amber-500'
                }`}
              />
            </span>
          </div>

          {!isCollapsed && (
            <motion.div
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -10 }}
              transition={{ duration: 0.2 }}
              className="overflow-hidden whitespace-nowrap"
            >
              <span className="text-base font-black tracking-wider bg-gradient-to-r from-cyan-400 via-teal-300 to-white bg-clip-text text-transparent">
                ADAPT-AI
              </span>
              <span className="block text-[10px] tracking-widest text-slate-400 font-medium uppercase">
                Healthcare Intelligence
              </span>
            </motion.div>
          )}
        </Link>

        {/* Mobile Close Button */}
        <button
          onClick={onMobileClose}
          className="md:hidden p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-900 transition-colors"
          aria-label="Close menu"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Desktop Collapse Toggle */}
        <button
          onClick={onToggleCollapse}
          className="hidden md:flex p-1.5 rounded-lg text-slate-500 hover:text-cyan-400 hover:bg-slate-900 transition-colors"
          title={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {isCollapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
        </button>
      </div>

      {/* Main Navigation Links */}
      <nav className="flex-1 overflow-y-auto px-3 py-4 space-y-1.5">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.path;

          return (
            <Link
              key={item.path}
              to={item.path}
              onClick={onMobileClose}
              title={isCollapsed ? item.label : undefined}
              className={`relative flex items-center gap-3.5 px-3 py-2.5 rounded-xl text-xs font-semibold transition-all group ${
                isActive
                  ? 'bg-gradient-to-r from-cyan-500/15 to-teal-500/10 text-cyan-300 border border-cyan-500/30 shadow-md shadow-cyan-950/40'
                  : 'text-slate-400 hover:text-white hover:bg-slate-900/80 hover:border-slate-800 border border-transparent'
              }`}
            >
              <div
                className={`flex items-center justify-center w-5 h-5 shrink-0 transition-transform group-hover:scale-110 ${
                  isActive ? 'text-cyan-400' : 'text-slate-400 group-hover:text-cyan-300'
                }`}
              >
                <Icon className="w-4 h-4" />
              </div>

              {!isCollapsed && (
                <span className="flex-1 truncate tracking-wide">{item.label}</span>
              )}

              {!isCollapsed && item.badge && (
                <span className="px-1.5 py-0.5 rounded-md text-[10px] font-bold bg-cyan-950 text-cyan-400 border border-cyan-800 shrink-0">
                  {item.badge}
                </span>
              )}

              {!isCollapsed && item.alert && (
                <span className="w-2 h-2 rounded-full bg-rose-500 shrink-0 animate-pulse" />
              )}
            </Link>
          );
        })}
      </nav>

      {/* Emergency Strip (when expanded) */}
      {!isCollapsed && (
        <div className="mx-3 mb-3 p-3 rounded-xl bg-gradient-to-r from-red-950/60 to-rose-950/40 border border-red-500/30">
          <div className="flex items-center justify-between text-xs font-bold text-rose-300 mb-1">
            <span>Emergency Support</span>
            <span className="text-[10px] bg-rose-900/80 px-1.5 py-0.5 rounded text-rose-200">
              India 24x7
            </span>
          </div>
          <p className="text-[11px] text-slate-300 mb-2 leading-tight">
            Acute chest pain or stroke symptoms?
          </p>
          <a
            href="tel:112"
            className="flex items-center justify-center gap-1.5 w-full py-1.5 rounded-lg bg-rose-600 hover:bg-rose-500 text-white text-xs font-bold shadow-md transition-colors"
          >
            <PhoneCall className="w-3.5 h-3.5" />
            <span>Call 112 / 108</span>
          </a>
        </div>
      )}

      {/* Bottom Controls: Language, Settings, & Status */}
      <div className="p-3 border-t border-slate-800/80 space-y-1.5 shrink-0 bg-slate-950/60">
        {/* Language selector toggle */}
        <div className="relative">
          <button
            onClick={() => setIsLangMenuOpen(!isLangMenuOpen)}
            className={`w-full flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-medium text-slate-400 hover:text-white hover:bg-slate-900 transition-colors ${
              isCollapsed ? 'justify-center' : 'justify-between'
            }`}
            title={`Current Language: ${currentLang.nativeName}`}
          >
            <div className="flex items-center gap-2.5 truncate">
              <Globe className="w-4 h-4 text-cyan-400 shrink-0" />
              {!isCollapsed && <span className="truncate">{currentLang.nativeName}</span>}
            </div>
            {!isCollapsed && (
              <span className="text-[10px] font-mono uppercase text-slate-500 bg-slate-900 px-1.5 py-0.5 rounded">
                {language}
              </span>
            )}
          </button>

          {/* Language dropdown menu */}
          {isLangMenuOpen && (
            <div className="absolute bottom-full left-0 mb-2 w-52 rounded-xl bg-slate-900 border border-slate-800 shadow-2xl py-1 z-50">
              <div className="px-3 py-1.5 text-[10px] font-bold text-slate-400 uppercase tracking-wider border-b border-slate-800">
                Select Interface Language
              </div>
              <div className="max-h-56 overflow-y-auto py-1">
                {supportedLanguages.map((lang) => (
                  <button
                    key={lang.code}
                    onClick={() => {
                      setLanguage(lang.code);
                      setIsLangMenuOpen(false);
                    }}
                    className={`w-full flex items-center justify-between px-3 py-2 text-xs text-left transition-colors ${
                      language === lang.code
                        ? 'bg-cyan-500/15 text-cyan-300 font-semibold'
                        : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                    }`}
                  >
                    <span className="flex items-center gap-2">
                      <span>{lang.flag}</span>
                      <span>{lang.nativeName}</span>
                    </span>
                    <span className="text-[10px] text-slate-500 uppercase">{lang.code}</span>
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Settings Route Link */}
        <Link
          to="/settings"
          onClick={onMobileClose}
          className={`flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-medium transition-colors ${
            location.pathname === '/settings'
              ? 'bg-cyan-500/15 text-cyan-300 font-semibold border border-cyan-500/30'
              : 'text-slate-400 hover:text-white hover:bg-slate-900'
          } ${isCollapsed ? 'justify-center' : ''}`}
          title="Settings & Privacy"
        >
          <Settings className="w-4 h-4 text-slate-400 shrink-0" />
          {!isCollapsed && <span>{t('nav.settings') || 'Settings & Privacy'}</span>}
        </Link>
      </div>
    </div>
  );

  return (
    <>
      {/* Desktop Persistent Left Sidebar */}
      <aside
        className={`hidden md:block fixed top-0 bottom-0 left-0 z-30 transition-all duration-300 ease-in-out ${
          isCollapsed ? 'w-[72px]' : 'w-[260px]'
        }`}
      >
        {sidebarContent}
      </aside>

      {/* Mobile Slide-in Drawer */}
      <AnimatePresence>
        {isMobileOpen && (
          <div className="md:hidden fixed inset-0 z-50 flex">
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={onMobileClose}
              className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm"
            />

            {/* Drawer */}
            <motion.div
              initial={{ x: '-100%' }}
              animate={{ x: 0 }}
              exit={{ x: '-100%' }}
              transition={{ type: 'spring', damping: 25, stiffness: 260 }}
              className="relative w-72 max-w-[85vw] h-full shadow-2xl z-10"
            >
              {sidebarContent}
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </>
  );
};

