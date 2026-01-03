export function getBaseUrl(): string {
  if (typeof window !== 'undefined') return '';

  const url =
    process.env.NEXT_PUBLIC_SITE_URL ||
    process.env.RENDER_EXTERNAL_URL ||
    process.env.VERCEL_URL ||
    `http://localhost:${process.env.PORT ?? 3000}`;

  return url.startsWith('http') ? url : `https://${url}`;
}

export default getBaseUrl;
