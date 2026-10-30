import React from 'react';
import { Link } from 'react-router-dom';
import { Activity, ShieldCheck, PhoneCall, AlertTriangle, Heart } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';

export const Footer: React.FC = () => {
  const { t } = useLanguage();

  return (
    <footer className="border-t border-slate-800/80 bg-slate-950/90 text-slate-400 mt-auto">
      {/* Emergency Strip */}
      <div className="bg-gradient-to-r from-red-950/40 via-rose-900/30 to-red-950/40 border-b border-red-900/30 py-3">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-wrap items-center justify-between gap-3 text-xs">
          <div className="flex items-center gap-2 text-rose-300 font-medium">
            <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0" />
            <span>Facing an urgent medical emergency or acute chest pain/stroke symptoms?</span>
          </div>
          <div className="flex items-center gap-4 text-xs font-semibold">
            <a
              href="tel:112"
              className="flex items-center gap-1.5 text-white bg-rose-600 hover:bg-rose-500 px-3 py-1 rounded-full shadow-md transition-colors"
            >
              <PhoneCall className="w-3.5 h-3.5" />
              <span>Call 112 (National Emergency)</span>
            </a>
            <a
              href="tel:108"
              className="flex items-center gap-1.5 text-rose-300 hover:text-white underline decoration-dotted"
            >
              <span>108 Ambulance</span>
            </a>
            <a
              href="tel:14416"
              className="hidden md:inline-flex items-center gap-1.5 text-rose-300 hover:text-white underline decoration-dotted"
            >
              <span>Tele-MANAS (14416)</span>
            </a>
          </div>
        </div>
      </div>

      {/* Main Footer Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand Info */}
          <div className="md:col-span-2 space-y-3">
            <div className="flex items-center gap-2.5">
              <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-gradient-to-tr from-cyan-500 to-teal-500 shadow-md">
                <Activity className="w-4 h-4 text-slate-950 stroke-[2.5]" />
              </div>
              <span className="text-base font-bold text-white tracking-wide">ADAPT-AI</span>
              <span className="text-xs px-2 py-0.5 rounded-full bg-cyan-950 text-cyan-400 border border-cyan-800">
                v1.0.0 India
              </span>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed max-w-md">
              Adaptive clinical intelligence combining retrieval-augmented generation (RAG) over
              peer-reviewed medical guidelines (NICE, WHO, CDC, AIIMS) with deterministic emergency
              triage, multimodal lab interpretation, and nationwide healthcare facility discovery.
            </p>
            <div className="flex items-center gap-2 text-xs text-emerald-400 pt-1">
              <ShieldCheck className="w-4 h-4 shrink-0" />
              <span>Strict Zero-Hallucination Retrieval & Regulatory Safe Boundaries</span>
            </div>
          </div>

          {/* Core Modules */}
          <div>
            <h4 className="text-xs font-semibold text-slate-200 uppercase tracking-wider mb-3">
              Core Modules
            </h4>
            <ul className="space-y-2 text-xs">
              <li>
                <Link to="/assistant" className="hover:text-cyan-400 transition-colors">
                  {t('nav.assistant')}
                </Link>
              </li>
              <li>
                <Link to="/healthcare-map" className="hover:text-cyan-400 transition-colors">
                  {t('nav.map')}
                </Link>
              </li>
              <li>
                <Link to="/find-healthcare" className="hover:text-cyan-400 transition-colors">
                  {t('nav.find')}
                </Link>
              </li>
              <li>
                <Link to="/documents" className="hover:text-cyan-400 transition-colors">
                  {t('nav.documents')}
                </Link>
              </li>
              <li>
                <Link to="/voice-assistant" className="hover:text-cyan-400 transition-colors">
                  {t('nav.voice')}
                </Link>
              </li>
            </ul>
          </div>

          {/* National Resources & Safety */}
          <div>
            <h4 className="text-xs font-semibold text-slate-200 uppercase tracking-wider mb-3">
              National Health & Safety
            </h4>
            <ul className="space-y-2 text-xs">
              <li>
                <Link to="/safety" className="hover:text-cyan-400 transition-colors">
                  Clinical Safety & FAST Protocol
                </Link>
              </li>
              <li>
                <Link to="/community-care" className="hover:text-cyan-400 transition-colors">
                  Ayushman Bharat & PM-JAY
                </Link>
              </li>
              <li>
                <a
                  href="https://janaushadhi.gov.in"
                  target="_blank"
                  rel="noreferrer"
                  className="hover:text-cyan-400 transition-colors"
                >
                  PM Jan Aushadhi Generic Drugs
                </a>
              </li>
              <li>
                <a
                  href="https://www.eraktkosh.in"
                  target="_blank"
                  rel="noreferrer"
                  className="hover:text-cyan-400 transition-colors"
                >
                  e-RaktKosh Blood Availability
                </a>
              </li>
              <li>
                <a
                  href="https://telemanas.mohfw.gov.in"
                  target="_blank"
                  rel="noreferrer"
                  className="hover:text-cyan-400 transition-colors"
                >
                  Tele-MANAS Mental Health
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Regulatory Disclaimer Notice */}
        <div className="mt-8 pt-6 border-t border-slate-800 text-[11px] text-slate-500 space-y-2">
          <p className="leading-relaxed">
            <strong className="text-slate-400">Clinical Disclaimer:</strong> ADAPT-AI is an
            informational clinical decision support and health education tool. It is not an FDA- or
            CDSCO-approved medical device, does not formulate definitive diagnoses, and does not prescribe
            medications. Always seek the advice of a qualified physician or other licensed healthcare
            provider with any questions regarding a medical condition.
          </p>
          <div className="flex flex-wrap items-center justify-between gap-2 pt-2 text-slate-600">
            <span>© {new Date().getFullYear()} ADAPT-AI Healthcare Intelligence. All rights reserved.</span>
            <span className="flex items-center gap-1">
              Engineered with <Heart className="w-3 h-3 text-rose-500 fill-rose-500 inline" /> for public health.
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
};

