'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  ShieldCheckIcon, 
  ExclamationTriangleIcon, 
  DocumentArrowDownIcon,
  ClipboardDocumentListIcon,
  LightBulbIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline'
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card'
import { Button } from './ui/Button'
import { ProgressBar } from './ui/ProgressBar'
import { ContractAnalysis, ContractIssue } from '@/types/contract.types'

interface ResultsDashboardProps {
  analysis: ContractAnalysis
  onExport?: (format: 'pdf' | 'json' | 'csv') => void
  className?: string
}

type TabType = 'summary' | 'clauses' | 'nextSteps'

const tabs: { id: TabType; label: string; icon: React.ComponentType<any> }[] = [
  { id: 'summary', label: 'Summary', icon: ChartBarIcon },
  { id: 'clauses', label: 'Key Clauses', icon: ClipboardDocumentListIcon },
  { id: 'nextSteps', label: 'Next Steps', icon: LightBulbIcon },
]

export function ResultsDashboard({ analysis, onExport, className }: ResultsDashboardProps) {
  const [activeTab, setActiveTab] = useState<TabType>('summary')
  const [selectedIssue, setSelectedIssue] = useState<ContractIssue | null>(null)
  const [showExportModal, setShowExportModal] = useState(false)

  const getRiskColor = (riskLevel: string) => {
    switch (riskLevel) {
      case 'low': return 'text-risk-low border-risk-low bg-risk-low/10'
      case 'medium': return 'text-risk-medium border-risk-medium bg-risk-medium/10'
      case 'high': return 'text-risk-high border-risk-high bg-risk-high/10'
      case 'critical': return 'text-risk-critical border-risk-critical bg-risk-critical/10'
      default: return 'text-neutral-500 border-neutral-300 bg-neutral-50'
    }
  }

  const getSeverityIcon = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'critical':
      case 'high':
        return <ExclamationTriangleIcon className="h-5 w-5" />
      default:
        return <ShieldCheckIcon className="h-5 w-5" />
    }
  }

  const handleExport = (format: 'pdf' | 'json' | 'csv') => {
    onExport?.(format)
    setShowExportModal(false)
  }

  const formatRiskScore = (score: number) => {
    if (score >= 80) return { level: 'critical', text: 'Critical Risk' }
    if (score >= 60) return { level: 'high', text: 'High Risk' }
    if (score >= 40) return { level: 'medium', text: 'Medium Risk' }
    return { level: 'low', text: 'Low Risk' }
  }

  const riskAssessment = formatRiskScore(analysis.riskScore)

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header with Risk Assessment */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="space-y-4"
      >
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h2 className="text-2xl font-bold text-foreground">Contract Analysis Results</h2>
            <p className="text-muted-foreground mt-1">{analysis.filename}</p>
          </div>
          <Button
            variant="outline"
            onClick={() => setShowExportModal(true)}
            className="self-start sm:self-auto"
          >
            <DocumentArrowDownIcon className="h-4 w-4 mr-2" />
            Export Report
          </Button>
        </div>

        {/* Risk Score Card */}
        <Card variant="elevated" className="bg-gradient-to-br from-background to-neutral-50 dark:to-neutral-900">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <div className="flex items-center gap-3 mb-2">
                  <div className={`p-2 rounded-lg border ${getRiskColor(riskAssessment.level)}`}>
                    {getSeverityIcon(riskAssessment.level)}
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold">{riskAssessment.text}</h3>
                    <p className="text-sm text-muted-foreground">
                      {analysis.totalIssues} issues found across {Object.keys(analysis.issuesByType).length} categories
                    </p>
                  </div>
                </div>
              </div>
              <div className="text-right">
                <div className="text-3xl font-bold text-foreground">{analysis.riskScore}</div>
                <div className="text-sm text-muted-foreground">Risk Score</div>
              </div>
            </div>
            <ProgressBar
              value={analysis.riskScore}
              variant={riskAssessment.level as any}
              className="mt-4"
            />
          </CardContent>
        </Card>
      </motion.div>

      {/* Tabs Navigation */}
      <div className="border-b border-border">
        <nav className="flex space-x-8" aria-label="Analysis sections">
          {tabs.map((tab) => {
            const Icon = tab.icon
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 py-2 px-1 border-b-2 font-medium text-sm transition-colors duration-200 ${
                  activeTab === tab.id
                    ? 'border-primary-500 text-primary-600 dark:text-primary-400'
                    : 'border-transparent text-muted-foreground hover:text-foreground hover:border-neutral-300'
                }`}
                aria-current={activeTab === tab.id ? 'page' : undefined}
              >
                <Icon className="h-4 w-4" />
                {tab.label}
              </button>
            )
          })}
        </nav>
      </div>

      {/* Tab Content */}
      <AnimatePresence mode="wait">
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -20 }}
          transition={{ duration: 0.2 }}
        >
          {activeTab === 'summary' && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Summary Text */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Executive Summary</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground leading-relaxed">{analysis.summary}</p>
                </CardContent>
              </Card>

              {/* Key Metrics */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Key Metrics</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm font-medium">GDPR Compliance</span>
                      <span className="text-sm text-muted-foreground">
                        {analysis.keyMetrics.gdprCompliance}%
                      </span>
                    </div>
                    <ProgressBar 
                      value={analysis.keyMetrics.gdprCompliance} 
                      variant={analysis.keyMetrics.gdprCompliance >= 80 ? 'success' : 'warning'}
                    />
                  </div>
                  <div>
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm font-medium">Data Protection</span>
                      <span className="text-sm text-muted-foreground">
                        {analysis.keyMetrics.dataProtectionScore}%
                      </span>
                    </div>
                    <ProgressBar 
                      value={analysis.keyMetrics.dataProtectionScore}
                      variant={analysis.keyMetrics.dataProtectionScore >= 80 ? 'success' : 'warning'}
                    />
                  </div>
                  <div>
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm font-medium">Contractual Risk</span>
                      <span className="text-sm text-muted-foreground">
                        {analysis.keyMetrics.contractualRiskScore}%
                      </span>
                    </div>
                    <ProgressBar 
                      value={analysis.keyMetrics.contractualRiskScore}
                      variant={analysis.keyMetrics.contractualRiskScore <= 20 ? 'success' : 'danger'}
                    />
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {activeTab === 'clauses' && (
            <div className="space-y-4">
              <p className="text-muted-foreground">
                Found {analysis.issues.length} issues requiring attention
              </p>
              <div className="grid gap-4">
                {analysis.issues.map((issue) => (
                  <Card 
                    key={issue.id} 
                    interactive 
                    className="cursor-pointer"
                    onClick={() => setSelectedIssue(selectedIssue?.id === issue.id ? null : issue)}
                  >
                    <CardContent className="p-4">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center gap-3 mb-2">
                            <span className={`px-2 py-1 rounded text-xs font-medium border ${getRiskColor(issue.riskLevel)}`}>
                              {issue.severity}
                            </span>
                            <span className="text-xs text-muted-foreground">{issue.type}</span>
                          </div>
                          <h4 className="font-semibold text-foreground mb-1">{issue.title}</h4>
                          <p className="text-sm text-muted-foreground line-clamp-2">{issue.description}</p>
                          {issue.pageNumber && (
                            <p className="text-xs text-muted-foreground mt-2">Page {issue.pageNumber}</p>
                          )}
                        </div>
                        <div className="ml-4 text-right">
                          <div className="text-sm font-medium">{Math.round(issue.confidence * 100)}%</div>
                          <div className="text-xs text-muted-foreground">Confidence</div>
                        </div>
                      </div>
                      
                      <AnimatePresence>
                        {selectedIssue?.id === issue.id && (
                          <motion.div
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: 'auto' }}
                            exit={{ opacity: 0, height: 0 }}
                            className="mt-4 pt-4 border-t border-border"
                          >
                            {issue.clause && (
                              <div className="mb-3">
                                <h5 className="text-sm font-medium mb-1">Relevant Clause:</h5>
                                <div className="text-sm bg-muted p-3 rounded-md italic">
                                  "{issue.clause}"
                                </div>
                              </div>
                            )}
                            {issue.recommendation && (
                              <div className="mb-3">
                                <h5 className="text-sm font-medium mb-1">Recommendation:</h5>
                                <p className="text-sm text-muted-foreground">{issue.recommendation}</p>
                              </div>
                            )}
                            {issue.remediation && (
                              <div>
                                <h5 className="text-sm font-medium mb-1">Remediation:</h5>
                                <p className="text-sm text-muted-foreground">{issue.remediation}</p>
                              </div>
                            )}
                          </motion.div>
                        )}
                      </AnimatePresence>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'nextSteps' && (
            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Recommended Actions</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {analysis.nextSteps.map((step, index) => (
                      <div key={index} className="flex items-start gap-3">
                        <div className="flex-shrink-0 w-6 h-6 bg-primary-100 dark:bg-primary-900 text-primary-600 dark:text-primary-400 rounded-full flex items-center justify-center text-sm font-medium">
                          {index + 1}
                        </div>
                        <p className="text-sm text-muted-foreground">{step}</p>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Priority Recommendations</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {analysis.keyMetrics.recommendationsPriority.map((rec, index) => (
                      <div key={index} className="flex items-center gap-3 p-3 bg-muted rounded-md">
                        <ExclamationTriangleIcon className="h-5 w-5 text-amber-500" />
                        <span className="text-sm font-medium">{rec}</span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
        </motion.div>
      </AnimatePresence>

      {/* Export Modal */}
      <AnimatePresence>
        {showExportModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50"
            onClick={() => setShowExportModal(false)}
          >
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="bg-background rounded-lg p-6 w-full max-w-md"
              onClick={(e) => e.stopPropagation()}
            >
              <h3 className="text-lg font-semibold mb-4">Export Analysis Report</h3>
              <div className="space-y-3">
                <Button 
                  variant="outline" 
                  className="w-full justify-start"
                  onClick={() => handleExport('pdf')}
                >
                  <DocumentArrowDownIcon className="h-4 w-4 mr-2" />
                  PDF Report
                </Button>
                <Button 
                  variant="outline" 
                  className="w-full justify-start"
                  onClick={() => handleExport('json')}
                >
                  <DocumentArrowDownIcon className="h-4 w-4 mr-2" />
                  JSON Data
                </Button>
                <Button 
                  variant="outline" 
                  className="w-full justify-start"
                  onClick={() => handleExport('csv')}
                >
                  <DocumentArrowDownIcon className="h-4 w-4 mr-2" />
                  CSV Export
                </Button>
              </div>
              <div className="flex justify-end mt-6">
                <Button variant="ghost" onClick={() => setShowExportModal(false)}>
                  Cancel
                </Button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}