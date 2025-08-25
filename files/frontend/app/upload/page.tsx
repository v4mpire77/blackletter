"use client";
import { useState } from "react";
import { uploadContract } from "../lib/api";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<string>("");

  async function handleUpload() {
    if (!file) return;
    setStatus("Uploading...");
    const res = await uploadContract(file);
    if (res?.job_id) {
      setStatus("Processing. Job ID: " + res.job_id);
      // Optionally, redirect to dashboard or status page
    } else {
      setStatus("Upload failed.");
    }
  }

  return (
    <main className="container mx-auto p-8">
      <h1 className="text-2xl font-bold mb-4">Upload Contract</h1>
      <input
        type="file"
        accept=".pdf,.docx,.txt"
        onChange={(e) => setFile(e.target.files?.[0] ?? null)}
      />
      <button
        className="mt-4 px-4 py-2 bg-black text-white rounded"
        onClick={handleUpload}
        disabled={!file}
      >
        Upload
      </button>
      <div className="mt-4 text-sm">{status}</div>
    </main>
  );
}