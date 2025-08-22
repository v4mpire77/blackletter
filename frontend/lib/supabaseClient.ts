import { createClient, type SupabaseClient } from '@supabase/supabase-js'

const supabaseUrl = (process.env.NEXT_PUBLIC_SUPABASE_URL || '').trim()
const supabaseAnonKey = (process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '').trim()

// Create a singleton Supabase client. Ensure env vars are set in your environment.
export const supabase: SupabaseClient = createClient(
  supabaseUrl as string,
  supabaseAnonKey as string
)


