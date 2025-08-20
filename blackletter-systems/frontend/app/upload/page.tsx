"use client";
import { useState, FormEvent } from "react";
export default function Upload() {
  const [resp, setResp] = useState<any>(null);
  const [busy, setBusy] = useState(false);
  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault(); setBusy(true);
    const input = e.currentTarget.elements.namedItem("file") as HTMLInputElement;
    const file = input?.files?.[0]; if (!file) return;
    const fd = new FormData(); fd.append("file", file);
  const url = (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000") + "/api/review";
    const r = await fetch(url, { method: "POST", body: fd });
    const j = await r.json(); setResp(j); setBusy(false);
  }
  return (
    <main>
      <h1>Upload Contract</h1>
      <p className="file">Select a PDF contract to run the quick mock analysis.</p>
      <form onSubmit={onSubmit} className="form">
        <input name="file" type="file" accept="application/pdf" />
        <button className="btn" type="submit" disabled={busy}>
          {busy ? "Checking…" : "Check"}
        </button>
      </form>

      <h2>Response</h2>
      <div className="response">
        <pre style={{margin:0}}>{resp ? JSON.stringify(resp, null, 2) : "(none yet)"}</pre>
      </div>
    </main>
  );
}
