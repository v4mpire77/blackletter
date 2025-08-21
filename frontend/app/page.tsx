'use client';

import { useState } from 'react';
import { API_URL, apiGet } from '@/lib/api';

interface ReviewResult {
  summary: string;
  risks: string[];
}

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [analysis, setAnalysis] = useState<ReviewResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [reportUrl, setReportUrl] = useState<string | null>(null);
  const apiBase = API_URL;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    setError(null);
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      const uploadRes = await fetch(`${apiBase}/api/contracts`, {
        method: 'POST',
        body: formData,
      });
      if (!uploadRes.ok) {
        throw new Error(await uploadRes.text());
      }
      const { id } = await uploadRes.json();
      const data: ReviewResult = await apiGet(`/api/contracts/${id}/findings`);
      setAnalysis(data);
      setReportUrl(`${apiBase}/api/contracts/${id}/report`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen p-8">
      <h1 className="text-3xl font-bold mb-8">Blackletter Systems Contract Review</h1>
      
      <form onSubmit={handleSubmit} className="mb-8">
        <div className="mb-4">
          <input
            type="file"
            accept=".pdf"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
        </div>
        <button
          type="submit"
          disabled={!file || loading}
          className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 disabled:opacity-50"
        >
          {loading ? 'Analyzing...' : 'Analyze Contract'}
        </button>
      </form>

      {error && (
        <div className="bg-red-50 text-red-700 p-4 rounded-md mb-4">
          {error}
        </div>
      )}

      {analysis && (
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Analysis Results</h2>
          <h3 className="font-medium mb-2">Summary</h3>
          <p className="mb-4">{analysis.summary}</p>
          <h3 className="font-medium mb-2">Key Risks</h3>
          <ul className="list-disc pl-5 space-y-1">
            {analysis.risks.map((risk, idx) => (
              <li key={idx}>{risk}</li>
            ))}
          </ul>
          {reportUrl && (
            <a
              href={reportUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 underline block mt-4"
            >
              View report
            </a>
          )}
        </div>
      )}
    </main>
  );
}
