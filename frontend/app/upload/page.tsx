'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useDropzone } from 'react-dropzone'
import ProtectedRoute from '@/components/auth/ProtectedRoute'
import dynamic from 'next/dynamic'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { FileTextIcon, UploadIcon, ShieldIcon, LockIcon } from 'lucide-react'

function UploadPage() {
  const router = useRouter()
  const [file, setFile] = useState<File | null>(null)
  const [documentType, setDocumentType] = useState('contract')
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'application/pdf': ['.pdf'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt']
    },
    maxFiles: 1,
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        setFile(acceptedFiles[0])
        setError(null)
      }
    }
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!file) {
      setError('Please select a file to upload')
      return
    }

    try {
      setUploading(true)
      setError(null)
      
      const formData = new FormData()
      formData.append('file', file)
      formData.append('document_type', documentType)
      
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/contracts/upload`, {
        method: 'POST',
        body: formData,
      })
      
      if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`)
      }
      
      const data = await response.json()
      
      // Redirect to review page with the document key
      router.push(`/upload/review?key=${data.document_key}`)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred')
    } finally {
      setUploading(false)
    }
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-900 text-white">
        {/* Header */}
        <header className="bg-gray-800 border-b border-gray-700 px-8 py-6">
          <div className="max-w-6xl mx-auto">
            <div className="flex items-center space-x-3 mb-2">
              <div className="w-10 h-10 bg-purple-600 rounded-lg flex items-center justify-center">
                <FileTextIcon className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-white">Upload Contract</h1>
                <p className="text-gray-400">AI-powered contract analysis and compliance review</p>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-4xl mx-auto px-8 py-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Upload Section */}
            <div className="lg:col-span-2">
              <Card className="bg-gray-800 border-gray-700">
                <CardHeader>
                  <CardTitle className="text-xl text-white">Document Upload</CardTitle>
                  <CardDescription className="text-gray-400">
                    Drag and drop documents for AI-powered analysis
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  {error && (
                    <div className="bg-red-900/20 border border-red-700 text-red-300 px-4 py-3 rounded-lg">
                      {error}
                    </div>
                  )}
                  
                  <div>
                    <label htmlFor="documentType" className="block text-sm font-medium text-gray-300 mb-2">Document Type</label>
                    <select
                      id="documentType"
                      value={documentType}
                      onChange={(e) => setDocumentType(e.target.value)}
                      className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                      aria-label="Select document type"
                    >
                      <option value="contract">Contract</option>
                      <option value="legislation">Legislation</option>
                      <option value="case">Case</option>
                      <option value="article">Article</option>
                      <option value="other">Other</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">Upload Document</label>
                    <div
                      {...getRootProps()}
                      className={`border-2 border-dashed rounded-lg p-10 text-center cursor-pointer transition-colors ${
                        isDragActive ? 'border-purple-500 bg-purple-900/20' : 'border-gray-600 hover:border-gray-500 bg-gray-700/50'
                      }`}
                    >
                      <input {...getInputProps()} />
                      {file ? (
                        <div className="py-4">
                          <div className="w-16 h-16 bg-green-600 rounded-lg flex items-center justify-center mx-auto mb-4">
                            <FileTextIcon className="w-8 h-8 text-white" />
                          </div>
                          <p className="font-medium text-white text-lg">{file.name}</p>
                          <p className="text-gray-400">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                        </div>
                      ) : isDragActive ? (
                        <div className="py-10">
                          <UploadIcon className="w-16 h-16 mx-auto text-purple-400 mb-4" />
                          <p className="text-xl text-white">Drop the file here...</p>
                        </div>
                      ) : (
                        <div className="py-10">
                          <UploadIcon className="w-16 h-16 mx-auto text-gray-400 mb-4" />
                          <p className="text-lg text-white mb-2">Drag and drop a file here, or click to select</p>
                          <Button variant="outline" className="border-gray-600 text-gray-300 hover:bg-gray-700">
                            + Select Files
                          </Button>
                        </div>
                      )}
                    </div>
                  </div>
                  
                  <div className="flex justify-end">
                    <Button
                      type="submit"
                      disabled={uploading || !file}
                      onClick={handleSubmit}
                      className={`px-8 py-3 rounded-lg font-medium transition-colors ${
                        uploading || !file
                          ? 'bg-gray-600 cursor-not-allowed'
                          : 'bg-purple-600 hover:bg-purple-700 text-white'
                      }`}
                    >
                      {uploading ? (
                        <span className="flex items-center">
                          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                          Uploading...
                        </span>
                      ) : 'Upload Document'}
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Info Panel */}
            <div className="space-y-6">
              {/* File Types */}
              <Card className="bg-gray-800 border-gray-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center space-x-2">
                    <FileTextIcon className="w-5 h-5" />
                    <span>Supported Formats</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-center space-x-2">
                      <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                      <span className="text-gray-300">PDF, DOCX, DOC, TXT</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                      <span className="text-gray-300">Up to 50MB</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                      <span className="text-gray-300">256-bit encryption</span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Security */}
              <Card className="bg-gray-800 border-gray-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center space-x-2">
                    <ShieldIcon className="w-5 h-5" />
                    <span>Security & Privacy</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3 text-sm text-gray-300">
                    <p>• Enterprise-grade encryption</p>
                    <p>• GDPR compliant processing</p>
                    <p>• Secure cloud storage</p>
                    <p>• Audit trail logging</p>
                  </div>
                </CardContent>
              </Card>

              {/* Processing */}
              <Card className="bg-gray-800 border-gray-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center space-x-2">
                    <LockIcon className="w-5 h-5" />
                    <span>AI Processing</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3 text-sm text-gray-300">
                    <p>• Contract risk analysis</p>
                    <p>• Compliance checking</p>
                    <p>• Clause identification</p>
                    <p>• Redline suggestions</p>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  )
}

export default dynamic(() => Promise.resolve(UploadPage), {
  ssr: false
})