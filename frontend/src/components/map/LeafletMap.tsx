import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { Facility } from '../../types';

// Fix standard Leaflet icon paths in bundled environments
const defaultIcon = L.icon({
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

const userIcon = L.divIcon({
  className: 'user-gps-marker',
  html: `
    <div style="position: relative; width: 20px; height: 20px;">
      <div style="position: absolute; width: 100%; height: 100%; border-radius: 50%; background: #06b6d4; opacity: 0.4; animation: ping 1.5s cubic-bezier(0, 0, 0.2, 1) infinite;"></div>
      <div style="position: absolute; top: 3px; left: 3px; width: 14px; height: 14px; border-radius: 50%; background: #06b6d4; border: 2px solid #ffffff; box-shadow: 0 0 10px #06b6d4;"></div>
    </div>
  `,
  iconSize: [20, 20],
  iconAnchor: [10, 10],
});

interface LeafletMapProps {
  center: [number, number];
  zoom?: number;
  userLocation?: [number, number] | null;
  facilities: Facility[];
  selectedFacility?: Facility | null;
  onSelectFacility?: (facility: Facility) => void;
  radiusKm?: number;
}

export const LeafletMap: React.FC<LeafletMapProps> = ({
  center,
  zoom = 12,
  userLocation,
  facilities,
  selectedFacility,
  onSelectFacility,
  radiusKm,
}) => {
  const mapRef = useRef<HTMLDivElement | null>(null);
  const leafletMapInstance = useRef<L.Map | null>(null);
  const markersLayerRef = useRef<L.LayerGroup | null>(null);
  const circleLayerRef = useRef<L.Circle | null>(null);

  // Initialize Map
  useEffect(() => {
    if (!mapRef.current) return;

    if (!leafletMapInstance.current) {
      const map = L.map(mapRef.current, {
        center,
        zoom,
        zoomControl: true,
      });

      // Dark style OpenStreetMap tiles via CartoDB Dark Matter
      L.tileLayer(
        'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png',
        {
          attribution:
            '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
          subdomains: 'abcd',
          maxZoom: 19,
        }
      ).addTo(map);

      markersLayerRef.current = L.layerGroup().addTo(map);
      leafletMapInstance.current = map;
    }

    return () => {
      if (leafletMapInstance.current) {
        leafletMapInstance.current.remove();
        leafletMapInstance.current = null;
      }
    };
  }, []);

  // Pan to center if center changes
  useEffect(() => {
    if (leafletMapInstance.current) {
      leafletMapInstance.current.flyTo(center, zoom, { duration: 1.2 });
    }
  }, [center, zoom]);

  // Update Markers & Radius Circle
  useEffect(() => {
    const map = leafletMapInstance.current;
    const markersLayer = markersLayerRef.current;
    if (!map || !markersLayer) return;

    markersLayer.clearLayers();

    // User location marker & radius
    if (userLocation) {
      const userMarker = L.marker(userLocation, { icon: userIcon }).bindPopup(
        '<strong>Your Current Location</strong>'
      );
      markersLayer.addLayer(userMarker);

      if (radiusKm) {
        if (circleLayerRef.current) {
          map.removeLayer(circleLayerRef.current);
        }
        const circle = L.circle(userLocation, {
          radius: radiusKm * 1000,
          color: '#06b6d4',
          fillColor: '#06b6d4',
          fillOpacity: 0.08,
          weight: 1.5,
          dashArray: '4, 6',
        }).addTo(map);
        circleLayerRef.current = circle;
      }
    }

    // Facility Markers
    facilities.forEach((fac) => {
      const marker = L.marker([fac.lat, fac.lon], { icon: defaultIcon });

      const popupContent = `
        <div style="font-family: inherit; font-size: 12px; color: #0f172a; min-width: 180px;">
          <h4 style="font-weight: 700; margin: 0 0 4px 0; color: #0f172a;">${fac.name}</h4>
          <p style="margin: 0 0 4px 0; color: #475569;">${fac.address}</p>
          <div style="display: flex; gap: 4px; margin-top: 6px; font-size: 10px;">
            <span style="background: #e0f2fe; color: #0284c7; padding: 2px 6px; border-radius: 4px; font-weight: 600;">
              ${fac.type.toUpperCase()}
            </span>
            ${
              fac.emergency
                ? '<span style="background: #fee2e2; color: #dc2626; padding: 2px 6px; border-radius: 4px; font-weight: 600;">24x7 EMERGENCY</span>'
                : ''
            }
          </div>
          ${
            fac.phone
              ? `<div style="margin-top: 6px;"><a href="tel:${fac.phone}" style="color: #0284c7; text-decoration: underline; font-weight: 600;">📞 ${fac.phone}</a></div>`
              : ''
          }
        </div>
      `;

      marker.bindPopup(popupContent);
      marker.on('click', () => {
        if (onSelectFacility) onSelectFacility(fac);
      });

      markersLayer.addLayer(marker);
    });
  }, [facilities, userLocation, radiusKm, onSelectFacility]);

  // Center selected facility if provided
  useEffect(() => {
    if (selectedFacility && leafletMapInstance.current) {
      leafletMapInstance.current.flyTo([selectedFacility.lat, selectedFacility.lon], 15, {
        duration: 1.0,
      });
    }
  }, [selectedFacility]);

  return (
    <div className="relative w-full h-full min-h-[450px] rounded-2xl overflow-hidden border border-slate-800 shadow-2xl">
      <div ref={mapRef} className="w-full h-full" style={{ minHeight: '450px' }} />
    </div>
  );
};

