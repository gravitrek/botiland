'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { useAuth } from '@/lib/auth'
import api from '@/lib/api'
import { SubscriptionPlan } from '@/lib/types'

export default function PricingPage() {
  const router = useRouter()
  const { user } = useAuth()
  const [plans, setPlans] = useState<SubscriptionPlan[]>([])
  const [loading, setLoading] = useState(true)
  const [billingPeriod, setBillingPeriod] = useState<'monthly' | 'yearly'>('monthly')

  useEffect(() => {
    loadPlans()
  }, [])

  const loadPlans = async () => {
    try {
      const response = await api.get('/auth/plans/')
      setPlans(response.data)
    } catch (error) {
      console.error('Failed to load plans:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleUpgrade = async (planId: string) => {
    if (!user) {
      router.push('/login?redirect=/pricing')
      return
    }

    try {
      // Redirect to PayPal checkout
      const response = await api.post('/payments/create-checkout/', {
        plan_id: planId,
        billing_period: billingPeriod,
      })

      if (response.data.checkout_url) {
        window.location.href = response.data.checkout_url
      }
    } catch (error) {
      console.error('Failed to initiate checkout:', error)
      alert('Failed to start checkout process. Please try again.')
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <Link href="/" className="text-2xl font-bold text-primary-600">
              QRGeek
            </Link>
            <div className="flex items-center space-x-4">
              {user ? (
                <Link href="/dashboard" className="text-gray-700 hover:text-gray-900">
                  Dashboard
                </Link>
              ) : (
                <>
                  <Link href="/login" className="text-gray-700 hover:text-gray-900">
                    Login
                  </Link>
                  <Link
                    href="/register"
                    className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700"
                  >
                    Sign Up
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-extrabold text-gray-900 mb-4">
            Choose Your Plan
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Select the perfect plan for your QR code needs. All plans include core features.
          </p>

          {/* Billing Toggle */}
          <div className="mt-8 flex items-center justify-center space-x-4">
            <span className={billingPeriod === 'monthly' ? 'text-gray-900 font-semibold' : 'text-gray-600'}>
              Monthly
            </span>
            <button
              onClick={() => setBillingPeriod(billingPeriod === 'monthly' ? 'yearly' : 'monthly')}
              className="relative inline-flex h-6 w-11 items-center rounded-full bg-primary-600"
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${
                  billingPeriod === 'yearly' ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
            <span className={billingPeriod === 'yearly' ? 'text-gray-900 font-semibold' : 'text-gray-600'}>
              Yearly
            </span>
            <span className="ml-2 px-3 py-1 bg-green-100 text-green-800 text-sm font-semibold rounded-full">
              Save 20%
            </span>
          </div>
        </div>

        {/* Pricing Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {plans.map((plan) => {
            const price = billingPeriod === 'yearly' ? plan.price * 12 * 0.8 : plan.price
            const isCurrentPlan = user?.subscription_name === plan.name

            return (
              <div
                key={plan.id}
                className={`bg-white rounded-2xl shadow-xl overflow-hidden ${
                  plan.is_featured ? 'ring-4 ring-primary-600 transform scale-105' : ''
                }`}
              >
                {plan.is_featured && (
                  <div className="bg-primary-600 text-white text-center py-2 text-sm font-semibold">
                    MOST POPULAR
                  </div>
                )}

                <div className="p-8">
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">{plan.name}</h3>
                  <div className="mb-6">
                    <span className="text-5xl font-extrabold text-gray-900">
                      ${Math.floor(price)}
                    </span>
                    <span className="text-gray-600">/{billingPeriod === 'monthly' ? 'mo' : 'yr'}</span>
                  </div>

                  <ul className="space-y-4 mb-8">
                    <li className="flex items-start">
                      <span className="text-green-500 mr-2">✓</span>
                      <span className="text-gray-700">
                        {plan.qr_limit === -1 ? 'Unlimited' : plan.qr_limit} QR Codes
                      </span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-green-500 mr-2">✓</span>
                      <span className="text-gray-700">
                        {plan.scan_limit === -1 ? 'Unlimited' : `${plan.scan_limit.toLocaleString()}`} Scans/month
                      </span>
                    </li>
                    {plan.features.advanced_analytics && (
                      <li className="flex items-start">
                        <span className="text-green-500 mr-2">✓</span>
                        <span className="text-gray-700">Advanced Analytics</span>
                      </li>
                    )}
                    {plan.features.custom_branding && (
                      <li className="flex items-start">
                        <span className="text-green-500 mr-2">✓</span>
                        <span className="text-gray-700">Custom Branding</span>
                      </li>
                    )}
                    {plan.features.api_access && (
                      <li className="flex items-start">
                        <span className="text-green-500 mr-2">✓</span>
                        <span className="text-gray-700">API Access</span>
                      </li>
                    )}
                    {plan.features.custom_domains && (
                      <li className="flex items-start">
                        <span className="text-green-500 mr-2">✓</span>
                        <span className="text-gray-700">Custom Domains</span>
                      </li>
                    )}
                    {plan.features.white_label && (
                      <li className="flex items-start">
                        <span className="text-green-500 mr-2">✓</span>
                        <span className="text-gray-700">White Label</span>
                      </li>
                    )}
                    {plan.features.priority_support && (
                      <li className="flex items-start">
                        <span className="text-green-500 mr-2">✓</span>
                        <span className="text-gray-700">Priority Support</span>
                      </li>
                    )}
                  </ul>

                  <button
                    onClick={() => handleUpgrade(plan.id)}
                    disabled={isCurrentPlan}
                    className={`w-full py-3 rounded-lg font-semibold transition ${
                      plan.is_featured
                        ? 'bg-primary-600 text-white hover:bg-primary-700'
                        : 'bg-gray-100 text-gray-900 hover:bg-gray-200'
                    } ${isCurrentPlan ? 'opacity-50 cursor-not-allowed' : ''}`}
                  >
                    {isCurrentPlan ? 'Current Plan' : plan.price === 0 ? 'Get Started' : 'Upgrade Now'}
                  </button>
                </div>
              </div>
            )
          })}
        </div>

        {/* FAQ Section */}
        <div className="mt-24">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Frequently Asked Questions
          </h2>
          <div className="max-w-3xl mx-auto bg-white rounded-2xl shadow-lg p-8 space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Can I change my plan anytime?
              </h3>
              <p className="text-gray-600">
                Yes! You can upgrade or downgrade your plan at any time. Changes take effect immediately.
              </p>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                What payment methods do you accept?
              </h3>
              <p className="text-gray-600">
                We accept PayPal, credit cards, and debit cards through our secure payment processor.
              </p>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Is there a free trial?
              </h3>
              <p className="text-gray-600">
                Yes! Our Free plan lets you create up to 5 QR codes with 500 scans per month. No credit card required.
              </p>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                What happens if I exceed my scan limit?
              </h3>
              <p className="text-gray-600">
                Your QR codes will continue to work, but you'll need to upgrade to access detailed analytics for additional scans.
              </p>
            </div>
          </div>
        </div>

        {/* Payment Note */}
        <div className="mt-12 text-center">
          <p className="text-gray-600">
            Secure payments processed via PayPal:{' '}
            <a
              href="https://paypal.me/yagzud"
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary-600 hover:text-primary-700 font-semibold"
            >
              paypal.me/yagzud
            </a>
          </p>
        </div>
      </div>
    </div>
  )
}
