#!/bin/bash

# QRGeek Server Setup Script
# This script sets up a fresh Ubuntu server for QRGeek deployment

set -e

echo "=== QRGeek Server Setup ==="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root or with sudo"
    exit 1
fi

# Update system
echo "[1/10] Updating system packages..."
apt-get update
apt-get upgrade -y

# Install system dependencies
echo "[2/10] Installing system dependencies..."
apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    postgresql \
    postgresql-contrib \
    redis-server \
    nginx \
    git \
    curl \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    certbot \
    python3-certbot-nginx

# Install Node.js
echo "[3/10] Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt-get install -y nodejs

# Configure PostgreSQL
echo "[4/10] Configuring PostgreSQL..."
sudo -u postgres psql -c "CREATE DATABASE qrgeek;" || true
sudo -u postgres psql -c "CREATE USER qrgeek WITH PASSWORD 'qrgeek';" || true
sudo -u postgres psql -c "ALTER ROLE qrgeek SET client_encoding TO 'utf8';" || true
sudo -u postgres psql -c "ALTER ROLE qrgeek SET default_transaction_isolation TO 'read committed';" || true
sudo -u postgres psql -c "ALTER ROLE qrgeek SET timezone TO 'UTC';" || true
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE qrgeek TO qrgeek;" || true

# Configure Redis
echo "[5/10] Configuring Redis..."
systemctl enable redis-server
systemctl start redis-server

# Create project directories
echo "[6/10] Creating project directories..."
mkdir -p /var/www/qrgeek
mkdir -p /var/log/qrgeek
mkdir -p /var/run/qrgeek

# Create www-data user if it doesn't exist
id -u www-data &>/dev/null || useradd -r -s /bin/bash www-data

# Set permissions
chown -R www-data:www-data /var/www/qrgeek
chown -R www-data:www-data /var/log/qrgeek
chown -R www-data:www-data /var/run/qrgeek

# Configure firewall
echo "[7/10] Configuring firewall..."
ufw --force enable
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS

# Install Let's Encrypt SSL certificate
echo "[8/10] SSL Setup (skipping for now, run certbot manually)..."
echo "To setup SSL, run: certbot --nginx -d qrgeek.com -d www.qrgeek.com"

# Enable services
echo "[9/10] Enabling services..."
systemctl enable postgresql
systemctl enable redis-server
systemctl enable nginx

# Print summary
echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "1. Clone your repository to /var/www/qrgeek"
echo "2. Copy .env.example to .env and configure"
echo "3. Run the deployment script: ./deploy.sh"
echo "4. Setup SSL: certbot --nginx -d qrgeek.com -d www.qrgeek.com"
echo ""
echo "Services status:"
echo "PostgreSQL: $(systemctl is-active postgresql)"
echo "Redis: $(systemctl is-active redis-server)"
echo "Nginx: $(systemctl is-active nginx)"
