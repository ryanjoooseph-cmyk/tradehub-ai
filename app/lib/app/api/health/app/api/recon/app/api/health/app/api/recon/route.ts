export async function GET() {
  return Response.json({ ok: true });
}

export async function POST(req: Request) {
  try {
    const payload = await req.json().catch(() => ({}));
    console.log('recon payload:', payload);
    return Response.json({ ok: true });
  } catch (err) {
    return Response.json({ ok: false, error: (err as Error).message }, { status: 500 });
  }
}
