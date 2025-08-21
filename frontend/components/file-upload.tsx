'use client'

import { useState, useCallback, useRef, useEffect } from 'react'
import { useDropzone, FileRejection } from 'react-dropzone'
import { motion, AnimatePresence } from 'framer-motion'
import { CloudArrowUpIcon, DocumentTextIcon, XMarkIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline'
import { ProgressBar } from './ui/ProgressBar'
import { LoadingSpinner } from './loading-spinner'
import { FileUploadStatus } from '@/types/contract.types'

interface FileUploadProps {
  onFileSelect: (file: File) => void
  maxSize?: number
  acceptedTypes?: string[]
  isLoading?: boolean
  uploadStatus?: FileUploadStatus
  onRemoveFile?: () => void
  selectedFile?: File | null
}

export function FileUpload({
  onFileSelect,
  maxSize = 10 * 1024 * 1024,
  acceptedTypes = ['application/pdf'],
  isLoading = false,
  uploadStatus,
  onRemoveFile,
  selectedFile = null,
}: FileUploadProps) {
  const [errors, setErrors] = useState<string[]>([])
  const [announceMessage, setAnnounceMessage] = useState<string>('')
  const announceRef = useRef<HTMLDivElement>(null)

  // Screen reader announcements
  const announce = useCallback((message: string) => {
    setAnnounceMessage(message)
    setTimeout(() => setAnnounceMessage(''), 1000)
  }, [])

  const onDrop = useCallback(
    (acceptedFiles: File[], rejectedFiles: FileRejection[]) => {
      setErrors([])
      
      if (rejectedFiles.length > 0) {
        const errorMessages: string[] = []
        rejectedFiles.forEach(({ file, errors: rejectErrors }) => {
          rejectErrors.forEach((err) => {
            if (err.code === 'file-too-large') {
              errorMessages.push(
                `File "${file.name}" is too large. Maximum size is ${Math.round(maxSize / (1024 * 1024))}MB.`
              )
            } else if (err.code === 'file-invalid-type') {
              errorMessages.push(
                `File "${file.name}" has an unsupported type. Only ${acceptedTypes
                  .map((t) => t.split('/')[1].toUpperCase())
                  .join(', ')} files are allowed.`
              )
            } else {
              errorMessages.push(`File "${file.name}" error: ${err.message}`)
            }
          })
        })
        setErrors(errorMessages)
        announce(`Upload failed: ${errorMessages[0]}`)
        return
      }

      if (acceptedFiles.length > 0) {
        const file = acceptedFiles[0]
        onFileSelect(file)
        announce(`File ${file.name} selected successfully`)
      }
    },
    [onFileSelect, maxSize, acceptedTypes, announce]
  )

  const acceptedMimeTypes = acceptedTypes.reduce(
    (acc, type) => {
      const ext = type.split('/')[1]
      return { ...acc, [type]: [`.${ext}`] }
    },
    {} as Record<string, string[]>
  )

  const {
    getRootProps,
    getInputProps,
    isDragActive,
    isDragAccept,
    isDragReject,
    open
  } = useDropzone({
    onDrop,
    maxSize,
    accept: acceptedMimeTypes,
    multiple: false,
    disabled: isLoading,
    noClick: true, // Disable default click to handle manually for better a11y
  })

  // Enhanced keyboard navigation
  const handleKeyDown = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault()
      if (!isLoading) {
        open()
      }
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const borderColor = errors.length > 0
    ? 'border-red-500 dark:border-red-400'
    : isDragAccept
    ? 'border-primary-500 dark:border-primary-400'
    : isDragReject
    ? 'border-red-500 dark:border-red-400'
    : 'border-neutral-300 dark:border-neutral-600'

  const backgroundColor = errors.length > 0
    ? 'bg-red-50 dark:bg-red-950/50'
    : isDragAccept
    ? 'bg-primary-50 dark:bg-primary-950/50'
    : isDragReject
    ? 'bg-red-50 dark:bg-red-950/50'
    : 'bg-neutral-50 dark:bg-neutral-900 hover:bg-neutral-100 dark:hover:bg-neutral-800'

  return (
    <div className="w-full max-w-2xl mx-auto">
      {/* Screen reader announcements */}
      <div
        ref={announceRef}
        aria-live="polite"
        aria-atomic="true"
        className="sr-only"
      >
        {announceMessage}
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        <div
          {...getRootProps()}
          className={`relative border-2 border-dashed rounded-xl p-8 text-center transition-all duration-200 ease-in-out ${borderColor} ${backgroundColor} ${
            isLoading ? 'opacity-70 cursor-not-allowed' : 'cursor-pointer focus-within:ring-2 focus-within:ring-primary-500 focus-within:ring-offset-2'
          }`}
          role="button"
          tabIndex={isLoading ? -1 : 0}
          aria-disabled={isLoading}
          aria-label={selectedFile ? `Selected file: ${selectedFile.name}. Press Enter or Space to choose a different file.` : 'Choose a contract file to upload. Press Enter or Space to browse files.'}
          onKeyDown={handleKeyDown}
          onClick={!isLoading ? open : undefined}
        >
          <input 
            {...getInputProps()} 
            id="contract-upload"
            aria-describedby="upload-description upload-requirements"
          />

          <motion.div
            className="mb-6"
            animate={{
              scale: isDragActive ? 1.1 : 1,
              rotate: isDragActive ? 5 : 0
            }}
            transition={{ type: "spring", stiffness: 300, damping: 30 }}
          >
            {selectedFile ? (
              <DocumentTextIcon className="mx-auto h-16 w-16 text-primary-500" aria-hidden="true" />
            ) : (
              <CloudArrowUpIcon 
                className={`mx-auto h-16 w-16 transition-colors duration-200 ${
                  isDragAccept ? 'text-primary-500' : errors.length > 0 ? 'text-red-400' : 'text-neutral-400'
                }`}
                aria-hidden="true"
              />
            )}
          </motion.div>

          <div className="space-y-3">
            {selectedFile ? (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="space-y-2"
              >
                <p className="text-lg font-semibold text-foreground">
                  {selectedFile.name}
                </p>
                <p className="text-sm text-muted-foreground">
                  {formatFileSize(selectedFile.size)}
                </p>
                {onRemoveFile && (
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation()
                      onRemoveFile()
                      announce('File removed')
                    }}
                    className="inline-flex items-center gap-2 px-3 py-1.5 text-sm text-red-600 hover:text-red-700 transition-colors"
                    aria-label={`Remove file ${selectedFile.name}`}
                  >
                    <XMarkIcon className="h-4 w-4" aria-hidden="true" />
                    Remove file
                  </button>
                )}
              </motion.div>
            ) : (
              <div className="space-y-2">
                <p className="text-lg font-medium text-foreground" id="upload-description">
                  {isLoading
                    ? 'Processing your contract...'
                    : isDragActive
                    ? 'Drop your contract here'
                    : 'Upload your contract'}
                </p>
                <p className="text-sm text-muted-foreground">
                  Drag and drop a PDF file, or{' '}
                  <span className="text-primary-600 dark:text-primary-400 font-medium">click to browse</span>
                </p>
                <p className="text-xs text-muted-foreground" id="upload-requirements">
                  Maximum file size: {(maxSize / 1024 / 1024).toFixed(0)}MB • PDF files only
                </p>
              </div>
            )}
          </div>

          {/* Upload Progress */}
          {uploadStatus && uploadStatus.status !== 'idle' && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              className="mt-6 space-y-3"
            >
              <ProgressBar
                value={uploadStatus.progress}
                variant={uploadStatus.status === 'error' ? 'danger' : 'default'}
                animated={uploadStatus.status === 'uploading' || uploadStatus.status === 'processing'}
                showLabel
                label={uploadStatus.status === 'error' ? 'Error' : `${uploadStatus.status} ${uploadStatus.progress}%`}
              />
              {uploadStatus.estimatedTimeRemaining && (
                <p className="text-xs text-muted-foreground">
                  Estimated time remaining: {uploadStatus.estimatedTimeRemaining}s
                </p>
              )}
            </motion.div>
          )}

          {/* Loading Overlay */}
          <AnimatePresence>
            {isLoading && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="absolute inset-0 flex items-center justify-center bg-background/80 backdrop-blur-sm rounded-xl"
              >
                <div className="flex flex-col items-center gap-3">
                  <LoadingSpinner className="text-primary-600 h-8 w-8" />
                  <p className="text-sm font-medium text-foreground">Processing...</p>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </motion.div>

      {/* Error Messages */}
      <AnimatePresence>
        {errors.length > 0 && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="mt-4 p-4 bg-red-50 dark:bg-red-950/50 border border-red-200 dark:border-red-800 rounded-lg"
            role="alert"
            aria-labelledby="error-title"
          >
            <div className="flex items-start gap-3">
              <ExclamationTriangleIcon className="h-5 w-5 text-red-400 mt-0.5 flex-shrink-0" aria-hidden="true" />
              <div className="flex-1">
                <h3 id="error-title" className="text-sm font-medium text-red-800 dark:text-red-200 mb-2">
                  Upload Error{errors.length > 1 ? 's' : ''}
                </h3>
                <ul className="space-y-1">
                  {errors.map((error, index) => (
                    <li key={index} className="text-sm text-red-700 dark:text-red-300">
                      {error}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
