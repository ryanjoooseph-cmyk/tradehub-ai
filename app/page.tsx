// app/page.tsx
import { getBaseUrl } from '../lib/getBaseUrl';

type JobRow = {
  id: string;
  title: string;
  created_at?: string | null;
};

async function getJobs(): Promise<JobRow[]> {
  const base = getBaseUrl();
  const res = await fetch(`${base}/api/jobs`, { cache: 'no-store' });
  if (!res.ok) return [];
  return res.json();
}

export default async function Home() {
  const jobs = await getJobs();

  return (
    <main style={{ padding: 24, maxWidth: 720, margin: '0 auto' }}>
      <h1 style={{ marginBottom: 16 }}>Jobs</h1>
      {jobs.length === 0 ? (
        <p>No jobs yet.</p>
      ) : (
        <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
          {jobs.map((j) => (
            <li
              key={j.id}
              style={{
                padding: '12px 0',
                borderBottom: '1px solid #eee',
              }}
            >
              <div style={{ fontWeight: 600 }}>{j.title}</div>
              <div style={{ fontSize: 12, opacity: 0.7 }}>
                {j.created_at ? new Date(j.created_at).toLocaleString() : null}
              </div>
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}
