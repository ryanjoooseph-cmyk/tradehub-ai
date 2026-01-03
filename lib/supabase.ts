// lib/supabase.ts
import { createClient, type SupabaseClient } from '@supabase/supabase-js';

const url  = process.env.NEXT_PUBLIC_SUPABASE_URL;
const anon = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

/**
 * Browser-safe Supabase client.
 * Throws with a clear message if envs are missing on the host.
 */
export function getBrowserClient(u?: string, a?: string): SupabaseClient {
  const supabaseUrl  = u ?? url;
  const supabaseAnon = a ?? anon;
  if (!supabaseUrl || !supabaseAnon) {
    throw new Error('Missing NEXT_PUBLIC_SUPABASE_URL or NEXT_PUBLIC_SUPABASE_ANON_KEY');
  }
  return createClient(supabaseUrl, supabaseAnon, {
    auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true },
  });
}

// Export both ways so **any** import style in your code keeps working.
export default getBrowserClient;
