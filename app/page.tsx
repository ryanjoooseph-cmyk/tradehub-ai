// app/page.tsx
import getBaseUrl from "../lib/getBaseUrl";

async function getJobs() {
  const base = getBaseUrl();
  const res = await fetch(`${base}/api/jobs`, { cache: "no-store" });
  if (!res.ok) return [];
  return res.json() as Promise<{ id: number; title: string; created_at: string }[]>;
}

export default async function Dashboard() {
  const jobs = await getJobs();
  return (
    <div>
      <h1 style={{ fontSize: 24, margin: "8px 0 16px" }}>Dashboard</h1>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(220px,1fr))", gap: 12 }}>
        <div style={{ border: "1px solid #1b1f24", borderRadius: 8, padding: 12 }}>
          <div style={{ fontSize: 12, opacity: .7 }}>Open Jobs</div>
          <div style={{ fontSize: 28, fontWeight: 700 }}>{jobs.length}</div>
        </div>
      </div>
    </div>
  );
}
