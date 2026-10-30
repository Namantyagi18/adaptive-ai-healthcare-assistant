import React, { useState } from 'react';
import {
  Compass,
  Search,
  Filter,
  Building2,
  Phone,
  Navigation,
  ShieldCheck,
  Info,
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { FacilityType } from '../types';
import { searchFacilitiesNationwide } from '../services/osmHealthcare';
import { FacilityCard } from '../components/map/FacilityCard';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';

const INDIAN_STATES = [
  'ALL',
  'Delhi',
  'Maharashtra',
  'Karnataka',
  'Chandigarh',
  'Tamil Nadu',
  'Telangana',
  'West Bengal',
  'Uttar Pradesh',
  'Punjab',
  'Kerala',
  'Gujarat',
  'Rajasthan',
];

export const FindHealthcare: React.FC = () => {
  const { t } = useLanguage();
  const [query, setQuery] = useState('');
  const [selectedState, setSelectedState] = useState('ALL');
  const [selectedType, setSelectedType] = useState<FacilityType | 'all'>('all');
  const [emergencyOnly, setEmergencyOnly] = useState(false);

  const filterType = selectedType === 'all' ? undefined : selectedType;
  const filteredFacilities = searchFacilitiesNationwide(query, selectedState, filterType).filter(
    (f) => !emergencyOnly || f.emergency
  );

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center max-w-2xl mx-auto space-y-3">
        <Badge variant="cyan" className="mx-auto">
          Nationwide Health Directory
        </Badge>
        <h1 className="text-3xl font-black text-white tracking-tight">
          Find Healthcare Facilities Across India
        </h1>
        <p className="text-xs sm:text-sm text-slate-400">
          Search over verified AIIMS centres, Government Civil Hospitals, Ayushman Arogya Mandirs (PHC),
          Jan Aushadhi Kendras, and verified blood centres.
        </p>
      </div>

      {/* Filter Bar */}
      <div className="rounded-2xl bg-slate-900/90 border border-slate-800 p-6 shadow-xl space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-12 gap-4">
          {/* Main search input */}
          <div className="md:col-span-6 relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search by facility name, specialty, city, or PIN code (e.g. AIIMS, KEM, 110029)..."
              className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-10 pr-4 py-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500"
            />
          </div>

          {/* State selector */}
          <div className="md:col-span-3">
            <select
              value={selectedState}
              onChange={(e) => setSelectedState(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2.5 text-xs text-slate-200 focus:outline-none focus:border-cyan-500"
            >
              <option value="ALL">All States / UTs</option>
              {INDIAN_STATES.filter((s) => s !== 'ALL').map((state) => (
                <option key={state} value={state}>
                  {state}
                </option>
              ))}
            </select>
          </div>

          {/* Facility Type */}
          <div className="md:col-span-3">
            <select
              value={selectedType}
              onChange={(e) => setSelectedType(e.target.value as any)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2.5 text-xs text-slate-200 focus:outline-none focus:border-cyan-500"
            >
              <option value="all">All Facility Types</option>
              <option value="hospital">Hospitals (24x7 Emergency)</option>
              <option value="jan_aushadhi">Jan Aushadhi Generic Kendras</option>
              <option value="blood_bank">Blood Banks & Apheresis</option>
              <option value="phc">Primary Health Centres (PHC)</option>
              <option value="clinic">Clinics & Outpatient</option>
            </select>
          </div>
        </div>

        {/* Quick Filter Tags */}
        <div className="flex flex-wrap items-center gap-2 pt-2 border-t border-slate-800/80">
          <span className="text-[11px] font-semibold text-slate-400 mr-2 flex items-center gap-1">
            <Filter className="w-3 h-3" />
            <span>Quick Filters:</span>
          </span>

          <button
            onClick={() => setEmergencyOnly(!emergencyOnly)}
            className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
              emergencyOnly
                ? 'bg-rose-500 text-white shadow-md'
                : 'bg-slate-800 text-slate-300 hover:text-white'
            }`}
          >
            🚨 24x7 Emergency Only
          </button>

          <button
            onClick={() => setQuery('Ayushman')}
            className="px-3 py-1 rounded-lg text-xs font-medium bg-slate-800 text-slate-300 hover:text-emerald-400 transition-colors"
          >
            🛡️ Ayushman Bharat (PM-JAY)
          </button>

          <button
            onClick={() => setSelectedType('jan_aushadhi')}
            className="px-3 py-1 rounded-lg text-xs font-medium bg-slate-800 text-slate-300 hover:text-teal-400 transition-colors"
          >
            💊 Jan Aushadhi Generic Kendras
          </button>

          <button
            onClick={() => setSelectedType('blood_bank')}
            className="px-3 py-1 rounded-lg text-xs font-medium bg-slate-800 text-slate-300 hover:text-rose-400 transition-colors"
          >
            🩸 Blood Banks
          </button>

          {(query || selectedState !== 'ALL' || selectedType !== 'all' || emergencyOnly) && (
            <button
              onClick={() => {
                setQuery('');
                setSelectedState('ALL');
                setSelectedType('all');
                setEmergencyOnly(false);
              }}
              className="text-xs text-cyan-400 hover:underline ml-auto"
            >
              Clear All Filters
            </button>
          )}
        </div>
      </div>

      {/* Facilities Results Grid */}
      <div className="space-y-4">
        <div className="flex items-center justify-between text-xs text-slate-400">
          <span>
            Showing <strong>{filteredFacilities.length}</strong> verified healthcare institutions
          </span>
          <span className="flex items-center gap-1 text-slate-500">
            <Info className="w-3.5 h-3.5" />
            <span>Data: Verified National Public Health Corpus & OpenStreetMap</span>
          </span>
        </div>

        {filteredFacilities.length === 0 ? (
          <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-12 text-center space-y-3">
            <Building2 className="w-10 h-10 text-slate-500 mx-auto" />
            <h3 className="text-base font-bold text-white">No healthcare facilities matched</h3>
            <p className="text-xs text-slate-400 max-w-sm mx-auto">
              We couldn't find any facilities matching your filters. Try selecting "All States" or clearing the search keyword.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {filteredFacilities.map((facility) => (
              <FacilityCard key={facility.id} facility={facility} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
