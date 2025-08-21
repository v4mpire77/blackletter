"use client";

import { useState } from "react";
import { Button } from "@/components/ui/Button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/Card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { cn } from "@/lib/utils"; // New import
import { Search, Loader2, LinkIcon } from "lucide-react"; // New import

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
    <div className="flex min-h-screen flex-col items-center justify-center p-4"> // Modified
      <Card className="w-full max-w-2xl shadow-lg rounded-lg"> // Modified
        <CardHeader>
          <CardTitle className="text-3xl font-bold text-center mb-4">Ask a legal question</CardTitle> // Modified
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="relative space-y-2"> // Modified
              <Label htmlFor="question">Question</Label>
              <Input
                id="question"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="What does clause 5 require?"
                className="pl-10" // Modified
              />
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" /> // New
            </div>
            <Button type="submit" disabled={!question || loading} className="w-full bg-blue-600 text-white hover:bg-blue-700"> // Modified
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" /> // New
                  Asking...
                </>
              ) : (
                "Ask"
              )}
            </Button>
          </form>

          {answer && (
            <Card className="mt-4 bg-gray-50 shadow-inner">
              <CardContent className="space-y-4">
                <p className="text-gray-800">{answer}</p>
                {citations.length > 0 && (
                  <div className="space-y-2">
                    <h4 className="font-semibold text-gray-700">Citations:</h4>
                    <ul className="list-none p-0 space-y-1">
                      {citations.map((c, i) => (
                        <li key={i} className="flex items-center text-sm text-gray-600">
                          <LinkIcon className="mr-2 h-4 w-4 text-blue-500" />
                          <a href={c.url} target="_blank" className="text-blue-500 hover:underline">
                            {c.source}
                          </a>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </CardContent>
            </Card>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

