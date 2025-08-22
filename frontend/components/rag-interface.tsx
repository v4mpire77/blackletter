"use client";

import React, { useState, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Separator } from '@/components/ui/separator';
import { Upload, Search, FileText, Brain, BarChart3, Compare } from 'lucide-react';

interface Document {
  doc_id: string;
  filename: string;
  upload_time: string;
  size: number;
  chunks_created: number;
  status: string;
}

interface QueryResult {
  answer: string;
  chunks: Array<{
    id: string;
    text: string;
    page: number;
    similarity_score: number;
    start_pos: number;
    end_pos: number;
  }>;
  query: string;
  total_chunks_retrieved: number;
}

interface SearchResult {
  id: string;
  doc_id: string;
  text: string;
  page: number;
  similarity_score: number;
  start_pos: number;
  end_pos: number;
  metadata: any;
}

export function RAGInterface() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [selectedDocument, setSelectedDocument] = useState<string>('');
  const [query, setQuery] = useState('');
  const [queryResult, setQueryResult] = useState<QueryResult | null>(null);
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  // Upload document
  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setIsLoading(true);
    setUploadProgress(0);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${API_BASE}/api/rag/upload`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        setDocuments(prev => [...prev, result]);
        setUploadProgress(100);
        alert('Document uploaded successfully!');
      } else {
        const error = await response.text();
        alert(`Upload failed: ${error}`);
      }
    } catch (error) {
      alert(`Upload error: ${error}`);
    } finally {
      setIsLoading(false);
      setUploadProgress(0);
    }
  };

  // Query documents
  const handleQuery = async () => {
    if (!query.trim()) return;

    setIsLoading(true);
    try {
      const formData = new URLSearchParams({
        query: query,
        top_k: '5',
        use_semantic_search: 'true'
      });

      if (selectedDocument) {
        formData.append('doc_id', selectedDocument);
      }

      const response = await fetch(`${API_BASE}/api/rag/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        setQueryResult(result);
      } else {
        const error = await response.text();
        alert(`Query failed: ${error}`);
      }
    } catch (error) {
      alert(`Query error: ${error}`);
    } finally {
      setIsLoading(false);
    }
  };

  // Search documents
  const handleSearch = async () => {
    if (!query.trim()) return;

    setIsLoading(true);
    try {
      const formData = new URLSearchParams({
        query: query,
        top_k: '10',
        similarity_threshold: '0.7'
      });

      if (selectedDocument) {
        formData.append('doc_id', selectedDocument);
      }

      const response = await fetch(`${API_BASE}/api/rag/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        setSearchResults(result.results || []);
      } else {
        const error = await response.text();
        alert(`Search failed: ${error}`);
      }
    } catch (error) {
      alert(`Search error: ${error}`);
    } finally {
      setIsLoading(false);
    }
  };

  // Load documents
  const loadDocuments = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/rag/documents`);
      if (response.ok) {
        const result = await response.json();
        setDocuments(result.documents || []);
      }
    } catch (error) {
      console.error('Failed to load documents:', error);
    }
  };

  // Load documents on component mount
  React.useEffect(() => {
    loadDocuments();
  }, []);

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-bold">RAG System Interface</h1>
        <p className="text-muted-foreground">
          Upload, search, and query your legal documents with AI-powered insights
        </p>
      </div>

      <Tabs defaultValue="upload" className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="upload" className="flex items-center gap-2">
            <Upload className="h-4 w-4" />
            Upload
          </TabsTrigger>
          <TabsTrigger value="query" className="flex items-center gap-2">
            <Brain className="h-4 w-4" />
            Query
          </TabsTrigger>
          <TabsTrigger value="search" className="flex items-center gap-2">
            <Search className="h-4 w-4" />
            Search
          </TabsTrigger>
          <TabsTrigger value="documents" className="flex items-center gap-2">
            <FileText className="h-4 w-4" />
            Documents
          </TabsTrigger>
        </TabsList>

        <TabsContent value="upload" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Upload Document</CardTitle>
              <CardDescription>
                Upload PDF, TXT, or DOCX files for RAG processing
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".pdf,.txt,.docx"
                  onChange={handleFileUpload}
                  className="hidden"
                  aria-label="Upload document file"
                />
                <Button
                  onClick={() => fileInputRef.current?.click()}
                  disabled={isLoading}
                  className="mb-4"
                >
                  <Upload className="h-4 w-4 mr-2" />
                  Choose File
                </Button>
                <p className="text-sm text-muted-foreground">
                  Supported formats: PDF, TXT, DOCX (max 10MB)
                </p>
              </div>
              
              {isLoading && (
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Uploading...</span>
                    <span>{uploadProgress}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${uploadProgress}%` }}
                    ></div>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="query" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Query Documents</CardTitle>
              <CardDescription>
                Ask questions about your documents and get AI-powered answers
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">Select Document (Optional)</label>
                <select
                  value={selectedDocument}
                  onChange={(e) => setSelectedDocument(e.target.value)}
                  className="w-full p-2 border rounded-md"
                  aria-label="Select document to query"
                >
                  <option value="">All Documents</option>
                  {documents.map((doc) => (
                    <option key={doc.doc_id} value={doc.doc_id}>
                      {doc.filename}
                    </option>
                  ))}
                </select>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Your Question</label>
                <Textarea
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="e.g., What are the payment terms in this contract?"
                  rows={3}
                />
              </div>

              <Button onClick={handleQuery} disabled={isLoading || !query.trim()}>
                {isLoading ? 'Processing...' : 'Ask Question'}
              </Button>

              {queryResult && (
                <div className="space-y-4 mt-6">
                  <Separator />
                  <div>
                    <h3 className="font-semibold mb-2">Answer:</h3>
                    <p className="text-sm bg-gray-50 p-3 rounded-md">
                      {queryResult.answer}
                    </p>
                  </div>
                  
                  <div>
                    <h3 className="font-semibold mb-2">Sources ({queryResult.total_chunks_retrieved}):</h3>
                    <div className="space-y-2">
                      {queryResult.chunks.map((chunk, index) => (
                        <div key={chunk.id} className="text-sm bg-gray-50 p-3 rounded-md">
                          <div className="flex justify-between items-center mb-1">
                            <Badge variant="secondary">Page {chunk.page}</Badge>
                            <Badge variant="outline">
                              Score: {chunk.similarity_score}
                            </Badge>
                          </div>
                          <p className="text-xs text-muted-foreground">
                            {chunk.text}
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="search" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Search Documents</CardTitle>
              <CardDescription>
                Find specific content across your documents
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">Select Document (Optional)</label>
                <select
                  value={selectedDocument}
                  onChange={(e) => setSelectedDocument(e.target.value)}
                  className="w-full p-2 border rounded-md"
                  aria-label="Select document to search"
                >
                  <option value="">All Documents</option>
                  {documents.map((doc) => (
                    <option key={doc.doc_id} value={doc.doc_id}>
                      {doc.filename}
                    </option>
                  ))}
                </select>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Search Query</label>
                <Input
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="e.g., liability clause, payment terms"
                />
              </div>

              <Button onClick={handleSearch} disabled={isLoading || !query.trim()}>
                {isLoading ? 'Searching...' : 'Search'}
              </Button>

              {searchResults.length > 0 && (
                <div className="space-y-4 mt-6">
                  <Separator />
                  <h3 className="font-semibold">Search Results ({searchResults.length}):</h3>
                  <div className="space-y-2">
                    {searchResults.map((result, index) => (
                      <div key={result.id} className="text-sm bg-gray-50 p-3 rounded-md">
                        <div className="flex justify-between items-center mb-1">
                          <Badge variant="secondary">Page {result.page}</Badge>
                          <Badge variant="outline">
                            Score: {result.similarity_score}
                          </Badge>
                        </div>
                        <p className="text-xs text-muted-foreground mb-1">
                          Document: {result.doc_id}
                        </p>
                        <p className="text-xs">
                          {result.text}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="documents" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Document Library</CardTitle>
              <CardDescription>
                Manage your uploaded documents
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {documents.length === 0 ? (
                  <p className="text-center text-muted-foreground">
                    No documents uploaded yet. Upload a document to get started.
                  </p>
                ) : (
                  documents.map((doc) => (
                    <div key={doc.doc_id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="space-y-1">
                        <h3 className="font-medium">{doc.filename}</h3>
                        <p className="text-sm text-muted-foreground">
                          Uploaded: {new Date(doc.upload_time).toLocaleDateString()}
                        </p>
                        <div className="flex gap-2">
                          <Badge variant="outline">
                            {doc.chunks_created} chunks
                          </Badge>
                          <Badge variant="secondary">
                            {(doc.size / 1024 / 1024).toFixed(2)} MB
                          </Badge>
                        </div>
                      </div>
                      <div className="flex gap-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => setSelectedDocument(doc.doc_id)}
                        >
                          Select
                        </Button>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
