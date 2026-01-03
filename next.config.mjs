import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname  = path.dirname(__filename);

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',
  webpack: (config) => {
    // allow "a/..." and "@/..." to resolve from repo root
    config.resolve.alias = {
      ...(config.resolve.alias ?? {}),
      a: path.resolve(__dirname),
      '@': path.resolve(__dirname),
    };
    return config;
  },
};

export default nextConfig;
