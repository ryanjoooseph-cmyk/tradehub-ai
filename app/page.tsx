// app/page.tsx
import getBaseUrl from '@/lib/getBaseUrl';

export const dynamic = 'force-dynamic';

type Job = { id: string; title: string; created_at: string };

async function getJobs(): Promise<Job[]> {
  const base = getBaseUrl();
  const res = await fetch(`${base}/api/jobs`, { cache: 'no-store' });
  if (!res.ok) return [];
  return res.json();
}

export default async function Home() {
  const jobs = await getJobs();

  return (
    <main style={{ padding: 24 }}>
      <h1>Jobs</h1>
      <ul style={{ marginTop: 12, lineHeight: 1.5 }}>
        {jobs.length === 0 && <li>No jobs yet.</li>}
        {jobs.map((j) => (
          <li key={j.id}>
            <strong>{j.title}</strong>
            <div style={{ fontSize: 12, opacity: 0.75 }}>
              {new Date(j.created_at).toLocaleString()}
            </div>
          </li>
        ))}
      </ul>
    </main>
  );
}
