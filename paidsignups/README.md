# PaidSignups - Lead Generation Platform

A complete lead generation platform that allows users to create and customize lead generation forms and landing pages.

## Features

- **User Authentication**: Secure login and registration with JWT tokens
- **Form Builder**: Create customizable lead generation forms with drag-and-drop
- **Landing Page Builder**: Design beautiful landing pages with templates
- **Lead Management**: Track and manage all leads in one dashboard
- **Subscription Management**: Free and paid tiers with PayPal integration
- **Analytics**: Track form views, submissions, and conversion rates
- **Email Notifications**: AWS SES integration for lead notifications
- **Admin Panel**: Django admin for managing users and content

## Tech Stack

### Backend
- Django 5.0
- Django REST Framework
- PostgreSQL
- JWT Authentication
- AWS SES for emails
- PayPal integration

### Frontend
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Axios for API calls

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd paidsignups/backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file from `.env.example`:
```bash
cp .env.example .env
```

5. Update the `.env` file with your configuration

6. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

7. Create a superuser:
```bash
python manage.py createsuperuser
```

8. Run the development server:
```bash
python manage.py runserver
```

The backend API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd paidsignups/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env.local` from `.env.local.example`:
```bash
cp .env.local.example .env.local
```

4. Update the `.env.local` file with your API URL

5. Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Subscription Plans

### Free
- 3 Forms
- 3 Landing Pages
- 100 Leads per month
- Basic Analytics

### Basic - $19.99/month
- 10 Forms
- 10 Landing Pages
- 1,000 Leads per month
- Custom Branding

### Pro - $49.99/month
- 50 Forms
- 50 Landing Pages
- 10,000 Leads per month
- Advanced Analytics
- API Access

### Enterprise - $99.99/month
- Unlimited Forms
- Unlimited Landing Pages
- Unlimited Leads
- All Features

## PayPal Integration

Payments are processed through PayPal. The platform uses PayPal's payment link:
`https://paypal.me/yagzud`

## Deployment

### AWS Lightsail Deployment

1. Create a Lightsail instance (Ubuntu 22.04)

2. Install dependencies:
```bash
sudo apt update
sudo apt install python3-pip python3-venv postgresql postgresql-contrib nginx
```

3. Setup PostgreSQL:
```bash
sudo -u postgres createdb paidsignups
sudo -u postgres createuser paidsignups_user
```

4. Clone the repository and setup backend

5. Configure Nginx as reverse proxy

6. Setup systemd service for Django

7. Build and deploy frontend

### Environment Variables

#### Backend (.env)
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to False in production
- `ALLOWED_HOSTS`: Your domain
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`: PostgreSQL credentials
- `AWS_SES_ACCESS_KEY_ID`, `AWS_SES_SECRET_ACCESS_KEY`: AWS SES credentials
- `PAYPAL_CLIENT_ID`, `PAYPAL_CLIENT_SECRET`: PayPal API credentials

#### Frontend (.env.local)
- `NEXT_PUBLIC_API_URL`: Backend API URL
- `NEXT_PUBLIC_PAYPAL_CLIENT_ID`: PayPal client ID

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login
- `POST /api/auth/refresh/` - Refresh JWT token
- `GET /api/auth/profile/` - Get user profile
- `PATCH /api/auth/profile/` - Update profile

### Forms
- `GET /api/forms/` - List all forms
- `POST /api/forms/` - Create new form
- `GET /api/forms/{id}/` - Get form details
- `PATCH /api/forms/{id}/` - Update form
- `DELETE /api/forms/{id}/` - Delete form
- `GET /api/forms/{id}/public/` - Get public form (no auth)

### Landing Pages
- `GET /api/landing-pages/` - List all landing pages
- `POST /api/landing-pages/` - Create new landing page
- `GET /api/landing-pages/{id}/` - Get landing page details
- `PATCH /api/landing-pages/{id}/` - Update landing page
- `DELETE /api/landing-pages/{id}/` - Delete landing page

### Leads
- `GET /api/leads/` - List all leads
- `POST /api/submit/` - Submit form (public endpoint)
- `GET /api/leads/stats/` - Get lead statistics
- `PATCH /api/leads/{id}/` - Update lead status

### Subscriptions
- `GET /api/subscriptions/` - List subscriptions
- `GET /api/subscriptions/current/` - Get current subscription
- `GET /api/subscriptions/plans/` - Get available plans
- `POST /api/subscriptions/` - Create subscription

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is proprietary software.

## Support

For support, email support@paidsignups.com or create an issue in the repository.
