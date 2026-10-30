import React, { useState, useEffect } from 'react';
import {
  MapPin,
  Search,
  Filter,
  Navigation,
  Compass,
  AlertTriangle,
  RotateCcw,
  Sliders,
  Map as MapIcon,
  List,
  Columns,
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { Facility, FacilityType } from '../types';
import {
  fetchNearbyFacilities,
  CURATED_FACILITIES,
  calculateDistanceKm,
} from '../services/osmHealthcare';
import { LeafletMap } from '../components/map/LeafletMap';
import { FacilityCard } from '../components/map/FacilityCard';
import { Button } from '../components/ui/Button';

// Known Indian city coordinate anchors for manual location jump
const CITY_COORDINATES: Record<string, [number, number]> = {
  delhi: [28.6139, 77.209],
  'new delhi': [28.5672, 77.21],
  mumbai: [19.076, 72.8777],
  bengaluru: [12.9716, 77.5946],
  bangalore: [12.9716, 77.5946],
  chennai: [13.0827, 80.2707],
  kolkata: [22.5726, 88.3639],
  hyderabad: [17.385, 78.4867],
  chandigarh: [30.7333, 76.7794],
  lucknow: [26.8467, 80.9462],
  jaipur: [26.9124, 75.7873],
  pune: [18.5204, 73.8567],
  ahmedabad: [23.0225, 72.5714],
};

export const HealthcareMap: React.FC = () => {
  const { t } = useLanguage();

  // Default coordinate: New Delhi (AIIMS area)
  const DEFAULT_COORDS: [number, number] = [28.5672, 77.21];

  const [coords, setCoords] = useState<[number, number]>(DEFAULT_COORDS);
  const [userLocation, setUserLocation] = useState<[number, number] | null>(null);
  const [radiusKm, setRadiusKm] = useState<number>(25);
  const [typeFilter, setTypeFilter] = useState<FacilityType | 'all'>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [facilities, setFacilities] = useState<Facility[]>([]);
  const [selectedFacility, setSelectedFacility] = useState<Facility | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [locationStatus, setLocationStatus] = useState<string>('Location: New Delhi (Default)');
  const [viewMode, setViewMode] = useState<'split' | 'map' | 'list'>('split');

  useEffect(() => {
    loadFacilities();
  }, [coords, radiusKm, typeFilter]);

  const loadFacilities = async () => {
    setIsLoading(true);
    try {
      const filter = typeFilter === 'all' ? undefined : typeFilter;
      const results = await fetchNearbyFacilities(coords[0], coords[1], radiusKm, filter);
      setFacilities(results);
    } catch {
      const fallback = CURATED_FACILITIES.map((f) => ({
        ...f,
        distanceKm: calculateDistanceKm(coords[0], coords[1], f.lat, f.lon),
      }));
      setFacilities(fallback);
    } finally {
      setIsLoading(false);
    }
  };

  const handleGetLocation = () => {
    if (!navigator.geolocation) {
      setLocationStatus('GPS not supported. Please type your city.');
      return;
    }

    setLocationStatus('Locating GPS position...');
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const userCoords: [number, number] = [pos.coords.latitude, pos.coords.longitude];
        setUserLocation(userCoords);
        setCoords(userCoords);
        setLocationStatus(`GPS Locked (${userCoords[0].toFixed(3)}, ${userCoords[1].toFixed(3)})`);
      },
      (err) => {
        setLocationStatus(`GPS unavailable (${err.message}). Showing verified directory.`);
      },
      { timeout: 8000, enableHighAccuracy: true }
    );
  };

  const handleManualLocationSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const cityKey = searchQuery.trim().toLowerCase();
    if (CITY_COORDINATES[cityKey]) {
      const targetCoords = CITY_COORDINATES[cityKey];
      setCoords(targetCoords);
      setUserLocation(targetCoords);
      setLocationStatus(`City: ${searchQuery} (${targetCoords[0]}, ${targetCoords[1]})`);
    } else {
      // Filter list directly by query
      loadFacilities();
    }
  };

  const filteredFacilities = facilities.filter((f) => {
    if (!searchQuery.trim()) return true;
    const q = searchQuery.toLowerCase();
    return (
      f.name.toLowerCase().includes(q) ||
      f.address.toLowerCase().includes(q) ||
      f.city.toLowerCase().includes(q) ||
      (f.pincode && f.pincode.includes(q))
    );
  });

  return (
    <div className="space-y-6">
      {/* Header and Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-white flex items-center gap-2.5">
            <Compass className="w-6 h-6 text-cyan-400" />
            <span>{t('map.title') || 'Interactive Healthcare Map'}</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Discover AIIMS, district civil hospitals, PHCs, Jan Aushadhi Kendras, and blood banks.
          </p>
        </div>

        <div className="flex items-center gap-2.5">
          {/* View Mode Toggle */}
          <div className="flex items-center bg-slate-900 border border-slate-800 rounded-xl p-1">
            <button
              onClick={() => setViewMode('split')}
              className={`p-1.5 rounded-lg text-xs font-semibold flex items-center gap-1 transition-colors ${
                viewMode === 'split' ? 'bg-cyan-500/20 text-cyan-300' : 'text-slate-400 hover:text-white'
              }`}
              title="Split View (Map + List)"
            >
              <Columns className="w-4 h-4" />
              <span className="hidden lg:inline">Split</span>
            </button>
            <button
              onClick={() => setViewMode('map')}
              className={`p-1.5 rounded-lg text-xs font-semibold flex items-center gap-1 transition-colors ${
                viewMode === 'map' ? 'bg-cyan-500/20 text-cyan-300' : 'text-slate-400 hover:text-white'
              }`}
              title="Map Only"
            >
              <MapIcon className="w-4 h-4" />
              <span className="hidden lg:inline">Map</span>
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`p-1.5 rounded-lg text-xs font-semibold flex items-center gap-1 transition-colors ${
                viewMode === 'list' ? 'bg-cyan-500/20 text-cyan-300' : 'text-slate-400 hover:text-white'
              }`}
              title="List Only"
            >
              <List className="w-4 h-4" />
              <span className="hidden lg:inline">List</span>
            </button>
          </div>

          <Button
            variant="emerald"
            size="sm"
            onClick={handleGetLocation}
            icon={<Navigation className="w-3.5 h-3.5" />}
          >
            Locate Me
          </Button>
          <Button
            variant="secondary"
            size="sm"
            onClick={loadFacilities}
            isLoading={isLoading}
            icon={<RotateCcw className="w-3.5 h-3.5 text-slate-400" />}
          >
            Refresh
          </Button>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="rounded-2xl bg-slate-900/80 border border-slate-800 p-4 space-y-3">
        <div className="grid grid-cols-1 md:grid-cols-12 gap-3">
          {/* Search box with manual city jump */}
          <form onSubmit={handleManualLocationSubmit} className="md:col-span-8 relative">
            <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search by city (Delhi, Mumbai, Bengaluru), hospital name, or PIN code..."
              className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-10 pr-20 py-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500"
            />
            <button
              type="submit"
              className="absolute right-2 top-1/2 -translate-y-1/2 px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-[11px] font-semibold text-slate-300"
            >
              Search
            </button>
          </form>

          {/* Radius selector */}
          <div className="md:col-span-4 flex items-center gap-3 bg-slate-950 border border-slate-800 rounded-xl px-3 py-2">
            <Sliders className="w-4 h-4 text-cyan-400 shrink-0" />
            <span className="text-xs text-slate-400 shrink-0">Radius:</span>
            <input
              type="range"
              min={5}
              max={50}
              step={5}
              value={radiusKm}
              onChange={(e) => setRadiusKm(Number(e.target.value))}
              className="w-full accent-cyan-500 h-1.5 bg-slate-800 rounded-lg cursor-pointer"
            />
            <span className="text-xs font-bold text-cyan-400 font-mono shrink-0">
              {radiusKm} km
            </span>
          </div>
        </div>

        {/* Category Filter Pills */}
        <div className="flex flex-wrap items-center gap-2 pt-1 border-t border-slate-800/60">
          <span className="text-[11px] font-semibold text-slate-400 mr-1 flex items-center gap-1">
            <Filter className="w-3 h-3" />
            <span>Category:</span>
          </span>

          {[
            { id: 'all', label: 'All Facilities' },
            { id: 'hospital', label: 'Hospitals (24x7)' },
            { id: 'clinic', label: 'Clinics & Outpatient' },
            { id: 'phc', label: 'Primary Health Centres (PHC)' },
            { id: 'pharmacy', label: 'Pharmacies' },
            { id: 'jan_aushadhi', label: 'Jan Aushadhi Kendras' },
            { id: 'blood_bank', label: 'Blood Banks' },
          ].map((item) => (
            <button
              key={item.id}
              onClick={() => setTypeFilter(item.id as any)}
              className={`px-2.5 py-1 rounded-lg text-xs font-medium transition-all ${
                typeFilter === item.id
                  ? 'bg-cyan-500 text-slate-950 font-bold shadow-sm'
                  : 'bg-slate-800/80 text-slate-300 hover:text-white hover:bg-slate-800'
              }`}
            >
              {item.label}
            </button>
          ))}

          <span className="text-[11px] text-slate-500 ml-auto hidden sm:inline">
            {locationStatus}
          </span>
        </div>
      </div>

      {/* Main Map + Facility List Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left Side: Facility Cards Scroll List */}
        {(viewMode === 'split' || viewMode === 'list') && (
          <div
            className={`${
              viewMode === 'list' ? 'lg:col-span-12' : 'lg:col-span-5'
            } space-y-3 max-h-[720px] overflow-y-auto pr-1`}
          >
            <div className="flex items-center justify-between text-xs text-slate-400 px-1">
              <span>
                Found <strong>{filteredFacilities.length}</strong> facilities within {radiusKm} km
              </span>
              {isLoading && <span className="text-cyan-400 animate-pulse">Loading map data...</span>}
            </div>

            {filteredFacilities.length === 0 ? (
              <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-8 text-center space-y-2">
                <AlertTriangle className="w-8 h-8 text-amber-400 mx-auto" />
                <h3 className="text-sm font-semibold text-white">No facilities found</h3>
                <p className="text-xs text-slate-400">
                  Try widening your search radius or clearing query filters.
                </p>
                <Button
                  variant="secondary"
                  size="sm"
                  onClick={() => {
                    setSearchQuery('');
                    setRadiusKm(50);
                    setTypeFilter('all');
                  }}
                >
                  Reset Filters
                </Button>
              </div>
            ) : (
              <div className={viewMode === 'list' ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4' : 'space-y-3'}>
                {filteredFacilities.map((facility) => (
                  <FacilityCard
                    key={facility.id}
                    facility={facility}
                    isSelected={selectedFacility?.id === facility.id}
                    onSelect={() => setSelectedFacility(facility)}
                  />
                ))}
              </div>
            )}
          </div>
        )}

        {/* Right Side: Leaflet Interactive Map */}
        {(viewMode === 'split' || viewMode === 'map') && (
          <div
            className={`${
              viewMode === 'map' ? 'lg:col-span-12' : 'lg:col-span-7'
            } h-[720px] sticky top-16`}
          >
            <LeafletMap
              center={coords}
              zoom={12}
              userLocation={userLocation}
              facilities={filteredFacilities}
              selectedFacility={selectedFacility}
              onSelectFacility={(fac) => setSelectedFacility(fac)}
              radiusKm={radiusKm}
            />
          </div>
        )}
      </div>
    </div>
  );
};
