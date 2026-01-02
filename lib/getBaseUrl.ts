// lib/getBaseUrl.ts
/**
 * Returns a safe absolute origin for server-side fetches.
 * Accepts any of: NEXT_PUBLIC_BASE_URL, RENDER_EXTERNAL_URL, or VERCEL_URL.
 * Guarantees protocol + double slash (https://...).
 */
export function getBaseUrl(): string {
  const cand = [
    process.env.NEXT_PUBLIC_BASE_URL,                                        // e.g. https://tradehub-app.onrender.com
    process.env.RENDER_EXTERNAL_URL,                                         // e.g. https://tradehub-app.onrender.com  (Render usually sets this)
    process.env.VERCEL_URL ? `https://${process.env.VERCEL_URL}` : undefined // Vercel-style
  ].filter(Boolean) as string[];

  for (const raw of cand) {
    try {
      // If someone saved just the host, add https://
      const str = raw.startsWith('http') ? raw : `https://${raw}`;
      const u = new URL(str);
      // Normalize accidental "https:/host" to "https://host"
      const fixed = `${u.protocol}//${u.host}`;
      return fixed;
    } catch {
      /* try next candidate */
    }
  }
  // Local dev fallback
  return 'http://localhost:3000';
}
