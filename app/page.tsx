// app/jobs/page.tsx
export const dynamic = "force-dynamic"; // no caching for demo list

import { getBaseUrl } from "../../lib/getBaseUrl";

type Job = { id?: number; title: string; created_at?: string };

async function getJobs(): Promise<Job[]> {
  const base = getBaseUrl();                   // "" on client, absolute on server
  const res = await fetch(`${base}/api/jobs`, { cache: "no-store" });
  if (!res.ok) return [];
  return (await res.json()) as Job[];
}

export default async function JobsPage() {
  const data = await getJobs();

  return (
    <main style={{ maxWidth: 720, margin: "40px auto", padding: 16 }}>
      <h1 style={{ fontSize: 24, fontWeight: 600, marginBottom: 12 }}>Jobs</h1>
      {data.length ? (
        <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
          {data.map((j, i) => (
            <li key={`${j.id ?? i}-${j.title}`} style={{ marginBottom: 12 }}>
              <div style={{ border: "1px solid #e5e7eb", borderRadius: 8, padding: 12 }}>
                <div style={{ fontWeight: 600 }}>{j.title ?? "(untitled)"}</div>
                {j.created_at && (
                  <div style={{ fontSize: 12, opacity: 0.7 }}>
                    {new Date(j.created_at).toLocaleString()}
                  </div>
                )}
              </div>
            </li>
          ))}
        </ul>
      ) : (
        <p>No jobs yet.</p>
      )}
    </main>
  );
}
