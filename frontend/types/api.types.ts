export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  error?: string
  message?: string
}

export interface UploadResponse {
  id: string
  filename: string
  size: number
  uploadTime: string
}

export interface AnalysisResponse {
  filename: string
  size: number
  issues: Array<{
    id: string
    type: string
    title: string
    description: string
    severity: string
    clause?: string
    page_number?: number
    remediation?: string
    timestamp: string
  }>
}

export interface HealthCheckResponse {
  status: 'healthy' | 'unhealthy'
  version: string
  uptime: number
  checks: {
    database: 'ok' | 'error'
    storage: 'ok' | 'error'
    llm: 'ok' | 'error'
  }
}

export interface ErrorResponse {
  error: string
  details?: string
  code?: string
}