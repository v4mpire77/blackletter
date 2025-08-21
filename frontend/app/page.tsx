'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { ArrowRightIcon, DocumentCheckIcon, ShieldCheckIcon, ChartBarIcon } from '@heroicons/react/24/outline'
import { FileUpload } from '@/components/file-upload'
import { ResultsDashboard } from '@/components/ResultsDashboard'
import { ProcessingStatus } from '@/components/ProcessingStatus'
import { SkipLinks } from '@/components/SkipLinks'
import { Button } from '@/components/ui/Button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { useContractAnalysis } from '@/hooks/useContractAnalysis'
import { useContractKeyboardShortcuts } from '@/hooks/useKeyboardShortcuts'
import GeminiChat from "../components/GeminiChat"; // New import

export default function Home() {
  const {
    isAnalyzing,
    uploadStatus,
    analysisProgress,
    result,
    error,
    analyzeContract,
    resetAnalysis
  } = useContractAnalysis()

  const [selectedFile, setSelectedFile] = useState<File | null>(null)

  // Keyboard shortcuts
  useContractKeyboardShortcuts({
    onUpload: () => {
      // Focus the file upload area
      const uploadArea = document.getElementById('contract-upload')
      uploadArea?.focus()
    },
    onHelp: () => {
      // Could open a help modal
      console.log('Help shortcuts: Cmd+U (Upload), Cmd+E (Export), Cmd+Shift+D (Dark mode)')
    }
  })

  const handleFileSelect = (file: File) => {
    setSelectedFile(file)
    analyzeContract(file)
  }

  const handleRemoveFile = () => {
    setSelectedFile(null)
    resetAnalysis()
  }

  const handleExport = (format: 'pdf' | 'json' | 'csv') => {
    if (!result) return
    
    // For demo purposes, just trigger a download
    const data = format === 'json' ? JSON.stringify(result, null, 2) : 'Export functionality would be implemented here'
    const blob = new Blob([data], { type: format === 'json' ? 'application/json' : 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `contract-analysis.${format}`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const features = [
    {
      icon: DocumentCheckIcon,
      title: 'AI-Powered Analysis',
      description: 'Advanced natural language processing to identify risks, compliance issues, and key clauses in your contracts.'
    },
    {
      icon: ShieldCheckIcon,
      title: 'GDPR & Legal Compliance',
      description: 'Comprehensive checks against UK/EU regulations, data protection requirements, and