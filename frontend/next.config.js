/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  images: { unoptimized: true }, // avoids next/image optimizer during export
  trailingSlash: true            // optional; helps with static hosting
};
module.exports = nextConfig;