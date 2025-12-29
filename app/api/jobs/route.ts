// app/api/jobs/route.ts
import { NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

export const dynamic = 'force-dynamic';

const SUPABASE_URL = process.env.SUPABASE_URL!;
const SUPABASE_SERVICE_ROLE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY!; // server-only

const sb = createClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY);

type JobRow = { id: string; title: string; created_at: string };

export async function GET() {
  const { data, error } = await sb
    .from('jobs')
    .select('id,title,created_at')
    .order('created_at', { ascending: false })
    .limit(50);

  if (error) {
    console.error('jobs GET error:', error);
    return NextResponse.json({ ok: false, error: error.message }, { status: 500 });
  }
  return NextResponse.json((data ?? []) as JobRow[]);
}

export async function POST(req: Request) {
  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: 'Invalid JSON' }, { status: 400 });
  }

  const title = (body as any)?.title?.toString().trim();
  if (!title) return NextResponse.json({ error: 'Missing "title"' }, { status: 400 });

  const { data, error } = await sb
    .from('jobs')
    .insert([{ title }])
    .select('id,title,created_at')
    .single();

  if (error) {
    console.error('jobs POST error:', error);
    return NextResponse.json({ ok: false, error: error.message }, { status: 500 });
  }
  return NextResponse.json(data as JobRow, { status: 201 });
}
