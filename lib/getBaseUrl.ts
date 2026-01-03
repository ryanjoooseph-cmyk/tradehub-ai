export function getBaseUrl(): string {
  if (typeof window !== "undefined") return "";
  const url =
    process.env.NEXT_PUBLIC_SITE_URL ||
    process.env.RENDER_EXTERNAL_URL ||
    process.env.VERCEL_URL ||
    process.env.URL;
  return url ? (url.startsWith("http") ? url : `https://${url}`) : "http://localhost:3000";
}

// keep both to satisfy any old imports your pages had
export const api = { baseUrl: getBaseUrl() };
export default getBaseUrl;
