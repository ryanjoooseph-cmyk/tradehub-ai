// app/page.tsx
export const dynamic = "force-dynamic";
import Link from "next/link";
import { api } from "@/lib/getBaseUrl";

type Job = { id: string; title: string; created_at: string };

async function getRecentJobs(): Promise<Job[]> {
  try {
    const res = await fetch(api("/api/jobs"), { cache: "no-store" });
    if (!res.ok) return [];
    return (await res.json()) as Job[];
  } catch {
    // On any network/env hiccup, render the page without crashing the server.
    return [];
  }
}

export default async function Home() {
  const jobs = await getRecentJobs();

  return (
    <main style={{ maxWidth: 960, margin: "40px auto", padding: 16 }}>
      <h1 style={{ fontSize: 28, fontWeight: 700, marginBottom: 8 }}>TradeHub</h1>

      <nav style={{ marginBottom: 24 }}>
        <Link href="/jobs">Jobs</Link> {" | "}
        <Link href="/market">Market</Link> {" | "}
        <Link href="/profile">Profile</Link>
      </nav>

      <section>
        <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 8 }}>
          Recent jobs
        </h2>
        {jobs.length === 0 ? (
          <p>No jobs yet.</p>
        ) : (
          <ul style={{ listStyle: "none", padding: 0 }}>
            {jobs.map((j) => (
              <li
                key={j.id}
                style={{
                  border: "1px solid #e5e7eb",
                  borderRadius: 8,
                  padding: 12,
                  marginBottom: 12,
                }}
              >
                <div style={{ fontWeight: 600 }}>{j.title || "(untitled)"}</div>
                <div style={{ opacity: 0.7, fontSize: 12 }}>
                  {new Date(j.created_at).toLocaleString()}
                </div>
              </li>
            ))}
          </ul>
        )}
      </section>
    </main>
  );
}
