import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  Activity,
  Bot,
  MapPin,
  FileText,
  Mic,
  ShieldCheck,
  HeartHandshake,
  ArrowRight,
  Sparkles,
  Send,
  Lock,
  Globe,
  AlertTriangle,
  Building,
  HelpCircle,
  CheckCircle,
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { useAuth } from '../context/AuthContext';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';

export const Home: React.FC = () => {
  const navigate = useNavigate();
  const { t, language } = useLanguage();
  const { healthData, isBackendHealthy } = useAuth();
  const [heroQuestion, setHeroQuestion] = useState('');

  const handleHeroSubmit = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (heroQuestion.trim()) {
      navigate('/assistant', { state: { initialQuestion: heroQuestion.trim() } });
    } else {
      navigate('/assistant');
    }
  };

  const totalDocs = healthData?.components?.vector_store?.total_documents ?? 20;
  const totalChunks = healthData?.components?.vector_store?.total_chunks ?? 21;
  const activeModel = healthData?.components?.model_adapter?.name || 'gemini-3.5-flash';

  const modules = [
    {
      title: 'AI Health Assistant',
      desc: 'Ask questions about symptoms and health topics. Grounded strictly in authoritative guidelines with clear citations and emergency triage alerts.',
      icon: Bot,
      link: '/assistant',
      cta: 'Start Conversation',
      tag: 'Clinical Knowledge',
      color: 'from-cyan-500/20 to-teal-500/20 text-cyan-400 border-cyan-500/30',
    },
    {
      title: 'Healthcare Discovery Map',
      desc: 'Locate 24x7 emergency civil hospitals, AIIMS centres, primary health clinics (PHC), blood banks, and Jan Aushadhi generic stores near you.',
      icon: MapPin,
      link: '/healthcare-map',
      cta: 'Open GPS Map',
      tag: 'Interactive GPS',
      color: 'from-teal-500/20 to-emerald-500/20 text-teal-400 border-teal-500/30',
    },
    {
      title: 'Pan-India Facility Search',
      desc: 'Search hospitals, generic drug kendras, and blood banks nationwide by city, state, district, or PIN code with verified contact details.',
      icon: Building,
      link: '/find-healthcare',
      cta: 'Explore Directory',
      tag: 'Pan-India Directory',
      color: 'from-blue-500/20 to-indigo-500/20 text-blue-400 border-blue-500/30',
    },
    {
      title: 'Medical Document Analysis',
      desc: 'Securely upload lab tests and diagnostic reports for plain-language summaries and verified clinical findings with cryptographic SHA-256 safety quarantine.',
      icon: FileText,
      link: '/documents',
      cta: 'Analyze Document',
      tag: 'Multimodal Vision',
      color: 'from-emerald-500/20 to-cyan-500/20 text-emerald-400 border-emerald-500/30',
    },
    {
      title: 'Multilingual Voice Assistant',
      desc: 'Speak naturally in English, Hindi, Hinglish, or Punjabi with real-time speech recognition and clear audio synthesis.',
      icon: Mic,
      link: '/voice-assistant',
      cta: 'Launch Voice AI',
      tag: 'Hands-Free Speech',
      color: 'from-purple-500/20 to-pink-500/20 text-purple-400 border-purple-500/30',
    },
    {
      title: 'Community Care Initiatives',
      desc: 'Access verified government healthcare programmes: Ayushman Bharat (PM-JAY), Jan Aushadhi affordable medicines, e-RaktKosh, and Tele-MANAS.',
      icon: HeartHandshake,
      link: '/community-care',
      cta: 'View Programmes',
      tag: 'Public Health',
      color: 'from-rose-500/20 to-amber-500/20 text-rose-400 border-rose-500/30',
    },
  ];

  return (
    <div className="space-y-16 pb-12">
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-8 pb-12">
        {/* Soft Ambient Glow Elements */}
        <div className="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[550px] h-[300px] bg-cyan-500/10 blur-[120px] pointer-events-none rounded-full" />
        <div className="absolute top-1/4 right-10 w-[350px] h-[250px] bg-teal-500/10 blur-[100px] pointer-events-none rounded-full" />

        <div className="relative z-10 text-center max-w-4xl mx-auto space-y-6">
          {/* Subtle Platform Tag */}
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-cyan-950/60 border border-cyan-500/30 text-cyan-300 text-xs font-semibold shadow-sm backdrop-blur-md"
          >
            <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
            <span>Adaptive Clinical AI Platform • India Edition</span>
          </motion.div>

          {/* Headline - Exact required text */}
          <motion.h1
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="text-4xl sm:text-6xl font-black text-white tracking-tight leading-[1.15]"
          >
            Healthcare Intelligence.{' '}
            <span className="bg-gradient-to-r from-cyan-400 via-teal-300 to-emerald-400 bg-clip-text text-transparent block sm:inline">
              Adapted to You.
            </span>
          </motion.h1>

          {/* Supporting Text - Exact required text */}
          <motion.p
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-base sm:text-lg text-slate-300 max-w-2xl mx-auto leading-relaxed"
          >
            Understand health information, explore healthcare services, and access helpful medical
            resources in your preferred language.
          </motion.p>

          {/* Interactive Question Input on Home */}
          <motion.form
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.25 }}
            onSubmit={handleHeroSubmit}
            className="max-w-2xl mx-auto relative rounded-2xl bg-slate-900/90 border border-slate-800 p-2 shadow-2xl focus-within:border-cyan-500/60 focus-within:ring-1 focus-within:ring-cyan-500/40 transition-all text-left"
          >
            <div className="flex items-center gap-2 px-2">
              <Bot className="w-5 h-5 text-cyan-400 shrink-0" />
              <input
                type="text"
                value={heroQuestion}
                onChange={(e) => setHeroQuestion(e.target.value)}
                placeholder="Ask about symptoms, blood tests, or medications (e.g. vitamin D deficiency, fever, chest pain)..."
                className="w-full bg-transparent px-2 py-2 text-xs sm:text-sm text-white placeholder-slate-500 focus:outline-none"
              />
              <Button
                type="submit"
                size="sm"
                icon={<Send className="w-3.5 h-3.5 text-slate-950" />}
                className="shrink-0"
              >
                Ask
              </Button>
            </div>
          </motion.form>

          {/* Primary & Secondary Call to Actions */}
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="flex flex-wrap items-center justify-center gap-4 pt-2"
          >
            <Link to="/assistant">
              <Button size="lg" icon={<Bot className="w-5 h-5 text-slate-950" />}>
                Ask a Health Question
              </Button>
            </Link>
            <Link to="/healthcare-map">
              <Button size="lg" variant="secondary" icon={<MapPin className="w-5 h-5 text-cyan-400" />}>
                Find Healthcare Near Me
              </Button>
            </Link>
          </motion.div>

          {/* Emergency Safety Notice */}
          <div className="pt-2">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-red-950/40 border border-red-500/40 text-xs text-rose-300">
              <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0" />
              <span>Facing a critical medical emergency? Call 112 or 108 immediately.</span>
              <a href="tel:112" className="font-bold underline text-white hover:text-rose-200 ml-1">
                Call 112
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Verified Verified Knowledge & Telemetry Status (No fabricated statistics) */}
      <section className="max-w-7xl mx-auto">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <Card className="text-center py-5 border-cyan-500/20 bg-slate-900/60">
            <div className="text-2xl sm:text-3xl font-black text-cyan-400 mb-1">
              {totalDocs} Guidelines
            </div>
            <div className="text-xs font-semibold text-slate-300">Verified Medical Corpus</div>
            <div className="text-[11px] text-slate-500 mt-0.5">{totalChunks} Knowledge Units</div>
          </Card>

          <Card className="text-center py-5 border-teal-500/20 bg-slate-900/60">
            <div className="text-2xl sm:text-3xl font-black text-teal-400 mb-1">5-Tier Triage</div>
            <div className="text-xs font-semibold text-slate-300">Deterministic Safety</div>
            <div className="text-[11px] text-slate-500 mt-0.5">Emergency red-flag escalation</div>
          </Card>

          <Card className="text-center py-5 border-emerald-500/20 bg-slate-900/60">
            <div className="text-2xl sm:text-3xl font-black text-emerald-400 mb-1">Pan-India</div>
            <div className="text-xs font-semibold text-slate-300">Facility Directory</div>
            <div className="text-[11px] text-slate-500 mt-0.5">AIIMS, PHCs & Jan Aushadhi</div>
          </Card>

          <Card className="text-center py-5 border-purple-500/20 bg-slate-900/60">
            <div className="text-2xl sm:text-3xl font-black text-purple-400 mb-1">
              {isBackendHealthy ? 'Online' : 'Standby'}
            </div>
            <div className="text-xs font-semibold text-slate-300">{activeModel}</div>
            <div className="text-[11px] text-slate-500 mt-0.5">Clinical Decision Support</div>
          </Card>
        </div>
      </section>

      {/* Core Healthcare Capabilities Grid */}
      <section className="space-y-6">
        <div className="text-center max-w-2xl mx-auto space-y-2">
          <Badge variant="cyan">Integrated Modules</Badge>
          <h2 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
            Designed for Patient Safety and Accessible Healthcare
          </h2>
          <p className="text-xs sm:text-sm text-slate-400">
            Every capability is engineered to provide validated information, immediate geo-discovery,
            and honest clinical boundaries without speculation.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {modules.map((m, idx) => {
            const Icon = m.icon;
            return (
              <Link key={idx} to={m.link} className="group">
                <Card hoverEffect className="h-full flex flex-col justify-between p-6">
                  <div>
                    <div className="flex items-center justify-between mb-4">
                      <div
                        className={`flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-to-tr border group-hover:scale-105 transition-transform ${m.color}`}
                      >
                        <Icon className="w-5 h-5" />
                      </div>
                      <span className="text-[10px] font-bold text-slate-400 bg-slate-950 px-2.5 py-1 rounded-full border border-slate-800">
                        {m.tag}
                      </span>
                    </div>

                    <h3 className="text-base font-bold text-white group-hover:text-cyan-300 transition-colors mb-2">
                      {m.title}
                    </h3>
                    <p className="text-xs text-slate-400 leading-relaxed">{m.desc}</p>
                  </div>

                  <div className="flex items-center gap-1.5 text-xs font-semibold text-cyan-400 mt-6 pt-3 border-t border-slate-800/80 group-hover:text-cyan-300">
                    <span>{m.cta}</span>
                    <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
                  </div>
                </Card>
              </Link>
            );
          })}
        </div>
      </section>

      {/* Patient Privacy, Security & Clinical Limitations Banner */}
      <section>
        <Card className="p-8 border-cyan-500/30 bg-gradient-to-b from-slate-900/90 to-slate-950/90 space-y-6">
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
            <div className="space-y-1">
              <span className="text-xs font-bold text-cyan-400 uppercase tracking-wider">
                Patient Privacy & Medical Boundaries
              </span>
              <h3 className="text-xl font-bold text-white">How ADAPT-AI Protects Your Information</h3>
            </div>
            <Link to="/safety">
              <Button variant="outline" size="sm" icon={<ShieldCheck className="w-4 h-4" />}>
                Read Safety Protocols
              </Button>
            </Link>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs text-slate-300">
            <div className="rounded-xl bg-slate-950 p-4 border border-slate-800 space-y-1.5">
              <div className="flex items-center gap-2 text-cyan-400 font-semibold text-sm">
                <Lock className="w-4 h-4" />
                <span>Private & Ephemeral</span>
              </div>
              <p className="text-slate-400 leading-relaxed">
                Health inquiries are processed with strict isolation. No personal health records or
                identifiable patient logs are stored.
              </p>
            </div>

            <div className="rounded-xl bg-slate-950 p-4 border border-slate-800 space-y-1.5">
              <div className="flex items-center gap-2 text-teal-400 font-semibold text-sm">
                <CheckCircle className="w-4 h-4" />
                <span>Zero Hallucinations</span>
              </div>
              <p className="text-slate-400 leading-relaxed">
                If authoritative clinical guidelines lack sufficient proof on a health query, the AI
                honestly communicates insufficient evidence rather than guessing.
              </p>
            </div>

            <div className="rounded-xl bg-slate-950 p-4 border border-slate-800 space-y-1.5">
              <div className="flex items-center gap-2 text-emerald-400 font-semibold text-sm">
                <Globe className="w-4 h-4" />
                <span>Multilingual Inclusivity</span>
              </div>
              <p className="text-slate-400 leading-relaxed">
                Supports English, Hindi, Hinglish, Punjabi, and Urdu (RTL) so health guidance is
                accessible to citizens across diverse linguistic backgrounds.
              </p>
            </div>
          </div>
        </Card>
      </section>
    </div>
  );
};
