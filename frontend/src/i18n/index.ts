/**
 * ADAPT-AI Multilingual Translation Dictionary
 * Comprehensive localization covering English, Hindi, Hinglish, Punjabi, and Indian regional languages.
 */

import { LanguageInfo } from '../types';

export const SUPPORTED_LANGUAGES: LanguageInfo[] = [
  { code: 'en', name: 'English', nativeName: 'English', dir: 'ltr', flag: '🇬🇧' },
  { code: 'hi', name: 'Hindi', nativeName: 'हिन्दी', dir: 'ltr', flag: '🇮🇳' },
  { code: 'hi-en', name: 'Hinglish', nativeName: 'Hinglish (Colloquial)', dir: 'ltr', flag: '🇮🇳' },
  { code: 'pa', name: 'Punjabi', nativeName: 'ਪੰਜਾਬੀ', dir: 'ltr', flag: '🇮🇳' },
  { code: 'bn', name: 'Bengali', nativeName: 'বাংলা', dir: 'ltr', flag: '🇮🇳' },
  { code: 'ta', name: 'Tamil', nativeName: 'தமிழ்', dir: 'ltr', flag: '🇮🇳' },
  { code: 'te', name: 'Telugu', nativeName: 'తెలుగు', dir: 'ltr', flag: '🇮🇳' },
  { code: 'mr', name: 'Marathi', nativeName: 'मराठी', dir: 'ltr', flag: '🇮🇳' },
  { code: 'ur', name: 'Urdu', nativeName: 'اردو', dir: 'rtl', flag: '🇮🇳' },
];

export const TRANSLATIONS: Record<string, Record<string, string>> = {
  en: {
    // Navigation
    'nav.brand': 'ADAPT-AI',
    'nav.tagline': 'Healthcare Intelligence',
    'nav.home': 'Home',
    'nav.assistant': 'AI Health Assistant',
    'nav.map': 'Healthcare Map',
    'nav.find': 'Find Care India',
    'nav.documents': 'Document Analysis',
    'nav.voice': 'Voice Assistant',
    'nav.community': 'Community Care',
    'nav.safety': 'Clinical Safety',
    'nav.settings': 'Settings',
    'nav.apiKey': 'API Key',
    'nav.backendOnline': 'Engine Online',
    'nav.backendOffline': 'Engine Connecting...',
    'nav.emergency112': 'Emergency: Call 112 / 108',

    // Hero
    'hero.badge': 'Adaptive Clinical AI Platform • India Edition',
    'hero.title': 'Adaptive Clinical AI Built for Trusted Care',
    'hero.highlight': 'Empowering 1.4 Billion Citizens',
    'hero.subtitle':
      'Real-time evidence retrieval from validated clinical guidelines (NICE, WHO, CDC, AIIMS) with built-in emergency red-flag triage, multilingual voice support, and nationwide healthcare facility discovery across India.',
    'hero.ctaAssistant': 'Consult AI Assistant',
    'hero.ctaFindCare': 'Find Hospitals Near Me',
    'hero.emergencyNotice': 'Facing a medical emergency? Call 112 or 108 immediately.',

    // Stats / Trust
    'stats.citations': '100% Validated Citations',
    'stats.citationsSub': 'Strict zero-hallucination boundary',
    'stats.triage': '5-Tier Clinical Triage',
    'stats.triageSub': 'Immediate red flag alert protocol',
    'stats.languages': '10+ Indian Languages',
    'stats.languagesSub': 'English, Hindi, Hinglish, Punjabi...',
    'stats.facilities': 'Pan-India Directory',
    'stats.facilitiesSub': 'AIIMS, Jan Aushadhi & PHC maps',

    // Assistant Chat
    'chat.placeholder': 'Describe your symptoms or ask a clinical question (e.g., vitamin D symptoms, chest discomfort, fever)...',
    'chat.send': 'Send Query',
    'chat.listening': 'Listening...',
    'chat.emergencyWarning': 'CRITICAL MEDICAL EMERGENCY DETECTED',
    'chat.urgentWarning': 'URGENT CLINICAL ASSESSMENT REQUIRED',
    'chat.sources': 'Clinical Guideline Citations',
    'chat.evidenceSufficiency': 'Evidence Status',
    'chat.uncertainty': 'Clinical Uncertainty Note',
    'chat.followUps': 'Suggested Follow-up Questions',
    'chat.disclaimer':
      'ADAPT-AI is an informational decision-support and health education tool. It does not replace professional clinical diagnosis or prescription.',

    // Map
    'map.title': 'Interactive India Healthcare Map',
    'map.subtitle': 'Discover AIIMS, district civil hospitals, PHCs, Jan Aushadhi Kendras, and blood banks near you.',
    'map.locateMe': 'Use My GPS Location',
    'map.searchPlaceholder': 'Search by city, hospital name, or PIN code...',
    'map.allTypes': 'All Facilities',
    'map.hospitals': 'Hospitals (24x7)',
    'map.clinics': 'Clinics & PHCs',
    'map.pharmacies': 'Pharmacies & Jan Aushadhi',
    'map.bloodBanks': 'Blood Banks',
    'map.distance': 'Distance',
    'map.beds': 'Available Beds',
    'map.call': 'Call Facility',
    'map.directions': 'Directions',

    // Document Analysis
    'doc.title': 'Diagnostic Document & Lab Report Analysis',
    'doc.subtitle': 'Securely upload clinical test results, prescriptions, or imaging scans for instant plain-language synthesis.',
    'doc.dropzone': 'Drag & drop your medical document (PDF, PNG, JPG, TXT) or click to browse',
    'doc.promptPlaceholder': 'Optional question (e.g. What does this ferritin level mean? Summarize test findings)',
    'doc.analyze': 'Analyze Document',
    'doc.quarantined': 'File safely quarantined & hashed (SHA-256)',
    'doc.extracted': 'Extracted Clinical Text',
    'doc.synthesis': 'Clinical Interpretation & Findings',

    // Voice Assistant
    'voice.title': 'Hands-Free Multilingual Voice Assistant',
    'voice.subtitle': 'Speak naturally in English, Hindi, Hinglish, or Punjabi with real-time speech synthesis.',
    'voice.start': 'Start Listening',
    'voice.stop': 'Stop Listening',
    'voice.rate': 'Speech Rate',
    'voice.detected': 'Live Transcript',

    // Safety Center
    'safety.title': 'Clinical Safety & Emergency Protocols',
    'safety.subtitle': 'How ADAPT-AI ensures zero unsafe diagnoses and rapid red-flag escalation.',
    'safety.fastProtocol': 'FAST Protocol for Suspected Stroke',
    'safety.miProtocol': 'Heart Attack / Myocardial Infarction Red Flags',
    'safety.helplines': 'National Emergency Helplines (India)',
    'safety.helpline112': '112 - Pan-India Unified Emergency Service',
    'safety.helpline108': '108 - Medical Emergency & Free Ambulance',
    'safety.helpline104': '104 - State Health Information & Blood Helpline',
    'safety.helplineTeleManas': '14416 - Tele-MANAS Mental Health Support (24x7)',
    'safety.helplineJanAushadhi': '1800-180-8080 - PM Jan Aushadhi Generic Helpline',
  },

  hi: {
    // Navigation
    'nav.brand': 'ADAPT-AI',
    'nav.tagline': 'स्वास्थ्य बुद्धिमत्ता मंच',
    'nav.home': 'होम',
    'nav.assistant': 'एआई स्वास्थ्य सहायक',
    'nav.map': 'स्वास्थ्य मानचित्र',
    'nav.find': 'चिकित्सा खोजें',
    'nav.documents': 'दस्तावेज़ विश्लेषण',
    'nav.voice': 'आवाज़ सहायक',
    'nav.community': 'सामुदायिक सेवा',
    'nav.safety': 'चिकित्सीय सुरक्षा',
    'nav.settings': 'सेटिंग्स',
    'nav.apiKey': 'एपीआई कुंजी',
    'nav.backendOnline': 'इंजन सक्रिय है',
    'nav.backendOffline': 'इंजन कनेक्ट हो रहा है...',
    'nav.emergency112': 'आपातकालीन: 112 / 108 डायल करें',

    // Hero
    'hero.badge': 'अनुकूली स्वास्थ्य एआई • भारत संस्करण',
    'hero.title': 'भरोसेमंद स्वास्थ्य सेवा के लिए अनुकूली एआई',
    'hero.highlight': '140 करोड़ नागरिकों का सशक्तिकरण',
    'hero.subtitle':
      'प्रमाणित चिकित्सीय दिशानिर्देशों (NICE, WHO, CDC, AIIMS) से रीयल-टाइम संदर्भ, आपातकालीन ट्राइएज, बहुभाषी वॉइस और देशव्यापी अस्पताल खोज।',
    'hero.ctaAssistant': 'एआई सहायक से पूछें',
    'hero.ctaFindCare': 'पास के अस्पताल खोजें',
    'hero.emergencyNotice': 'चिकित्सीय आपातकाल है? तुरंत 112 या 108 पर कॉल करें।',

    // Stats / Trust
    'stats.citations': '100% सत्यापित संदर्भ',
    'stats.citationsSub': 'शून्य-भ्रम और पुख्ता साक्ष्य सीमा',
    'stats.triage': '5-स्तरीय नैदानिक ट्राइएज',
    'stats.triageSub': 'तत्काल आपातकालीन चेतावनी प्रणाली',
    'stats.languages': '10+ भारतीय भाषाएं',
    'stats.languagesSub': 'हिन्दी, English, Hinglish, ਪੰਜਾਬੀ...',
    'stats.facilities': 'अखिल भारतीय डायरेक्टरी',
    'stats.facilitiesSub': 'एम्स, जन औषधि और पीएचसी केंद्र',

    // Assistant Chat
    'chat.placeholder': 'अपने लक्षण बताएं या सवाल पूछें (जैसे: विटामिन डी की कमी, सीने में दर्द, बुखार)...',
    'chat.send': 'सवाल पूछें',
    'chat.listening': 'सुन रहे हैं...',
    'chat.emergencyWarning': 'गंभीर चिकित्सीय आपातकाल का पता चला!',
    'chat.urgentWarning': 'तत्काल डॉक्टर से परामर्श की आवश्यकता है',
    'chat.sources': 'प्रमाणित दिशानिर्देश संदर्भ (Citations)',
    'chat.evidenceSufficiency': 'साक्ष्य स्थिति',
    'chat.uncertainty': 'नैदानिक अनिश्चितता नोट',
    'chat.followUps': 'संबंधित अनुवर्ती प्रश्न',
    'chat.disclaimer':
      'ADAPT-AI केवल सूचनात्मक और शैक्षिक सहायता के लिए है। यह पेशेवर डॉक्टर की जांच अथवा दवा के पर्चे का विकल्प नहीं है।',

    // Map
    'map.title': 'इंटरएक्टिव भारत स्वास्थ्य मानचित्र',
    'map.subtitle': 'अपने निकटतम एम्स, जिला अस्पताल, पीएचसी, जन औषधि केंद्र और ब्लड बैंक खोजें।',
    'map.locateMe': 'मेरी लोकेशन इस्तेमाल करें',
    'map.searchPlaceholder': 'शहर, अस्पताल का नाम या पिन कोड दर्ज करें...',
    'map.allTypes': 'सभी सुविधाएं',
    'map.hospitals': 'अस्पताल (24x7)',
    'map.clinics': 'क्लिनिक और पीएचसी',
    'map.pharmacies': 'दवा की दुकानें व जन औषधि',
    'map.bloodBanks': 'ब्लड बैंक',
    'map.distance': 'दूरी',
    'map.beds': 'उपलब्ध बिस्तर',
    'map.call': 'कॉल करें',
    'map.directions': 'दिशा-निर्देश',

    // Document Analysis
    'doc.title': 'मेडिकल रिपोर्ट और लैब जांच विश्लेषण',
    'doc.subtitle': 'अपनी लैब रिपोर्ट, प्रिस्क्रिप्शन या स्कैन सुरक्षित रूप से अपलोड करें और सरल भाषा में विश्लेषण पाएं।',
    'doc.dropzone': 'अपनी रिपोर्ट (PDF, PNG, JPG, TXT) यहां ड्रैग करें या फाइल चुनें',
    'doc.promptPlaceholder': 'वैकल्पिक सवाल (जैसे: इस रिपोर्ट के मुख्य निष्कर्ष क्या हैं?)',
    'doc.analyze': 'रिपोर्ट का विश्लेषण करें',
    'doc.quarantined': 'फ़ाइल सुरक्षित रूप से संगरोधित और जांची गई (SHA-256)',
    'doc.extracted': 'निकाला गया टेक्स्ट',
    'doc.synthesis': 'नैदानिक व्याख्या और निष्कर्ष',

    // Voice Assistant
    'voice.title': 'हाथों से मुक्त बहुभाषी वॉइस सहायक',
    'voice.subtitle': 'हिन्दी, Hinglish या अंग्रेजी में स्वाभाविक रूप से बोलें।',
    'voice.start': 'बोलना शुरू करें',
    'voice.stop': 'रोकें',
    'voice.rate': 'बोलने की गति',
    'voice.detected': 'लाइव प्रतिलेख (Transcript)',

    // Safety Center
    'safety.title': 'नैदानिक सुरक्षा और आपातकालीन प्रोटोकॉल',
    'safety.subtitle': 'ADAPT-AI किस प्रकार सुरक्षित और सत्यापित स्वास्थ्य जानकारी सुनिश्चित करता है।',
    'safety.fastProtocol': 'स्ट्रोक के लिए FAST प्रोटोकॉल',
    'safety.miProtocol': 'दिल के दौरे (Heart Attack) के चेतावनी संकेत',
    'safety.helplines': 'भारत की राष्ट्रीय आपातकालीन हेल्पलाइन',
    'safety.helpline112': '112 - एकीकृत अखिल भारतीय आपातकालीन सेवा',
    'safety.helpline108': '108 - चिकित्सा आपातकाल एवं निशुल्क एम्बुलेंस',
    'safety.helpline104': '104 - राज्य स्वास्थ्य सूचना एवं ब्लड हेल्पलाइन',
    'safety.helplineTeleManas': '14416 - टेली-मानस मानसिक स्वास्थ्य सहायता (24x7)',
    'safety.helplineJanAushadhi': '1800-180-8080 - पीएम जन औषधि जेनेरिक हेल्पलाइन',
  },

  'hi-en': {
    // Navigation
    'nav.brand': 'ADAPT-AI',
    'nav.tagline': 'Healthcare Intelligence',
    'nav.home': 'Home',
    'nav.assistant': 'AI Health Assistant',
    'nav.map': 'Healthcare Map',
    'nav.find': 'Find Care India',
    'nav.documents': 'Doc Analysis',
    'nav.voice': 'Voice Assistant',
    'nav.community': 'Community Care',
    'nav.safety': 'Safety Protocols',
    'nav.settings': 'Settings',
    'nav.apiKey': 'API Key',
    'nav.backendOnline': 'Engine Online',
    'nav.backendOffline': 'Connecting Engine...',
    'nav.emergency112': 'Emergency: Dial 112 / 108',

    // Hero
    'hero.badge': 'Adaptive Health AI • Bharat Edition',
    'hero.title': 'Accurate Medical AI for Real People',
    'hero.highlight': '140 Crore Indians ke Swasthya ke Liye',
    'hero.subtitle':
      'Verified clinical guidelines (NICE, WHO, CDC, AIIMS) se direct evidence, emergency detection, multilingual voice aur pan-India hospital search.',
    'hero.ctaAssistant': 'Ask AI Assistant',
    'hero.ctaFindCare': 'Nearby Hospitals Dekhein',
    'hero.emergencyNotice': 'Medical emergency hai? Turant 112 ya 108 pe call karein.',

    // Stats / Trust
    'stats.citations': '100% Genuine Citations',
    'stats.citationsSub': 'No fake answers or hallucination',
    'stats.triage': '5-Tier Clinical Triage',
    'stats.triageSub': 'Immediate red flag alert protocol',
    'stats.languages': '10+ Indian Languages',
    'stats.languagesSub': 'English, Hindi, Hinglish, Punjabi...',
    'stats.facilities': 'Pan-India Directory',
    'stats.facilitiesSub': 'AIIMS, Jan Aushadhi & PHC centres',

    // Assistant Chat
    'chat.placeholder': 'Apne symptoms likhein ya sawaal poochein (jaise: vitamin D deficiency, chest pain, fever)...',
    'chat.send': 'Send Query',
    'chat.listening': 'Sun rahe hain...',
    'chat.emergencyWarning': 'CRITICAL MEDICAL EMERGENCY DETECTED!',
    'chat.urgentWarning': 'URGENT CLINICAL ATTENTION NEEDED',
    'chat.sources': 'Medical Guideline Citations',
    'chat.evidenceSufficiency': 'Evidence Status',
    'chat.uncertainty': 'Uncertainty Note',
    'chat.followUps': 'Suggested Follow-up Questions',
    'chat.disclaimer':
      'ADAPT-AI sirf health education aur decision support ke liye hai. Yeh doctor ke clinical diagnosis ya prescription ka substitute nahi hai.',

    // Map
    'map.title': 'Interactive India Healthcare Map',
    'map.subtitle': 'Apne pass ke AIIMS, Civil Hospitals, PHCs, Jan Aushadhi Kendras aur Blood Banks khojein.',
    'map.locateMe': 'Use My GPS Location',
    'map.searchPlaceholder': 'Search city, hospital name, ya PIN code...',
    'map.allTypes': 'All Facilities',
    'map.hospitals': 'Hospitals (24x7)',
    'map.clinics': 'Clinics & PHCs',
    'map.pharmacies': 'Jan Aushadhi & Medical Stores',
    'map.bloodBanks': 'Blood Banks',
    'map.distance': 'Distance',
    'map.beds': 'Available Beds',
    'map.call': 'Call Karein',
    'map.directions': 'Directions',

    // Document Analysis
    'doc.title': 'Medical Lab Report Analysis',
    'doc.subtitle': 'Apni blood test report ya prescription upload karein aur simple Hinglish summary paayein.',
    'doc.dropzone': 'Report upload karein (PDF, JPG, PNG) ya file select karein',
    'doc.promptPlaceholder': 'Optional sawaal (jaise: iss report ka kya matlab hai?)',
    'doc.analyze': 'Analyze Karein',
    'doc.quarantined': 'File safely quarantined (SHA-256 verified)',
    'doc.extracted': 'Extracted Text',
    'doc.synthesis': 'Clinical Interpretation & Findings',

    // Voice Assistant
    'voice.title': 'Hands-Free Multilingual Voice Assistant',
    'voice.subtitle': 'English, Hindi ya Hinglish mein aaram se baat karein.',
    'voice.start': 'Boliye (Start Mic)',
    'voice.stop': 'Stop Mic',
    'voice.rate': 'Voice Speed',
    'voice.detected': 'Live Transcript',

    // Safety Center
    'safety.title': 'Safety & Emergency Red-Flag Protocols',
    'safety.subtitle': 'How ADAPT-AI protects patients with strict safety boundaries.',
    'safety.fastProtocol': 'Stroke ke liye FAST Protocol',
    'safety.miProtocol': 'Heart Attack ke Red Flag Signs',
    'safety.helplines': 'India National Emergency Numbers',
    'safety.helpline112': '112 - Unified All-India Emergency Service',
    'safety.helpline108': '108 - Free Emergency Ambulance Service',
    'safety.helpline104': '104 - Health Advice & Blood Bank Helpline',
    'safety.helplineTeleManas': '14416 - Tele-MANAS Mental Health Support (24x7)',
    'safety.helplineJanAushadhi': '1800-180-8080 - PM Jan Aushadhi Generic Helpline',
  },

  pa: {
    // Navigation
    'nav.brand': 'ADAPT-AI',
    'nav.tagline': 'ਸਿਹਤ ਬੁੱਧੀਮੱਤਾ ਮੰਚ',
    'nav.home': 'ਮੁੱਖ ਪੰਨਾ',
    'nav.assistant': 'ਏਆਈ ਸਿਹਤ ਸਹਾਇਕ',
    'nav.map': 'ਸਿਹਤ ਨਕਸ਼ਾ',
    'nav.find': 'ਹਸਪਤਾਲ ਲੱਭੋ',
    'nav.documents': 'ਰਿਪੋਰਟ ਵਿਸ਼ਲੇਸ਼ਣ',
    'nav.voice': 'ਆਵਾਜ਼ ਸਹਾਇਕ',
    'nav.community': 'ਭਾਈਚਾਰਕ ਸੇਵਾ',
    'nav.safety': 'ਸੁਰੱਖਿਆ ਨੇਮ',
    'nav.settings': 'ਸੈਟਿੰਗਜ਼',
    'nav.apiKey': 'API ਕੁੰਜੀ',
    'nav.backendOnline': 'ਇੰਜਣ ਚਾਲੂ ਹੈ',
    'nav.backendOffline': 'ਜੁੜ ਰਿਹਾ ਹੈ...',
    'nav.emergency112': 'ਐਮਰਜੈਂਸੀ: 112 / 108 ਡਾਇਲ ਕਰੋ',

    // Hero
    'hero.badge': 'ਅਨੁਕੂਲਿਤ ਸਿਹਤ ਏਆਈ • ਭਾਰਤ ਐਡੀਸ਼ਨ',
    'hero.title': 'ਭਰੋਸੇਯੋਗ ਸਿਹਤ ਸੇਵਾ ਲਈ ਆਧੁਨਿਕ ਏਆਈ',
    'hero.highlight': '140 ਕਰੋੜ ਨਾਗਰਿਕਾਂ ਲਈ ਸਮਰਪਿਤ',
    'hero.subtitle':
      'ਪ੍ਰਮਾਣਿਤ ਕਲੀਨਿਕਲ ਦਿਸ਼ਾ-ਨਿਰਦੇਸ਼ਾਂ (NICE, WHO, CDC, AIIMS) ਤੋਂ ਅਸਲ ਹਵਾਲੇ, ਐਮਰਜੈਂਸੀ ਚੇਤਾਵਨੀ ਅਤੇ ਦੇਸ਼ ਭਰ ਦੇ ਹਸਪਤਾਲਾਂ ਦੀ ਖੋਜ।',
    'hero.ctaAssistant': 'ਸਿਹਤ ਸਹਾਇਕ ਤੋਂ ਪੁੱਛੋ',
    'hero.ctaFindCare': 'ਨੇੜਲੇ ਹਸਪਤਾਲ ਲੱਭੋ',
    'hero.emergencyNotice': 'ਗੰਭੀਰ ਐਮਰਜੈਂਸੀ ਹੈ? ਤੁਰੰਤ 112 ਜਾਂ 108 ਤੇ ਕਾਲ ਕਰੋ।',

    // Stats / Trust
    'stats.citations': '100% ਪ੍ਰਮਾਣਿਤ ਹਵਾਲੇ',
    'stats.citationsSub': 'ਕੋਈ ਗਲਤ ਜਾਂ ਝੂਠੀ ਜਾਣਕਾਰੀ ਨਹੀਂ',
    'stats.triage': '5-ਪੱਧਰੀ ਕਲੀਨਿਕਲ ਟ੍ਰਾਈਏਜ',
    'stats.triageSub': 'ਤੁਰੰਤ ਐਮਰਜੈਂਸੀ ਅਲਰਟ ਪ੍ਰਣਾਲੀ',
    'stats.languages': '10+ ਭਾਰਤੀ ਭਾਸ਼ਾਵਾਂ',
    'stats.languagesSub': 'ਪੰਜਾਬੀ, हिन्दी, English, Hinglish...',
    'stats.facilities': 'ਪੂਰੇ ਭਾਰਤ ਦੀ ਡਾਇਰੈਕਟਰੀ',
    'stats.facilitiesSub': 'ਏਮਜ਼, ਜਨ ਔਸ਼ਧੀ ਅਤੇ ਸਿਹਤ ਕੇਂਦਰ',

    // Assistant Chat
    'chat.placeholder': 'ਆਪਣੇ ਲੱਛਣ ਦੱਸੋ ਜਾਂ ਸਵਾਲ ਪੁੱਛੋ (ਜਿਵੇਂ: ਵਿਟਾਮਿਨ ਡੀ ਦੀ ਘਾਟ, ਛਾਤੀ ਵਿੱਚ ਦਰਦ, ਬੁਖਾਰ)...',
    'chat.send': 'ਸਵਾਲ ਭੇਜੋ',
    'chat.listening': 'ਸੁਣ ਰਹੇ ਹਾਂ...',
    'chat.emergencyWarning': 'ਗੰਭੀਰ ਐਮਰਜੈਂਸੀ ਚੇਤਾਵਨੀ!',
    'chat.urgentWarning': 'ਤੁਰੰਤ ਡਾਕਟਰੀ ਸਲਾਹ ਦੀ ਲੋੜ ਹੈ',
    'chat.sources': 'ਦਿਸ਼ਾ-ਨਿਰਦੇਸ਼ ਹਵਾਲੇ (Citations)',
    'chat.evidenceSufficiency': 'ਸਬੂਤ ਸਥਿਤੀ',
    'chat.uncertainty': 'ਅਨਿਸ਼ਚਿਤਤਾ ਨੋਟ',
    'chat.followUps': 'ਸਬੰਧਿਤ ਸਵਾਲ',
    'chat.disclaimer':
      'ADAPT-AI ਸਿਰਫ ਸਿੱਖਿਆ ਅਤੇ ਫੈਸਲਾ ਸਹਾਇਤਾ ਲਈ ਹੈ। ਇਹ ਡਾਕਟਰ ਦੀ ਜਾਂਚ ਜਾਂ ਦਵਾਈ ਦਾ ਬਦਲ ਨਹੀਂ ਹੈ।',

    // Map
    'map.title': 'ਭਾਰਤ ਸਿਹਤ ਨਕਸ਼ਾ',
    'map.subtitle': 'ਆਪਣੇ ਨੇੜਲੇ ਏਮਜ਼, ਸਿਵਲ ਹਸਪਤਾਲ, ਜਨ ਔਸ਼ਧੀ ਕੇਂਦਰ ਅਤੇ ਬਲੱਡ ਬੈਂਕ ਲੱਭੋ।',
    'map.locateMe': 'ਮੇਰੀ ਲੋਕੇਸ਼ਨ ਵਰਤੋ',
    'map.searchPlaceholder': 'ਸ਼ਹਿਰ, ਹਸਪਤਾਲ ਦਾ ਨਾਮ ਜਾਂ ਪਿੰਨ ਕੋਡ ਦਰਜ ਕਰੋ...',
    'map.allTypes': 'ਸਾਰੀਆਂ ਸਹੂਲਤਾਂ',
    'map.hospitals': 'ਹਸਪਤਾਲ (24x7)',
    'map.clinics': 'ਕਲੀਨਿਕ ਅਤੇ ਸਿਹਤ ਕੇਂਦਰ',
    'map.pharmacies': 'ਦਵਾਈਆਂ ਦੀਆਂ ਦੁਕਾਨਾਂ ਤੇ ਜਨ ਔਸ਼ਧੀ',
    'map.bloodBanks': 'ਬਲੱਡ ਬੈਂਕ',
    'map.distance': 'ਦੂਰੀ',
    'map.beds': 'ਉਪਲਬਧ ਬੈੱਡ',
    'map.call': 'ਕਾਲ ਕਰੋ',
    'map.directions': 'ਦਿਸ਼ਾ-ਨਿਰਦੇਸ਼',

    // Document Analysis
    'doc.title': 'ਲੈਬ ਰਿਪੋਰਟ ਤੇ ਟੈਸਟ ਵਿਸ਼ਲੇਸ਼ਣ',
    'doc.subtitle': 'ਆਪਣੀ ਰਿਪੋਰਟ ਅੱਪਲੋਡ ਕਰੋ ਅਤੇ ਸਰਲ ਭਾਸ਼ਾ ਵਿੱਚ ਨਤੀਜੇ ਜਾਣੋ।',
    'doc.dropzone': 'ਫਾਈਲ (PDF, PNG, JPG) ਇੱਥੇ ਖਿੱਚੋ ਜਾਂ ਚੁਣੋ',
    'doc.promptPlaceholder': 'ਵਿਕਲਪਿਕ ਸਵਾਲ (ਜਿਵੇਂ: ਇਸ ਰਿਪੋਰਟ ਦਾ ਮੁੱਖ ਮਤਲਬ ਕੀ ਹੈ?)',
    'doc.analyze': 'ਵਿਸ਼ਲੇਸ਼ਣ ਕਰੋ',
    'doc.quarantined': 'ਫਾਈਲ ਸੁਰੱਖਿਅਤ ਕੀਤੀ ਗਈ (SHA-256)',
    'doc.extracted': 'ਕੱਢਿਆ ਗਿਆ ਟੈਕਸਟ',
    'doc.synthesis': 'ਕਲੀਨਿਕਲ ਵਿਆਖਿਆ',

    // Voice Assistant
    'voice.title': 'ਆਵਾਜ਼ ਸਹਾਇਕ',
    'voice.subtitle': 'ਪੰਜਾਬੀ ਜਾਂ ਅੰਗਰੇਜ਼ੀ ਵਿੱਚ ਸੁਭਾਵਿਕ ਤਰੀਕੇ ਨਾਲ ਗੱਲ ਕਰੋ।',
    'voice.start': 'ਬੋਲਣਾ ਸ਼ੁਰੂ ਕਰੋ',
    'voice.stop': 'ਰੋਕੋ',
    'voice.rate': 'ਆਵਾਜ਼ ਦੀ ਗਤੀ',
    'voice.detected': 'ਲਾਈਵ ਟ੍ਰਾਂਸਕ੍ਰਿਪਟ',

    // Safety Center
    'safety.title': 'ਕਲੀਨਿਕਲ ਸੁਰੱਖਿਆ ਪ੍ਰੋਟੋਕੋਲ',
    'safety.subtitle': 'ਸਹੀ ਅਤੇ ਸੁਰੱਖਿਅਤ ਸਿਹਤ ਜਾਣਕਾਰੀ ਦੇ ਨਿਯਮ।',
    'safety.fastProtocol': 'ਸਟ੍ਰੋਕ ਲਈ FAST ਪ੍ਰੋਟੋਕੋਲ',
    'safety.miProtocol': 'ਦਿਲ ਦੇ ਦੌਰੇ ਦੇ ਚੇਤਾਵਨੀ ਸੰਕੇਤ',
    'safety.helplines': 'ਭਾਰਤ ਦੀਆਂ ਰਾਸ਼ਟਰੀ ਐਮਰਜੈਂਸੀ ਹੈਲਪਲਾਈਨਾਂ',
    'safety.helpline112': '112 - ਆਲ ਇੰਡੀਆ ਐਮਰਜੈਂਸੀ ਸੇਵਾ',
    'safety.helpline108': '108 - ਮੁਫ਼ਤ ਐਂਬੂਲੈਂਸ ਤੇ ਮੈਡੀਕਲ ਐਮਰਜੈਂਸੀ',
    'safety.helpline104': '104 - ਰਾਜ ਸਿਹਤ ਸਲਾਹ ਤੇ ਬਲੱਡ ਬੈਂਕ ਹੈਲਪਲਾਈਨ',
    'safety.helplineTeleManas': '14416 - ਟੈਲੀ-ਮਾਨਸ ਮਾਨਸਿਕ ਸਿਹਤ ਸਹਾਇਤਾ (24x7)',
    'safety.helplineJanAushadhi': '1800-180-8080 - ਪ੍ਰਧਾਨ ਮੰਤਰੀ ਜਨ ਔਸ਼ਧੀ ਹੈਲਪਲਾਈਨ',
  },
};

