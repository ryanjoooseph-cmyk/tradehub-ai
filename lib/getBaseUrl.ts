// lib/getBaseUrl.ts
export default function getBaseUrl(): string {
  // Prefer Render’s external URL if present
  const ext = process.env.RENDER_EXTERNAL_URL;
  if (ext && ext.trim().length > 0) {
    // Normalize: ensure scheme
    return ext.startsWith('http') ? ext : `https://${ext}`;
  }

  // Vercel fallback (harmless on Render)
  const vercel = process.env.VERCEL_URL;
  if (vercel && vercel.trim().length > 0) {
    return vercel.startsWith('http') ? vercel : `https://${vercel}`;
  }

  // Local dev
  return 'http://localhost:3000';
}
