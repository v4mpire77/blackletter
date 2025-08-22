/** @type {import('next').NextConfig} */
const nextConfig = {
  // Remove static export for web service deployment
  // output: 'export',
  // trailingSlash: true,
  images: {
    unoptimized: true
  },
  // Enable server-side rendering for better performance
  experimental: {
    serverActions: true,
  }
};

module.exports = nextConfig;
