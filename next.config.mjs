import path from "path";

/** @type {import('next').NextConfig} */
const config = {
  reactStrictMode: true,
  experimental: { appDir: true },
  webpack: (cfg) => {
    // Support legacy imports like: import X from 'a/...'
    cfg.resolve.alias = {
      ...(cfg.resolve.alias || {}),
      a: path.resolve(__dirname)
    };
    return cfg;
  }
};

export default config;
