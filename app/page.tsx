// app/page.tsx
import { api } from "a/lib/getBaseUrl";

export default async function Page() {
  const res = await fetch(api("/api/jobs"), { cache: "no-store" });
  const jobs = res.ok ? await res.json() : [];
  return (
    <main style={{ padding: 24 }}>
      <h1>TradeHub</h1>
      <p>Jobs (sample)</p>
      <pre>{JSON.stringify(jobs, null, 2)}</pre>
    </main>
  );
}
