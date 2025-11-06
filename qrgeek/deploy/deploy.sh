#!/bin/bash

# QRGeek Deployment Script
# This script deploys the QRGeek application to a production server

set -e  # Exit on error

echo "=== QRGeek Deployment Script ==="
echo ""

# Configuration
PROJECT_DIR="/var/www/qrgeek"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"
VENV_DIR="$PROJECT_DIR/venv"
LOG_DIR="/var/log/qrgeek"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    log_error "Please run as root or with sudo"
    exit 1
fi

log_info "Starting deployment..."

# Create directories
log_info "Creating directories..."
mkdir -p $PROJECT_DIR
mkdir -p $LOG_DIR
mkdir -p /var/run/qrgeek

# Pull latest code
log_info "Pulling latest code from Git..."
cd $PROJECT_DIR
if [ -d ".git" ]; then
    git pull origin main
else
    log_warn "Not a git repository. Skipping git pull."
fi

# Backend deployment
log_info "Deploying backend..."

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    log_info "Creating virtual environment..."
    python3 -m venv $VENV_DIR
fi

# Activate virtual environment and install dependencies
log_info "Installing Python dependencies..."
source $VENV_DIR/bin/activate
cd $BACKEND_DIR
pip install -r requirements.txt

# Run migrations
log_info "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
log_info "Collecting static files..."
python manage.py collectstatic --noinput

# Create cache table
log_info "Creating cache table..."
python manage.py createcachetable || true

# Deactivate virtual environment
deactivate

# Frontend deployment
log_info "Deploying frontend..."
cd $FRONTEND_DIR

# Install Node dependencies
if [ ! -d "node_modules" ]; then
    log_info "Installing Node dependencies..."
    npm ci --production
fi

# Build Next.js
log_info "Building Next.js application..."
npm run build

# Set permissions
log_info "Setting permissions..."
chown -R www-data:www-data $PROJECT_DIR
chown -R www-data:www-data $LOG_DIR
chown -R www-data:www-data /var/run/qrgeek
chmod -R 755 $PROJECT_DIR

# Install systemd services
log_info "Installing systemd services..."
cp deploy/systemd/qrgeek-backend.service /etc/systemd/system/
cp deploy/systemd/qrgeek-celery.service /etc/systemd/system/
cp deploy/systemd/qrgeek-frontend.service /etc/systemd/system/

# Install Nginx configuration
log_info "Installing Nginx configuration..."
cp deploy/nginx/qrgeek.conf /etc/nginx/sites-available/qrgeek
if [ ! -L /etc/nginx/sites-enabled/qrgeek ]; then
    ln -s /etc/nginx/sites-available/qrgeek /etc/nginx/sites-enabled/qrgeek
fi

# Test Nginx configuration
log_info "Testing Nginx configuration..."
nginx -t

# Reload systemd
log_info "Reloading systemd..."
systemctl daemon-reload

# Restart services
log_info "Restarting services..."
systemctl restart qrgeek-backend
systemctl restart qrgeek-celery
systemctl restart qrgeek-frontend
systemctl reload nginx

# Enable services on boot
log_info "Enabling services on boot..."
systemctl enable qrgeek-backend
systemctl enable qrgeek-celery
systemctl enable qrgeek-frontend
systemctl enable nginx

# Check service status
log_info "Checking service status..."
systemctl status qrgeek-backend --no-pager
systemctl status qrgeek-celery --no-pager
systemctl status qrgeek-frontend --no-pager

log_info "Deployment completed successfully!"
log_info "Please check the logs in $LOG_DIR if you encounter any issues."

echo ""
echo "=== Service Status ==="
echo "Backend: $(systemctl is-active qrgeek-backend)"
echo "Celery: $(systemctl is-active qrgeek-celery)"
echo "Frontend: $(systemctl is-active qrgeek-frontend)"
echo "Nginx: $(systemctl is-active nginx)"
