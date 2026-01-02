import { NextResponse, NextRequest } from 'next/server'
import { createClient } from '@supabase/supabase-js'
export const dynamic = 'force-dynamic'

function getClient() {
  const url = process.env.SUPABASE_URL
  const serviceRole = process.env.SUPABASE_SERVICE_ROLE
  if (!url || !serviceRole) return { client: null, error: 'Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE' }
  return { client: createClient(url, serviceRole), error: null }
}

export async function GET(_req: NextRequest) {
  const { client, error } = getClient()
  if (error) return NextResponse.json({ ok: false, error }, { status: 500 })
  const { data, error: qerr } = await client
    .from('jobs')
    .select('id,title,created_at')
    .order('created_at', { ascending: false })
    .limit(50)
  if (qerr) return NextResponse.json({ ok: false, error: qerr.message }, { status: 500 })
  return NextResponse.json(data ?? [])
}

export async function POST(req: NextRequest) {
  const { client, error } = getClient()
  if (error) return NextResponse.json({ ok: false, error }, { status: 500 })
  let body: any; try { body = await req.json() } catch { return NextResponse.json({ ok:false, error:'Invalid JSON' }, { status: 400 }) }
  const title = String(body?.title ?? '').trim()
  if (!title) return NextResponse.json({ ok:false, error:'title is required' }, { status: 400 })
  const { data, error: ierr } = await client.from('jobs').insert({ title }).select('id').single()
  if (ierr) return NextResponse.json({ ok:false, error:ierr.message }, { status: 500 })
  return NextResponse.json({ ok:true, id: data?.id }, { status: 201 })
}
