/**
 * API client for Blackletter Systems.
 */
import { createSupabaseClient } from './supabase'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

async function json<T>(res: Response): Promise<T> {
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

/**
 * Get auth headers for API requests
 */
async function getAuthHeaders(): Promise<Record<string, string>> {
  const supabase = createSupabaseClient()
  const { data: { session } } = await supabase.auth.getSession()
  
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  }
  
  if (session?.access_token) {
    headers['Authorization'] = `Bearer ${session.access_token}`
  }
  
  return headers
}

/**
 * Upload a document for analysis.
 */
export async function uploadDocument(file: File, documentType: string, metadata?: object) {
  const supabase = createSupabaseClient()
  const { data: { session } } = await supabase.auth.getSession()
  
  const formData = new FormData();
  formData.append('file', file);
  formData.append('document_type', documentType);
  
  if (metadata) {
    formData.append('metadata', JSON.stringify(metadata));
  }
  
  const headers: Record<string, string> = {}
  if (session?.access_token) {
    headers['Authorization'] = `Bearer ${session.access_token}`
  }
  
  const response = await fetch(`${API_URL}/contracts/upload`, {
    method: 'POST',
    headers,
    body: formData,
  });
  
  if (!response.ok) {
    throw new Error(`Upload failed: ${response.statusText}`);
  }
  
  return await response.json();
}

/**
 * Review a contract document.
 */
export async function reviewContract(documentKey: string, documentType: string, playbook?: string) {
  const headers = await getAuthHeaders();
  
  const response = await fetch(`${API_URL}/contracts/review`, {
    method: 'POST',
    headers,
    body: JSON.stringify({
      document_key: documentKey,
      document_type: documentType,
      playbook,
    }),
  });
  
  if (!response.ok) {
    throw new Error(`Review failed: ${response.statusText}`);
  }
  
  return await response.json();
}

/**
 * Get a download URL for a file.
 */
export async function getDownloadUrl(fileKey: string) {
  const headers = await getAuthHeaders();
  
  const response = await fetch(`${API_URL}/contracts/download/${encodeURIComponent(fileKey)}`, {
    headers,
  });
  
  if (!response.ok) {
    throw new Error(`Failed to get download URL: ${response.statusText}`);
  }
  
  const data = await response.json();
  return data.url;
}

/**
 * Submit a research query.
 */
export async function submitResearchQuery(query: string, filters?: object, limit: number = 10) {
  const headers = await getAuthHeaders();
  
  const response = await fetch(`${API_URL}/research/query`, {
    method: 'POST',
    headers,
    body: JSON.stringify({
      query,
      filters,
      limit,
    }),
  });
  
  if (!response.ok) {
    throw new Error(`Query failed: ${response.statusText}`);
  }
  
  return await response.json();
}

/**
 * Get compliance items.
 */
export async function getComplianceItems(sourceType?: string, tag?: string, limit: number = 10, offset: number = 0) {
  const headers = await getAuthHeaders();
  
  const params = new URLSearchParams();
  
  if (sourceType) params.append('source_type', sourceType);
  if (tag) params.append('tag', tag);
  params.append('limit', limit.toString());
  params.append('offset', offset.toString());
  
  const response = await fetch(`${API_URL}/compliance/items?${params.toString()}`, {
    headers,
  });
  
  if (!response.ok) {
    throw new Error(`Failed to get compliance items: ${response.statusText}`);
  }
  
  return await response.json();
}

/**
 * Get available compliance sources.
 */
export async function getComplianceSources() {
  const headers = await getAuthHeaders();
  
  const response = await fetch(`${API_URL}/compliance/sources`, {
    headers,
  });
  
  if (!response.ok) {
    throw new Error(`Failed to get compliance sources: ${response.statusText}`);
  }
  
  return await response.json();
}

/**
 * Get available research sources.
 */
export async function getResearchSources(sourceType?: string, limit: number = 10, offset: number = 0) {
  const headers = await getAuthHeaders();
  
  const params = new URLSearchParams();
  
  if (sourceType) params.append('source_type', sourceType);
  params.append('limit', limit.toString());
  params.append('offset', offset.toString());
  
  const response = await fetch(`${API_URL}/research/sources?${params.toString()}`, {
    headers,
  });
  
  if (!response.ok) {
    throw new Error(`Failed to get research sources: ${response.statusText}`);
  }
  
  return await response.json();
}

/**
 * RAG API Functions
 */

/**
 * Upload document to RAG system
 */
export async function uploadToRAG(file: File) {
  const supabase = createSupabaseClient()
  const { data: { session } } = await supabase.auth.getSession()
  
  const formData = new FormData();
  formData.append('file', file);
  
  const headers: Record<string, string> = {}
  if (session?.access_token) {
    headers['Authorization'] = `Bearer ${session.access_token}`
  }
  
  const response = await fetch(`${API_URL}/api/rag/upload`, {
    method: 'POST',
    headers,
    body: formData,
  });
  
  if (!response.ok) {
    throw new Error(`RAG upload failed: ${response.statusText}`);
  }
  
  return await response.json();
}

/**
 * Query RAG system
 */
export async function queryRAG(query: string, docId?: string, topK: number = 5) {
  const headers = await getAuthHeaders();
  
  const formData = new URLSearchParams({
    query: query.trim(),
    top_k: topK.toString(),
    use_semantic_search: 'true'
  });
  
  if (docId) {
    formData.append('doc_id', docId);
  }
  
  const response = await fetch(`${API_URL}/api/rag/query`, {
    method: 'POST',
    headers: {
      ...headers,
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: formData,
  });
  
  if (!response.ok) {
    throw new Error(`RAG query failed: ${response.statusText}`);
  }
  
  return await response.json();
}

export const api = {
  getIssues: () => fetch(`${API_URL}/api/issues`, { cache: 'no-store' }).then(json),
  analyze: (form: FormData) =>
    fetch(`${API_URL}/api/analyze`, { method: 'POST', body: form }).then(json),
  gdprCoverage: (docId: string) =>
    fetch(`${API_URL}/api/gdpr-coverage?docId=${encodeURIComponent(docId)}`).then(json),
  statuteCoverage: (docId: string) =>
    fetch(`${API_URL}/api/statute-coverage?docId=${encodeURIComponent(docId)}`).then(json),
  caselaw: (docId: string) =>
    fetch(`${API_URL}/api/caselaw?docId=${encodeURIComponent(docId)}`).then(json),
};
