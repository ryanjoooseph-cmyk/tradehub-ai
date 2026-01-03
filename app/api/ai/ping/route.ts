import OpenAI from "openai";

export async function GET() {
  try {
    const ai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
    const models = await ai.models.list();
    return Response.json({ ok: true, count: models.data.length });
  } catch (err: any) {
    return Response.json({ ok: false, error: String(err?.message ?? err) }, { status: 500 });
  }
}
