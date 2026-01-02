import { NextResponse } from "next/server";
import { createClient } from "@supabase/supabase-js";

const url = process.env.SUPABASE_URL!;
const serviceKey = process.env.SUPABASE_SERVICE_ROLE!;
const supabase = createClient(url, serviceKey, { auth: { persistSession: false } });

export async function GET() {
  const { data, error } = await supabase
    .from("jobs")
    .select("id,title,created_at")
    .order("created_at", { ascending: false });
  if (error) return NextResponse.json({ ok: false, error }, { status: 500 });
  return NextResponse.json(data ?? [], { status: 200 });
}

export async function POST(req: Request) {
  const body = await req.json().catch(() => ({}));
  const title = (body?.title ?? "").toString().slice(0, 200) || "Untitled job";
  const { data, error } = await supabase
    .from("jobs")
    .insert({ title })
    .select("id,title,created_at")
    .single();
  if (error) return NextResponse.json({ ok: false, error }, { status: 500 });
  return NextResponse.json(data, { status: 201 });
}
