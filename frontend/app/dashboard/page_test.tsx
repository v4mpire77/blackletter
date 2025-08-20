"use client";

import React from "react";

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-4">
        Dashboard Test
      </h1>
      <p className="text-gray-600">
        If you can see this, the basic component is working.
      </p>
      <div className="mt-8 p-4 bg-white rounded-lg shadow">
        <h2 className="text-xl font-semibold mb-2">Test Card</h2>
        <p>This is a test to ensure the page renders correctly.</p>
      </div>
    </div>
  );
}
