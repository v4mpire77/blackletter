'use client'

import React from 'react'

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
  estimatedTime
}: ProcessingStatusProps) {
  const statusConfig = {
    uploading: {
      icon: '⬆️',
      title: 'Uploading contract',
      description: 'Securely transferring your file...',
      color: 'blue'
    },
    extracting: {
      icon: '📄',
      title: 'Extracting text',
      description: 'Reading contract content...',
      color: 'blue'
    },
    analyzing: {
      icon: '🔍',
      title: 'Analyzing contract',
      description: 'AI is reviewing clauses and identifying risks...',
      color: 'blue'
    },
    complete: {
      icon: '✅',
      title: 'Analysis complete',
      description: 'Your contract review is ready',
      color: 'green'
    },
    error: {
      icon: '❌',
      title: 'Processing failed',
      description: 'Something went wrong. Please try again.',
      color: 'red'
    }
  } as const

  const config = statusConfig[status]

  return (
    <div className="w-full max-w-md mx-auto p-6 bg-white rounded-xl shadow-lg">
      <div className="text-center mb-6">
        <div className="text-4xl mb-2">{config.icon}</div>
        <h3 className="text-lg font-semibold text-neutral-900">{config.title}</h3>
        <p className="text-sm text-neutral-600 mt-1">{config.description}</p>
        {fileName && <p className="text-xs text-neutral-500 mt-2 truncate">{fileName}</p>}
      </div>
      {status !== 'complete' && status !== 'error' && (
        <div className="mb-4">
          <div className="flex justify-between text-sm text-neutral-600 mb-2">
            <span>Progress</span>
            <span>{Math.round(progress)}%</span>
          </div>
          <div className="w-full bg-neutral-200 rounded-full h-2">
            <div
              className={`bg-${config.color}-500 h-2 rounded-full transition-all duration-500 ease-out`}
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      )}
      {estimatedTime && status !== 'complete' && status !== 'error' && (
        <div className="text-center text-sm text-neutral-500">
          Estimated time remaining: {Math.ceil(estimatedTime / 60)} minutes
        </div>
      )}
      {status !== 'complete' && status !== 'error' && (
        <div className="flex justify-center mt-4">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary-600"></div>
        </div>
      )}
    </div>
  )
}
