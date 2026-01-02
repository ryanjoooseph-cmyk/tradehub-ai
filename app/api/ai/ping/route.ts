// app/api/ai-test/route.ts
import { NextResponse } from 'next/server';

export async function GET() {
  try {
    const key = process.env.OPENAI_API_KEY;
    if (!key) {
      return NextResponse.json(
        { ok: false, error: 'OPENAI_API_KEY missing' },
        { status: 500 }
      );
    }

    const resp = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${key}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'gpt-4o-mini',
        messages: [{ role: 'user', content: 'ping' }],
        max_tokens: 1,
      }),
    });

    return NextResponse.json({ ok: resp.ok, status: resp.status });
  } catch (e: any) {
    return NextResponse.json(
      { ok: false, error: e?.message ?? 'error' },
      { status: 500 }
    );
  }
}
