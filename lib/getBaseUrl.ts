export function getBaseUrl() {
  const ext = process.env.RENDER_EXTERNAL_URL || process.env.NEXT_PUBLIC_BASE_URL;
  if (ext) return ext.startsWith('http') ? ext : `https://${ext}`;
  if (process.env.VERCEL_URL) return `https://${process.env.VERCEL_URL}`;
  return 'http://localhost:3000';
}
