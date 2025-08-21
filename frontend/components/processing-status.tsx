'use client'

import React from 'react'
import { LoadingSpinner } from './loading-spinner'
import { designTokens } from '@/lib/design-tokens'

interface ProcessingStatusProps {
  status: 'uploading' | 'extracting' | 'analyzing' | 'complete' | 'error'
  progress?: number
  fileName?: string
  estimatedTime?: number
}

export function ProcessingStatus({
  status,
  progress = 0,
  fileName,
  estimatedTime,
}: ProcessingStatusProps) {
  const statusConfig = {
    uploading: {
      icon: '⬆️',
      title: 'Uploading contract',
      description: 'Securely transferring your file...',
      progressColor: 'bg-primary-500',
      iconColor: 'text-primary-600',
    },
    extracting: {
      icon: '📄',
      title: 'Extracting text',
      description: 'Reading contract content...',
      progressColor: 'bg-primary-500',
      iconColor: 'text-primary-600',
    },
    analyzing: {
      icon: '🔍',
      title: 'Analyzing contract',
      description: 'AI is reviewing clauses and identifying risks...',
      progressColor: 'bg-primary-500',
      iconColor: 'text-primary-600',
    },
    complete: {
      icon: '✅',
      title: 'Analysis complete',
      description: 'Your contract review is ready',
      progressColor: 'bg-semantic-success',
      iconColor: 'text-semantic-success',
    },
    error: {
      icon: '❌',
      title: 'Processing failed',
      description: 'Something went wrong. Please try again.',
      progressColor: 'bg-semantic-error',
      iconColor: 'text-semantic-error',
    },
  } as const

  const config = statusConfig[status]
  const isProgressVisible = status !== 'complete' && status !== 'error'

  const formatTime = (seconds?: number) => {
    if (seconds === undefined || seconds < 0) return ''
    const minutes = Math.floor(seconds / 60)
    const remainingSeconds = seconds % 60
    if (minutes > 0) {
      return `${minutes} min${remainingSeconds > 0 ? ` ${remainingSeconds} sec` : ''}`
    }
    return `${remainingSeconds} sec`
  }

  return (
    <div className="w-full max-w-md mx-auto p-6 bg-white rounded-xl shadow-lg">
      <div className="text-center mb-6">
        <div className={`text-4xl mb-2 ${config.iconColor}`}>{config.icon}</div>
        <h3 className="text-lg font-semibold text-neutral-900">{config.title}</h3>
        <p className="text-sm text-neutral-600 mt-1">{config.description}</p>
        {fileName && (
          <p className="text-xs text-neutral-500 mt-2 truncate">File: {fileName}</p>
        )}
      </div>

      {isProgressVisible && (
        <div className="mb-4">
          <div className="flex justify-between text-sm text-neutral-600 mb-2">
            <span>Progress</span>
            <span>{Math.round(progress)}%</span>
          </div>
          <div className="w-full bg-neutral-200 rounded-full h-2">
            <div
              className={`${config.progressColor} h-2 rounded-full ${designTokens.transition.duration} ${designTokens.transition.timing}`}
              style={{ width: `${progress}%` }}
              role="progressbar"
              aria-valuenow={progress}
              aria-valuemin={0}
              aria-valuemax={100}
            />
          </div>
        </div>
      )}

      {isProgressVisible && estimatedTime !== undefined && estimatedTime > 0 && (
        <div className="text-center text-sm text-neutral-500 mt-2">
          Estimated time remaining: {formatTime(estimatedTime)}
        </div>
      )}

      {isProgressVisible && (
        <div className="flex justify-center mt-4">
          <LoadingSpinner className="h-6 w-6 text-primary-600" />
        </div>
      )}
    </div>
  )
}
