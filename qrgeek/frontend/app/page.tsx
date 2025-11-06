import Link from 'next/link'

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-primary-600">QRGeek</h1>
            </div>
            <div className="flex items-center space-x-4">
              <Link href="/login" className="text-gray-700 hover:text-gray-900">
                Login
              </Link>
              <Link
                href="/register"
                className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center">
          <h1 className="text-5xl font-extrabold text-gray-900 sm:text-6xl md:text-7xl">
            Professional QR Code
            <span className="block text-primary-600">Generator & Analytics</span>
          </h1>
          <p className="mt-6 max-w-2xl mx-auto text-xl text-gray-600">
            Create, customize, and track QR codes for your business. Advanced analytics,
            industry-specific templates, and unlimited possibilities.
          </p>
          <div className="mt-10 flex justify-center gap-4">
            <Link
              href="/register"
              className="bg-primary-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-primary-700 transition"
            >
              Start Free Trial
            </Link>
            <Link
              href="/pricing"
              className="bg-white text-primary-600 px-8 py-4 rounded-lg text-lg font-semibold border-2 border-primary-600 hover:bg-primary-50 transition"
            >
              View Pricing
            </Link>
          </div>
        </div>

        {/* Features Grid */}
        <div className="mt-24 grid grid-cols-1 md:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div key={index} className="bg-white p-6 rounded-xl shadow-lg">
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">
                {feature.title}
              </h3>
              <p className="text-gray-600">{feature.description}</p>
            </div>
          ))}
        </div>

        {/* Industries */}
        <div className="mt-24">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Built for Every Industry
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {industries.map((industry, index) => (
              <div
                key={index}
                className="bg-white p-6 rounded-lg shadow-md text-center hover:shadow-xl transition"
              >
                <div className="text-3xl mb-2">{industry.icon}</div>
                <h4 className="font-semibold text-gray-900">{industry.name}</h4>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 text-white mt-24 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p>&copy; 2024 QRGeek. All rights reserved.</p>
        </div>
      </footer>
    </main>
  )
}

const features = [
  {
    icon: '🎨',
    title: 'Full Customization',
    description: 'Customize colors, add logos, and create branded QR codes that match your style.',
  },
  {
    icon: '📊',
    title: 'Advanced Analytics',
    description: 'Track scans, locations, devices, and user behavior with real-time analytics.',
  },
  {
    icon: '🏭',
    title: 'Industry Templates',
    description: 'Pre-built templates for restaurants, retail, events, healthcare, and more.',
  },
  {
    icon: '🔗',
    title: 'URL Shortening',
    description: 'Shorten URLs and track every scan with detailed analytics.',
  },
  {
    icon: '📱',
    title: 'Multiple Formats',
    description: 'Download QR codes in PNG, SVG, PDF, and EPS formats.',
  },
  {
    icon: '🚀',
    title: 'Bulk Operations',
    description: 'Create and download hundreds of QR codes at once.',
  },
]

const industries = [
  { icon: '🍽️', name: 'Restaurants' },
  { icon: '🛍️', name: 'Retail' },
  { icon: '🎉', name: 'Events' },
  { icon: '🏥', name: 'Healthcare' },
  { icon: '🏠', name: 'Real Estate' },
  { icon: '🎓', name: 'Education' },
  { icon: '📢', name: 'Marketing' },
  { icon: '🏭', name: 'Manufacturing' },
]
