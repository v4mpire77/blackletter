import { NextResponse } from "next/server";

export async function POST(request: Request) {
  try {
    const backendUrl = process.env.BACKEND_URL || "https://blackletter-backend.onrender.com/review";
    const body = await request.json();

    const response = await fetch(backendUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error("Error talking to backend:", error);
    return NextResponse.json(
      { error: "Failed to connect to backend" },
      { status: 500 }
    );
  }
}

export function GET() {
  return NextResponse.json({ error: "Method not allowed" }, { status: 405 });
}
