/**
 * ADAPT-AI Centralized API Service Client
 * Handles seamless patient session authentication and communication with the FastAPI backend.
 */

import {
  QuestionRequest,
  QuestionResponse,
  ImageUploadResponse,
  HealthStatus,
  ChatMessage,
} from '../types';

const DEFAULT_API_BASE = import.meta.env.VITE_API_BASE_URL || '';

// In-memory cache for patient session token
let inMemoryPatientToken: string | null = null;
let sessionFetchPromise: Promise<string> | null = null;

/**
 * Gets a developer override key if explicitly configured in Developer Settings
 */
export function getDeveloperOverrideKey(): string | null {
  try {
    if (typeof localStorage !== 'undefined') {
      return localStorage.getItem('adapt_ai_dev_override_key') || null;
    }
  } catch {
    // Ignore error in non-browser context
  }
  return null;
}

/**
 * Sets a developer override key for clinical test bench / debugging
 */
export function setDeveloperOverrideKey(key: string | null): void {
  try {
    if (typeof localStorage !== 'undefined') {
      if (key && key.trim()) {
        localStorage.setItem('adapt_ai_dev_override_key', key.trim());
      } else {
        localStorage.removeItem('adapt_ai_dev_override_key');
      }
    }
  } catch {
    // Ignore error in non-browser context
  }
}

/**
 * Ensures an active patient session token exists without prompting the user.
 * Communicates with POST /api/v1/auth/session to acquire signed time-limited access.
 */
export async function getActiveAuthToken(): Promise<string> {
  // Check developer override first
  const devKey = getDeveloperOverrideKey();
  if (devKey) {
    return devKey;
  }

  // Check in-memory token
  if (inMemoryPatientToken) {
    return inMemoryPatientToken;
  }

  // Check sessionStorage for tab persistence
  try {
    if (typeof sessionStorage !== 'undefined') {
      const stored = sessionStorage.getItem('adapt_ai_pat_token');
      if (stored) {
        inMemoryPatientToken = stored;
        return stored;
      }
    }
  } catch {
    // Ignore
  }

  // Acquire new patient session token
  if (!sessionFetchPromise) {
    sessionFetchPromise = (async () => {
      try {
        const url = `${DEFAULT_API_BASE}/api/v1/auth/session`;
        const res = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({}),
        });

        if (res.ok) {
          const data = await res.json();
          inMemoryPatientToken = data.token;
          try {
            if (typeof sessionStorage !== 'undefined') {
              sessionStorage.setItem('adapt_ai_pat_token', data.token);
            }
          } catch {
            // Ignore
          }
          return data.token;
        }
      } catch (err) {
        console.warn('Failed to obtain patient session token automatically:', err);
      }
      return '';
    })().finally(() => {
      sessionFetchPromise = null;
    });
  }

  return sessionFetchPromise;
}

async function request<T>(endpoint: string, options: RequestInit = {}, isRetry = false): Promise<T> {
  const url = `${DEFAULT_API_BASE}${endpoint}`;
  const token = await getActiveAuthToken();

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(token ? { 'X-API-Key': token } : {}),
    ...((options.headers as Record<string, string>) || {}),
  };

  try {
    const res = await fetch(url, {
      ...options,
      headers,
    });

    // If 401 Unauthorized, refresh the patient session token and retry once
    if (res.status === 401 && !isRetry) {
      inMemoryPatientToken = null;
      try {
        if (typeof sessionStorage !== 'undefined') {
          sessionStorage.removeItem('adapt_ai_pat_token');
        }
      } catch {
        // Ignore
      }
      return request<T>(endpoint, options, true);
    }

    if (!res.ok) {
      let errorMsg = `Server returned status ${res.status}`;
      try {
        const errorJson = await res.json();
        errorMsg = errorJson.detail || errorJson.message || errorMsg;
      } catch {
        // Fallback to status
      }
      throw new Error(errorMsg);
    }

    return (await res.json()) as T;
  } catch (err: any) {
    if (err.name === 'TypeError' && err.message.includes('fetch')) {
      throw new Error(
        'Unable to connect to ADAPT-AI Backend service at ' +
          (DEFAULT_API_BASE || 'localhost:8000') +
          '. Please ensure the backend server is running.'
      );
    }
    throw err;
  }
}

export const apiService = {
  /**
   * Health status check (public endpoint)
   */
  async getHealth(): Promise<HealthStatus> {
    return request<HealthStatus>('/api/v1/health');
  },

  /**
   * Submit healthcare question under clinical guardrails
   */
  async askQuestion(req: QuestionRequest): Promise<QuestionResponse> {
    return request<QuestionResponse>('/api/v1/chat/question', {
      method: 'POST',
      body: JSON.stringify(req),
    });
  },

  /**
   * Get session history turns
   */
  async getSessionHistory(sessionId: string): Promise<ChatMessage[]> {
    return request<ChatMessage[]>(`/api/v1/chat/history/${encodeURIComponent(sessionId)}`);
  },

  /**
   * Clear session history
   */
  async clearSession(sessionId: string): Promise<{ status: string; session_id: string }> {
    return request<{ status: string; session_id: string }>(
      `/api/v1/chat/session/${encodeURIComponent(sessionId)}`,
      { method: 'DELETE' }
    );
  },

  /**
   * Upload diagnostic image or document
   */
  async uploadDocument(payload: {
    filename: string;
    content_base64: string;
    prompt?: string;
  }): Promise<ImageUploadResponse> {
    return request<ImageUploadResponse>('/api/v1/media/upload', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  /**
   * Get RAG stats
   */
  async getRagStats(): Promise<any> {
    return request<any>('/api/v1/rag/stats');
  },
};
