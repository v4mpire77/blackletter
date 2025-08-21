'use client'

import { motion } from 'framer-motion'
import { ExclamationTriangleIcon, InformationCircleIcon, ShieldCheckIcon } from '@heroicons/react/24/outline'
import { Card, CardContent } from './ui/Card'
import { ContractIssue } from '@/types/contract.types'

interface ContractClauseCardProps {
  issue: ContractIssue
  onClick?: () => void
  className?: string
  expanded?: boolean
}

export function ContractClauseCard({ issue, onClick, className, expanded = false }: ContractClauseCardProps) {
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
      case 'medium':
        return <InformationCircleIcon className="h-5 w-5" />
      default:
        return <ShieldCheckIcon className="h-5 w-5" />
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-GB', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={className}
    >
      <Card 
        interactive={!!onClick}
        className={`transition-all duration-200 ${onClick ? 'cursor-pointer hover:shadow-md' : ''}`}
        onClick={onClick}
      >
        <CardContent className="p-4">
          <div className="flex items-start justify-between mb-3">
            <div className="flex items-center gap-3">
              <div className={`p-2 rounded-lg border ${getRiskColor(issue.riskLevel)}`}>
                {getSeverityIcon(issue.severity)}
              </div>
              <div>
                <span className={`px-2 py-1 rounded text-xs font-medium border ${getRiskColor(issue.riskLevel)}`}>
                  {issue.severity}
                </span>
                <span className="ml-2 text-xs text-muted-foreground">{issue.type}</span>
              </div>
            </div>
            <div className="text-right">
              <div className="text-sm font-medium">{Math.round(issue.confidence * 100)}%</div>
              <div className="text-xs text-muted-foreground">Confidence</div>
            </div>
          </div>

          <h4 className="font-semibold text-foreground mb-2 leading-tight">
            {issue.title}
          </h4>
          
          <p className="text-sm text-muted-foreground leading-relaxed mb-3">
            {issue.description}
          </p>

          <div className="flex items-center justify-between text-xs text-muted-foreground">
            <div className="flex items-center gap-4">
              {issue.pageNumber && (
                <span>Page {issue.pageNumber}</span>
              )}
              {issue.tags && issue.tags.length > 0 && (
                <div className="flex gap-1">
                  {issue.tags.slice(0, 2).map((tag, index) => (
                    <span 
                      key={index}
                      className="px-2 py-0.5 bg-neutral-100 dark:bg-neutral-800 rounded text-xs"
                    >
                      {tag}
                    </span>
                  ))}
                  {issue.tags.length > 2 && (
                    <span className="text-muted-foreground">
                      +{issue.tags.length - 2} more
                    </span>
                  )}
                </div>
              )}
            </div>
            <time dateTime={issue.timestamp}>
              {formatDate(issue.timestamp)}
            </time>
          </div>

          {expanded && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="mt-4 pt-4 border-t border-border space-y-3"
            >
              {issue.clause && (
                <div>
                  <h5 className="text-sm font-medium mb-2 text-foreground">Relevant Clause:</h5>
                  <div className="text-sm bg-muted p-3 rounded-md italic border-l-4 border-primary-500">
                    "{issue.clause}"
                  </div>
                </div>
              )}
              
              {issue.recommendation && (
                <div>
                  <h5 className="text-sm font-medium mb-2 text-foreground">Recommendation:</h5>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    {issue.recommendation}
                  </p>
                </div>
              )}
              
              {issue.remediation && (
                <div>
                  <h5 className="text-sm font-medium mb-2 text-foreground">Remediation:</h5>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    {issue.remediation}
                  </p>
                </div>
              )}

              {issue.citation && (
                <div>
                  <h5 className="text-sm font-medium mb-2 text-foreground">Legal Citation:</h5>
                  <p className="text-sm text-muted-foreground font-mono">
                    {issue.citation}
                  </p>
                </div>
              )}
            </motion.div>
          )}
        </CardContent>
      </Card>
    </motion.div>
  )
}