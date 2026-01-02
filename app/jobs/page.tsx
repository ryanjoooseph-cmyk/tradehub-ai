// app/jobs/page.tsx
import { getBaseUrl } from "../../lib/getBaseUrl";

export const dynamic = "force-dynamic";

type Job = { id: string | number; title: string; created_at?: string };

async function getJobs(): Promise<Job[]> {
  const res = await fetch(`${getBaseUrl()}/api/jobs`, { cache: "no-store" });
  if (!res.ok) return [];
  return res.json();
}

export default async function JobsPage() {
  const data = await getJobs();

  return (
    <div>
      <h2>Jobs</h2>
      {data.length ? (
        <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
          {data.map((j) => (
            <li key={j.id} style={{ border: "1px solid #eee7eb", borderRadius: 8, padding: 12, marginBottom: 10 }}>
              <div style={{ fontWeight: 600 }}>{j.title || "(untitled)"}</div>
              <div style={{ fontSize: 12, opacity: 0.7 }}>
                {j.created_at ? new Date(j.created_at).toLocaleString() : null}
              </div>
            </li>
          ))}
        </ul>
      ) : (
        <p>No jobs yet.</p>
      )}
    </div>
  );
}
