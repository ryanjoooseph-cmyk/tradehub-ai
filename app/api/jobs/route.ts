// app/api/jobs/route.ts
import { NextResponse } from 'next/server';
import { supabase } from '@/lib/supabaseAdmin';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

export async function GET() {
  const { data, error } = await supabase
    .from('jobs')
    .select('*')
    .order('created_at', { ascending: false })
    .limit(50);

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
  return NextResponse.json({ data: data ?? [] }, { status: 200 });
}

export async function POST(req: Request) {
  let payload: any = {};
  try {
    payload = await req.json();
  } catch {
    /* ignore */
  }

  const title =
    typeof payload?.title === 'string' && payload.title.trim().length > 0
      ? payload.title.trim()
      : null;

  if (!title) {
    return NextResponse.json({ error: 'title required' }, { status: 400 });
  }

  const insertRow = { title, payload: payload?.payload ?? null };

  const { data, error } = await supabase
    .from('jobs')
    .insert(insertRow)
    .select('*')
    .single();

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }

  return NextResponse.json({ data }, { status: 201 });
}
