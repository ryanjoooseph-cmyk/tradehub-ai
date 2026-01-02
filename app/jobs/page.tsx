// app/jobs/page.tsx
export const dynamic = 'force-dynamic';
import SubmitJob from './SubmitJob';

type Row = { id: string; title: string; created_at: string };

async function getJobs(): Promise<Row[]> {
  const base =
    process.env.RENDER_EXTERNAL_URL
      ? `https://${process.env.RENDER_EXTERNAL_URL}`
      : '';
  const res = await fetch(`${base}/api/jobs`, { cache: 'no-store' });
  if (!res.ok) return [];
  return (await res.json()) as Row[];
}

export default async function JobsPage() {
  const data = await getJobs();

  return (
    <main style={{ maxWidth:720, margin:'40px auto', padding:16 }}>
      <h1 style={{ fontSize:24, fontWeight:700, marginBottom:12 }}>Jobs</h1>

      <SubmitJob />

      {data.length ? (
        <ul style={{ listStyle:'none', padding:0, margin:0 }}>
          {data.map((j) => (
            <li key={j.id} style={{ border:'1px solid #eee', borderRadius:8, padding:12, marginBottom:10 }}>
              <div style={{ fontWeight:600 }}>{j.title || '(untitled)'}</div>
              <div style={{ fontSize:12, opacity:0.7 }}>
                {new Date(j.created_at).toLocaleString()}
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
