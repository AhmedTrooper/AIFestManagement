/** @type {import('next').NextConfig} */
const nextConfig = {
  typedRoutes: true,
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: process.env.NEXT_PUBLIC_API_BASE_URL
          ? `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/:path*`
          : "http://localhost:8000/api/:path*"
      }
    ];
  }
};

export default nextConfig;
