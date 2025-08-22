/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  trailingSlash: true,
  basePath: '/app',
  assetPrefix: '/app/',
  images: {
    unoptimized: true
  },
  // Configure build optimization and caching
  swcMinify: true,
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production',
  },
};
module.exports = nextConfig;
