// supabase/functions/agent-runner/index.ts
// Minimal, safe queue runner for Supabase Edge
// Claims one task at a time (atomic via status swap) with the SERVICE ROLE
// Env: SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, OPENAI_API_KEY
// Optional: TASKS_TABLE (defaults to 'agent_tasks')

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SUPABASE_SERVICE_ROLE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const OPENAI_API_KEY = Deno.env.get("OPENAI_API_KEY")!;
const TASKS_TABLE = Deno.env.get("TASKS_TABLE") ?? "agent_tasks";

const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY);

async function claimOne() {
  // Uses the SQL function you already created: claim_agent_task()
  const { data, error } = await supabase.rpc("claim_agent_task");
  if (error) throw new Error(`claim_agent_task failed: ${error.message}`);
  return data as
    | { id: string; payload: any; task_type: string; run_count: number }
    | null;
}

async function callOpenAI(payload: any) {
  const notes = payload?.notes ?? "Return a JSON object with {\"ok\":true}.";
  const messages = [
    { role: "system", content: "You are a code generator that returns JSON only." },
    { role: "user", content: notes },
  ];

  const resp = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${OPENAI_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: "gpt-4o-mini",
      messages,
      response_format: { type: "json_object" },
    }),
  });

  if (!resp.ok) {
    const text = await resp.text();
    throw new Error(`OpenAI HTTP ${resp.status}: ${text}`);
  }
  return await resp.json();
}

async function processOne() {
  const task = await claimOne();
  if (!task) return 0; // nothing to do

  const { id, payload } = task;
  try {
    const result = await callOpenAI(payload);
    await supabase
      .from(TASKS_TABLE)
      .update({
        status: "done",
        result,
        error: null,
        updated_at: new Date().toISOString(),
      })
      .eq("id", id);
    return 1;
  } catch (e) {
    await supabase
      .from(TASKS_TABLE)
      .update({
        status: "failed",
        error: String(e),
        updated_at: new Date().toISOString(),
      })
      .eq("id", id);
    return 0;
  }
}

Deno.serve(async (req) => {
  let body: any = {};
  try { body = await req.json(); } catch {}
  const mode = body?.mode ?? "drain";

  let processed = 0;
  if (mode === "queue") {
    processed += await processOne();
  } else {
    for (let i = 0; i < 25; i++) { // drain a few per request
      const n = await processOne();
      if (n === 0) break;
      processed += n;
    }
  }

  return new Response(JSON.stringify({ mode, processed }), {
    headers: { "Content-Type": "application/json" },
  });
});
