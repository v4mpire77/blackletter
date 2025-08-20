'use client'

import { useState, useCallback } from 'react'
import { useDropzone, FileRejection } from 'react-dropzone'
import { LoadingSpinner } from './loading-spinner'

interface FileUploadProps {
  onFileSelect: (file: File) => void
  maxSize?: number
  acceptedTypes?: string[]
  isLoading?: boolean
}

export function FileUpload({
  onFileSelect,
  maxSize = 10 * 1024 * 1024,
  acceptedTypes = ['application/pdf'],
  isLoading = false,
}: FileUploadProps) {
  const [errors, setErrors] = useState<string[]>([])

  const onDrop = useCallback(
    (acceptedFiles: File[], rejectedFiles: FileRejection[]) => {
      setErrors([])
      if (rejectedFiles.length > 0) {
        const errorMessages: string[] = []
        rejectedFiles.forEach(({ file, errors: rejectErrors }) => {
          rejectErrors.forEach((err) => {
            if (err.code === 'file-too-large') {
              errorMessages.push(
                `File "${file.name}" is too large. Max size is ${Math.round(maxSize / (1024 * 1024))}MB.`
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
        return
      }
      if (acceptedFiles.length > 0) {
        onFileSelect(acceptedFiles[0])
      }
    },
    [onFileSelect, maxSize, acceptedTypes]
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
  } = useDropzone({
    onDrop,
    maxSize,
    accept: acceptedMimeTypes,
    multiple: false,
    disabled: isLoading,
  })

  const borderColor =
    errors.length > 0
      ? 'border-red-500'
      : isDragAccept
      ? 'border-primary-500'
      : isDragReject
      ? 'border-red-500'
      : 'border-neutral-300'

  const backgroundColor =
    errors.length > 0
      ? 'bg-red-50'
      : isDragAccept
      ? 'bg-primary-50'
      : isDragReject
      ? 'bg-red-50'
      : 'hover:bg-neutral-50'

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div
        {...getRootProps()}
        className={`relative border-2 border-dashed rounded-xl p-8 text-center transition-all duration-200 ease-in-out ${borderColor} ${backgroundColor} ${
          isLoading ? 'opacity-70 cursor-not-allowed' : 'cursor-pointer'
        }`}
        aria-disabled={isLoading}
      >
        <input {...getInputProps()} id="contract-upload" />

        <div className="mb-4">
          <svg
            className="mx-auto h-12 w-12 text-neutral-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={1.5}
              d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
            />
          </svg>
        </div>

        <div className="space-y-2">
          <p className="text-lg font-medium text-neutral-900">
            {isLoading
              ? 'Processing...'
              : isDragActive
              ? 'Drop your contract here'
              : 'Upload your contract'}
          </p>
          <p className="text-sm text-neutral-600">
            Drag and drop a PDF file, or{' '}
            <span className="text-primary-600 font-medium">click to browse</span>
          </p>
          <p className="text-xs text-neutral-500">
            Maximum file size: {(maxSize / 1024 / 1024).toFixed(0)}MB • PDF only
          </p>
        </div>

        {isLoading && (
          <div className="absolute inset-0 flex items-center justify-center bg-white bg-opacity-75 rounded-xl">
            <LoadingSpinner className="text-primary-600 h-8 w-8" />
          </div>
        )}
      </div>

      {errors.length > 0 && (
        <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
          <div className="flex items-center">
            <svg className="h-5 w-5 text-red-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                clipRule="evenodd"
              />
            </svg>
            <div>
              {errors.map((error, index) => (
                <p key={index} className="text-sm text-red-700">
                  {error}
                </p>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
