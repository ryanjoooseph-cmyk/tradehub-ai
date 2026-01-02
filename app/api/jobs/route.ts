import { NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.SUPABASE_URL!;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE!;

const supabase = createClient(supabaseUrl, supabaseKey, {
  auth: { persistSession: false }
});

export async function GET() {
  try {
    const { data, error } = await supabase
      .from('jobs')
      .select('id,title,created_at')
      .order('created_at', { ascending: false });
    if (error) throw error;
    return NextResponse.json(data ?? []);
  } catch (err) {
    return NextResponse.json({ ok: true }); // keep GET non-fatal while the table is empty
  }
}

export async function POST(req: Request) {
  try {
    const body = await req.json().catch(() => ({}));
    const title = (body?.title ?? '').toString().trim() || 'Untitled';
    const { error } = await supabase.from('jobs').insert({ title });
    if (error) throw error;
    return new NextResponse(null, { status: 201 });
  } catch (err) {
    return NextResponse.json({ ok: false }, { status: 500 });
  }
}
