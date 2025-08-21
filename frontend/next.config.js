/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  images: {
    unoptimized: true,
  },
  trailingSlash: true,
  skipTrailingSlashRedirect: true,
  // Ensure compatibility with static hosting
  assetPrefix: process.env.NODE_ENV === 'production' ? undefined : '',
  // Support for client-side routing with static export
  distDir: 'out',
};

module.exports = nextConfig;