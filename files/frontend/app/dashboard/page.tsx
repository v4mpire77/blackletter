"use client";
import { useEffect, useState } from "react";

type Issue = {
  id: string;
  doc_id: string;
  clause_path: string;
  type: "GDPR" | "Statute" | "Case Law";
  citation: string;
  severity: "High" | "Medium" | "Low";
  confidence: number;
  status: "Open" | "In Review" | "Resolved";
  snippet: string;
  recommendation: string;
  created_at: string;
};

type Coverage = {
  article: string;
  status: "OK" | "Partial" | "GAP";
  details?: string;
  found_clauses: string[];
};

type JobResult = {
  job_id: string;
  issues: Issue[];
  coverage: Coverage[];
  summary: string;
  confidence_score: number;
};

export default function DashboardPage() {
  const [jobId, setJobId] = useState<string>("");
  const [result, setResult] = useState<JobResult | null>(null);

  async function fetchResult() {
    if (!jobId) return;
    const res = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/jobs/${jobId}/result`
    );
    if (res.ok) {
      setResult(await res.json());
    } else {
      setResult(null);
    }
  }

  return (
    <main className="container mx-auto p-8">
      <h1 className="text-2xl font-bold mb-4">Compliance Dashboard</h1>
      <input
        className="border p-2"
        placeholder="Enter Job ID"
        value={jobId}
        onChange={(e) => setJobId(e.target.value)}
      />
      <button className="ml-2 px-4 py-2 bg-black text-white rounded" onClick={fetchResult}>
        Fetch Result
      </button>

      {result && (
        <div className="mt-6">
          <div className="font-bold">Summary:</div>
          <div className="mb-4">{result.summary}</div>
          <div className="font-bold">Issues:</div>
          <ul>
            {result.issues.map((issue) => (
              <li key={issue.id} className="mb-2 border-b pb-2">
                <div>
                  <strong>{issue.clause_path}</strong> [{issue.severity}]<br />
                  {issue.snippet}
                </div>
                <div className="text-xs text-gray-500">{issue.recommendation}</div>
              </li>
            ))}
          </ul>
          <div className="font-bold mt-4">Coverage Map:</div>
          <ul>
            {result.coverage.map((c) => (
              <li key={c.article}>
                {c.article}: {c.status}
              </li>
            ))}
          </ul>
        </div>
      )}
    </main>
  );
}