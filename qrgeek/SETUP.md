# QRGeek Setup Guide

Complete setup instructions for the QRGeek QR code platform.

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (optional)

## Quick Start with Docker

The fastest way to get started:

```bash
# Clone the repository
git clone <repository-url>
cd qrgeek

# Start all services
docker-compose up -d

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Create initial data (subscription plans)
docker-compose exec backend python manage.py loaddata initial_data
```

Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Admin Panel: http://localhost:8000/admin
- API Docs: http://localhost:8000/api/docs

## Manual Setup

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your settings
# At minimum, set DATABASE_URL and SECRET_KEY

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Create initial subscription plans
python manage.py shell
```

In Python shell:
```python
from accounts.models import SubscriptionPlan

SubscriptionPlan.objects.create(
    name="Free",
    slug="free",
    price=0,
    billing_period="monthly",
    qr_limit=5,
    scan_limit=500,
    features={"basic_analytics": True},
    is_active=True,
    display_order=1
)

SubscriptionPlan.objects.create(
    name="Starter",
    slug="starter",
    price=9,
    billing_period="monthly",
    qr_limit=25,
    scan_limit=5000,
    features={"advanced_analytics": True, "custom_branding": True},
    is_active=True,
    is_featured=True,
    display_order=2
)

SubscriptionPlan.objects.create(
    name="Professional",
    slug="professional",
    price=29,
    billing_period="monthly",
    qr_limit=100,
    scan_limit=50000,
    features={"advanced_analytics": True, "custom_branding": True, "api_access": True, "custom_domains": True},
    is_active=True,
    display_order=3
)

SubscriptionPlan.objects.create(
    name="Enterprise",
    slug="enterprise",
    price=99,
    billing_period="monthly",
    qr_limit=-1,  # unlimited
    scan_limit=-1,  # unlimited
    features={"everything": True, "white_label": True, "priority_support": True, "sso": True},
    is_active=True,
    display_order=4
)
```

Exit shell and start server:
```bash
python manage.py runserver
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env.local

# Start development server
npm run dev
```

### 3. Background Tasks (Celery)

In a new terminal:
```bash
cd backend
source venv/bin/activate
celery -A config worker -l info
```

## Database Setup

### PostgreSQL

Create database:
```sql
CREATE DATABASE qrgeek;
CREATE USER qrgeek WITH PASSWORD 'qrgeek';
ALTER ROLE qrgeek SET client_encoding TO 'utf8';
ALTER ROLE qrgeek SET default_transaction_isolation TO 'read committed';
ALTER ROLE qrgeek SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE qrgeek TO qrgeek;
```

### Redis

Install Redis:
```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS
brew install redis

# Start Redis
redis-server
```

## Environment Configuration

### Backend (.env)

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_URL=postgresql://qrgeek:qrgeek@localhost:5432/qrgeek
REDIS_URL=redis://localhost:6379/0

# AWS (for production)
USE_S3=False
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
AWS_S3_REGION_NAME=us-east-1
AWS_SES_REGION_NAME=us-east-1

# Frontend
FRONTEND_URL=http://localhost:3000
CORS_ALLOWED_ORIGINS=http://localhost:3000

# URL Shortening
SHORT_URL_DOMAIN=qrgeek.com

# Email
DEFAULT_FROM_EMAIL=noreply@qrgeek.com
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_SITE_URL=http://localhost:3000
```

## Production Deployment

### Backend

1. Set DEBUG=False
2. Set strong SECRET_KEY
3. Configure PostgreSQL (AWS RDS recommended)
4. Configure Redis (AWS ElastiCache recommended)
5. Set up AWS S3 for media files
6. Configure Amazon SES for emails
7. Set up Sentry for error tracking
8. Use Gunicorn as WSGI server
9. Use Nginx as reverse proxy
10. Set up SSL/TLS certificates

### Frontend

1. Build production bundle: `npm run build`
2. Deploy to Vercel, Netlify, or your server
3. Set environment variables
4. Configure custom domain
5. Enable CDN

## Testing

### Backend Tests
```bash
cd backend
python manage.py test
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Common Issues

### Database Connection Error
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Verify database exists and user has permissions

### Redis Connection Error
- Ensure Redis is running
- Check REDIS_URL in .env

### QR Code Generation Error
- Ensure Pillow dependencies are installed
- Check file permissions for media directory

### CORS Error
- Add frontend URL to CORS_ALLOWED_ORIGINS
- Check ALLOWED_HOSTS includes your domain

## API Documentation

Once the backend is running, access API documentation:
- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/

## Development Workflow

1. Create feature branch
2. Make changes
3. Run tests
4. Format code (Black for Python, Prettier for JS/TS)
5. Commit and push
6. Create pull request

## Support

For issues and questions:
- GitHub Issues: <repository-url>/issues
- Email: support@qrgeek.com

## License

Proprietary - All rights reserved
