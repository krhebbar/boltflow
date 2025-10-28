/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  experimental: {
    serverActions: {
      enabled: true,
    },
  },
  images: {
    domains: [
      'localhost',
      '*.supabase.co',
      '*.vercel-storage.com',
    ],
    formats: ['image/avif', 'image/webp'],
  },
  transpilePackages: ['@boltflow/ui', '@boltflow/db'],
}

module.exports = nextConfig
