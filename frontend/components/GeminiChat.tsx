"use client";
import { useState } from "react";

export default function GeminiChat() {
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim()) return;

    setLoading(true);
    setResponse(null);

    try {
      const res = await fetch("/api/gemini", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });

      if (!res.ok) {
        throw new Error(await res.text());
      }

      const data = await res.json();
      // Gemini response lives inside candidates[0].content.parts[0].text
      const output =
        data?.candidates?.[0]?.content?.parts?.[0]?.text || "No response";
      setResponse(output);
    } catch (err: any) {
      setResponse("❌ Error: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 border rounded-md shadow-md">
      <h2 className="text-xl font-bold mb-4">⚡ Gemini Demo</h2>
      <form onSubmit={handleSubmit} className="flex gap-2 mb-4">
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Ask Gemini something..."
          className="flex-1 px-3 py-2 border rounded-md"
        />
        <button
          type="submit"
          disabled={loading}
          className="px-4 py-2 bg-blue-600 text-white rounded-md"
        >
          {loading ? "Loading..." : "Ask"}
        </button>
      </form>
      {response && (
        <div className="mt-4 p-3 bg-gray-100 border rounded-md">
          <strong>Response:</strong>
          <p className="whitespace-pre-line">{response}</p>
        </div>
      )}
    </div>
  );
}

