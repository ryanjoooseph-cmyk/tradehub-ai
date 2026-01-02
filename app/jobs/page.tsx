// app/jobs/page.tsx
import React from 'react';
import getBaseUrl from '../../lib/getBaseUrl';
import SubmitJob from './SubmitJob';

export const dynamic = 'force-dynamic';

type Job = { id: string; title: string; created_at: string };

async function getJobs(): Promise<Job[]> {
  const base = getBaseUrl();
  const res = await fetch(`${base}/api/jobs`, { cache: 'no-store' });
  if (!res.ok) return [];
  return res.json();
}

export default async function JobsPage() {
  const data = await getJobs();

  return (
    <div style={{ maxWidth: 720 }}>
      <h1 style={{ fontSize: 28, fontWeight: 800, marginBottom: 12 }}>Jobs</h1>
      <SubmitJob />
      {data.length ? (
        <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'grid', gap: 8 }}>
          {data.map((j) => (
            <li key={j.id} style={{ border: '1px solid #e5e7eb', padding: 12, borderRadius: 8 }}>
              <div style={{ fontWeight: 700 }}>{j.title || '(untitled)'}</div>
              <div style={{ color: '#6b7280', fontSize: 12 }}>
                {j.created_at ? new Date(j.created_at).toLocaleString() : ''}
              </div>
            </li>
          ))}
        </ul>
      ) : (
        <p style={{ color: '#6b7280' }}>No jobs yet.</p>
      )}
    </div>
  );
}
