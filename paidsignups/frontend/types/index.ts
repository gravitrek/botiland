export interface User {
  id: string;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  company_name?: string;
  phone_number?: string;
  website?: string;
  subscription_plan: 'FREE' | 'BASIC' | 'PRO' | 'ENTERPRISE';
  subscription_active: boolean;
  subscription_start_date?: string;
  subscription_end_date?: string;
  forms_created: number;
  landing_pages_created: number;
  leads_this_month: number;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
}

export interface Form {
  id: string;
  user: string;
  user_email: string;
  name: string;
  description?: string;
  slug: string;
  fields: FormField[];
  submit_button_text: string;
  success_message: string;
  redirect_url?: string;
  send_notification: boolean;
  notification_email?: string;
  notification_subject: string;
  theme: any;
  is_active: boolean;
  is_published: boolean;
  views: number;
  submissions: number;
  conversion_rate: number;
  created_at: string;
  updated_at: string;
}

export interface FormField {
  name: string;
  type: 'text' | 'email' | 'tel' | 'number' | 'textarea' | 'select' | 'checkbox' | 'radio';
  label: string;
  placeholder?: string;
  required: boolean;
  options?: string[];
  validation?: any;
}

export interface LandingPage {
  id: string;
  user: string;
  user_email: string;
  name: string;
  description?: string;
  slug: string;
  content: any;
  form?: string;
  form_name?: string;
  meta_title?: string;
  meta_description?: string;
  meta_keywords?: string;
  theme: any;
  custom_css?: string;
  custom_js?: string;
  is_active: boolean;
  is_published: boolean;
  views: number;
  conversions: number;
  conversion_rate: number;
  tracking_code?: string;
  created_at: string;
  updated_at: string;
}

export interface Lead {
  id: string;
  form: string;
  form_name: string;
  user: string;
  data: any;
  source_url?: string;
  source_landing_page?: string;
  landing_page_name?: string;
  referrer?: string;
  user_agent?: string;
  ip_address?: string;
  status: 'NEW' | 'CONTACTED' | 'QUALIFIED' | 'CONVERTED' | 'LOST';
  notes?: string;
  email_sent: boolean;
  email_sent_at?: string;
  created_at: string;
  updated_at: string;
}

export interface Subscription {
  id: string;
  user: string;
  user_email: string;
  plan: 'FREE' | 'BASIC' | 'PRO' | 'ENTERPRISE';
  amount: string;
  paypal_subscription_id?: string;
  paypal_order_id?: string;
  paypal_payer_id?: string;
  paypal_payer_email?: string;
  status: 'PENDING' | 'ACTIVE' | 'CANCELLED' | 'EXPIRED' | 'SUSPENDED';
  start_date: string;
  end_date?: string;
  next_billing_date?: string;
  cancelled_at?: string;
  cancellation_reason?: string;
  created_at: string;
  updated_at: string;
}

export interface SubscriptionPlan {
  price: number;
  max_forms: number;
  max_landing_pages: number;
  max_leads_per_month: number;
  custom_branding: boolean;
  advanced_analytics: boolean;
  api_access: boolean;
}
