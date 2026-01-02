import { headers } from 'next/headers';

export const dynamic = 'force-dynamic';

type Job = { id: string; title: string; created_at: string };

async function getJobs(): Promise<Job[]> {
  try {
    const h = headers();
    const host = h.get('host') || '';
    if (!host) return []; // safety: avoid relative fetch during static contexts

    const proto = host.includes('localhost') ? 'http' : 'https';
    const origin = `${proto}://${host}`;

    const r = await fetch(`${origin}/api/jobs`, { cache: 'no-store' });
    if (!r.ok) return [];
    return (await r.json()) as Job[];
  } catch {
    return [];
  }
}

export default async function JobsPage() {
  const data = await getJobs();

  return (
    <main style={{ maxWidth: 720, margin: '40px auto', padding: 16 }}>
      <h1 style={{ fontSize: 24, fontWeight: 600, marginBottom: 12 }}>Jobs</h1>

      {data.length ? (
        <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
          {data.map((j) => (
            <li key={j.id} style={{ marginBottom: 10 }}>
              <div
                style={{
                  border: '1px solid #e5e7eb',
                  borderRadius: 8,
                  padding: 12,
                }}
              >
                <div style={{ fontWeight: 600 }}>{j.title || '(untitled)'}</div>
                <div style={{ fontSize: 12, opacity: 0.7 }}>
                  {new Date(j.created_at).toLocaleString()}
                </div>
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
