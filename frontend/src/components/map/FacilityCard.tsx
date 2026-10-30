import React from 'react';
import { MapPin, Phone, Clock, Bed, Navigation, ShieldCheck, AlertCircle } from 'lucide-react';
import { Facility } from '../../types';
import { Badge } from '../ui/Badge';

interface FacilityCardProps {
  facility: Facility;
  isSelected?: boolean;
  onSelect?: () => void;
}

export const FacilityCard: React.FC<FacilityCardProps> = ({
  facility,
  isSelected = false,
  onSelect,
}) => {
  const directionsUrl = `https://www.google.com/maps/dir/?api=1&destination=${facility.lat},${facility.lon}`;

  const typeLabels: Record<string, { label: string; variant: any }> = {
    hospital: { label: 'Hospital', variant: 'cyan' },
    clinic: { label: 'Clinic / Outpatient', variant: 'purple' },
    pharmacy: { label: 'Pharmacy', variant: 'emerald' },
    jan_aushadhi: { label: 'PM Jan Aushadhi', variant: 'emerald' },
    blood_bank: { label: 'Blood Bank', variant: 'rose' },
    phc: { label: 'Primary Health Centre (PHC)', variant: 'amber' },
  };

  const typeInfo = typeLabels[facility.type] || { label: facility.type, variant: 'slate' };

  return (
    <div
      onClick={onSelect}
      className={`relative rounded-xl border p-4 transition-all cursor-pointer ${
        isSelected
          ? 'bg-slate-900 border-cyan-500 shadow-lg shadow-cyan-500/10 ring-1 ring-cyan-500/50'
          : 'bg-slate-900/60 border-slate-800 hover:border-slate-700 hover:bg-slate-900/90'
      }`}
    >
      <div className="flex items-start justify-between gap-3 mb-2">
        <div>
          <div className="flex items-center gap-2 flex-wrap mb-1">
            <Badge variant={typeInfo.variant}>{typeInfo.label}</Badge>
            {facility.emergency && (
              <Badge variant="emergency" pulse>
                24x7 Emergency
              </Badge>
            )}
            {facility.distanceKm !== undefined && (
              <span className="text-xs font-semibold text-cyan-400 bg-cyan-950/60 px-2 py-0.5 rounded-md border border-cyan-500/30">
                {facility.distanceKm} km away
              </span>
            )}
          </div>
          <h3 className="text-sm font-bold text-white group-hover:text-cyan-300 transition-colors">
            {facility.name}
          </h3>
        </div>
      </div>

      <div className="space-y-1.5 text-xs text-slate-400 my-2.5">
        <div className="flex items-start gap-2">
          <MapPin className="w-3.5 h-3.5 text-slate-500 shrink-0 mt-0.5" />
          <span className="line-clamp-2">
            {facility.address}, {facility.city}, {facility.state} {facility.pincode ? `- ${facility.pincode}` : ''}
          </span>
        </div>

        {facility.operatingHours && (
          <div className="flex items-center gap-2">
            <Clock className="w-3.5 h-3.5 text-slate-500 shrink-0" />
            <span>{facility.operatingHours}</span>
          </div>
        )}

        {facility.beds && (
          <div className="flex items-center gap-2">
            <Bed className="w-3.5 h-3.5 text-cyan-500 shrink-0" />
            <span className="text-slate-300 font-medium">{facility.beds} Inpatient Beds</span>
          </div>
        )}
      </div>

      {facility.schemesSupported && facility.schemesSupported.length > 0 && (
        <div className="flex flex-wrap gap-1.5 my-2.5">
          {facility.schemesSupported.map((scheme, i) => (
            <span
              key={i}
              className="inline-flex items-center gap-1 text-[10px] font-medium bg-slate-950 px-2 py-0.5 rounded-md text-emerald-400 border border-emerald-500/30"
            >
              <ShieldCheck className="w-2.5 h-2.5" />
              <span>{scheme}</span>
            </span>
          ))}
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex items-center gap-2 mt-3 pt-2.5 border-t border-slate-800">
        {facility.phone ? (
          <a
            href={`tel:${facility.phone}`}
            onClick={(e) => e.stopPropagation()}
            className="flex-1 flex items-center justify-center gap-1.5 py-1.5 px-3 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 transition-colors"
          >
            <Phone className="w-3.5 h-3.5 text-teal-400" />
            <span>Call</span>
          </a>
        ) : (
          <span className="flex-1 text-[11px] text-slate-500 italic text-center py-1.5">
            Phone unlisted
          </span>
        )}

        <a
          href={directionsUrl}
          target="_blank"
          rel="noopener noreferrer"
          onClick={(e) => e.stopPropagation()}
          className="flex-1 flex items-center justify-center gap-1.5 py-1.5 px-3 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-xs font-semibold text-slate-950 shadow-sm transition-colors"
        >
          <Navigation className="w-3.5 h-3.5" />
          <span>Directions</span>
        </a>
      </div>
    </div>
  );
};

