// app/jobs/page.tsx
import { api } from "a/lib/getBaseUrl";

export const dynamic = "force-dynamic";

export default async function JobsPage() {
  const res = await fetch(api("/api/jobs"), { cache: "no-store" });
  const jobs = res.ok ? await res.json() : [];
  return (
    <main style={{ padding: 24 }}>
      <h1>Jobs</h1>
      <pre>{JSON.stringify(jobs, null, 2)}</pre>
    </main>
  );
}
