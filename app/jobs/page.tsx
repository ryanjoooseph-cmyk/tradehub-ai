import { getBaseUrl } from "@/lib/getBaseUrl";
export const dynamic = "force-dynamic";

export default async function JobsPage() {
  const res = await fetch(`${getBaseUrl()}/api/jobs`, { cache: "no-store" });
  const jobs = await res.json();
  return (
    <>
      <h1>Jobs</h1>
      <pre>{JSON.stringify(jobs, null, 2)}</pre>
    </>
  );
}
