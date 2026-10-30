/**
 * OpenStreetMap & India Healthcare Discovery Service
 * Provides GPS-based location search and curated directory of Indian healthcare facilities.
 */

import { Facility, FacilityType } from '../types';

// Curated high-reliability healthcare facilities directory across India
export const CURATED_FACILITIES: Facility[] = [
  // Delhi NCR
  {
    id: 'aiims-new-delhi',
    name: 'All India Institute of Medical Sciences (AIIMS)',
    type: 'hospital',
    address: 'Sri Aurobindo Marg, Ansari Nagar East',
    city: 'New Delhi',
    state: 'Delhi',
    pincode: '110029',
    lat: 28.5672,
    lon: 77.2100,
    phone: '+91-11-26588500',
    emergency: true,
    beds: 2478,
    operatingHours: '24x7 Emergency',
    schemesSupported: ['PM-JAY', 'CGHS', 'Ayushman Bharat', 'ECHS'],
  },
  {
    id: 'safdarjung-delhi',
    name: 'Safdarjung Hospital & Vardhman Mahavir Medical College',
    type: 'hospital',
    address: 'Ring Road, Opposite AIIMS',
    city: 'New Delhi',
    state: 'Delhi',
    pincode: '110029',
    lat: 28.5701,
    lon: 77.2076,
    phone: '+91-11-26165060',
    emergency: true,
    beds: 2000,
    operatingHours: '24x7 Emergency',
    schemesSupported: ['PM-JAY', 'CGHS', 'Ayushman Bharat'],
  },
  {
    id: 'jan-aushadhi-delhi-1',
    name: 'Pradhan Mantri Bhartiya Janaushadhi Kendra - AIIMS Gate',
    type: 'jan_aushadhi',
    address: 'Near Metro Station Gate 2, Ansari Nagar',
    city: 'New Delhi',
    state: 'Delhi',
    pincode: '110029',
    lat: 28.5685,
    lon: 77.2091,
    phone: '1800-180-8080',
    emergency: false,
    operatingHours: '08:00 AM - 10:00 PM',
    schemesSupported: ['PMBJP Affordable Generic Medicines'],
  },
  {
    id: 'red-cross-blood-bank-delhi',
    name: 'Indian Red Cross Society National Headquarters Blood Bank',
    type: 'blood_bank',
    address: '1 Red Cross Road',
    city: 'New Delhi',
    state: 'Delhi',
    pincode: '110001',
    lat: 28.6219,
    lon: 77.2105,
    phone: '+91-11-23711551',
    emergency: true,
    operatingHours: '24x7 Blood Bank & Apheresis',
    schemesSupported: ['Voluntary Blood Donation', 'ERCS'],
  },
  {
    id: 'phc-mehrauli',
    name: 'Primary Health Centre (PHC) Mehrauli',
    type: 'phc',
    address: 'Near Qutub Minar, Mehrauli',
    city: 'New Delhi',
    state: 'Delhi',
    pincode: '110030',
    lat: 28.5186,
    lon: 77.1856,
    phone: '+91-11-26643210',
    emergency: false,
    operatingHours: '09:00 AM - 04:00 PM',
    schemesSupported: ['Ayushman Arogya Mandir', 'MCH Immunization'],
  },

  // Mumbai / Maharashtra
  {
    id: 'kem-hospital-mumbai',
    name: 'King Edward Memorial (KEM) Hospital',
    type: 'hospital',
    address: 'Acharya Donde Marg, Parel',
    city: 'Mumbai',
    state: 'Maharashtra',
    pincode: '400012',
    lat: 18.9986,
    lon: 72.8427,
    phone: '+91-22-24107000',
    emergency: true,
    beds: 1800,
    operatingHours: '24x7 Emergency & Trauma',
    schemesSupported: ['Mahatma Jyotirao Phule Jan Arogya Yojana', 'PM-JAY'],
  },
  {
    id: 'tata-memorial-mumbai',
    name: 'Tata Memorial Hospital (Cancer Research & Care)',
    type: 'hospital',
    address: 'Dr. E Borges Road, Parel',
    city: 'Mumbai',
    state: 'Maharashtra',
    pincode: '400012',
    lat: 19.0042,
    lon: 72.8431,
    phone: '+91-22-24177000',
    emergency: true,
    beds: 700,
    operatingHours: '24x7 Critical Oncology Care',
    schemesSupported: ['PM-JAY', 'Government Subsidized Oncology'],
  },
  {
    id: 'jan-aushadhi-mumbai-1',
    name: 'Pradhan Mantri Jan Aushadhi Kendra - Dadar',
    type: 'jan_aushadhi',
    address: 'Shop 4, Swami Gyan Jivandas Marg, Dadar East',
    city: 'Mumbai',
    state: 'Maharashtra',
    pincode: '400014',
    lat: 19.0178,
    lon: 72.8478,
    phone: '1800-180-8080',
    emergency: false,
    operatingHours: '09:00 AM - 09:30 PM',
    schemesSupported: ['PMBJP Generic Medicines'],
  },

  // Bengaluru / Karnataka
  {
    id: 'nimhans-bengaluru',
    name: 'NIMHANS (National Institute of Mental Health and Neurosciences)',
    type: 'hospital',
    address: 'Hosur Road, Lakkasandra',
    city: 'Bengaluru',
    state: 'Karnataka',
    pincode: '560029',
    lat: 12.9392,
    lon: 77.5959,
    phone: '+91-80-26995000',
    emergency: true,
    beds: 1000,
    operatingHours: '24x7 Neuro & Psychiatric Emergency',
    schemesSupported: ['PM-JAY', 'Ayushman Bharat-Arogya Karnataka'],
  },
  {
    id: 'victoria-hospital-bengaluru',
    name: 'Victoria Hospital (BMCRI)',
    type: 'hospital',
    address: 'Fort Road, Near City Market, Kalasipalya',
    city: 'Bengaluru',
    state: 'Karnataka',
    pincode: '560002',
    lat: 12.9634,
    lon: 77.5756,
    phone: '+91-80-26701150',
    emergency: true,
    beds: 1000,
    operatingHours: '24x7 Emergency',
    schemesSupported: ['PM-JAY', 'Ayushman Bharat', 'ECHS'],
  },
  {
    id: 'rotary-ttk-blood-bank-bengaluru',
    name: 'Rotary Bangalore TTK Blood Centre',
    type: 'blood_bank',
    address: 'New Thippasandra Main Road, HAL 3rd Stage',
    city: 'Bengaluru',
    state: 'Karnataka',
    pincode: '560075',
    lat: 12.9719,
    lon: 77.6548,
    phone: '+91-80-25287903',
    emergency: true,
    operatingHours: '24x7 Blood Bank & Platelet Donor Registry',
    schemesSupported: ['Thalassemia Free Blood Support'],
  },

  // Chandigarh / Punjab / Haryana
  {
    id: 'pgimer-chandigarh',
    name: 'Postgraduate Institute of Medical Education and Research (PGIMER)',
    type: 'hospital',
    address: 'Sector 12',
    city: 'Chandigarh',
    state: 'Chandigarh',
    pincode: '160012',
    lat: 30.7651,
    lon: 76.7745,
    phone: '+91-172-2746018',
    emergency: true,
    beds: 1948,
    operatingHours: '24x7 Emergency & Advanced Trauma Centre',
    schemesSupported: ['PM-JAY', 'Sarbat Sehat Bima Yojana', 'CGHS'],
  },
  {
    id: 'gmch-32-chandigarh',
    name: 'Government Medical College & Hospital (GMCH 32)',
    type: 'hospital',
    address: 'Chandi Path, Sector 32',
    city: 'Chandigarh',
    state: 'Chandigarh',
    pincode: '160030',
    lat: 30.7107,
    lon: 76.7828,
    phone: '+91-172-2665253',
    emergency: true,
    beds: 800,
    operatingHours: '24x7 Emergency',
    schemesSupported: ['PM-JAY', 'Ayushman Bharat'],
  },

  // Chennai / Tamil Nadu
  {
    id: 'rggh-chennai',
    name: 'Rajiv Gandhi Government General Hospital (Madras Medical College)',
    type: 'hospital',
    address: 'EVR Periyar Salai, Park Town',
    city: 'Chennai',
    state: 'Tamil Nadu',
    pincode: '600003',
    lat: 13.0805,
    lon: 80.2767,
    phone: '+91-44-25305000',
    emergency: true,
    beds: 2722,
    operatingHours: '24x7 Emergency & Trauma',
    schemesSupported: ['Chief Minister Comprehensive Health Insurance', 'PM-JAY'],
  },

  // Hyderabad / Telangana
  {
    id: 'osmania-hyderabad',
    name: 'Osmania General Hospital',
    type: 'hospital',
    address: 'Afzal Gunj',
    city: 'Hyderabad',
    state: 'Telangana',
    pincode: '500012',
    lat: 17.3753,
    lon: 78.4744,
    phone: '+91-40-24600121',
    emergency: true,
    beds: 1168,
    operatingHours: '24x7 Emergency',
    schemesSupported: ['Aarogyasri Health Scheme', 'PM-JAY'],
  },

  // Kolkata / West Bengal
  {
    id: 'sskm-kolkata',
    name: 'SSKM Hospital (IPGMER)',
    type: 'hospital',
    address: '244 AJC Bose Road, Bhowanipore',
    city: 'Kolkata',
    state: 'West Bengal',
    pincode: '700020',
    lat: 22.5390,
    lon: 88.3430,
    phone: '+91-33-22231589',
    emergency: true,
    beds: 1775,
    operatingHours: '24x7 Emergency',
    schemesSupported: ['Swasthya Sathi', 'PM-JAY'],
  },

  // Lucknow / Uttar Pradesh
  {
    id: 'kgmu-lucknow',
    name: "King George's Medical University (KGMU)",
    type: 'hospital',
    address: 'Shah Mina Road, Chowk',
    city: 'Lucknow',
    state: 'Uttar Pradesh',
    pincode: '226003',
    lat: 26.8687,
    lon: 80.9138,
    phone: '+91-522-2257450',
    emergency: true,
    beds: 4500,
    operatingHours: '24x7 Trauma & Critical Care',
    schemesSupported: ['PM-JAY', 'Ayushman Bharat', 'UP State Health'],
  },
];

/**
 * Calculates Great-Circle distance between two coordinates in kilometers using Haversine formula
 */
export function calculateDistanceKm(lat1: number, lon1: number, lat2: number, lon2: number): number {
  const R = 6371; // Earth radius in km
  const dLat = ((lat2 - lat1) * Math.PI) / 180;
  const dLon = ((lon2 - lon1) * Math.PI) / 180;
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos((lat1 * Math.PI) / 180) *
      Math.cos((lat2 * Math.PI) / 180) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return Math.round(R * c * 10) / 10;
}

/**
 * Queries OpenStreetMap Overpass API for real medical facilities near coordinates
 * Gracefully falls back to curated database on network error or timeout.
 */
export async function fetchNearbyFacilities(
  lat: number,
  lon: number,
  radiusKm = 25,
  typeFilter?: FacilityType
): Promise<Facility[]> {
  const radiusMeters = radiusKm * 1000;
  const query = `
    [out:json][timeout:10];
    (
      node["amenity"="hospital"](around:${radiusMeters},${lat},${lon});
      way["amenity"="hospital"](around:${radiusMeters},${lat},${lon});
      node["amenity"="clinic"](around:${radiusMeters},${lat},${lon});
      node["amenity"="pharmacy"](around:${radiusMeters},${lat},${lon});
    );
    out center 25;
  `;

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 6000);

    const res = await fetch('https://overpass-api.de/api/interpreter', {
      method: 'POST',
      body: `data=${encodeURIComponent(query)}`,
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      signal: controller.signal,
    });
    clearTimeout(timeoutId);

    if (res.ok) {
      const data = await res.json();
      const osmFacilities: Facility[] = (data.elements || [])
        .map((el: any) => {
          const itemLat = el.lat || el.center?.lat;
          const itemLon = el.lon || el.center?.lon;
          if (!itemLat || !itemLon) return null;

          const tags = el.tags || {};
          let fType: FacilityType = 'clinic';
          if (tags.amenity === 'hospital') fType = 'hospital';
          if (tags.amenity === 'pharmacy') fType = 'pharmacy';

          return {
            id: `osm-${el.id}`,
            name: tags.name || tags['name:en'] || `Healthcare Facility (${fType})`,
            type: fType,
            address: [tags['addr:street'], tags['addr:suburb'], tags['addr:city']]
              .filter(Boolean)
              .join(', ') || 'Address not listed on OpenStreetMap',
            city: tags['addr:city'] || tags['addr:state'] || 'Local Area',
            state: tags['addr:state'] || '',
            pincode: tags['addr:postcode'],
            lat: itemLat,
            lon: itemLon,
            phone: tags.phone || tags['contact:phone'],
            emergency: tags.emergency === 'yes' || fType === 'hospital',
            operatingHours: tags.opening_hours || (fType === 'hospital' ? '24x7' : 'Standard Hours'),
            distanceKm: calculateDistanceKm(lat, lon, itemLat, itemLon),
          } as Facility;
        })
        .filter(Boolean);

      if (osmFacilities.length > 0) {
        return osmFacilities
          .filter((f) => !typeFilter || f.type === typeFilter)
          .sort((a, b) => (a.distanceKm || 0) - (b.distanceKm || 0));
      }
    }
  } catch (err) {
    // Overpass rate limited or offline; fallback smoothly
    console.warn('Overpass API query timed out or failed; falling back to verified directory.', err);
  }

  // Fallback to curated facilities with calculated distances
  return CURATED_FACILITIES.map((f) => ({
    ...f,
    distanceKm: calculateDistanceKm(lat, lon, f.lat, f.lon),
  }))
    .filter((f) => !typeFilter || f.type === typeFilter)
    .sort((a, b) => (a.distanceKm || 0) - (b.distanceKm || 0));
}

/**
 * Filter facilities nationwide by query, city, state, or facility type
 */
export function searchFacilitiesNationwide(
  query: string,
  filterState?: string,
  filterType?: FacilityType
): Facility[] {
  const q = query.trim().toLowerCase();

  return CURATED_FACILITIES.filter((f) => {
    const matchesQuery =
      !q ||
      f.name.toLowerCase().includes(q) ||
      f.city.toLowerCase().includes(q) ||
      f.state.toLowerCase().includes(q) ||
      f.address.toLowerCase().includes(q) ||
      (f.pincode && f.pincode.includes(q)) ||
      (f.schemesSupported && f.schemesSupported.some((s) => s.toLowerCase().includes(q)));

    const matchesState = !filterState || filterState === 'ALL' || f.state === filterState;
    const matchesType = !filterType || filterType === ('all' as any) || f.type === filterType;

    return matchesQuery && matchesState && matchesType;
  });
}

