"use client";

import { useState } from "react";
import { Button } from "@/components/ui/Button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

interface Citation {
  source: string;
  url: string;
}

export default function QA() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState<string | null>(null);
  const [citations, setCitations] = useState<Citation[]>([]);
  const [loading, setLoading] = useState(false);

  const api = process.env.NEXT_PUBLIC_RAG_URL || "http://localhost:8001";

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!question) return;
    setLoading(true);
    setAnswer(null);
    setCitations([]);
    try {
      const res = await fetch(`${api}/rag/qa`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      const data = await res.json();
      setAnswer(data.answer);
      setCitations(data.citations || []);
    } catch (err) {
      setAnswer("Error fetching answer");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="p-4 max-w-2xl mx-auto">
      <Card>
        <CardHeader>
          <CardTitle>Ask a legal question</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="question">Question</Label>
              <Input
                id="question"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="What does clause 5 require?"
              />
            </div>
            <Button type="submit" disabled={!question || loading}>
              {loading ? "Asking..." : "Ask"}
            </Button>
          </form>

          {answer && (
            <div className="mt-4 space-y-2">
              <p>{answer}</p>
              <ul className="list-disc list-inside">
                {citations.map((c, i) => (
                  <li key={i}>
                    <a href={c.url} target="_blank" className="text-blue-500 underline">
                      {c.source}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
