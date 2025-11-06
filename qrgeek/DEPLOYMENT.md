# QRGeek Production Deployment Guide

Complete guide for deploying QRGeek to a production server.

## Prerequisites

- Ubuntu 20.04 or 22.04 LTS server
- Domain name pointed to your server
- Root or sudo access
- At least 2GB RAM, 2 CPU cores, 20GB storage

## Quick Deployment

### 1. Initial Server Setup

```bash
# Run the automated server setup script
sudo bash deploy/setup-server.sh
```

This script will:
- Update system packages
- Install Python, Node.js, PostgreSQL, Redis, Nginx
- Configure PostgreSQL and Redis
- Set up firewall rules
- Create necessary directories

### 2. Clone Repository

```bash
cd /var/www/qrgeek
git clone <your-repo-url> .
```

### 3. Configure Environment

#### Backend (.env)
```bash
cd backend
cp .env.example .env
nano .env
```

Update the following:
```env
DEBUG=False
SECRET_KEY=<generate-strong-secret-key>
ALLOWED_HOSTS=qrgeek.com,www.qrgeek.com
DATABASE_URL=postgresql://qrgeek:your-db-password@localhost:5432/qrgeek
REDIS_URL=redis://localhost:6379/0

# AWS (recommended for production)
USE_S3=True
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_STORAGE_BUCKET_NAME=qrgeek-media
AWS_S3_REGION_NAME=us-east-1
AWS_SES_REGION_NAME=us-east-1

# Email
DEFAULT_FROM_EMAIL=noreply@qrgeek.com

# Frontend
FRONTEND_URL=https://qrgeek.com
CORS_ALLOWED_ORIGINS=https://qrgeek.com,https://www.qrgeek.com

# Sentry (optional)
SENTRY_DSN=your-sentry-dsn
```

#### Frontend (.env.production)
```bash
cd ../frontend
cp .env.example .env.production
nano .env.production
```

```env
NEXT_PUBLIC_API_URL=https://qrgeek.com/api
NEXT_PUBLIC_SITE_URL=https://qrgeek.com
NODE_ENV=production
```

### 4. Run Deployment Script

```bash
cd /var/www/qrgeek
sudo bash deploy/deploy.sh
```

This script will:
- Create virtual environment
- Install dependencies
- Run migrations
- Collect static files
- Build Next.js
- Install systemd services
- Configure Nginx
- Start all services

### 5. Setup SSL Certificate

```bash
sudo certbot --nginx -d qrgeek.com -d www.qrgeek.com
```

Follow the prompts to set up HTTPS.

### 6. Create Superuser

```bash
cd /var/www/qrgeek/backend
source /var/www/qrgeek/venv/bin/activate
python manage.py createsuperuser
```

### 7. Load Initial Data

```python
python manage.py shell

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
    qr_limit=-1,
    scan_limit=-1,
    features={"everything": True, "white_label": True, "priority_support": True, "sso": True},
    is_active=True,
    display_order=4
)
```

## Manual Steps

If you prefer manual deployment:

### 1. Install Dependencies

```bash
# Python dependencies
cd /var/www/qrgeek/backend
python3 -m venv /var/www/qrgeek/venv
source /var/www/qrgeek/venv/bin/activate
pip install -r requirements.txt

# Node dependencies
cd /var/www/qrgeek/frontend
npm ci --production
npm run build
```

### 2. Database Setup

```bash
# Run migrations
cd /var/www/qrgeek/backend
source /var/www/qrgeek/venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
```

### 3. Install Services

```bash
# Copy systemd service files
sudo cp deploy/systemd/*.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable and start services
sudo systemctl enable qrgeek-backend qrgeek-celery qrgeek-frontend
sudo systemctl start qrgeek-backend qrgeek-celery qrgeek-frontend
```

### 4. Configure Nginx

```bash
# Copy Nginx configuration
sudo cp deploy/nginx/qrgeek.conf /etc/nginx/sites-available/qrgeek
sudo ln -s /etc/nginx/sites-available/qrgeek /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

## AWS Configuration

### S3 Bucket Setup

1. Create S3 bucket: `qrgeek-media`
2. Enable public access for media files
3. Configure CORS:

```json
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "HEAD"],
        "AllowedOrigins": ["https://qrgeek.com"],
        "ExposeHeaders": []
    }
]
```

### SES Email Setup

1. Verify domain in AWS SES
2. Request production access (remove sandbox mode)
3. Configure DKIM and SPF records
4. Set up bounce and complaint notifications

## Monitoring

### Check Service Status

```bash
sudo systemctl status qrgeek-backend
sudo systemctl status qrgeek-celery
sudo systemctl status qrgeek-frontend
sudo systemctl status nginx
```

### View Logs

```bash
# Backend logs
sudo journalctl -u qrgeek-backend -f

# Celery logs
sudo journalctl -u qrgeek-celery -f

# Frontend logs
sudo journalctl -u qrgeek-frontend -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Application logs
sudo tail -f /var/log/qrgeek/gunicorn-access.log
sudo tail -f /var/log/qrgeek/gunicorn-error.log
```

## Updates and Maintenance

### Deploy Updates

```bash
cd /var/www/qrgeek
git pull origin main
sudo bash deploy/deploy.sh
```

### Database Backup

```bash
# Backup
sudo -u postgres pg_dump qrgeek > backup.sql

# Restore
sudo -u postgres psql qrgeek < backup.sql
```

### Clear Cache

```bash
# Django cache
cd /var/www/qrgeek/backend
source /var/www/qrgeek/venv/bin/activate
python manage.py clear_cache

# Redis cache
redis-cli FLUSHDB
```

## Security Checklist

- [ ] Change default PostgreSQL password
- [ ] Set strong SECRET_KEY
- [ ] Enable firewall (UFW)
- [ ] Setup SSL/TLS certificates
- [ ] Configure fail2ban for SSH protection
- [ ] Enable automatic security updates
- [ ] Set up regular backups
- [ ] Configure Sentry for error tracking
- [ ] Review and update Nginx security headers
- [ ] Implement rate limiting
- [ ] Regular dependency updates

## Performance Optimization

### Database
- Enable connection pooling
- Add database indexes
- Regular VACUUM and ANALYZE

### Redis
- Configure max memory and eviction policy
- Enable persistence if needed

### Nginx
- Enable gzip compression
- Configure caching headers
- Set up rate limiting

### Django
- Use database query optimization
- Enable template caching
- Compress static files

## Troubleshooting

### Service Won't Start

```bash
# Check service status
sudo systemctl status qrgeek-backend

# Check logs
sudo journalctl -u qrgeek-backend -n 50
```

### 502 Bad Gateway

- Check if backend service is running
- Verify Gunicorn is listening on correct port
- Check Nginx upstream configuration

### Database Connection Error

- Verify PostgreSQL is running
- Check DATABASE_URL in .env
- Ensure database user has correct permissions

### Static Files Not Loading

- Run `python manage.py collectstatic`
- Check Nginx static files configuration
- Verify file permissions

## Support

For issues:
- Check logs in `/var/log/qrgeek/`
- Review service status with `systemctl status`
- Consult documentation at docs.qrgeek.com
- Contact support@qrgeek.com

## License

Proprietary - All rights reserved
