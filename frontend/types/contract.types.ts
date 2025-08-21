export interface ContractIssue {
  id: string
  type: 'GDPR' | 'Statute' | 'Case Law' | 'Best Practice'
  title: string
  description: string
  severity: 'Low' | 'Medium' | 'High' | 'Critical'
  riskLevel: 'low' | 'medium' | 'high' | 'critical'
  clause?: string
  pageNumber?: number
  recommendation?: string
  remediation?: string
  confidence: number
  timestamp: string
  tags?: string[]
  citation?: string
}

export interface ContractAnalysis {
  id: string
  filename: string
  fileSize: number
  uploadTime: string
  processingTime?: number
  summary: string
  riskScore: number
  totalIssues: number
  issuesByType: Record<string, number>
  issuesBySeverity: Record<string, number>
  issues: ContractIssue[]
  keyMetrics: {
    gdprCompliance: number
    dataProtectionScore: number
    contractualRiskScore: number
    recommendationsPriority: string[]
  }
  nextSteps: string[]
  reportUrl?: string
}

export interface FileUploadStatus {
  progress: number
  status: 'idle' | 'uploading' | 'processing' | 'completed' | 'error'
  error?: string
  estimatedTimeRemaining?: number
}

export interface AnalysisProgress {
  stage: 'upload' | 'ocr' | 'analysis' | 'validation' | 'complete'
  progress: number
  message: string
}