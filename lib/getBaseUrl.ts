// lib/getBaseUrl.ts
export default function getBaseUrl() {
  const ext = process.env.RENDER_EXTERNAL_URL || process.env.VERCEL_URL;
  if (ext) return ext.startsWith('http') ? ext : `https://${ext}`;
  return 'http://localhost:3000';
}
