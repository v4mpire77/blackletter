export default function HomePage() {
  return (
    <main className="p-6">
      <h1 className="text-2xl font-semibold">Blackletter Systems</h1>
      <p className="mt-2 text-sm text-neutral-600">
        Upload a contract and get a fast, compliance‑aware summary.
      </p>
      <div className="mt-4 space-x-3">
        <a className="underline" href="/upload">Upload</a>
        <a className="underline" href="/dashboard">Dashboard</a>
      </div>
    </main>
  );
}
