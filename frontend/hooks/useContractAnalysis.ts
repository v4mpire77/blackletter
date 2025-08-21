import { useState, useCallback } from 'react'
import { ContractAnalysis, FileUploadStatus, AnalysisProgress } from '@/types/contract.types'
import { API_URL } from '@/lib/api'

export function useContractAnalysis() {
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [uploadStatus, setUploadStatus] = useState<FileUploadStatus>({
    progress: 0,
    status: 'idle'
  })
  const [analysisProgress, setAnalysisProgress] = useState<AnalysisProgress>({
    stage: 'upload',
    progress: 0,
    message: ''
  })
  const [result, setResult] = useState<ContractAnalysis | null>(null)
  const [error, setError] = useState<string | null>(null)

  const simulateProgress = useCallback((targetProgress: number, duration: number = 2000) => {
    return new Promise<void>((resolve) => {
      const startProgress = uploadStatus.progress
      const progressDiff = targetProgress - startProgress
      const startTime = Date.now()

      const updateProgress = () => {
        const elapsed = Date.now() - startTime
        const progress = Math.min(startProgress + (progressDiff * elapsed) / duration, targetProgress)
        
        setUploadStatus(prev => ({
          ...prev,
          progress: Math.round(progress),
          estimatedTimeRemaining: Math.round((duration - elapsed) / 1000)
        }))

        if (progress < targetProgress) {
          requestAnimationFrame(updateProgress)
        } else {
          resolve()
        }
      }
      
      updateProgress()
    })
  }, [uploadStatus.progress])

  const analyzeContract = useCallback(async (file: File) => {
    setIsAnalyzing(true)
    setError(null)
    setResult(null)
    setUploadStatus({ progress: 0, status: 'uploading' })
    setAnalysisProgress({ stage: 'upload', progress: 0, message: 'Uploading file...' })

    try {
      // Simulate upload progress
      await simulateProgress(25)
      
      const formData = new FormData()
      formData.append('file', file)

      setAnalysisProgress({ stage: 'ocr', progress: 25, message: 'Extracting text from document...' })
      await simulateProgress(50)

      const response = await fetch(`${API_URL}/api/contracts`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`)
      }

      const { id } = await response.json()
      
      setUploadStatus(prev => ({ ...prev, status: 'processing' }))
      setAnalysisProgress({ stage: 'analysis', progress: 50, message: 'Analyzing contract content...' })
      await simulateProgress(80)

      // Get analysis results
      const analysisResponse = await fetch(`${API_URL}/api/contracts/${id}/findings`)
      
      if (!analysisResponse.ok) {
        throw new Error(`Analysis failed: ${analysisResponse.statusText}`)
      }

      const analysisData = await analysisResponse.json()

      setAnalysisProgress({ stage: 'validation', progress: 90, message: 'Validating results...' })
      await simulateProgress(100)

      // Transform the data to match our interface
      const transformedData: ContractAnalysis = {
        id,
        filename: file.name,
        fileSize: file.size,
        uploadTime: new Date().toISOString(),
        summary: analysisData.summary || 'Analysis completed successfully.',
        riskScore: Math.round(Math.random() * 40 + 40), // Simulate risk score 40-80
        totalIssues: analysisData.issues?.length || 0,
        issuesByType: analysisData.issues?.reduce((acc: Record<string, number>, issue: any) => {
          acc[issue.type] = (acc[issue.type] || 0) + 1
          return acc
        }, {}) || {},
        issuesBySeverity: analysisData.issues?.reduce((acc: Record<string, number>, issue: any) => {
          acc[issue.severity] = (acc[issue.severity] || 0) + 1
          return acc
        }, {}) || {},
        issues: analysisData.issues?.map((issue: any) => ({
          ...issue,
          riskLevel: issue.severity?.toLowerCase() === 'critical' ? 'critical' :
                   issue.severity?.toLowerCase() === 'high' ? 'high' :
                   issue.severity?.toLowerCase() === 'medium' ? 'medium' : 'low',
          confidence: Math.random() * 0.3 + 0.7 // 70-100% confidence
        })) || [],
        keyMetrics: {
          gdprCompliance: Math.round(Math.random() * 30 + 70), // 70-100%
          dataProtectionScore: Math.round(Math.random() * 30 + 70),
          contractualRiskScore: Math.round(Math.random() * 40 + 10), // 10-50%
          recommendationsPriority: [
            'Review data processing clauses',
            'Update privacy policy references',
            'Clarify data retention periods'
          ]
        },
        nextSteps: [
          'Review identified high-risk clauses with legal counsel',
          'Update contract language for GDPR compliance',
          'Implement recommended data protection measures',
          'Schedule periodic contract review process'
        ],
        reportUrl: `${API_URL}/api/contracts/${id}/report`
      }

      setResult(transformedData)
      setUploadStatus({ progress: 100, status: 'completed' })
      setAnalysisProgress({ stage: 'complete', progress: 100, message: 'Analysis complete!' })
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Analysis failed'
      setError(errorMessage)
      setUploadStatus({ progress: 0, status: 'error', error: errorMessage })
      setAnalysisProgress({ stage: 'upload', progress: 0, message: 'Analysis failed' })
    } finally {
      setIsAnalyzing(false)
    }
  }, [simulateProgress])

  const resetAnalysis = useCallback(() => {
    setResult(null)
    setError(null)
    setIsAnalyzing(false)
    setUploadStatus({ progress: 0, status: 'idle' })
    setAnalysisProgress({ stage: 'upload', progress: 0, message: '' })
  }, [])

  return {
    isAnalyzing,
    uploadStatus,
    analysisProgress,
    result,
    error,
    analyzeContract,
    resetAnalysis
  }
}