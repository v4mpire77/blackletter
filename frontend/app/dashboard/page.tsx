"use client";

import { useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

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
  const apiBase = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const ragApi = process.env.NEXT_PUBLIC_RAG_URL || "http://localhost:8001";

  const runChecks = async () => {
    if (!file) return;
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
      const findingsRes = await fetch(`${apiBase}/api/contracts/${id}/findings`);
      if (!findingsRes.ok) {
        throw new Error(await findingsRes.text());
      }
      const data = await findingsRes.json();
      entry.id = id;
      entry.status = "done";
      entry.summary = data.summary;
      setContracts((prev) => [...prev]);

      if (data.findings) {
        await Promise.all(
          data.findings.map((f: { id: string }) =>
            fetch(`${ragApi}/rag/explain-finding`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ finding_id: f.id }),
            }).catch(() => null)
          )
        );
      }
    } catch (err) {
      entry.status = "error";
      entry.error = err instanceof Error ? err.message : String(err);
      setContracts((prev) => [...prev]);
    }
  };

  return (
    <div className="p-4 space-y-4">
      <div className="flex gap-2">
        <Input type="file" accept="application/pdf" onChange={(e) => setFile(e.target.files?.[0] || null)} />
        <Button onClick={runChecks} disabled={!file}>
          Run checks
        </Button>
      </div>
      {contracts.length > 0 && (
        <table className="w-full text-sm">
          <thead>
            <tr>
              <th className="text-left">Contract</th>
              <th>Status</th>
              <th>Report</th>
            </tr>
          </thead>
          <tbody>
            {contracts.map((c, i) => (
              <tr key={i} className="border-t">
                <td>{c.name}</td>
                <td>
                  {c.status === "done"
                    ? "Completed"
                    : c.status === "processing"
                    ? "Processing"
                    : "Error"}
                </td>
                <td>
                  {c.status === "done" ? (
                    <Link
                      href={`${apiBase}/api/contracts/${c.id}/report`}
                      target="_blank"
                      className="text-blue-500 underline"
                    >
                      View
                    </Link>
                  ) : c.status === "error" ? (
                    <span className="text-red-500">{c.error}</span>
                  ) : (
                    "-"
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

