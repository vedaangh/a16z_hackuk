/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: '/api/:path*',
      },
    ];
  },
  env: {
    MISTRAL_API_KEY: process.env.MISTRAL_API_KEY,
  },
};

export default nextConfig;
