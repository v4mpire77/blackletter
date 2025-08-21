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
      description: 'Comprehensive checks against UK/EU regulations, data protection requirements, and industry standards.'
    },
    {
      icon: ChartBarIcon,
      title: 'Detailed Reporting',
      description: 'Professional reports with risk assessments, recommendations, and actionable next steps for your legal team.'
    }
  ]

  return (
    <>
      <SkipLinks />
      
      <main id="main-content" className="min-h-screen bg-gradient-to-br from-neutral-50 via-white to-neutral-100 dark:from-neutral-950 dark:via-neutral-900 dark:to-neutral-800">
        {/* Hero Section */}
        <section className="relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-r from-primary-500/5 to-legal-navy/5" />
          <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="text-center mb-16"
            >
              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-legal-navy dark:text-white mb-6">
                Professional Contract{' '}
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary-600 to-legal-gold">
                  Analysis
                </span>
              </h1>
              <p className="text-xl text-neutral-600 dark:text-neutral-300 max-w-3xl mx-auto leading-relaxed">
                Leverage advanced AI to identify risks, ensure compliance, and optimize your contracts with professional-grade analysis trusted by UK and EU legal professionals.
              </p>
            </motion.div>

            {/* Features Grid */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="grid md:grid-cols-3 gap-8 mb-16"
            >
              {features.map((feature, index) => (
                <Card key={index} variant="elevated" className="text-center group hover:shadow-legal transition-all duration-300">
                  <CardContent className="p-8">
                    <div className="inline-flex items-center justify-center w-16 h-16 rounded-lg bg-primary-100 dark:bg-primary-900 text-primary-600 dark:text-primary-400 mb-6 group-hover:scale-110 transition-transform duration-300">
                      <feature.icon className="h-8 w-8" />
                    </div>
                    <h3 className="text-xl font-semibold text-foreground mb-4">{feature.title}</h3>
                    <p className="text-muted-foreground leading-relaxed">{feature.description}</p>
                  </CardContent>
                </Card>
              ))}
            </motion.div>
          </div>
        </section>

        {/* Main Upload Section */}
        <section id="file-upload" className="py-16">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
            >
              {!result && !isAnalyzing && (
                <Card variant="elevated" className="mb-8">
                  <CardHeader className="text-center">
                    <CardTitle className="text-2xl">Upload Your Contract</CardTitle>
                    <p className="text-muted-foreground">
                      Upload a PDF contract to begin professional analysis
                    </p>
                  </CardHeader>
                  <CardContent className="px-8 pb-8">
                    <FileUpload
                      onFileSelect={handleFileSelect}
                      uploadStatus={uploadStatus}
                      selectedFile={selectedFile}
                      onRemoveFile={handleRemoveFile}
                      isLoading={isAnalyzing}
                    />
                  </CardContent>
                </Card>
              )}

              {error && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="mb-8"
                >
                  <Card variant="danger" className="border-red-200 dark:border-red-800">
                    <CardContent className="p-6">
                      <div className="flex items-center gap-3">
                        <div className="p-2 bg-red-100 dark:bg-red-900 rounded-lg">
                          <DocumentCheckIcon className="h-6 w-6 text-red-600 dark:text-red-400" />
                        </div>
                        <div>
                          <h3 className="font-semibold text-red-800 dark:text-red-200">Analysis Failed</h3>
                          <p className="text-red-600 dark:text-red-300 mt-1">{error}</p>
                        </div>
                      </div>
                      <div className="mt-4">
                        <Button variant="outline" onClick={resetAnalysis}>
                          Try Again
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                </motion.div>
              )}

              {isAnalyzing && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="mb-8"
                >
                  <ProcessingStatus progress={analysisProgress} />
                </motion.div>
              )}

              {result && (
                <motion.div
                  id="results"
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6 }}
                >
                  <ResultsDashboard
                    analysis={result}
                    onExport={handleExport}
                  />
                  
                  <div className="mt-8 text-center">
                    <Button variant="outline" onClick={resetAnalysis}>
                      Analyze Another Contract
                    </Button>
                  </div>
                </motion.div>
              )}
            </motion.div>
          </div>
        </section>

        {/* Additional Info Section */}
        {!result && !isAnalyzing && (
          <section className="py-16 bg-neutral-50 dark:bg-neutral-900/50">
            <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
              <motion.div
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.6 }}
              >
                <h2 className="text-3xl font-bold text-foreground mb-8">
                  Trusted by Legal Professionals
                </h2>
                <div className="grid md:grid-cols-2 gap-8">
                  <Card>
                    <CardContent className="p-6">
                      <h3 className="font-semibold text-lg mb-3">GDPR Compliance</h3>
                      <p className="text-muted-foreground">
                        Comprehensive analysis against UK and EU data protection regulations, ensuring your contracts meet the highest compliance standards.
                      </p>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardContent className="p-6">
                      <h3 className="font-semibold text-lg mb-3">Risk Assessment</h3>
                      <p className="text-muted-foreground">
                        Advanced AI identifies potential legal risks, liability issues, and areas requiring attention from your legal team.
                      </p>
                    </CardContent>
                  </Card>
                </div>
                <div className="mt-8">
                  <p className="text-sm text-muted-foreground">
                    Professional analysis • Secure processing • Detailed reporting
                  </p>
                </div>
              </motion.div>
            </div>
          </section>
        )}
      </main>
    </>
  )
}
