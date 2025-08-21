"use client";
import { useState, FormEvent } from "react";

// Define types that match our backend schemas
type Severity = 'high' | 'medium' | 'low';

type IssueType = 
  | 'data_protection' 
  | 'consumer_rights' 
  | 'employment' 
  | 'gdpr' 
  | 'ip_rights' 
  | 'anti_money_laundering' 
  | 'competition_law' 
  | 'environmental' 
  | 'tax' 
  | 'other';

interface Issue {
  id: string;
  type: IssueType;
  title: string;
  description: string;
  severity: Severity;
  clause?: string;
  page_number?: number;
  remediation?: string;
  timestamp: string;
}

interface AnalysisResponse {
  filename: string;
  size: number;
  issues: Issue[];
}

export default function Upload() {
  const [response, setResponse] = useState<AnalysisResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  
  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setBusy(true);
    setError(null);
    
    const input = e.currentTarget.elements.namedItem("file") as HTMLInputElement;
    const file = input?.files?.[0]; 
    
    if (!file) {
      setError("Please select a file");
      setBusy(false);
      return;
    }
    
    try {
      const formData = new FormData(); 
      formData.append("file", file);
      const url = (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000") + "/api/review";
      
      const response = await fetch(url, { 
        method: "POST", 
        body: formData 
      });
      
      if (!response.ok) {
        throw new Error(`Error: ${response.status} ${response.statusText}`);
      }
      
      const data = await response.json();
      setResponse(data);
    } catch (err) {
      console.error("Upload error:", err);
      setError(err instanceof Error ? err.message : "Unknown error occurred");
    } finally {
      setBusy(false);
    }
  }
  
  // Helper function to get color based on severity
  const getSeverityColor = (severity: Severity) => {
    switch (severity) {
      case 'high': return 'red';
      case 'medium': return 'orange';
      case 'low': return 'blue';
      default: return 'gray';
    }
  };
  
  return (
    <main>
      <h1>Upload Contract</h1>
      <p className="file">Select a PDF contract to run the quick analysis.</p>
      
      <form onSubmit={onSubmit} className="form">
        <label htmlFor="file-upload">Contract PDF:</label>
        <input id="file-upload" name="file" type="file" accept="application/pdf" />
        <button className="btn" type="submit" disabled={busy}>
          {busy ? "Analyzing..." : "Analyze Contract"}
        </button>
      </form>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {response && (
        <div className="results">
          <h2>Analysis Results</h2>
          <div className="file-info">
            <p><strong>File:</strong> {response.filename}</p>
            <p><strong>Size:</strong> {(response.size / 1024).toFixed(2)} KB</p>
            <p><strong>Issues Found:</strong> {response.issues.length}</p>
          </div>
          
          {response.issues.length > 0 ? (
            <div className="issues-list">
              <h3>Compliance Issues</h3>
              {response.issues.map(issue => (
                <div 
                  key={issue.id} 
                  className="issue-card"
                  style={{ borderLeftColor: getSeverityColor(issue.severity) }}
                >
                  <h4>{issue.title}</h4>
                  <div className="issue-metadata">
                    <span className={`severity-badge severity-${issue.severity}`}>
                      {issue.severity.toUpperCase()}
                    </span>
                    <span>{issue.type.replace(/_/g, ' ').toUpperCase()}</span>
                    {issue.clause && <span>Clause: {issue.clause}</span>}
                    {issue.page_number && <span>Page: {issue.page_number}</span>}
                  </div>
                  <p className="issue-description">{issue.description}</p>
                  {issue.remediation && (
                    <div className="issue-remediation">
                      <strong>Recommendation:</strong> {issue.remediation}
                    </div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <div className="no-issues">
              <p>No compliance issues were detected in this contract.</p>
            </div>
          )}
        </div>
      )}

      {!response && !error && !busy && (
        <div className="response empty-state">
          <p>Upload a contract to see analysis results</p>
        </div>
      )}
    </main>
  );
}
