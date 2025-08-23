"use client"
import { useState } from 'react'
import { getSupabaseClient } from '@/lib/supabaseClient'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [status, setStatus] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleMagicLink = async (e: React.FormEvent) => {
    e.preventDefault()
    setStatus(null)
    setError(null)
    try {
      const supabase = getSupabaseClient()
      const { error: signInError } = await supabase.auth.signInWithOtp({ email })
      if (signInError) {
        setError(signInError.message)
        return
      }
      setStatus('Magic link sent. Check your email to continue.')
    } catch (err: any) {
      setError(err?.message || 'Unexpected error')
    }
  }

  return (
    <div className="max-w-md mx-auto">
      <h2 className="text-2xl font-semibold mb-4">Login</h2>
      <form onSubmit={handleMagicLink} className="space-y-4">
        <div>
          <label htmlFor="email" className="block text-sm font-medium">E-mail</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="mt-1 w-full border rounded px-3 py-2"
            placeholder="you@example.com"
          />
        </div>
        <button type="submit" className="bg-[#0A2342] text-white px-4 py-2 rounded">
          Send magic link
        </button>
      </form>
      {status && <p className="mt-4 text-green-600">{status}</p>}
      {error && <p className="mt-4 text-red-600">{error}</p>}
    </div>
  )
}


