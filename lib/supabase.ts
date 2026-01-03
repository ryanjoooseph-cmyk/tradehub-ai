// lib/supabase.ts
import { createClient, type SupabaseClient } from '@supabase/supabase-js';

let _client: SupabaseClient | null = null;

/**
 * Browser-safe Supabase client.
 * Throws with a clear message if required env vars are missing.
 * Exports BOTH a named and default export so either import style works.
 */
export function getBrowserClient(): SupabaseClient {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const anon = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

  if (!url || !anon) {
    throw new Error(
      'Supabase env missing: set NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY on Render.'
    );
  }

  if (!_client) _client = createClient(url, anon);
  return _client;
}

// allow: import getBrowserClient from '@/lib/supabase'
export default getBrowserClient;
