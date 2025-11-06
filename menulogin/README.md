# MenuLogin - Restaurant Tech SaaS Platform

A comprehensive multi-tenant restaurant management platform built with Django, PostgreSQL, React, and Next.js.

## Features

### Core Platform Features
- **Multi-Tenant Architecture**: Each restaurant operates independently with isolated data
- **Restaurant Management**: Complete restaurant profile and settings management
- **Menu Management**: Categories, items, modifiers, variants, and pricing
- **Order Management**: Dine-in, takeout, and delivery orders
- **Table Management**: QR code-based ordering, reservations, and table tracking
- **Customer Management**: Customer profiles, loyalty programs, and preferences
- **Payment Processing**: Stripe integration for payments and subscriptions
- **Notifications**: Email (AWS SES) and WhatsApp (Twilio) notifications
- **Analytics & Reporting**: Comprehensive sales analytics and customer insights

### User Roles
- **Platform Admin**: Manages the entire platform and all restaurants
- **Restaurant Owner**: Owns and manages their restaurant(s)
- **Restaurant Manager**: Manages restaurant operations
- **Restaurant Staff**: Handles orders and customer service
- **Customer**: Places orders and makes reservations

### Technology Stack

#### Backend
- **Framework**: Django 5.0.1
- **API**: Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (SimpleJWT)
- **File Storage**: AWS S3 (optional, local storage for development)
- **Email**: AWS SES
- **WhatsApp**: Twilio
- **Payment**: Stripe
- **Task Queue**: Celery with Redis
- **QR Codes**: qrcode library

#### Frontend (To be implemented)
- **Framework**: Next.js 15
- **UI Library**: React 18
- **Styling**: TailwindCSS
- **State Management**: React Context API
- **API Client**: Axios

### API Endpoints (Planned)

#### Authentication
- POST `/api/auth/register/` - User registration
- POST `/api/auth/login/` - User login
- POST `/api/auth/refresh/` - Refresh JWT token
- POST `/api/auth/logout/` - User logout

#### Restaurants
- GET `/api/restaurants/` - List all restaurants
- POST `/api/restaurants/` - Create restaurant (Owner/Admin)
- GET `/api/restaurants/{id}/` - Restaurant details
- PUT `/api/restaurants/{id}/` - Update restaurant
- DELETE `/api/restaurants/{id}/` - Delete restaurant

#### Menus
- GET `/api/restaurants/{id}/menu/` - Get restaurant menu
- POST `/api/restaurants/{id}/menu/categories/` - Create category
- POST `/api/restaurants/{id}/menu/items/` - Create menu item
- PUT `/api/menu/items/{id}/` - Update menu item
- DELETE `/api/menu/items/{id}/` - Delete menu item

#### Orders
- GET `/api/orders/` - List orders (filtered by restaurant/user)
- POST `/api/orders/` - Create new order
- GET `/api/orders/{id}/` - Order details
- PUT `/api/orders/{id}/status/` - Update order status
- POST `/api/orders/{id}/cancel/` - Cancel order

#### Tables
- GET `/api/restaurants/{id}/tables/` - List tables
- POST `/api/restaurants/{id}/tables/` - Create table
- GET `/api/tables/{id}/qr-code/` - Generate/get QR code
- POST `/api/tables/{id}/reservations/` - Create reservation

#### Payments
- POST `/api/payments/create-intent/` - Create Stripe payment intent
- POST `/api/payments/webhook/` - Stripe webhook handler
- GET `/api/payments/history/` - Payment history

## Database Models

### Core Models
1. **User** - Custom user model with role-based access
2. **Restaurant** - Multi-tenant restaurant data
3. **RestaurantSettings** - Restaurant-specific configurations

### Menu Models
4. **MenuCategory** - Menu categories
5. **MenuItem** - Individual menu items
6. **MenuItemModifier** - Customization options
7. **MenuItemModifierOption** - Modifier choices
8. **MenuItemModifierLink** - Links items to modifiers
9. **MenuItemVariant** - Item variants (sizes, flavors)

### Order Models
10. **Order** - Main order model
11. **OrderItem** - Individual items in an order
12. **OrderItemModifier** - Selected modifiers for order items
13. **OrderStatusHistory** - Audit trail for order status changes

### Table Models
14. **Table** - Restaurant tables with QR codes
15. **TableReservation** - Table booking system
16. **TableSession** - Table usage tracking

### Customer Models
17. **Customer** - Customer profiles and loyalty
18. **CustomerAddress** - Saved delivery addresses

### Payment Models
19. **Payment** - Order payment transactions
20. **SubscriptionPayment** - SaaS subscription payments

### Notification Models
21. **Notification** - Multi-channel notifications
22. **EmailTemplate** - Customizable email templates

### Analytics Models
23. **DailySalesReport** - Daily aggregated sales data
24. **MenuItemAnalytics** - Menu item performance
25. **CustomerBehavior** - Customer insights and patterns

## Setup Instructions

### Backend Setup

1. **Install Dependencies**
```bash
cd menulogin/backend
pip install -r requirements.txt
```

2. **Configure Environment Variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Create Database**
```bash
# For PostgreSQL
createdb menulogin_db
```

4. **Run Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create Superuser**
```bash
python manage.py createsuperuser
```

6. **Run Development Server**
```bash
python manage.py runserver
```

### Frontend Setup (To be implemented)

```bash
cd menulogin/frontend
npm install
npm run dev
```

## Environment Variables

### Database
- `DB_NAME` - PostgreSQL database name
- `DB_USER` - Database user
- `DB_PASSWORD` - Database password
- `DB_HOST` - Database host (default: localhost)
- `DB_PORT` - Database port (default: 5432)

### AWS
- `AWS_ACCESS_KEY_ID` - AWS access key
- `AWS_SECRET_ACCESS_KEY` - AWS secret key
- `AWS_STORAGE_BUCKET_NAME` - S3 bucket name
- `AWS_S3_REGION_NAME` - AWS region
- `USE_S3` - Enable S3 storage (default: False)

### Email (AWS SES)
- `AWS_SES_REGION_NAME` - SES region
- `DEFAULT_FROM_EMAIL` - Default sender email

### Twilio (WhatsApp)
- `TWILIO_ACCOUNT_SID` - Twilio account SID
- `TWILIO_AUTH_TOKEN` - Twilio auth token
- `TWILIO_WHATSAPP_NUMBER` - Twilio WhatsApp number

### Stripe
- `STRIPE_PUBLIC_KEY` - Stripe publishable key
- `STRIPE_SECRET_KEY` - Stripe secret key
- `STRIPE_WEBHOOK_SECRET` - Stripe webhook secret

### Celery & Redis
- `CELERY_BROKER_URL` - Redis URL for Celery (default: redis://localhost:6379/0)
- `CELERY_RESULT_BACKEND` - Redis URL for results

## Development Roadmap

### Phase 1: Backend Foundation ✅
- [x] Database models
- [x] Django settings configuration
- [x] Multi-tenant architecture
- [ ] Admin interfaces
- [ ] API serializers
- [ ] API views and endpoints
- [ ] Authentication system

### Phase 2: Core Features
- [ ] Restaurant onboarding flow
- [ ] Menu management API
- [ ] Order processing system
- [ ] Table QR code generation
- [ ] Payment integration (Stripe)

### Phase 3: Frontend
- [ ] Next.js project setup
- [ ] Authentication UI
- [ ] Restaurant dashboard
- [ ] Menu management UI
- [ ] Order management UI
- [ ] Customer ordering interface

### Phase 4: Advanced Features
- [ ] Real-time order updates (WebSockets)
- [ ] Email notifications (AWS SES)
- [ ] WhatsApp notifications (Twilio)
- [ ] Analytics dashboard
- [ ] Reporting features

### Phase 5: Deployment
- [ ] AWS infrastructure setup
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Production environment
- [ ] Monitoring and logging

## API Documentation

API documentation will be available at:
- Development: http://localhost:8000/swagger/
- Development (ReDoc): http://localhost:8000/redoc/

## Admin Interface

Django admin is available at:
- Development: http://localhost:8000/admin/

## Contributing

This is a proprietary project. Contact the development team for contribution guidelines.

## License

Proprietary - All rights reserved

## Support

For support and questions, please contact the development team.
