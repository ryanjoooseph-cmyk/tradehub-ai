// lib/getBaseUrl.ts
export function getBaseUrl(): URL {
  // Prefer a fully-qualified external URL if Render provided it
  const external =
    process.env.RENDER_EXTERNAL_URL ||
    process.env.NEXT_PUBLIC_BASE_URL ||
    process.env.VERCEL_URL;

  if (external) {
    // Accept either "example.com" or "https://example.com"
    const url = external.startsWith("http") ? external : `https://${external}`;
    return new URL(url);
  }

  // Fallback for local dev
  return new URL("http://localhost:3000");
}

export function api(path: string): string {
  const base = getBaseUrl();
  const normalized = path.startsWith("/") ? path : `/${path}`;
  return new URL(normalized, base).toString();
}
