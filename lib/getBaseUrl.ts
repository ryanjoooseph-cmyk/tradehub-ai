import { headers } from 'next/headers';

export function getBaseUrl(): string {
  const h = headers();
  const proto = h.get('x-forwarded-proto') ?? 'https';
  const host  = h.get('x-forwarded-host') ?? h.get('host');

  if (host) return `${proto}://${host}`;
  if (process.env.RENDER_EXTERNAL_URL) return `https://${process.env.RENDER_EXTERNAL_URL}`;
  return 'http://localhost:3000';
}

// compatibility exports for existing imports
export default getBaseUrl;
export const api = getBaseUrl;
