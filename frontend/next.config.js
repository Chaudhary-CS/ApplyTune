/** @type {import('next').NextConfig} */
const nextConfig = {
  // Might need this for large resume files
  api: {
    bodyParser: {
      sizeLimit: '10mb',
    },
  },
  // Enable if deploying to production
  reactStrictMode: true,
}

module.exports = nextConfig
