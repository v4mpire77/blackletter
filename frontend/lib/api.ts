export const API_URL = process.env.NEXT_PUBLIC_API_URL!;

export async function apiGet(path: string, init?: RequestInit) {
  const res = await fetch(`${API_URL}${path}`, { ...init, cache: "no-store" });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}
export async function apiPost(path: string, body: any, init?: RequestInit) {
  const res = await fetch(`${API_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    ...init,
  });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}
