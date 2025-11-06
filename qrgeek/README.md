# QRGeek.com - Professional QR Code Platform

A comprehensive QR code generation and management platform with advanced analytics, industry-specific templates, and customization options.

## Features

- **Multi-Industry Support**: Restaurants, Retail, Events, Healthcare, Real Estate, Education
- **Advanced Analytics**: Track scans, locations, devices, and user behavior
- **Customization**: Colors, logos, sizes, formats (PNG, SVG, PDF)
- **QR Types**: URL, vCard, WiFi, Email, SMS, Text, and more
- **Tracking Options**: Enable/disable scan tracking per QR code
- **Bulk Operations**: Create and download multiple QR codes
- **Admin Panel**: React-based administration interface
- **Email Integration**: Amazon SES for transactional emails

## Technology Stack

### Backend
- Django 4.2+ with Django REST Framework
- PostgreSQL 15+
- Redis (caching and task queue)
- Celery (background tasks)
- AWS S3 (storage)
- Amazon SES (email)

### Frontend
- Next.js 14+ (App Router)
- React 18+
- Tailwind CSS + shadcn/ui
- TanStack Query
- Recharts (analytics)

### DevOps
- Docker + Docker Compose
- Nginx
- Gunicorn + PM2
- GitHub Actions (CI/CD)

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Docker Setup
```bash
docker-compose up -d
```

## Project Structure

```
qrgeek/
├── backend/              # Django backend
│   ├── config/          # Django settings
│   ├── accounts/        # User management
│   ├── qrcodes/         # QR code generation
│   ├── analytics/       # Tracking and analytics
│   ├── industries/      # Industry-specific features
│   └── common/          # Shared utilities
├── frontend/            # Next.js frontend
│   ├── app/            # App router pages
│   ├── components/     # React components
│   ├── lib/            # Utilities
│   └── public/         # Static assets
├── deploy/             # Deployment configs
├── docs/               # Documentation
└── docker-compose.yml  # Docker configuration
```

## Environment Variables

### Backend (.env)
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@localhost:5432/qrgeek
REDIS_URL=redis://localhost:6379/0
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_STORAGE_BUCKET_NAME=your-s3-bucket
AWS_SES_REGION_NAME=us-east-1
FRONTEND_URL=http://localhost:3000
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_SITE_URL=http://localhost:3000
```

## API Documentation

API documentation is available at `/api/docs/` when running the backend server.

## Development

### Running Tests
```bash
# Backend tests
cd backend
python manage.py test

# Frontend tests
cd frontend
npm test
```

### Code Formatting
```bash
# Backend (Black + isort)
cd backend
black .
isort .

# Frontend (Prettier)
cd frontend
npm run format
```

## Deployment

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed deployment instructions.

## License

Proprietary - All rights reserved

## Support

For issues and questions, contact: support@qrgeek.com
