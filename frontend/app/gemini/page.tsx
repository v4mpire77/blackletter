'use client';

import { useState } from 'react';

export default function GeminiChat() {
  const [prompt, setPrompt] = useState('');
  const [contract, setContract] = useState('');
  const [response, setResponse] = useState('');
  const [review, setReview] = useState('');

  // Gemini handler
  const handleGemini = async () => {
    const res = await fetch('/api/gemini', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt }),
    });
    const data = await res.json();
    setResponse(data.reply || JSON.stringify(data));
  };

  // Contract review handler
  const handleReview = async () => {
    const res = await fetch('/api/review', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ contractText: contract }),
    });
    const data = await res.json();
    setReview(JSON.stringify(data, null, 2));
  };

  return (
    <div>
      <h1>Gemini Chat</h1>
      <textarea
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Ask Gemini something..."
      />
      <button onClick={handleGemini}>Send to Gemini</button>
      <p>Gemini Response: {response}</p>

      <hr />

      <h1>Contract Review</h1>
      <textarea
        value={contract}
        onChange={(e) => setContract(e.target.value)}
        placeholder="Paste contract text here..."
      />
      <button onClick={handleReview}>Submit for Review</button>
      <pre>{review}</pre>
    </div>
  );
}
