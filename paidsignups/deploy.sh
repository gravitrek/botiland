#!/bin/bash

# PaidSignups Deployment Script for AWS Lightsail
# This script automates the deployment process

set -e

echo "🚀 Starting PaidSignups deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -eq 0 ]; then
  echo -e "${RED}Please do not run as root${NC}"
  exit 1
fi

# Update system packages
echo -e "${YELLOW}📦 Updating system packages...${NC}"
sudo apt update
sudo apt upgrade -y

# Install required packages
echo -e "${YELLOW}📦 Installing required packages...${NC}"
sudo apt install -y python3-pip python3-venv postgresql postgresql-contrib nginx git

# Install Node.js 18.x
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}📦 Installing Node.js...${NC}"
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt install -y nodejs
fi

# Setup PostgreSQL
echo -e "${YELLOW}🗄️  Setting up PostgreSQL...${NC}"
sudo -u postgres psql -c "SELECT 1 FROM pg_database WHERE datname = 'paidsignups'" | grep -q 1 || sudo -u postgres psql -c "CREATE DATABASE paidsignups;"
sudo -u postgres psql -c "SELECT 1 FROM pg_user WHERE usename = 'paidsignups_user'" | grep -q 1 || sudo -u postgres psql -c "CREATE USER paidsignups_user WITH PASSWORD 'changeme';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE paidsignups TO paidsignups_user;"

# Setup backend
echo -e "${YELLOW}🐍 Setting up Django backend...${NC}"
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
pip install gunicorn

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please update the .env file with your configuration${NC}"
fi

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (interactive)
echo -e "${YELLOW}👤 Create Django superuser (skip if already exists)${NC}"
python manage.py createsuperuser --noinput || echo "Superuser may already exist"

# Collect static files
python manage.py collectstatic --noinput

# Setup systemd service for Django
echo -e "${YELLOW}⚙️  Setting up systemd service...${NC}"
sudo tee /etc/systemd/system/paidsignups.service > /dev/null <<EOF
[Unit]
Description=PaidSignups Django Backend
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=$(pwd)
Environment="PATH=$(pwd)/venv/bin"
ExecStart=$(pwd)/venv/bin/gunicorn --workers 3 --bind unix:$(pwd)/paidsignups.sock config.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable paidsignups
sudo systemctl restart paidsignups

# Setup frontend
echo -e "${YELLOW}⚛️  Setting up Next.js frontend...${NC}"
cd ../frontend

# Install Node dependencies
npm install

# Build frontend
npm run build

# Create .env.local if it doesn't exist
if [ ! -f ".env.local" ]; then
    cp .env.local.example .env.local
    echo -e "${YELLOW}⚠️  Please update the .env.local file with your configuration${NC}"
fi

# Setup systemd service for Next.js
echo -e "${YELLOW}⚙️  Setting up Next.js systemd service...${NC}"
sudo tee /etc/systemd/system/paidsignups-frontend.service > /dev/null <<EOF
[Unit]
Description=PaidSignups Next.js Frontend
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=$(pwd)
Environment="PATH=/usr/bin:/usr/local/bin"
Environment="NODE_ENV=production"
ExecStart=/usr/bin/npm start

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable paidsignups-frontend
sudo systemctl restart paidsignups-frontend

# Setup Nginx
echo -e "${YELLOW}🌐 Setting up Nginx...${NC}"
cd ..

sudo tee /etc/nginx/sites-available/paidsignups > /dev/null <<EOF
# Backend API
server {
    listen 80;
    server_name api.paidsignups.com;  # Change to your domain

    location /static/ {
        alias $(pwd)/backend/staticfiles/;
    }

    location /media/ {
        alias $(pwd)/backend/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:$(pwd)/backend/paidsignups.sock;
    }
}

# Frontend
server {
    listen 80;
    server_name paidsignups.com www.paidsignups.com;  # Change to your domain

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF

# Enable site
sudo ln -sf /etc/nginx/sites-available/paidsignups /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Setup firewall
echo -e "${YELLOW}🔥 Setting up firewall...${NC}"
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
echo "y" | sudo ufw enable

echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Update /etc/nginx/sites-available/paidsignups with your domain"
echo "2. Update backend/.env with your configuration"
echo "3. Update frontend/.env.local with your API URL"
echo "4. Setup SSL certificate with: sudo certbot --nginx"
echo ""
echo "Service commands:"
echo "  Backend:  sudo systemctl status paidsignups"
echo "  Frontend: sudo systemctl status paidsignups-frontend"
echo "  Nginx:    sudo systemctl status nginx"
echo ""
echo "View logs:"
echo "  Backend:  sudo journalctl -u paidsignups -f"
echo "  Frontend: sudo journalctl -u paidsignups-frontend -f"
