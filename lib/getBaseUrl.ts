export function getBaseUrl(): string {
  // Render provides RENDER_EXTERNAL_URL. Vercel provides VERCEL_URL.
  const ext =
    process.env.NEXT_PUBLIC_BASE_URL ||
    process.env.RENDER_EXTERNAL_URL ||
    process.env.VERCEL_URL;

  if (ext) {
    const url = ext.startsWith("http") ? ext : `https://${ext}`;
    return url;
  }

  // Server fallback (local dev)
  if (typeof window === "undefined") return "http://localhost:3000";

  // Client: relative
  return "";
}
