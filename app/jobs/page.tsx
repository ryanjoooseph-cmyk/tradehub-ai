import { getBaseUrl } from "a/lib/getBaseUrl";

type Job = { id: number; title: string; created_at: string };

async function getJobs(): Promise<Job[]> {
  const base = getBaseUrl();
  const res = await fetch(`${base}/api/jobs`, { cache: "no-store" });
  if (!res.ok) return [];
  return res.json() as Promise<Job[]>;
}

export default async function JobsPage() {
  const data = await getJobs();
  return (
    <div>
      <h1>Jobs</h1>
      {data.length ? (
        <ul style={{ listStyle: "none", padding: 0 }}>
          {data.map((j) => (
            <li key={j.id} style={{ border: "1px solid #e5e7eb", padding: 12, borderRadius: 8, marginBottom: 8 }}>
              <div style={{ fontWeight: 600 }}>{j.title || "(untitled)"}</div>
              <div style={{ fontSize: 12, opacity: 0.7 }}>
                {new Date(j.created_at).toLocaleString()}
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
