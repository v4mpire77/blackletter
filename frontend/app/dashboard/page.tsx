"use client";

import { useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card";
import { API_URL, apiGet } from "@/lib/api";
import { ResultsDashboard } from "@/components/results-dashboard";
import { FileUpload } from "@/components/file-upload";
import { ProcessingStatus } from "@/components/processing-status";
import { mockAnalysisResult } from "@/data/sample-analysis";
import { ContractAnalysisResult } from "@/types/contract-analysis";

interface ContractEntry {
  id: string;
  name: string;
  status: "processing" | "done" | "error";
  summary?: string;
  error?: string;
}

export default function Dashboard() {
  const [file, setFile] = useState<File | null>(null);
  const [contracts, setContracts] = useState<ContractEntry[]>([]);
  const [currentAnalysis, setCurrentAnalysis] = useState<ContractAnalysisResult | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [showSampleData, setShowSampleData] = useState(false);
  const apiBase = API_URL;

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

      // Create a mock analysis result based on the real data
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

      {/* Results Dashboard */}
      <ResultsDashboard 
        analysisResult={currentAnalysis}
        onAnalyze={file ? runChecks : handleAnalyzeSample}
        isAnalyzing={isAnalyzing}
      />
    </div>
  );
}
