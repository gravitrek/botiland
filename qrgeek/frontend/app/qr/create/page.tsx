'use client'

import { useState, useRef } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { QRCodeSVG } from 'qrcode.react'
import { useAuth } from '@/lib/auth'
import api from '@/lib/api'
import { QRType, QRCreateData } from '@/lib/types'

const QR_TYPES: Array<{ value: QRType; label: string; icon: string; description: string }> = [
  { value: 'url', label: 'URL / Website', icon: '🌐', description: 'Link to any website or webpage' },
  { value: 'vcard', label: 'Business Card', icon: '👤', description: 'Share contact information' },
  { value: 'wifi', label: 'WiFi', icon: '📶', description: 'Connect to WiFi network' },
  { value: 'email', label: 'Email', icon: '📧', description: 'Send an email' },
  { value: 'sms', label: 'SMS', icon: '💬', description: 'Send a text message' },
  { value: 'phone', label: 'Phone', icon: '📞', description: 'Make a phone call' },
  { value: 'text', label: 'Plain Text', icon: '📝', description: 'Display text message' },
  { value: 'location', label: 'Location', icon: '📍', description: 'GPS coordinates' },
  { value: 'event', label: 'Event', icon: '📅', description: 'Calendar event' },
  { value: 'menu', label: 'Restaurant Menu', icon: '🍽️', description: 'Digital menu' },
]

export default function CreateQRPage() {
  const router = useRouter()
  const { user } = useAuth()
  const [step, setStep] = useState(1)
  const [qrType, setQrType] = useState<QRType>('url')
  const [name, setName] = useState('')
  const [content, setContent] = useState<any>({})
  const [customization, setCustomization] = useState({
    foreground_color: '#000000',
    background_color: '#FFFFFF',
    size: 400,
    error_correction: 'M' as 'L' | 'M' | 'Q' | 'H',
    enable_tracking: true,
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const getPreviewContent = () => {
    switch (qrType) {
      case 'url':
        return content.url || 'https://example.com'
      case 'email':
        return `mailto:${content.to || 'email@example.com'}`
      case 'sms':
        return `sms:${content.phone || '1234567890'}`
      case 'phone':
        return `tel:${content.phone || '1234567890'}`
      case 'text':
        return content.text || 'Hello World'
      case 'wifi':
        return `WIFI:T:${content.security_type || 'WPA'};S:${content.ssid || 'MyWiFi'};P:${content.password || ''};H:false;;`
      case 'vcard':
        return `BEGIN:VCARD\nVERSION:3.0\nFN:${content.first_name || 'John'} ${content.last_name || 'Doe'}\nEND:VCARD`
      default:
        return 'QRGeek.com'
    }
  }

  const handleSubmit = async () => {
    if (!name.trim()) {
      setError('Please enter a name for your QR code')
      return
    }

    setLoading(true)
    setError('')

    try {
      const qrData: QRCreateData = {
        name,
        qr_type: qrType,
        content,
        ...customization,
      }

      const response = await api.post('/qr/', qrData)
      router.push(`/qr/${response.data.id}`)
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to create QR code')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <Link href="/dashboard" className="text-2xl font-bold text-primary-600">
              QRGeek
            </Link>
            <Link href="/dashboard" className="text-gray-600 hover:text-gray-900">
              ← Back to Dashboard
            </Link>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Progress Steps */}
        <div className="mb-8">
          <div className="flex items-center justify-center space-x-4">
            <div className={`flex items-center ${step >= 1 ? 'text-primary-600' : 'text-gray-400'}`}>
              <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold ${step >= 1 ? 'bg-primary-600 text-white' : 'bg-gray-200'}`}>
                1
              </div>
              <span className="ml-2 hidden sm:inline">Type</span>
            </div>
            <div className="w-16 h-1 bg-gray-200"></div>
            <div className={`flex items-center ${step >= 2 ? 'text-primary-600' : 'text-gray-400'}`}>
              <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold ${step >= 2 ? 'bg-primary-600 text-white' : 'bg-gray-200'}`}>
                2
              </div>
              <span className="ml-2 hidden sm:inline">Content</span>
            </div>
            <div className="w-16 h-1 bg-gray-200"></div>
            <div className={`flex items-center ${step >= 3 ? 'text-primary-600' : 'text-gray-400'}`}>
              <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold ${step >= 3 ? 'bg-primary-600 text-white' : 'bg-gray-200'}`}>
                3
              </div>
              <span className="ml-2 hidden sm:inline">Customize</span>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-lg p-8">
              {error && (
                <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
                  {error}
                </div>
              )}

              {/* Step 1: Choose Type */}
              {step === 1 && (
                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">Choose QR Code Type</h2>
                  <p className="text-gray-600 mb-6">Select what you want your QR code to do</p>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    {QR_TYPES.map((type) => (
                      <button
                        key={type.value}
                        onClick={() => setQrType(type.value)}
                        className={`p-6 rounded-lg border-2 text-left transition ${
                          qrType === type.value
                            ? 'border-primary-600 bg-primary-50'
                            : 'border-gray-200 hover:border-gray-300'
                        }`}
                      >
                        <div className="text-4xl mb-2">{type.icon}</div>
                        <h3 className="font-semibold text-gray-900 mb-1">{type.label}</h3>
                        <p className="text-sm text-gray-600">{type.description}</p>
                      </button>
                    ))}
                  </div>

                  <button
                    onClick={() => setStep(2)}
                    className="mt-8 w-full bg-primary-600 text-white py-3 rounded-lg font-semibold hover:bg-primary-700 transition"
                  >
                    Continue
                  </button>
                </div>
              )}

              {/* Step 2: Enter Content */}
              {step === 2 && (
                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">Enter Content</h2>
                  <p className="text-gray-600 mb-6">Fill in the details for your {qrType} QR code</p>

                  <div className="space-y-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        QR Code Name *
                      </label>
                      <input
                        type="text"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        placeholder="My QR Code"
                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                      />
                    </div>

                    {/* URL Type */}
                    {qrType === 'url' && (
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Website URL *
                        </label>
                        <input
                          type="url"
                          value={content.url || ''}
                          onChange={(e) => setContent({ ...content, url: e.target.value })}
                          placeholder="https://example.com"
                          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                        />
                      </div>
                    )}

                    {/* Email Type */}
                    {qrType === 'email' && (
                      <>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Email Address *
                          </label>
                          <input
                            type="email"
                            value={content.to || ''}
                            onChange={(e) => setContent({ ...content, to: e.target.value })}
                            placeholder="contact@example.com"
                            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Subject
                          </label>
                          <input
                            type="text"
                            value={content.subject || ''}
                            onChange={(e) => setContent({ ...content, subject: e.target.value })}
                            placeholder="Email subject"
                            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                          />
                        </div>
                      </>
                    )}

                    {/* Phone Type */}
                    {qrType === 'phone' && (
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Phone Number *
                        </label>
                        <input
                          type="tel"
                          value={content.phone || ''}
                          onChange={(e) => setContent({ ...content, phone: e.target.value })}
                          placeholder="+1234567890"
                          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                        />
                      </div>
                    )}

                    {/* SMS Type */}
                    {qrType === 'sms' && (
                      <>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Phone Number *
                          </label>
                          <input
                            type="tel"
                            value={content.phone || ''}
                            onChange={(e) => setContent({ ...content, phone: e.target.value })}
                            placeholder="+1234567890"
                            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Message
                          </label>
                          <textarea
                            value={content.message || ''}
                            onChange={(e) => setContent({ ...content, message: e.target.value })}
                            placeholder="Your message here"
                            rows={4}
                            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                          />
                        </div>
                      </>
                    )}

                    {/* Text Type */}
                    {qrType === 'text' && (
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Text Content *
                        </label>
                        <textarea
                          value={content.text || ''}
                          onChange={(e) => setContent({ ...content, text: e.target.value })}
                          placeholder="Enter your text here"
                          rows={6}
                          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                        />
                      </div>
                    )}

                    {/* WiFi Type */}
                    {qrType === 'wifi' && (
                      <>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Network Name (SSID) *
                          </label>
                          <input
                            type="text"
                            value={content.ssid || ''}
                            onChange={(e) => setContent({ ...content, ssid: e.target.value })}
                            placeholder="My WiFi Network"
                            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Password
                          </label>
                          <input
                            type="text"
                            value={content.password || ''}
                            onChange={(e) => setContent({ ...content, password: e.target.value })}
                            placeholder="WiFi password"
                            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Security Type
                          </label>
                          <select
                            value={content.security_type || 'WPA'}
                            onChange={(e) => setContent({ ...content, security_type: e.target.value })}
                            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                          >
                            <option value="WPA">WPA/WPA2</option>
                            <option value="WEP">WEP</option>
                            <option value="">None</option>
                          </select>
                        </div>
                      </>
                    )}

                    {/* vCard Type */}
                    {qrType === 'vcard' && (
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            First Name *
                          </label>
                          <input
                            type="text"
                            value={content.first_name || ''}
                            onChange={(e) => setContent({ ...content, first_name: e.target.value })}
                            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Last Name *
                          </label>
                          <input
                            type="text"
                            value={content.last_name || ''}
                            onChange={(e) => setContent({ ...content, last_name: e.target.value })}
                            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Phone *
                          </label>
                          <input
                            type="tel"
                            value={content.phone || ''}
                            onChange={(e) => setContent({ ...content, phone: e.target.value })}
                            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Email
                          </label>
                          <input
                            type="email"
                            value={content.email || ''}
                            onChange={(e) => setContent({ ...content, email: e.target.value })}
                            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                          />
                        </div>
                        <div className="md:col-span-2">
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Company
                          </label>
                          <input
                            type="text"
                            value={content.company || ''}
                            onChange={(e) => setContent({ ...content, company: e.target.value })}
                            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                          />
                        </div>
                      </div>
                    )}
                  </div>

                  <div className="flex space-x-4 mt-8">
                    <button
                      onClick={() => setStep(1)}
                      className="flex-1 border-2 border-gray-300 text-gray-700 py-3 rounded-lg font-semibold hover:bg-gray-50 transition"
                    >
                      Back
                    </button>
                    <button
                      onClick={() => setStep(3)}
                      className="flex-1 bg-primary-600 text-white py-3 rounded-lg font-semibold hover:bg-primary-700 transition"
                    >
                      Continue
                    </button>
                  </div>
                </div>
              )}

              {/* Step 3: Customize */}
              {step === 3 && (
                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">Customize Design</h2>
                  <p className="text-gray-600 mb-6">Make your QR code unique</p>

                  <div className="space-y-6">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Foreground Color
                        </label>
                        <input
                          type="color"
                          value={customization.foreground_color}
                          onChange={(e) => setCustomization({ ...customization, foreground_color: e.target.value })}
                          className="w-full h-12 border border-gray-300 rounded-lg cursor-pointer"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Background Color
                        </label>
                        <input
                          type="color"
                          value={customization.background_color}
                          onChange={(e) => setCustomization({ ...customization, background_color: e.target.value })}
                          className="w-full h-12 border border-gray-300 rounded-lg cursor-pointer"
                        />
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Size: {customization.size}px
                      </label>
                      <input
                        type="range"
                        min="200"
                        max="1000"
                        step="50"
                        value={customization.size}
                        onChange={(e) => setCustomization({ ...customization, size: parseInt(e.target.value) })}
                        className="w-full"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Error Correction Level
                      </label>
                      <select
                        value={customization.error_correction}
                        onChange={(e) => setCustomization({ ...customization, error_correction: e.target.value as any })}
                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                      >
                        <option value="L">Low (7%)</option>
                        <option value="M">Medium (15%)</option>
                        <option value="Q">Quartile (25%)</option>
                        <option value="H">High (30%)</option>
                      </select>
                    </div>

                    <div className="flex items-center">
                      <input
                        type="checkbox"
                        id="tracking"
                        checked={customization.enable_tracking}
                        onChange={(e) => setCustomization({ ...customization, enable_tracking: e.target.checked })}
                        className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                      />
                      <label htmlFor="tracking" className="ml-2 block text-sm text-gray-900">
                        Enable scan tracking and analytics
                      </label>
                    </div>
                  </div>

                  <div className="flex space-x-4 mt-8">
                    <button
                      onClick={() => setStep(2)}
                      className="flex-1 border-2 border-gray-300 text-gray-700 py-3 rounded-lg font-semibold hover:bg-gray-50 transition"
                    >
                      Back
                    </button>
                    <button
                      onClick={handleSubmit}
                      disabled={loading}
                      className="flex-1 bg-primary-600 text-white py-3 rounded-lg font-semibold hover:bg-primary-700 transition disabled:opacity-50"
                    >
                      {loading ? 'Creating...' : 'Create QR Code'}
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Preview Panel */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-lg p-6 sticky top-8">
              <h3 className="text-lg font-bold text-gray-900 mb-4">Preview</h3>
              <div className="bg-gray-50 p-8 rounded-lg flex items-center justify-center">
                <QRCodeSVG
                  value={getPreviewContent()}
                  size={200}
                  level={customization.error_correction}
                  fgColor={customization.foreground_color}
                  bgColor={customization.background_color}
                />
              </div>
              <div className="mt-4 text-center">
                <p className="text-sm text-gray-600">
                  {name || 'Untitled QR Code'}
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  Type: {QR_TYPES.find(t => t.value === qrType)?.label}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
