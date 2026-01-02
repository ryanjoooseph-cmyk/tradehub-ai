// app/jobs/page.tsx
import getBaseUrl from "../../lib/getBaseUrl";

async function getJobs() {
  const res = await fetch(`${getBaseUrl()}/api/jobs`, { cache: "no-store" });
  if (!res.ok) return [];
  return res.json() as Promise<{ id: number; title: string; created_at: string }[]>;
}

export default async function JobsPage() {
  const rows = await getJobs();
  return (
    <main style={{ maxWidth: 720, margin: "0 auto" }}>
      <h1 style={{ fontSize: 24, margin: "8px 0 16px" }}>Jobs</h1>
      {rows.length ? (
        <ul style={{ listStyle: "none", padding: 0, margin: 0, display: "grid", gap: 10 }}>
          {rows.map((r) => (
            <li key={r.id} style={{ border: "1px solid #1b1f24", padding: 12, borderRadius: 8 }}>
              <div style={{ fontWeight: 700 }}>{r.title}</div>
              <div style={{ fontSize: 12, opacity: .7 }}>{new Date(r.created_at).toLocaleString()}</div>
            </li>
          ))}
        </ul>
      ) : (
        <p>No jobs yet.</p>
      )}
    </main>
  );
}
