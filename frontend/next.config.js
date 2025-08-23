/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Use regular Next.js build instead of static export
  // output: 'export', // Commented out for Render deployment
  trailingSlash: true,
  // Enable image optimization
  images: {
    domains: ['localhost'],
  },
  // Ensure proper asset handling
  assetPrefix: process.env.NODE_ENV === 'production' ? '' : '',
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
    NEXT_PUBLIC_SUPABASE_URL: process.env.NEXT_PUBLIC_SUPABASE_URL || '',
    NEXT_PUBLIC_SUPABASE_ANON_KEY: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '',
  },
}

module.exports = nextConfig