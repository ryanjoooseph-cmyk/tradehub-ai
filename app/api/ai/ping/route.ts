// app/api/ai/ping/route.ts
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export async function GET() {
  if (!process.env.OPENAI_API_KEY) {
    return Response.json(
      { ok: false, error: "Missing OPENAI_API_KEY" },
      { status: 500 }
    );
  }

  try {
    // Minimal, near-free usage just to verify billing/usage pipeline
    const res = await client.responses.create({
      model: "gpt-4o-mini",
      input: "Reply with the word: pong",
      max_output_tokens: 5,
    });
    return Response.json({ ok: true, text: res.output_text ?? "" });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : String(err);
    return Response.json({ ok: false, error: message }, { status: 500 });
  }
}
