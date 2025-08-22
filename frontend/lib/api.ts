/**
 * API client for Blackletter Systems.
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Upload a document for analysis.
 */
export async function uploadDocument(file: File, documentType: string, metadata?: object) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('document_type', documentType);
  
  if (metadata) {
    formData.append('metadata', JSON.stringify(metadata));
  }
  
  const response = await fetch(`${API_URL}/contracts/upload`, {
    method: 'POST',
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
  const response = await fetch(`${API_URL}/contracts/review`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
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
  const response = await fetch(`${API_URL}/contracts/download/${encodeURIComponent(fileKey)}`);
  
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
  const response = await fetch(`${API_URL}/research/query`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
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
  const params = new URLSearchParams();
  
  if (sourceType) params.append('source_type', sourceType);
  if (tag) params.append('tag', tag);
  params.append('limit', limit.toString());
  params.append('offset', offset.toString());
  
  const response = await fetch(`${API_URL}/compliance/items?${params.toString()}`);
  
  if (!response.ok) {
    throw new Error(`Failed to get compliance items: ${response.statusText}`);
  }
  
  return await response.json();
}

/**
 * Get available compliance sources.
 */
export async function getComplianceSources() {
  const response = await fetch(`${API_URL}/compliance/sources`);
  
  if (!response.ok) {
    throw new Error(`Failed to get compliance sources: ${response.statusText}`);
  }
  
  return await response.json();
}

/**
 * Get available research sources.
 */
export async function getResearchSources(sourceType?: string, limit: number = 10, offset: number = 0) {
  const params = new URLSearchParams();
  
  if (sourceType) params.append('source_type', sourceType);
  params.append('limit', limit.toString());
  params.append('offset', offset.toString());
  
  const response = await fetch(`${API_URL}/research/sources?${params.toString()}`);
  
  if (!response.ok) {
    throw new Error(`Failed to get research sources: ${response.statusText}`);
  }
  
  return await response.json();
}
