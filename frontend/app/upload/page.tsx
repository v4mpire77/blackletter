"use client";
import { useState } from "react";

export default function UploadPage() {
  const [res, setRes] = useState<any>(null);
  const [busy, setBusy] = useState(false);

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const f = new FormData(e.currentTarget);
    setBusy(true);
    try {
      const api = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const r = await fetch(`${api}/api/review`, { method: "POST", body: f });
      const j = await r.json();
      setRes(j);
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="p-6 space-y-4">
      <h2 className="text-xl font-semibold">Contract Review</h2>
      <form onSubmit={onSubmit} className="space-y-3">
        <input name="file" type="file" accept=".pdf,.txt" required className="block" />
        <button disabled={busy} className="rounded bg-black px-4 py-2 text-white">
          {busy ? "Analyzing…" : "Upload & Analyze"}
        </button>
      </form>
      {res && (
        <pre className="rounded bg-neutral-100 p-3 text-xs">{JSON.stringify(res, null, 2)}</pre>
      )}
    </main>
  );
}
