'use client'

import { motion } from 'framer-motion'
import { CheckCircleIcon, ClockIcon, ExclamationCircleIcon } from '@heroicons/react/24/outline'
import { ProgressBar } from './ui/ProgressBar'
import { AnalysisProgress } from '@/types/contract.types'

interface ProcessingStatusProps {
  progress: AnalysisProgress
  className?: string
}

const stageLabels = {
  upload: 'Uploading Document',
  ocr: 'Extracting Text',
  analysis: 'Analyzing Contract',
  validation: 'Validating Results',
  complete: 'Analysis Complete'
}

const stageIcons = {
  upload: ClockIcon,
  ocr: ClockIcon,
  analysis: ClockIcon,
  validation: ClockIcon,
  complete: CheckCircleIcon
}

export function ProcessingStatus({ progress, className }: ProcessingStatusProps) {
  const Icon = stageIcons[progress.stage]
  const isComplete = progress.stage === 'complete'
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`bg-white dark:bg-neutral-900 rounded-lg border border-neutral-200 dark:border-neutral-700 p-6 ${className}`}
    >
      <div className="flex items-center gap-4 mb-4">
        <div className={`p-2 rounded-full ${isComplete ? 'bg-risk-low/10 text-risk-low' : 'bg-primary-50 dark:bg-primary-950 text-primary-600 dark:text-primary-400'}`}>
          <Icon className="h-6 w-6" />
        </div>
        <div>
          <h3 className="font-semibold text-foreground">
            {stageLabels[progress.stage]}
          </h3>
          <p className="text-sm text-muted-foreground mt-1">
            {progress.message}
          </p>
        </div>
      </div>
      
      <ProgressBar
        value={progress.progress}
        variant={isComplete ? 'success' : 'default'}
        animated={!isComplete}
        showLabel
        label={`${progress.progress}% Complete`}
      />
      
      {!isComplete && (
        <div className="mt-4 flex justify-center">
          <div className="flex space-x-1">
            {[0, 1, 2].map((i) => (
              <motion.div
                key={i}
                className="w-2 h-2 bg-primary-500 rounded-full"
                animate={{ opacity: [0.3, 1, 0.3] }}
                transition={{
                  repeat: Infinity,
                  duration: 1.5,
                  delay: i * 0.2,
                  ease: 'easeInOut'
                }}
              />
            ))}
          </div>
        </div>
      )}
    </motion.div>
  )
}