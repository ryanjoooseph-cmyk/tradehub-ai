// app/lib/supabaseServer.ts
// Server-only Supabase client (for Route Handlers / Server Components)
import 'server-only';
import { createClient } from '@supabase/supabase-js';

const url = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const service = process.env.SUPABASE_SERVICE_ROLE_KEY!; // server only

if (!url || !service) {
  throw new Error('Supabase URL or Service Role key is not set');
}

export const supabaseServer = createClient(url, service, {
  auth: { persistSession: false },
});