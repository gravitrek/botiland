/**
 * TypeScript type definitions for QRGeek
 */

export interface User {
  id: string
  email: string
  username: string
  full_name: string
  company_name: string
  industry: string
  is_verified: boolean
  qr_code_count: number
  subscription_name: string
  qr_code_limit: number
  scan_limit: number
  created_at: string
  updated_at: string
}

export interface QRCode {
  id: string
  name: string
  qr_type: QRType
  qr_type_display: string
  content: Record<string, any>
  short_code: string
  short_url: string
  custom_domain: string
  foreground_color: string
  background_color: string
  logo: string | null
  size: number
  format: 'png' | 'svg' | 'pdf' | 'eps'
  error_correction: 'L' | 'M' | 'Q' | 'H'
  qr_image: string | null
  enable_tracking: boolean
  is_active: boolean
  is_expired: boolean
  expires_at: string | null
  total_scans: number
  unique_scans: number
  last_scanned_at: string | null
  tags: Tag[]
  folder: string
  created_at: string
  updated_at: string
}

export type QRType =
  | 'url'
  | 'vcard'
  | 'text'
  | 'email'
  | 'sms'
  | 'phone'
  | 'wifi'
  | 'location'
  | 'event'
  | 'app'
  | 'pdf'
  | 'menu'
  | 'product'
  | 'social'

export interface Tag {
  id: string
  name: string
  slug: string
  created_at: string
}

export interface QRTemplate {
  id: string
  name: string
  description: string
  category: string
  qr_type: QRType
  foreground_color: string
  background_color: string
  template_image: string
  is_premium: boolean
  usage_count: number
}

export interface Analytics {
  total_scans: number
  unique_scans: number
  last_scanned_at: string | null
  top_countries: Array<{ country: string; count: number }>
  top_devices: Array<{ device_type: string; count: number }>
  top_browsers: Array<{ browser: string; count: number }>
}

export interface DashboardStats {
  total_qr_codes: number
  active_qr_codes: number
  total_scans: number
  qr_code_limit: number
  scan_limit: number
}

export interface SubscriptionPlan {
  id: string
  name: string
  slug: string
  description: string
  price: number
  billing_period: 'monthly' | 'yearly'
  qr_limit: number
  scan_limit: number
  features: Record<string, any>
  is_featured: boolean
}

export interface QRCreateData {
  name: string
  qr_type: QRType
  content: Record<string, any>
  foreground_color?: string
  background_color?: string
  logo?: File | null
  size?: number
  format?: 'png' | 'svg' | 'pdf' | 'eps'
  error_correction?: 'L' | 'M' | 'Q' | 'H'
  enable_tracking?: boolean
  expires_at?: string | null
  tag_ids?: string[]
  folder?: string
}

export interface RestaurantMenu {
  restaurant_name: string
  menu_data: {
    categories: Array<{
      name: string
      items: Array<{
        name: string
        description: string
        price: number
        image?: string
        allergens?: string[]
      }>
    }>
  }
  allergen_info: Record<string, any>
  language: string
  theme: string
  show_prices: boolean
  show_images: boolean
}

export interface VCard {
  first_name: string
  last_name: string
  company: string
  title: string
  phone: string
  email: string
  website: string
  address: string
  social_links: Record<string, string>
  photo?: File | null
}

export interface WiFiCredentials {
  ssid: string
  password: string
  security_type: 'WPA' | 'WEP' | ''
  hidden: boolean
}

export interface EventInfo {
  event_name: string
  event_date: string
  location: string
  description: string
  ticket_info: Record<string, any>
  registration_url: string
}
