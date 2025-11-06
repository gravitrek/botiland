# MenuLogin - Deployment Guide

Complete deployment guide for the MenuLogin Restaurant SaaS Platform on AWS.

## Architecture Overview

### Components
- **Backend**: Django REST API
- **Database**: PostgreSQL (AWS RDS)
- **File Storage**: AWS S3
- **Email**: AWS SES
- **SMS/WhatsApp**: Twilio
- **Payment**: Stripe
- **Cache/Queue**: Redis (AWS ElastiCache)
- **Frontend**: Next.js (AWS Amplify or Vercel)
- **Hosting**: AWS EC2 or ECS

## Prerequisites

### AWS Account Setup
1. Create AWS account
2. Set up IAM user with necessary permissions:
   - EC2 full access
   - RDS full access
   - S3 full access
   - SES full access
   - ElastiCache access

### Required Services
1. **Domain name** (e.g., menulogin.com)
2. **AWS Account**
3. **Stripe Account** (for payments)
4. **Twilio Account** (for WhatsApp/SMS)

## Part 1: AWS Infrastructure Setup

### 1.1 Create PostgreSQL Database (AWS RDS)

```bash
# Via AWS Console or CLI
aws rds create-db-instance \
    --db-instance-identifier menulogin-db \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --engine-version 15.3 \
    --master-username menulogin_admin \
    --master-user-password YOUR_SECURE_PASSWORD \
    --allocated-storage 20 \
    --backup-retention-period 7 \
    --vpc-security-group-ids sg-xxxxx \
    --publicly-accessible
```

**Database Configuration:**
- Instance type: db.t3.micro (or larger for production)
- Engine: PostgreSQL 15.x
- Storage: 20GB SSD (auto-scaling enabled)
- Backup: 7 days retention
- Multi-AZ: Enabled (for production)

### 1.2 Create S3 Bucket for Media Files

```bash
# Create S3 bucket
aws s3 mb s3://menulogin-media --region us-east-1

# Set bucket policy for public read access
aws s3api put-bucket-policy --bucket menulogin-media --policy file://s3-policy.json

# Enable CORS
aws s3api put-bucket-cors --bucket menulogin-media --cors-configuration file://cors.json
```

**s3-policy.json:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::menulogin-media/*"
    }
  ]
}
```

**cors.json:**
```json
{
  "CORSRules": [
    {
      "AllowedOrigins": ["*"],
      "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
      "AllowedHeaders": ["*"],
      "ExposeHeaders": ["ETag"],
      "MaxAgeSeconds": 3000
    }
  ]
}
```

### 1.3 Configure AWS SES for Email

```bash
# Verify your domain
aws ses verify-domain-identity --domain menulogin.com

# Verify sender email
aws ses verify-email-identity --email noreply@menulogin.com

# Request production access (required to send to any email)
# This must be done through AWS Console
```

### 1.4 Set up Redis (AWS ElastiCache)

```bash
aws elasticache create-cache-cluster \
    --cache-cluster-id menulogin-redis \
    --cache-node-type cache.t3.micro \
    --engine redis \
    --num-cache-nodes 1
```

## Part 2: Backend Deployment

### 2.1 EC2 Instance Setup

```bash
# Launch Ubuntu EC2 instance (t3.small or larger)
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and required packages
sudo apt install python3.11 python3.11-venv python3-pip postgresql-client nginx supervisor -y

# Install Redis CLI (for testing)
sudo apt install redis-tools -y
```

### 2.2 Deploy Backend Application

```bash
# Create app directory
sudo mkdir -p /var/www/menulogin
sudo chown ubuntu:ubuntu /var/www/menulogin
cd /var/www/menulogin

# Clone repository (or upload files)
git clone https://your-repo/menulogin.git .
cd backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Create .env file
nano .env
```

**Production .env:**
```bash
# Django
SECRET_KEY=your-super-secret-key-change-this
DEBUG=False
ALLOWED_HOSTS=menulogin.com,www.menulogin.com,your-ec2-ip

# Database
USE_POSTGRESQL=True
DB_NAME=menulogin_db
DB_USER=menulogin_admin
DB_PASSWORD=your-db-password
DB_HOST=your-rds-endpoint.rds.amazonaws.com
DB_PORT=5432

# AWS
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=menulogin-media
AWS_S3_REGION_NAME=us-east-1
USE_S3=True

# AWS SES
AWS_SES_REGION_NAME=us-east-1
DEFAULT_FROM_EMAIL=noreply@menulogin.com

# Twilio
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Stripe
STRIPE_PUBLIC_KEY=pk_live_xxx
STRIPE_SECRET_KEY=sk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx

# Redis
CELERY_BROKER_URL=redis://your-redis-endpoint:6379/0
CELERY_RESULT_BACKEND=redis://your-redis-endpoint:6379/0

# Frontend
FRONTEND_URL=https://menulogin.com
```

```bash
# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser
```

### 2.3 Configure Gunicorn

Create `/var/www/menulogin/backend/gunicorn_config.py`:
```python
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
errorlog = "/var/www/menulogin/logs/gunicorn-error.log"
accesslog = "/var/www/menulogin/logs/gunicorn-access.log"
loglevel = "info"
```

### 2.4 Configure Supervisor

Create `/etc/supervisor/conf.d/menulogin.conf`:
```ini
[program:menulogin]
directory=/var/www/menulogin/backend
command=/var/www/menulogin/backend/venv/bin/gunicorn config.wsgi:application -c /var/www/menulogin/backend/gunicorn_config.py
user=ubuntu
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/www/menulogin/logs/gunicorn.log

[program:celery]
directory=/var/www/menulogin/backend
command=/var/www/menulogin/backend/venv/bin/celery -A config worker -l info
user=ubuntu
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/www/menulogin/logs/celery.log
```

```bash
# Create logs directory
mkdir -p /var/www/menulogin/logs

# Update supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start all
```

### 2.5 Configure Nginx

Create `/etc/nginx/sites-available/menulogin`:
```nginx
upstream menulogin_backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name menulogin.com www.menulogin.com;

    client_max_body_size 20M;

    location /static/ {
        alias /var/www/menulogin/backend/staticfiles/;
    }

    location /media/ {
        # Redirect to S3 in production
        return 302 https://menulogin-media.s3.amazonaws.com$request_uri;
    }

    location / {
        proxy_pass http://menulogin_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/menulogin /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 2.6 SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d menulogin.com -d www.menulogin.com
```

## Part 3: Frontend Deployment (Next.js)

### Option A: Deploy to Vercel

```bash
cd /path/to/menulogin/frontend

# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

**Environment Variables (Vercel):**
```
NEXT_PUBLIC_API_URL=https://api.menulogin.com
```

### Option B: Deploy to AWS Amplify

1. Go to AWS Amplify Console
2. Connect your GitHub repository
3. Configure build settings:
   - Build command: `npm run build`
   - Output directory: `.next`
4. Set environment variables
5. Deploy

### Option C: Self-host with PM2

```bash
cd /var/www/menulogin/frontend
npm install
npm run build

# Install PM2
npm install -g pm2

# Start Next.js
pm2 start npm --name "menulogin-frontend" -- start
pm2 save
pm2 startup
```

## Part 4: Domain Configuration

### DNS Records
```
Type    Name    Value
A       @       your-ec2-ip (or load balancer)
A       www     your-ec2-ip
CNAME   api     your-backend-domain
```

## Part 5: Monitoring & Maintenance

### 5.1 Set up CloudWatch

```bash
# Install CloudWatch agent
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
sudo dpkg -i amazon-cloudwatch-agent.deb
```

### 5.2 Database Backups

- RDS automated backups: Already configured (7 days)
- Manual snapshots: Create weekly via AWS Console
- Export to S3: Configure automated exports

### 5.3 Log Management

```bash
# Rotate logs
sudo nano /etc/logrotate.d/menulogin
```

```
/var/www/menulogin/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    missingok
    create 0644 ubuntu ubuntu
}
```

## Part 6: Security Checklist

- [ ] Change all default passwords
- [ ] Enable AWS WAF
- [ ] Configure security groups (only necessary ports open)
- [ ] Enable DDoS protection (AWS Shield)
- [ ] Set up fail2ban on EC2
- [ ] Enable database encryption at rest
- [ ] Use SSL/TLS for all connections
- [ ] Regular security updates
- [ ] Enable MFA for AWS account
- [ ] Configure backup and disaster recovery

## Part 7: Scaling Considerations

### Horizontal Scaling
- Use AWS Auto Scaling Groups
- Deploy behind Application Load Balancer
- Use RDS Read Replicas for read-heavy operations

### Vertical Scaling
- Upgrade EC2 instance types
- Upgrade RDS instance types
- Increase ElastiCache node size

## Troubleshooting

### Backend Issues
```bash
# Check Gunicorn logs
sudo tail -f /var/www/menulogin/logs/gunicorn-error.log

# Check Nginx logs
sudo tail -f /var/nginx/error.log

# Restart services
sudo supervisorctl restart all
sudo systemctl restart nginx
```

### Database Connection Issues
```bash
# Test database connection
psql -h your-rds-endpoint -U menulogin_admin -d menulogin_db

# Check security groups
# Ensure EC2 security group can access RDS security group
```

### Celery Issues
```bash
# Check Celery logs
sudo tail -f /var/www/menulogin/logs/celery.log

# Restart Celery
sudo supervisorctl restart celery
```

## Cost Estimation (Monthly)

### Minimal Setup
- EC2 t3.small: ~$15
- RDS db.t3.micro: ~$15
- S3 (100GB): ~$2
- ElastiCache t3.micro: ~$12
- Data Transfer: ~$10
- **Total: ~$54/month**

### Production Setup
- EC2 t3.medium x2 (load balanced): ~$60
- RDS db.t3.small (Multi-AZ): ~$60
- S3 (500GB): ~$12
- ElastiCache t3.small: ~$30
- Load Balancer: ~$20
- Data Transfer: ~$50
- **Total: ~$232/month**

## Support & Resources

- AWS Documentation: https://docs.aws.amazon.com/
- Django Deployment: https://docs.djangoproject.com/en/5.0/howto/deployment/
- Stripe Integration: https://stripe.com/docs
- Twilio Documentation: https://www.twilio.com/docs

## Post-Deployment

1. Test all features thoroughly
2. Set up monitoring alerts
3. Document any custom configurations
4. Create runbook for common operations
5. Schedule regular backups
6. Plan for disaster recovery

---

**Last Updated**: November 2025
**Version**: 1.0.0
