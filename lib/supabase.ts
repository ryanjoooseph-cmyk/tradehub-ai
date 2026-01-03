import { createClient } from '@supabase/supabase-js';

const url = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const anon = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

// Single browser client instance
export const supabase = createClient(url, anon);

// Named export used in your pages
export function getBrowserClient() {
  return supabase;
}

export type { Session, User } from '@supabase/supabase-js';
