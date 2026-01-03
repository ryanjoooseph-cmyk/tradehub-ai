export const dynamic = "force-dynamic";

import { api } from "@/lib/getBaseUrl";

type Job = { id: string; title: string; created_at: string };

async function getJobs(): Promise<Job[]> {
  const res = await fetch(api("/api/jobs"), { cache: "no-store" });
  if (!res.ok) return [];
  return res.json();
}

export default async function JobsPage() {
  const jobs = await getJobs();
  return (
    <main style={{ padding: 24 }}>
      <h1>Jobs</h1>
      {jobs.length === 0 ? (
        <p>No jobs yet.</p>
      ) : (
        <ul>
          {jobs.map((j) => (
            <li key={j.id}>
              {j.title} <small>{new Date(j.created_at).toLocaleString()}</small>
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}
