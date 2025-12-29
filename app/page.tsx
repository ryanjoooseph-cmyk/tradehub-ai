// FILE: app/jobs/page.tsx
'use client';

import { useEffect, useState } from 'react';

type Job = {
  id: string;
  title: string;
  status: 'open' | 'in_progress' | 'done' | 'cancelled';
  created_at: string;
};

export default function JobsPage() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [title, setTitle] = useState('');
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  async function refresh() {
    setErr(null);
    const r = await fetch('/api/jobs', { cache: 'no-store' });
    if (!r.ok) {
      setErr('Failed to load jobs');
      return;
    }
    const j = await r.json();
    setJobs(j.jobs ?? []);
  }

  useEffect(() => {
    refresh();
  }, []);

  async function createJob(e: React.FormEvent) {
    e.preventDefault();
    if (!title.trim()) return;
    setBusy(true);
    setErr(null);
    try {
      const r = await fetch('/api/jobs', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ title }),
      });
      const j = await r.json();
      if (!r.ok) throw new Error(j?.error || 'Failed to create job');
      setTitle('');
      await refresh();
    } catch (e: any) {
      setErr(e?.message ?? 'Error');
    } finally {
      setBusy(false);
    }
  }

  return (
    <main style={{ maxWidth: 680, margin: '3rem auto', padding: '0 1rem', lineHeight: 1.5 }}>
      <h1>Jobs</h1>
      <p>Backed by Supabase. Add a job to see it persist.</p>

      <form onSubmit={createJob} style={{ display: 'flex', gap: 8, margin: '1rem 0' }}>
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Job title…"
          aria-label="Job title"
          style={{ flex: 1, padding: '0.6rem 0.8rem' }}
        />
        <button disabled={busy || !title.trim()} style={{ padding: '0.6rem 0.9rem' }}>
          {busy ? 'Adding…' : 'Add'}
        </button>
      </form>

      {err && <p style={{ color: 'crimson' }}>{err}</p>}

      <ul style={{ listStyle: 'none', padding: 0, marginTop: 16 }}>
        {jobs.map((j) => (
          <li key={j.id} style={{ padding: '10px 0', borderBottom: '1px solid #eee' }}>
            <div style={{ fontWeight: 600 }}>{j.title}</div>
            <div style={{ fontSize: 12, opacity: 0.7 }}>
              {j.status} • {new Date(j.created_at).toLocaleString()}
            </div>
          </li>
        ))}
        {!jobs.length && <li>No jobs yet — add one above.</li>}
      </ul>
    </main>
  );
}
