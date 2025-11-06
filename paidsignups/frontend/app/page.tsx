'use client';

import Link from 'next/link';
import { CheckCircle2, Zap, TrendingUp, Shield } from 'lucide-react';

export default function Home() {
  const features = [
    {
      icon: <Zap className="w-8 h-8 text-primary-500" />,
      title: 'Easy Form Builder',
      description: 'Create beautiful lead generation forms in minutes with our drag-and-drop builder.',
    },
    {
      icon: <TrendingUp className="w-8 h-8 text-primary-500" />,
      title: 'Landing Pages',
      description: 'Build high-converting landing pages with customizable templates.',
    },
    {
      icon: <Shield className="w-8 h-8 text-primary-500" />,
      title: 'Lead Management',
      description: 'Track and manage all your leads in one centralized dashboard.',
    },
    {
      icon: <CheckCircle2 className="w-8 h-8 text-primary-500" />,
      title: 'Analytics',
      description: 'Get insights into form performance and lead conversion rates.',
    },
  ];

  const pricing = [
    {
      name: 'Free',
      price: '$0',
      features: ['3 Forms', '3 Landing Pages', '100 Leads/month', 'Basic Analytics'],
    },
    {
      name: 'Basic',
      price: '$19.99',
      features: ['10 Forms', '10 Landing Pages', '1,000 Leads/month', 'Custom Branding'],
    },
    {
      name: 'Pro',
      price: '$49.99',
      features: ['50 Forms', '50 Landing Pages', '10,000 Leads/month', 'Advanced Analytics', 'API Access'],
      popular: true,
    },
    {
      name: 'Enterprise',
      price: '$99.99',
      features: ['Unlimited Forms', 'Unlimited Landing Pages', 'Unlimited Leads', 'All Features'],
    },
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary-600 to-primary-800 text-white">
        <div className="container mx-auto px-4 py-20">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-5xl md:text-6xl font-bold mb-6">
              Generate More Leads with PaidSignups
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-primary-100">
              Create beautiful forms and landing pages in minutes. No coding required.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/register" className="btn btn-primary bg-white text-primary-600 hover:bg-gray-100 text-lg px-8 py-3">
                Get Started Free
              </Link>
              <Link href="/login" className="btn bg-primary-700 hover:bg-primary-600 text-lg px-8 py-3">
                Sign In
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12">Powerful Features</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="card text-center">
                <div className="flex justify-center mb-4">{feature.icon}</div>
                <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section className="bg-gray-50 py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12">Simple Pricing</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 max-w-7xl mx-auto">
            {pricing.map((plan, index) => (
              <div
                key={index}
                className={`card relative ${plan.popular ? 'ring-2 ring-primary-500' : ''}`}
              >
                {plan.popular && (
                  <span className="absolute -top-4 left-1/2 transform -translate-x-1/2 bg-primary-500 text-white px-4 py-1 rounded-full text-sm font-medium">
                    Most Popular
                  </span>
                )}
                <h3 className="text-2xl font-bold mb-2">{plan.name}</h3>
                <div className="text-4xl font-bold mb-6">
                  {plan.price}
                  <span className="text-lg text-gray-600">/mo</span>
                </div>
                <ul className="space-y-3 mb-8">
                  {plan.features.map((feature, idx) => (
                    <li key={idx} className="flex items-center gap-2">
                      <CheckCircle2 className="w-5 h-5 text-green-500" />
                      <span>{feature}</span>
                    </li>
                  ))}
                </ul>
                <Link
                  href="/register"
                  className={`btn w-full ${plan.popular ? 'btn-primary' : 'btn-secondary'}`}
                >
                  Get Started
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="container mx-auto px-4 text-center">
          <p className="text-lg mb-4">© 2025 PaidSignups. All rights reserved.</p>
          <p className="text-gray-400">
            Need help? Contact us at support@paidsignups.com
          </p>
        </div>
      </footer>
    </div>
  );
}
