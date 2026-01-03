import OpenAI from "openai";

export async function GET() {
  const hasKey = !!process.env.OPENAI_API_KEY;

  try {
    if (hasKey) {
      const ai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY! });
      // light call; prevents build-time import errors without heavy usage
      await ai.models.list({ limit: 1 } as any);
    }
    return Response.json({ ok: hasKey });
  } catch {
    // don't fail the route; just report inability to reach OpenAI
    return Response.json({ ok: hasKey, error: "openai_call_failed" }, { status: 200 });
  }
}
