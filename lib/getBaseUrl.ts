export function getBaseUrl(): string {
  const ext = process.env.RENDER_EXTERNAL_URL;
  if (ext) return ext.startsWith('http') ? ext : `https://${ext}`;
  const vercel = process.env.VERCEL_URL;
  if (vercel) return `https://${vercel}`;
  return 'http://localhost:3000';
}
