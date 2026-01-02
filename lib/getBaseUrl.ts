// lib/getBaseUrl.ts
export function getBaseUrl() {
  // Prefer Render’s externally reachable URL (it’s auto-set on Render),
  // otherwise fall back to a custom NEXT_PUBLIC_BASE_URL or local dev.
  const ext =
    process.env.RENDER_EXTERNAL_URL ||
    process.env.NEXT_PUBLIC_BASE_URL ||
    '';

  if (ext && ext.startsWith('http')) return ext;
  if (process.env.VERCEL_URL) return `https://${process.env.VERCEL_URL}`;
  return 'http://localhost:3000';
}
