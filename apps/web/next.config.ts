import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  // Security headers land in full with the P0 auth stage; the baseline
  // below is the minimum that ships from day one (no inline-script
  // reliance, no framing of marketplace pages).
  async headers() {
    return [
      {
        source: "/:path*",
        headers: [
          { key: "X-Content-Type-Options", value: "nosniff" },
          { key: "X-Frame-Options", value: "DENY" },
          { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
        ],
      },
    ];
  },
};

export default nextConfig;
