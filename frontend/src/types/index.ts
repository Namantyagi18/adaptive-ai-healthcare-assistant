/**
 * ADAPT-AI Core Type Definitions
 * Strict types matching backend schemas and frontend UI components.
 */

export type TriageLevel =
  | 'EMERGENCY_IMMEDIATE'
  | 'URGENT_CARE'
  | 'ROUTINE_CLINICAL'
  | 'SELF_CARE_EDUCATION'
  | 'UNCERTAIN_AMBIGUOUS';

export type EvidenceSufficiency = 'SUFFICIENT' | 'INSUFFICIENT' | 'CONTRADICTORY';

export interface EvidenceReference {
  doc_id: string;
  title: string;
  source: string;
  chunk_id: string;
  relevance_score: number;
  excerpt: string;
}

export interface QuestionRequest {
  question: string;
  session_id?: string;
  include_citations?: boolean;
  language_hint?: string;
  country_code?: string;
}

export interface QuestionResponse {
  answer: string;
  triage_level: TriageLevel;
  is_emergency: boolean;
  emergency_guidance?: string | null;
  citations: EvidenceReference[];
  evidence_sufficiency: EvidenceSufficiency;
  uncertainty_statement?: string | null;
  follow_up_questions: string[];
  session_id: string;
  model_used: string;
  latency_ms: number;
  safety_disclaimer: string;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
  isEmergency?: boolean;
  triageLevel?: TriageLevel;
  citations?: EvidenceReference[];
  emergencyGuidance?: string | null;
  evidenceSufficiency?: EvidenceSufficiency;
  uncertaintyStatement?: string | null;
  followUpQuestions?: string[];
  latencyMs?: number;
  modelUsed?: string;
}

export interface ImageUploadResponse {
  file_id: string;
  original_filename: string;
  content_type: string;
  size_bytes: number;
  sha256_hash: string;
  quarantined_path: string;
  image_metadata: Record<string, any>;
  text_extracted?: string | null;
  extraction_status: string;
  clinical_interpretation: string;
  safety_note: string;
}

export interface HealthStatus {
  status: string;
  service: string;
  version: string;
  environment: string;
  components: {
    model_adapter: {
      name: string;
      healthy: boolean;
      configured_provider: string;
    };
    vector_store: {
      total_documents: number;
      total_chunks: number;
      categories: Record<string, number>;
    };
  };
}

export type FacilityType =
  | 'hospital'
  | 'clinic'
  | 'pharmacy'
  | 'blood_bank'
  | 'phc'
  | 'jan_aushadhi';

export interface Facility {
  id: string;
  name: string;
  type: FacilityType;
  address: string;
  city: string;
  state: string;
  pincode?: string;
  lat: number;
  lon: number;
  phone?: string;
  emergency?: boolean;
  beds?: number;
  distanceKm?: number;
  operatingHours?: string;
  schemesSupported?: string[]; // e.g. ["PM-JAY", "CGHS", "Ayushman Bharat"]
}

export interface LanguageInfo {
  code: string;
  name: string;
  nativeName: string;
  dir: 'ltr' | 'rtl';
  flag: string;
}

