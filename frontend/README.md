# ADAPT-AI — Adaptive Healthcare Intelligence Platform (Web Application)

A modern, responsive, clinical-grade React 18 web application engineered for **ADAPT-AI (Adaptive AI Healthcare Intelligence Platform)**. Built specifically for India's healthcare landscape, empowering citizens with peer-reviewed medical guideline retrieval, deterministic red-flag emergency triage, multimodal diagnostic document analysis, GPS-based healthcare discovery, and hands-free multilingual voice assistance.

---

## 🧭 Architecture Highlights

### 1. Persistent Left Sidebar Navigation
- **Primary Desktop Navigation**: Fixed left sidebar (~260px wide, collapsible to 72px) with smooth Framer Motion transitions. The main content automatically adjusts so the sidebar never covers or overlaps content.
- **Brand & Visual Identity**: ADAPT-AI glowing clinical emblem, system connection pulse, and clear hierarchy.
- **Navigation Routes**:
  1. `Home` (`/`)
  2. `AI Health Assistant` (`/assistant`)
  3. `Healthcare Map` (`/healthcare-map`)
  4. `Find Healthcare` (`/find-healthcare`)
  5. `Medical Documents` (`/documents`)
  6. `Voice Assistant` (`/voice-assistant`)
  7. `Community Care` (`/community-care`)
  8. `Safety Center` (`/safety`)
- **Bottom Navigation**: Quick language switcher, Settings & Privacy (`/settings`), 24x7 emergency call action (`112 / 108`), and collapse/expand toggle.
- **Mobile Responsive Drawer**: Accessible slide-in navigation drawer with backdrop, triggered by the top contextual header.

### 2. Zero-Popup Seamless Patient Access
- **No Shared Secrets for Patients**: Ordinary users never see an API key configuration dialog.
- **Signed Patient Session Tokens**: The frontend transparently requests a time-limited patient session token from `POST /api/v1/auth/session` (authenticated via HMAC-SHA256).
- **Separated Developer Diagnostics**: Developers can optionally test administrative endpoints via an advanced diagnostics panel tucked in `/settings`.

---

## 🚀 Core Features & Modules

### 1. Home Page (`/`)
- **Headline**: "Healthcare Intelligence. Adapted to You."
- **Interactive Question Input**: Type a question directly on the hero section to automatically open and query the clinical assistant.
- **Quick Discovery Buttons**: Direct entry to "Ask a Health Question" and "Find Healthcare Near Me".
- **Verified Metrics**: Displays actual knowledge units in vector store and active engine health with zero fabricated statistics.

### 2. AI Health Assistant (`/assistant`)
- **Evidence-Grounded Inquiries**: Connected to `/api/v1/chat/question` with multi-turn session persistence.
- **Patient-Friendly Guideline Citations**: Clearly formatted source bodies (NICE, WHO, CDC, AIIMS) with confidence percentages and expandable original passages (no technical jargon like RAG or cosine similarity).
- **5-Tier Clinical Triage Engine**:
  - `EMERGENCY_IMMEDIATE` — Pulsing red alert with 1-click calling to National Emergency **112** and **108** Ambulance.
  - `URGENT_CARE` — Advises prompt in-person clinical assessment within 12–24 hours.
  - `ROUTINE_CLINICAL` — Recommends primary care consultation.
  - `SELF_CARE_EDUCATION` — Educational guidance and preventative health literacy.
  - `UNCERTAIN_AMBIGUOUS` — Highlights clinical ambiguity when symptoms are incomplete.
- **Copy Response & Retry Controls**: One-click clipboard copy and retry controls on network interruptions.

### 3. Interactive Healthcare Map (`/healthcare-map`)
- **GPS-Powered Healthcare Discovery**: HTML5 Geolocation (`navigator.geolocation`) with manual city jump (Delhi, Mumbai, Bengaluru, Chandigarh, Chennai, Kolkata, etc.).
- **Live Leaflet Map**: Custom pulsing GPS user marker, adjustable search radius slider (5 km to 50 km), and interactive facility pins with popups.
- **View Modes**: Split View (Map + List), Map Only, List Only.
- **Category Filters**: Hospitals (24x7 Emergency), Clinics & Outpatient, Primary Health Centres (PHC), Pharmacies, Jan Aushadhi Kendras, Blood Banks.
- **Actionable Facility Cards**: Displays distance in km, operating hours, inpatient bed count, click-to-call phone buttons, and Google Maps directions.

### 4. Pan-India Healthcare Search (`/find-healthcare`)
- **Nationwide Directory**: Search across AIIMS, District Civil Hospitals, Ayushman Arogya Mandirs (PHCs), Jan Aushadhi Kendras, and Blood Banks.
- **Filters**: State, Facility Type, 24x7 Emergency, Ayushman Bharat (PM-JAY) empanelment.

### 5. Diagnostic Document & Lab Report Analysis (`/documents`)
- **Multimodal Uploads**: Accepts PDF, PNG, JPG, JPEG, and TXT diagnostic reports and lab results.
- **Security & Provenance Tracking**: File preview, size validation (max 15MB), progress bar, and cryptographic SHA-256 hash.
- **OCR & Clinical Extraction**: Presents raw extracted clinical text side-by-side with plain-language diagnostic interpretation.
- **One-Click Sample Report**: Preloaded CBC & Serum Ferritin blood report for instantaneous testing.

### 6. Multilingual Voice Assistant (`/voice-assistant`)
- **Hands-Free Speech Recognition**: Utilizes Web Speech API for real-time speech-to-text.
- **Editable Transcript**: Spoken words appear in an editable text area before submission.
- **Animated Audio Waveform**: Real-time frequency bar visualizer that pulses during speech input and synthesis.
- **Speech Synthesis (TTS)**: Reads out clinical guidance in natural cadence with adjustable speech rate (0.7x – 1.4x) and mute toggle.
- **Supported Voice Languages**: English, Hindi, Hinglish, Punjabi, and Urdu (with RTL direction).

### 7. Community Care & Public Health Schemes (`/community-care`)
- **Ayushman Bharat PM-JAY**: Details ₹5 Lakh annual cashless hospitalization guarantee across 28,000+ empanelled hospitals.
- **Pradhan Mantri Jan Aushadhi (PMBJP)**: Guide to 10,000+ kendras offering 1,900+ generic drugs at 50%–90% savings.
- **e-RaktKosh National Blood Network**: Direct connection to live blood unit stocks and voluntary donor portals.
- **Tele-MANAS Mental Health Helpline**: 24x7 toll-free counseling support (**14416**).

### 8. Clinical Safety Center (`/safety`)
- **FAST Stroke Recognition**: Step-by-step visual guide for Face drooping, Arm weakness, Speech difficulty, Time to call 112.
- **Heart Attack Red Flags**: Clear clinical signs of acute myocardial infarction.
- **Regulatory Boundaries**: Transparently discloses non-prescription and non-diagnosis compliance.

---

## 🛠️ Tech Stack

- **Framework**: React 18.3.1 + TypeScript 5.6.3
- **Build Tool**: Vite 6.0.1 (Optimized manual code chunking)
- **Styling**: Tailwind CSS 3.4.16 + Tailwind Typography
- **Motion & Transitions**: Framer Motion 11.15.0
- **Icons**: Lucide React 0.468.0
- **Routing**: React Router DOM 6.28.0
- **Maps**: Leaflet 1.9.4 + CartoDB tiles
- **Testing**: Vitest 2.1.8 + Python unittest

---

## 💻 Installation & Development

### 1. Run the FastAPI Backend
In the repository root:
```bash
python run_server.py
```
The backend starts at `http://127.0.0.1:8000`.

### 2. Run the Frontend Development Server
In a separate terminal:
```bash
cd frontend
npm run dev
```
The frontend launches at `http://localhost:3000` (or `http://localhost:5173`). Requests to `/api/*` are automatically proxied to the FastAPI backend.

### 3. Run Automated Tests
```bash
# Frontend Unit Tests
cd frontend
npm test

# Backend Integration & Safety Tests
python -m unittest discover -s tests
```

### 4. Build for Production
```bash
cd frontend
npm run build
```
Creates minified, chunked production bundle in `dist/`.
