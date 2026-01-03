import OpenAI from 'openai';

export async function GET() {
  try {
    const ai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
    await ai.models.list();
    return Response.json({ ok: true });
  } catch (err: any) {
    return Response.json({ ok: false, error: String(err?.message || err) }, { status: 500 });
  }
}
