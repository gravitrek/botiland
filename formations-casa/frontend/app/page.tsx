export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-primary-600">formations.casa</h1>
            <div className="space-x-4">
              <a href="/formations" className="text-gray-700 hover:text-primary-600">Formations</a>
              <a href="/centers" className="text-gray-700 hover:text-primary-600">Centers</a>
              <a href="/coaches" className="text-gray-700 hover:text-primary-600">Coaches</a>
              <a href="/login" className="text-primary-600 hover:text-primary-700">Login</a>
              <a href="/register" className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700">
                Sign Up
              </a>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-700 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-5xl font-bold mb-4">
            Professional Training in Casablanca
          </h1>
          <p className="text-xl mb-8">
            Discover and book the best training courses in Morocco
          </p>
          <div className="flex gap-4 justify-center">
            <a href="/formations" className="bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100">
              Browse Formations
            </a>
            <a href="/register?role=coach" className="border-2 border-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-primary-600">
              Become a Coach
            </a>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h2 className="text-3xl font-bold text-center mb-12">How It Works</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="text-center p-6">
            <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-3xl">🔍</span>
            </div>
            <h3 className="text-xl font-semibold mb-2">Browse Formations</h3>
            <p className="text-gray-600">
              Explore hundreds of professional training courses across various categories
            </p>
          </div>
          <div className="text-center p-6">
            <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-3xl">📚</span>
            </div>
            <h3 className="text-xl font-semibold mb-2">Enroll & Learn</h3>
            <p className="text-gray-600">
              Sign up for courses, receive payment instructions, and start learning
            </p>
          </div>
          <div className="text-center p-6">
            <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-3xl">🏆</span>
            </div>
            <h3 className="text-xl font-semibold mb-2">Earn Badges</h3>
            <p className="text-gray-600">
              Complete courses, earn points, and unlock achievements
            </p>
          </div>
        </div>
      </div>

      {/* Stats Section */}
      <div className="bg-primary-50 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold text-primary-600">1000+</div>
              <div className="text-gray-600 mt-2">Formations</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-primary-600">500+</div>
              <div className="text-gray-600 mt-2">Coaches</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-primary-600">50+</div>
              <div className="text-gray-600 mt-2">Training Centers</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-primary-600">10000+</div>
              <div className="text-gray-600 mt-2">Students</div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-xl font-bold mb-4">formations.casa</h3>
              <p className="text-gray-400">Professional training marketplace in Casablanca, Morocco</p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">For Learners</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="/formations">Browse Formations</a></li>
                <li><a href="/centers">Training Centers</a></li>
                <li><a href="/coaches">Find Coaches</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">For Coaches</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="/coach/dashboard">Dashboard</a></li>
                <li><a href="/coach/formations/create">Create Formation</a></li>
                <li><a href="/coach/payments">Manage Payments</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="/about">About Us</a></li>
                <li><a href="/blog">Blog</a></li>
                <li><a href="/contact">Contact</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2025 formations.casa. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </main>
  )
}
