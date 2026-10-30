import React, { useState } from 'react';
import {
  HeartHandshake,
  ShieldCheck,
  PhoneCall,
  ExternalLink,
  Pill,
  Droplet,
  Brain,
  Building,
  Heart,
  Users,
  CheckCircle2,
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { Card } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';

interface HealthScheme {
  id: string;
  name: string;
  hindiName: string;
  category: 'insurance' | 'generic_drugs' | 'blood' | 'mental_health' | 'maternal';
  badge: string;
  description: string;
  coverage: string;
  helpline: string;
  portalUrl: string;
  keyBenefits: string[];
}

const SCHEMES: HealthScheme[] = [
  {
    id: 'pmjay',
    name: 'Ayushman Bharat PM-JAY',
    hindiName: 'आयुष्मान भारत प्रधानमंत्री जन आरोग्य योजना',
    category: 'insurance',
    badge: 'Flagship Health Insurance',
    description:
      "World's largest government-funded health assurance scheme providing comprehensive secondary and tertiary care hospitalization coverage.",
    coverage: '₹5,00,000 per family per year (Cashless across 28,000+ empanelled hospitals)',
    helpline: '14555',
    portalUrl: 'https://pmjay.gov.in',
    keyBenefits: [
      'Cashless & paperless treatment at public & private empanelled hospitals',
      'Covers pre-existing conditions from Day 1',
      'No cap on family size, age, or gender',
      'Includes diagnostic tests, medications, and 15 days post-hospitalization care',
    ],
  },
  {
    id: 'pmbjp',
    name: 'Pradhan Mantri Bhartiya Janaushadhi Pariyojana (PMBJP)',
    hindiName: 'प्रधानमंत्री भारतीय जन औषधि परियोजना',
    category: 'generic_drugs',
    badge: 'Affordable Generic Medicines',
    description:
      'Making quality generic medicines accessible at 50% to 90% lower prices compared to branded equivalents through 10,000+ Kendras.',
    coverage: '1,965 generic medicines & 293 surgical items',
    helpline: '1800-180-8080',
    portalUrl: 'https://janaushadhi.gov.in',
    keyBenefits: [
      'WHO-GMP compliant manufacturing quality',
      'Suvidha oxo-biodegradable sanitary napkins at ₹1 each',
      'Chronic disease medications (diabetes, cardiac, hypertension) at fraction of retail',
      'Dedicated Jan Aushadhi Sugam mobile locator',
    ],
  },
  {
    id: 'eraktkosh',
    name: 'e-RaktKosh National Blood Portal',
    hindiName: 'ई-रक्तकोष राष्ट्रीय रक्त बैंक नेटवर्क',
    category: 'blood',
    badge: 'Live Blood Stock & Donors',
    description:
      'Centralized digital platform connecting all licensed blood centres across India to monitor real-time availability of blood units and components.',
    coverage: '3,800+ Blood Centres Nationwide',
    helpline: '104 / 1917',
    portalUrl: 'https://www.eraktkosh.in',
    keyBenefits: [
      'Live search for available blood groups (A, B, AB, O positive/negative)',
      'Voluntary donor appointment scheduling',
      'Free blood transfusions for Thalassemia and Hemophilia patients',
      'Standardized blood safety and nucleic acid testing (NAT)',
    ],
  },
  {
    id: 'tele-manas',
    name: 'Tele-MANAS (Mental Health Helpline)',
    hindiName: 'टेली-मानस मानसिक स्वास्थ्य सेवा',
    category: 'mental_health',
    badge: '24x7 Free Psychological Care',
    description:
      'National tele-mental health programme anchored by NIMHANS providing 24x7 toll-free mental health counseling in 20+ Indian languages.',
    coverage: '24x7 Toll-Free Across All 36 States/UTs',
    helpline: '14416 / 1800-891-4416',
    portalUrl: 'https://telemanas.mohfw.gov.in',
    keyBenefits: [
      'Immediate crisis intervention for anxiety, depression, exam stress, and trauma',
      'Confidential and anonymous consultations',
      'Referral to district mental health programmes and psychiatric centres',
      'Available in regional languages with trained clinical psychologists',
    ],
  },
  {
    id: 'arogya-mandir',
    name: 'Ayushman Arogya Mandirs (PHCs)',
    hindiName: 'आयुष्मान आरोग्य मंदिर',
    category: 'maternal',
    badge: 'Comprehensive Primary Health',
    description:
      'Transformed Primary Health Centres (PHCs) and Sub-Centres delivering essential primary healthcare closer to homes in rural and urban India.',
    coverage: '160,000+ Operational Arogya Mandirs',
    helpline: '1075',
    portalUrl: 'https://ab-hws.nhp.gov.in',
    keyBenefits: [
      'Free essential medicines and 60+ free point-of-care diagnostics',
      'Maternal, neonatal, and child health immunization',
      'Universal screening for hypertension, diabetes, oral, breast, and cervical cancers',
      'Yoga and wellness sessions for preventive lifestyle care',
    ],
  },
];

export const CommunityCare: React.FC = () => {
  const { t } = useLanguage();
  const [filter, setFilter] = useState<string>('all');

  const filteredSchemes = SCHEMES.filter(
    (s) => filter === 'all' || s.category === filter
  );

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-10">
      {/* Page Header */}
      <div className="text-center max-w-3xl mx-auto space-y-3">
        <Badge variant="cyan" className="mx-auto">
          Public Health Inclusivity
        </Badge>
        <h1 className="text-3xl sm:text-4xl font-black text-white tracking-tight">
          Community Care & National Health Initiatives
        </h1>
        <p className="text-xs sm:text-sm text-slate-400 leading-relaxed">
          Connecting Indian citizens directly to universal healthcare guarantees: Ayushman Bharat,
          low-cost Jan Aushadhi generic medicines, nationwide blood availability, and Tele-MANAS mental health.
        </p>
      </div>

      {/* Emergency Helpline Strip */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <Card className="p-4 bg-slate-900 border-red-500/30 text-center space-y-1">
          <PhoneCall className="w-5 h-5 text-rose-400 mx-auto" />
          <div className="text-lg font-black text-white">112</div>
          <div className="text-[11px] font-semibold text-rose-300">National Emergency</div>
          <a href="tel:112" className="text-[10px] text-cyan-400 block hover:underline">
            Tap to Call
          </a>
        </Card>

        <Card className="p-4 bg-slate-900 border-amber-500/30 text-center space-y-1">
          <PhoneCall className="w-5 h-5 text-amber-400 mx-auto" />
          <div className="text-lg font-black text-white">108</div>
          <div className="text-[11px] font-semibold text-amber-300">Free Ambulance</div>
          <a href="tel:108" className="text-[10px] text-cyan-400 block hover:underline">
            Tap to Call
          </a>
        </Card>

        <Card className="p-4 bg-slate-900 border-teal-500/30 text-center space-y-1">
          <PhoneCall className="w-5 h-5 text-teal-400 mx-auto" />
          <div className="text-lg font-black text-white">14416</div>
          <div className="text-[11px] font-semibold text-teal-300">Tele-MANAS Mental Health</div>
          <a href="tel:14416" className="text-[10px] text-cyan-400 block hover:underline">
            Tap to Call
          </a>
        </Card>

        <Card className="p-4 bg-slate-900 border-cyan-500/30 text-center space-y-1">
          <PhoneCall className="w-5 h-5 text-cyan-400 mx-auto" />
          <div className="text-lg font-black text-white">1800-180-8080</div>
          <div className="text-[11px] font-semibold text-cyan-300">PM Jan Aushadhi</div>
          <a href="tel:18001808080" className="text-[10px] text-cyan-400 block hover:underline">
            Tap to Call
          </a>
        </Card>
      </div>

      {/* Filter Tabs */}
      <div className="flex flex-wrap items-center justify-center gap-2">
        {[
          { id: 'all', label: 'All Initiatives' },
          { id: 'insurance', label: 'PM-JAY Health Cover' },
          { id: 'generic_drugs', label: 'Jan Aushadhi Generic Drugs' },
          { id: 'blood', label: 'e-RaktKosh Blood Network' },
          { id: 'mental_health', label: 'Tele-MANAS Mental Support' },
          { id: 'maternal', label: 'Primary Care Centres (PHC)' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setFilter(tab.id)}
            className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-all ${
              filter === tab.id
                ? 'bg-cyan-500 text-slate-950 shadow-md shadow-cyan-500/20'
                : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Schemes Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {filteredSchemes.map((scheme) => (
          <Card key={scheme.id} hoverEffect className="p-6 border-slate-800 bg-slate-900/80 flex flex-col justify-between">
            <div>
              <div className="flex items-start justify-between gap-3 mb-2">
                <div>
                  <Badge variant="emerald" className="mb-1.5">
                    {scheme.badge}
                  </Badge>
                  <h3 className="text-lg font-bold text-white">{scheme.name}</h3>
                  <div className="text-xs text-teal-400 font-medium">{scheme.hindiName}</div>
                </div>
              </div>

              <p className="text-xs text-slate-300 leading-relaxed mt-2 mb-4">
                {scheme.description}
              </p>

              <div className="rounded-xl bg-slate-950 p-3 border border-slate-800/80 mb-4 space-y-1">
                <span className="text-[10px] font-bold uppercase tracking-wider text-cyan-400">
                  National Benefit / Coverage:
                </span>
                <p className="text-xs font-semibold text-white">{scheme.coverage}</p>
              </div>

              <div className="space-y-2 mb-6">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-400 block">
                  Key Citizen Entitlements:
                </span>
                {scheme.keyBenefits.map((b, idx) => (
                  <div key={idx} className="flex items-start gap-2 text-xs text-slate-300">
                    <CheckCircle2 className="w-3.5 h-3.5 text-teal-400 shrink-0 mt-0.5" />
                    <span>{b}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="flex items-center gap-3 pt-4 border-t border-slate-800">
              <a
                href={`tel:${scheme.helpline.replace(/[^0-9]/g, '')}`}
                className="flex-1 flex items-center justify-center gap-1.5 py-2 px-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 transition-colors"
              >
                <PhoneCall className="w-3.5 h-3.5 text-cyan-400" />
                <span>Helpline: {scheme.helpline}</span>
              </a>

              <a
                href={scheme.portalUrl}
                target="_blank"
                rel="noreferrer"
                className="flex-1 flex items-center justify-center gap-1.5 py-2 px-3 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-xs font-semibold text-slate-950 shadow-sm transition-colors"
              >
                <span>Official Portal</span>
                <ExternalLink className="w-3.5 h-3.5" />
              </a>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};

