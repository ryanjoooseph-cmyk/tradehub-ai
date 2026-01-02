// app/jobs/page.tsx
import { getBaseUrl } from "@/lib/getBaseUrl";

export const dynamic = "force-dynamic";

export default async function JobsPage() {
  const base = getBaseUrl();
  const r = await fetch(`${base}/api/jobs`, { cache: "no-store" });
  const jobs = r.ok ? await r.json() : [];

  return (
    <main style={{ padding: 24 }}>
      <h2>Jobs</h2>
      {(!jobs || jobs.length === 0) && <p>No jobs yet.</p>}
      <ul>
        {Array.isArray(jobs) &&
          jobs.map((j: any, i: number) => (
            <li key={i}>
              <strong>{j.title ?? "Untitled"}</strong>{" "}
              <small>{j.created_at ?? ""}</small>
            </li>
          ))}
      </ul>
    </main>
  );
}
