// app/api/jobs/route.ts
// Minimal, safe route. Swap to Supabase later if you want.
// Keeps runtime happy even with no DB env set.

export async function GET() {
  // Return an empty list by default
  return Response.json([]);
}
