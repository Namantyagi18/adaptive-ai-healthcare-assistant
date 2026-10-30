/**
 * ADAPT-AI Language & Localization Context
 */

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { SUPPORTED_LANGUAGES, TRANSLATIONS } from '../i18n';
import { LanguageInfo } from '../types';

interface LanguageContextType {
  language: string;
  currentLangInfo: LanguageInfo;
  setLanguage: (code: string) => void;
  t: (key: string) => string;
  isRTL: boolean;
  supportedLanguages: LanguageInfo[];
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export const LanguageProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [language, setLanguageState] = useState<string>(() => {
    return localStorage.getItem('adapt_ai_language') || 'en';
  });

  const currentLangInfo =
    SUPPORTED_LANGUAGES.find((l) => l.code === language) || SUPPORTED_LANGUAGES[0];

  const isRTL = currentLangInfo.dir === 'rtl';

  useEffect(() => {
    localStorage.setItem('adapt_ai_language', language);
    document.documentElement.dir = isRTL ? 'rtl' : 'ltr';
    document.documentElement.lang = language;
  }, [language, isRTL]);

  const setLanguage = (code: string) => {
    setLanguageState(code);
  };

  const t = (key: string): string => {
    const langDict = TRANSLATIONS[language] || TRANSLATIONS.en;
    if (langDict && langDict[key]) {
      return langDict[key];
    }
    // Fallback to English
    if (TRANSLATIONS.en && TRANSLATIONS.en[key]) {
      return TRANSLATIONS.en[key];
    }
    return key;
  };

  return (
    <LanguageContext.Provider
      value={{
        language,
        currentLangInfo,
        setLanguage,
        t,
        isRTL,
        supportedLanguages: SUPPORTED_LANGUAGES,
      }}
    >
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = (): LanguageContextType => {
  const ctx = useContext(LanguageContext);
  if (!ctx) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return ctx;
};

