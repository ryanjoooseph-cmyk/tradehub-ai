export const dynamic = "force-dynamic";

import { getBaseUrl } from "a/lib/getBaseUrl";

type Job = { id: string; title: string; created_at?: string };

async function getJobs(): Promise<Job[]> {
  const base = getBaseUrl();
  const res = await fetch(`${base}/api/jobs`, { cache: "no-store" });
  if (!res.ok) return [];
  return (await res.json()) as Job[];
}

export default async function MarketPage() {
  const jobs = await getJobs();

  return (
    <main style={{ maxWidth: 960, margin: "40px auto", padding: 16 }}>
      <h1 style={{ fontSize: 24, fontWeight: 700, marginBottom: 12 }}>Market</h1>
      {jobs.length === 0 ? (
        <p>No jobs yet.</p>
      ) : (
        <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
          {jobs.map((j) => (
            <li key={j.id} style={{ border: "1px solid #e5e7eb", padding: 12, borderRadius: 8, marginBottom: 8 }}>
              <div style={{ fontWeight: 700 }}>{j.title}</div>
              {j.created_at ? (
                <div style={{ opacity: 0.7, fontSize: 12 }}>
                  {new Date(j.created_at).toLocaleString()}
                </div>
              ) : null}
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}
