import { describe, it, expect } from 'vitest';
import { SUPPORTED_LANGUAGES, TRANSLATIONS } from '../i18n';

describe('i18n Translation & Localization Tests', () => {
  it('supports core languages: English, Hindi, Hinglish, Punjabi, and Urdu', () => {
    const codes = SUPPORTED_LANGUAGES.map((l) => l.code);
    expect(codes).toContain('en');
    expect(codes).toContain('hi');
    expect(codes).toContain('hi-en');
    expect(codes).toContain('pa');
    expect(codes).toContain('ur');
  });

  it('marks Urdu with RTL direction and other languages with LTR', () => {
    const urdu = SUPPORTED_LANGUAGES.find((l) => l.code === 'ur');
    const hindi = SUPPORTED_LANGUAGES.find((l) => l.code === 'hi');
    const english = SUPPORTED_LANGUAGES.find((l) => l.code === 'en');

    expect(urdu?.dir).toBe('rtl');
    expect(hindi?.dir).toBe('ltr');
    expect(english?.dir).toBe('ltr');
  });

  it('contains mandatory emergency helpline string across all primary dictionaries', () => {
    const primaryLangs = ['en', 'hi', 'hi-en', 'pa'];
    primaryLangs.forEach((lang) => {
      const dict = TRANSLATIONS[lang];
      expect(dict).toBeDefined();
      expect(dict['nav.emergency112']).toBeDefined();
      expect(dict['chat.emergencyWarning']).toBeDefined();
    });
  });
});

