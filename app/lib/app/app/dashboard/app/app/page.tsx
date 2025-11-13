// app/jobs/page.tsx
import Link from 'next/link';

async function fetchJobs() {
  const res = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/api/jobs`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to load jobs');
  const { data } = await res.json();
  return data as any[];
}

export default async function JobsList() {
  const jobs = await fetchJobs();
  return (
    <main className="max-w-3xl mx-auto p-6">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-semibold">Jobs</h1>
        <Link className="px-3 py-2 rounded bg-black text-white" href="/jobs/new">Post a Job</Link>
      </div>
      <ul className="space-y-3">
        {jobs.map((j) => (
          <li key={j.id} className="border rounded p-4">
            <div className="flex items-center justify-between">
              <Link href={`/jobs/${j.id}`} className="font-medium">{j.title}</Link>
              <span className="text-xs uppercase tracking-wide">{j.status}</span>
            </div>
            {j.location && <p className="text-sm text-gray-600 mt-1">{j.location}</p>}
            {j.budget != null && <p className="text-sm mt-1">Budget: ${Number(j.budget).toFixed(2)}</p>}
          </li>
        ))}
        {jobs.length === 0 && <p className="text-gray-500">No jobs yet.</p>}
      </ul>
    </main>
  );
}