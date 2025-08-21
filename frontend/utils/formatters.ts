/**
 * Format file size in human readable format
 */
export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes'
  
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

/**
 * Format risk score with appropriate color coding
 */
export const formatRiskScore = (score: number): { level: string; color: string; label: string } => {
  if (score >= 80) return { level: 'critical', color: 'text-risk-critical', label: 'Critical Risk' }
  if (score >= 60) return { level: 'high', color: 'text-risk-high', label: 'High Risk' }
  if (score >= 40) return { level: 'medium', color: 'text-risk-medium', label: 'Medium Risk' }
  return { level: 'low', color: 'text-risk-low', label: 'Low Risk' }
}

/**
 * Format percentage with appropriate precision
 */
export const formatPercentage = (value: number, precision: number = 1): string => {
  return `${value.toFixed(precision)}%`
}

/**
 * Format confidence score
 */
export const formatConfidence = (confidence: number): string => {
  return `${Math.round(confidence * 100)}%`
}

/**
 * Format date for display
 */
export const formatDate = (dateString: string, options?: Intl.DateTimeFormatOptions): string => {
  const defaultOptions: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }
  
  return new Date(dateString).toLocaleDateString('en-GB', { ...defaultOptions, ...options })
}

/**
 * Format relative time (e.g., "2 hours ago")
 */
export const formatRelativeTime = (dateString: string): string => {
  const date = new Date(dateString)
  const now = new Date()
  const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000)
  
  if (diffInSeconds < 60) return 'Just now'
  if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m ago`
  if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h ago`
  if (diffInSeconds < 2592000) return `${Math.floor(diffInSeconds / 86400)}d ago`
  
  return formatDate(dateString, { year: 'numeric', month: 'short', day: 'numeric' })
}

/**
 * Truncate text with ellipsis
 */
export const truncateText = (text: string, maxLength: number): string => {
  if (text.length <= maxLength) return text
  return text.slice(0, maxLength - 3) + '...'
}

/**
 * Format contract issue count
 */
export const formatIssueCount = (count: number): string => {
  if (count === 0) return 'No issues'
  if (count === 1) return '1 issue'
  return `${count} issues`
}

/**
 * Format processing time
 */
export const formatProcessingTime = (milliseconds: number): string => {
  const seconds = Math.floor(milliseconds / 1000)
  if (seconds < 60) return `${seconds}s`
  
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  
  if (remainingSeconds === 0) return `${minutes}m`
  return `${minutes}m ${remainingSeconds}s`
}

/**
 * Format currency (for potential billing features)
 */
export const formatCurrency = (amount: number, currency: string = 'GBP'): string => {
  return new Intl.NumberFormat('en-GB', {
    style: 'currency',
    currency
  }).format(amount)
}

/**
 * Sanitize filename for download
 */
export const sanitizeFilename = (filename: string): string => {
  return filename
    .replace(/[^a-z0-9]/gi, '_')
    .replace(/_+/g, '_')
    .replace(/^_|_$/g, '')
    .toLowerCase()
}

/**
 * Generate download filename with timestamp
 */
export const generateDownloadFilename = (baseFilename: string, extension: string): string => {
  const timestamp = new Date().toISOString().slice(0, 19).replace(/[:.]/g, '-')
  const sanitizedBase = sanitizeFilename(baseFilename)
  return `${sanitizedBase}_${timestamp}.${extension}`
}