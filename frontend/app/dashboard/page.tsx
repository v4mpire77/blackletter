"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card";
import { API_URL, apiGet } from "@/lib/api";
import { ResultsDashboard } from "@/components/results-dashboard";
import { FileUpload } from "@/components/file-upload";
import { ProcessingStatus } from "@/components/processing-status";
import { mockAnalysisResult, mockIssues } from "@/data/sample-analysis";
import { ContractAnalysisResult, Issue } from "@/types/contract-analysis";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { toPercent } from "@/lib/utils";


interface ContractEntry {
  id: string;
  name: string;
  status: "processing" | "done" | "error";
  summary?: string;
  error?: string;
}

export default function Dashboard() {
  // Combined state from both branches
  const [file, setFile] = useState<File | null>(null);
  const [contracts, setContracts] = useState<ContractEntry[]>([]);
  const [currentAnalysis, setCurrentAnalysis] = useState<ContractAnalysisResult | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [showSampleData, setShowSampleData] = useState(false);
  const apiBase = API_URL;

  const [darkMode, setDarkMode] = useState(false);
  const [apiHealth, setApiHealth] = useState<'loading' | 'ok' | 'error'>('loading');
  const [searchTerm, setSearchTerm] = useState("");
  const [typeFilter, setTypeFilter] = useState<"All" | "GDPR" | "Statute" | "Case Law">("All");
  const [severityFilter, setSeverityFilter] = useState<"All" | "High" | "Medium" | "Low">("All");
  const [statusFilter, setStatusFilter] = useState<"All" | "Open" | "In Review" | "Resolved">("All");
  const [gdprFocus, setGdprFocus] = useState(false);
  const [hideResolved, setHideResolved] = useState(false);
  const [issues, setIssues] = useState<Issue[]>(mockIssues);
  const [explanations, setExplanations] = useState<Record<string, { reasoning: string; citations: { source: string; url: string }[] }>>({});
  const ragApi = process.env.NEXT_PUBLIC_RAG_URL || 'http://localhost:8001';

  const filteredIssues = issues.filter(issue => {
    const termMatch = issue.snippet.toLowerCase().includes(searchTerm.toLowerCase()) || issue.recommendation.toLowerCase().includes(searchTerm.toLowerCase());
    const typeMatch = typeFilter === "All" || issue.type === typeFilter;
    const severityMatch = severityFilter === "All" || issue.severity === severityFilter;
    const statusMatch = statusFilter === "All" || issue.status === statusFilter;
    const gdprMatch = !gdprFocus || issue.type === "GDPR";
    const hideResolvedMatch = !hideResolved || issue.status !== "Resolved";
    return termMatch && typeMatch && severityMatch && statusMatch && gdprMatch && hideResolvedMatch;
  });

  // Combined logic from both branches
  async function fetchExplanation(id: string) {
    if (explanations[id]) return;
    try {
      const res = await fetch(`${ragApi}/rag/explain-finding`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ finding_id: id })
      });
      const data = await res.json();
      setExplanations(prev => ({ ...prev, [id]: data }));
    } catch (err) {
      // ignore errors for demo
    }
  }
  
  const runChecks = async () => {
    if (!file) return;
    setIsAnalyzing(true);
    const formData = new FormData();
    formData.append("file", file);
    const entry: ContractEntry = { id: "", name: file.name, status: "processing" };
    setContracts((prev) => [...prev, entry]);
    
    try {
      const uploadRes = await fetch(`${apiBase}/api/contracts`, {
        method: "POST",
        body: formData,
      });
      if (!uploadRes.ok) {
        throw new Error(await uploadRes.text());
      }
      const { id } = await uploadRes.json();
      const data = await apiGet(`/api/contracts/${id}/findings`);
      entry.id = id;
      entry.status = "done";
      entry.summary = data.summary;
      setContracts((prev) => [...prev]);

      const analysisResult: ContractAnalysisResult = {
        id: id,
        contractName: file.name,
        uploadedAt: new Date().toISOString(),
        status: "completed",
        summary: data.summary || "Analysis completed successfully.",
        totalIssues: 0,
        highRiskIssues: 0,
        mediumRiskIssues: 0,
        lowRiskIssues: 0,
        averageConfidence: 0.85,
        clauses: [],
        issues: [],
        riskScore: 45,
        complianceScore: 78
      };
      setCurrentAnalysis(analysisResult);
    } catch (err) {
      entry.status = "error";
      entry.error = err instanceof Error ? err.message : String(err);
      setContracts((prev) => [...prev]);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleAnalyzeSample = () => {
    setShowSampleData(true);
    setCurrentAnalysis(mockAnalysisResult);
  };

  const handleFileSelect = (selectedFile: File) => {
    setFile(selectedFile);
  };
  
  // Combined useEffects
  useEffect(() => {
    issues.forEach((i) => {
      if (!explanations[i.id]) {
        fetchExplanation(i.id);
      }
    });
  }, [issues]);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const response = await fetch('http://localhost:8000/health');
        if (response.ok) {
          setApiHealth('ok');
        } else {
          setApiHealth('error');
        }
      } catch (error) {
        setApiHealth('error');
      }
    };
    checkHealth();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header with Upload */}
      <div className="bg-gradient-to-r from-slate-50 to-slate-100 p-6 rounded-lg border">
        <h1 className="text-3xl font-bold mb-2">Contract Analysis Dashboard</h1>
        <p className="text-muted-foreground mb-6">
          Upload contracts for AI-powered compliance analysis and risk assessment
        </p>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Upload Contract</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <FileUpload
                onFileSelect={handleFileSelect}
                isLoading={isAnalyzing}
                acceptedTypes={['application/pdf']}
                maxSize={10 * 1024 * 1024}
              />
              <div className="flex gap-2">
                <Button onClick={runChecks} disabled={!file || isAnalyzing} className="flex-1">
                  {isAnalyzing ? "Analyzing..." : "Analyze Contract"}
                </Button>
                <Button variant="outline" onClick={handleAnalyzeSample}>
                  View Sample
                </Button>
              </div>
            </CardContent>
          </Card>

          {isAnalyzing && (
            <Card>
              <CardHeader>
                <CardTitle>Processing Status</CardTitle>
              </CardHeader>
              <CardContent>
                <ProcessingStatus
                  status="analyzing"
                  fileName={file?.name}
                  progress={65}
                  estimatedTime={30}
                />
              </CardContent>
            </Card>
          )}
        </div>
      </div>

      {/* Contract History */}
      {contracts.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Recent Analyses</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b">
                    <th className="text-left p-2">Contract</th>
                    <th className="text-left p-2">Status</th>
                    <th className="text-left p-2">Report</th>
                  </tr>
                </thead>
                <tbody>
                  {contracts.map((c, i) => (
                    <tr key={i} className="border-b">
                      <td className="p-2">{c.name}</td>
                      <td className="p-2">
                        <span className={`px-2 py-1 rounded-full text-xs ${
                          c.status === "done"
                            ? "bg-green-100 text-green-700"
                            : c.status === "processing"
                            ? "bg-blue-100 text-blue-700"
                            : "bg-red-100 text-red-700"
                        }`}>
                          {c.status === "done"
                            ? "Completed"
                            : c.status === "processing"
                            ? "Processing"
                            : "Error"}
                        </span>
                      </td>
                      <td className="p-2">
                        {c.status === "done" ? (
                          <Link
                            href={`${apiBase}/api/contracts/${c.id}/report`}
                            target="_blank"
                            className="text-blue-500 underline hover:text-blue-700"
                          >
                            View Report
                          </Link>
                        ) : c.status === "error" ? (
                          <span className="text-red-500 text-xs">{c.error}</span>
                        ) : (
                          <span className="text-muted-foreground">-</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Main Dashboard - Issues Table */}
      {currentAnalysis && (
        <Card>
          <CardHeader>
            <CardTitle>Analysis Results</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex gap-4 mb-4">
              <Input
                placeholder="Search issues..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
              <Button onClick={() => setHideResolved(prev => !prev)} variant={hideResolved ? "default" : "outline"}>
                {hideResolved ? "Show All Issues" : "Hide Resolved"}
              </Button>
            </div>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Document</TableHead>
                  <TableHead>Type</TableHead>
                  <TableHead>Severity</TableHead>
                  <TableHead>Snippet</TableHead>
                  <TableHead>Confidence</TableHead>
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredIssues.map((issue) => (
                  <TableRow key={issue.id}>
                    <TableCell>
                      <div className="max-w-[150px] truncate">{issue.docName}</div>
                    </TableCell>
                    <TableCell>
                      <Badge variant="outline">{issue.type}</Badge>
                    </TableCell>
                    <TableCell>
                      <Badge variant={issue.severity === "High" ? "destructive" : issue.severity === "Medium" ? "secondary" : "default"}>
                        {issue.severity}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <div className="max-w-[250px] truncate text-sm">{issue.snippet}</div>
                    </TableCell>
                    <TableCell>{toPercent(issue.confidence)}</TableCell>
                    <TableCell>
                      <Dialog>
                        <DialogTrigger asChild>
                          <Button variant="outline" size="sm">View</Button>
                        </DialogTrigger>
                        <DialogContent className="max-w-4xl">
                          <DialogHeader>
                            <DialogTitle>{issue.id} - {issue.docName}</DialogTitle>
                          </DialogHeader>
                          <Tabs defaultValue="details" className="w-full">
                            <TabsList>
                              <TabsTrigger value="details">Details</TabsTrigger>
                              <TabsTrigger value="trace">LLM Trace</TabsTrigger>
                              <TabsTrigger value="citations">Citations</TabsTrigger>
                              <TabsTrigger value="justification">Justification</TabsTrigger>
                              <TabsTrigger value="history">History</TabsTrigger>
                            </TabsList>
                            <TabsContent value="details" className="space-y-4">
                              <div className="grid grid-cols-2 gap-4">
                                <div>
                                  <Label>Clause Path</Label>
                                  <p className="mt-1">{issue.clausePath}</p>
                                </div>
                                <div>
                                  <Label>Citation</Label>
                                  <p className="mt-1">{issue.citation}</p>
                                </div>
                              </div>
                              <div>
                                <Label>Snippet</Label>
                                <Textarea value={issue.snippet} readOnly className="mt-1" rows={3} />
                              </div>
                              <div>
                                <Label>Recommendation</Label>
                                <Textarea value={issue.recommendation} readOnly className="mt-1" rows={4} />
                              </div>
                            </TabsContent>
                            <TabsContent value="trace" className="space-y-4">
                              <div className="rounded bg-neutral-50 p-4 dark:bg-neutral-800">
                                <pre className="whitespace-pre-wrap text-sm">
                                  {`Model: gpt-4-turbo
Input Tokens: 2,847
Output Tokens: 312
Latency: 2.3s
System: You are a UK legal compliance expert...
User: Analyze this clause for GDPR compliance...
Assistant: I've identified a high-severity GDPR issue...`}
                                </pre>
                              </div>
                            </TabsContent>
                            <TabsContent value="citations" className="space-y-4">
                              <div className="space-y-2">
                                <div className="rounded border p-3">
                                  <div className="font-medium">UK GDPR Article 44</div>
                                  <div className="mt-1 text-neutral-600 dark:text-neutral-400">
                                    General principle for transfers: Any transfer of personal data...
                                  </div>
                                </div>
                                <div className="rounded border p-3">
                                  <div className="font-medium">DPA 2018 Part 2</div>
                                  <div className="mt-1 text-neutral-600 dark:text-neutral-400">
                                    Processing for law enforcement purposes...
                                  </div>
                                </div>
                              </div>
                            </TabsContent>
                            <TabsContent value="justification" className="space-y-4">
                              {explanations[issue.id] ? (
                                <div className="space-y-4">
                                  <div>
                                    <Label>Reasoning</Label>
                                    <p className="mt-1 text-sm">{explanations[issue.id].reasoning}</p>
                                  </div>
                                  <div>
                                    <Label>Citations</Label>
                                    <ul className="list-disc list-inside">
                                      {explanations[issue.id].citations.map((c, i) => (
                                        <li key={i}>
                                          <a href={c.url} target="_blank" className="text-blue-500 underline">
                                            {c.source}
                                          </a>
                                        </li>
                                      ))}
                                    </ul>
                                  </div>
                                </div>
                              ) : (
                                <p className="text-sm text-neutral-500">Loading...</p>
                              )}
                            </TabsContent>
                            <TabsContent value="history" className="space-y-4">
                              <div className="space-y-2">
                                <div className="flex items-center gap-2 text-sm">
                                  <span className="text-neutral-500">2025-08-14 10:22</span>
                                  <span>Created by AI Analysis</span>
                                </div>
                                <div className="flex items-center gap-2 text-sm">
                                  <span className="text-neutral-500">2025-08-14 15:30</span>
                                  <span>Assigned to Omar</span>
                                </div>
                              </div>
                            </TabsContent>
                          </Tabs>
                        </DialogContent>
                      </Dialog>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
            {filteredIssues.length === 0 && (
              <div className="py-8 text-center text-neutral-500 dark:text-neutral-400">
                <p>No issues found matching the current filters.</p>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Results Dashboard - This is a separate component, not part of the conflict */}
      <ResultsDashboard
        analysisResult={currentAnalysis}
        onAnalyze={file ? runChecks : handleAnalyzeSample}
        isAnalyzing={isAnalyzing}
      />
    </div>
  );
}