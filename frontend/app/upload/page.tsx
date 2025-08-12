'use client';

import { useState, useEffect } from 'react';

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [apiHealth, setApiHealth] = useState<'ok' | 'error' | 'loading'>('loading');

  useEffect(() => {
    checkApiHealth();
  }, []);

  async function checkApiHealth() {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/health`);
      setApiHealth(res.ok ? 'ok' : 'error');
    } catch (e) {
      setApiHealth('error');
    }
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/review`, {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        throw new Error(await res.text());
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen p-8">
      <div className="mb-8 flex items-center justify-between">
        <h1 className="text-3xl font-bold">Contract Review</h1>
        <div className={`px-3 py-1 rounded-full text-sm ${
          apiHealth === 'ok' ? 'bg-green-100 text-green-700' :
          apiHealth === 'error' ? 'bg-red-100 text-red-700' :
          'bg-gray-100 text-gray-700'
        }`}>
          API: {apiHealth === 'loading' ? 'Checking...' : apiHealth.toUpperCase()}
        </div>
      </div>

      <form onSubmit={handleSubmit} className="mb-8">
        <div className="mb-4">
          <input
            type="file"
            accept="application/pdf"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
          <p className="mt-1 text-sm text-gray-500">Max file size: 10MB</p>
        </div>
        <button
          type="submit"
          disabled={!file || loading}
          className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 disabled:opacity-50"
        >
          {loading ? 'Analyzing...' : 'Review Contract'}
        </button>
      </form>

      {error && (
        <div className="bg-red-50 text-red-700 p-4 rounded-md mb-4">
          {error}
        </div>
      )}

      {result && (
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Analysis</h2>
          <div className="prose">
            <h3 className="text-lg font-medium mb-2">Summary</h3>
            <p className="mb-4">{result.summary}</p>
            
            <h3 className="text-lg font-medium mb-2">Key Risks</h3>
            <ul className="list-disc pl-5">
              {result.risks.map((risk: string, i: number) => (
                <li key={i} className="mb-2">{risk}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </main>
  );
}
