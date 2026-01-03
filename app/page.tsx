import { getBaseUrl } from "@/lib/getBaseUrl";

export default function Home() {
  return (
    <>
      <h1>TradeHub</h1>
      <p>Base URL detected: <code>{getBaseUrl()}</code></p>
      <p>Visit <a href="/jobs">/jobs</a> or hit <a href="/api/ai-test">/api/ai-test</a>.</p>
    </>
  );
}
