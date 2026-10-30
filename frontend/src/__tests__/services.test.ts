import { describe, it, expect, beforeEach } from 'vitest';
import {
  calculateDistanceKm,
  searchFacilitiesNationwide,
  CURATED_FACILITIES,
} from '../services/osmHealthcare';
import { getDeveloperOverrideKey, setDeveloperOverrideKey } from '../services/api';

describe('Healthcare Services & Distance Calculations', () => {
  it('correctly calculates zero distance for identical coordinates', () => {
    const dist = calculateDistanceKm(28.5672, 77.21, 28.5672, 77.21);
    expect(dist).toBe(0);
  });

  it('calculates approximately correct distance between Delhi and Mumbai (~1150-1200 km)', () => {
    // Delhi: 28.6139, 77.2090; Mumbai: 19.0760, 72.8777
    const dist = calculateDistanceKm(28.6139, 77.209, 19.076, 72.8777);
    expect(dist).toBeGreaterThan(1100);
    expect(dist).toBeLessThan(1250);
  });

  it('filters curated facilities by query term', () => {
    const aiimsResults = searchFacilitiesNationwide('AIIMS');
    expect(aiimsResults.length).toBeGreaterThan(0);
    expect(aiimsResults[0].name).toContain('AIIMS');
  });

  it('filters curated facilities by Indian State', () => {
    const karnatakaFacilities = searchFacilitiesNationwide('', 'Karnataka');
    expect(karnatakaFacilities.length).toBeGreaterThan(0);
    karnatakaFacilities.forEach((f) => {
      expect(f.state).toBe('Karnataka');
    });
  });

  it('filters curated facilities by Facility Type (jan_aushadhi)', () => {
    const genericKendras = searchFacilitiesNationwide('', undefined, 'jan_aushadhi');
    expect(genericKendras.length).toBeGreaterThan(0);
    genericKendras.forEach((f) => {
      expect(f.type).toBe('jan_aushadhi');
    });
  });
});

describe('Developer Security Key Override', () => {
  let mockStore: Record<string, string> = {};

  beforeEach(() => {
    mockStore = {};
    (globalThis as any).localStorage = {
      getItem: (key: string) => mockStore[key] || null,
      setItem: (key: string, val: string) => {
        mockStore[key] = val;
      },
      removeItem: (key: string) => {
        delete mockStore[key];
      },
      clear: () => {
        mockStore = {};
      },
    };
  });

  it('returns null by default for ordinary patient sessions', () => {
    const key = getDeveloperOverrideKey();
    expect(key).toBeNull();
  });

  it('saves and retrieves custom developer override key from localStorage', () => {
    setDeveloperOverrideKey('custom_clinical_key_987');
    expect(getDeveloperOverrideKey()).toBe('custom_clinical_key_987');
    setDeveloperOverrideKey(null);
    expect(getDeveloperOverrideKey()).toBeNull();
  });
});
