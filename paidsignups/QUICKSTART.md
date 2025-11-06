# Quick Start Guide - PaidSignups

This guide will help you get PaidSignups running on your local machine in 10 minutes.

## Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Git

## Step 1: Clone and Navigate

```bash
cd paidsignups
```

## Step 2: Setup PostgreSQL Database

```bash
# Login to PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE paidsignups;
CREATE USER paidsignups_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE paidsignups TO paidsignups_user;
\q
```

## Step 3: Setup Backend

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and update these values:
# DB_NAME=paidsignups
# DB_USER=paidsignups_user
# DB_PASSWORD=your_password
# SECRET_KEY=your-secret-key

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

Backend is now running at http://localhost:8000

## Step 4: Setup Frontend (New Terminal)

```bash
cd paidsignups/frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.local.example .env.local

# Edit .env.local:
# NEXT_PUBLIC_API_URL=http://localhost:8000/api

# Run development server
npm run dev
```

Frontend is now running at http://localhost:3000

## Step 5: Test the Platform

1. Open http://localhost:3000
2. Click "Get Started Free" to register
3. Login with your credentials
4. Explore the dashboard

## Admin Panel

Access the Django admin at http://localhost:8000/admin with your superuser credentials.

## API Documentation

The API is available at http://localhost:8000/api/

Key endpoints:
- `/api/auth/register/` - Register
- `/api/auth/login/` - Login
- `/api/forms/` - Forms management
- `/api/landing-pages/` - Landing pages management
- `/api/leads/` - Leads management
- `/api/subscriptions/` - Subscription management

## Default Subscription Plans

### Free Plan
- 3 Forms
- 3 Landing Pages
- 100 Leads/month

### Basic Plan - $19.99/month
- 10 Forms
- 10 Landing Pages
- 1,000 Leads/month
- Custom Branding

### Pro Plan - $49.99/month
- 50 Forms
- 50 Landing Pages
- 10,000 Leads/month
- Advanced Analytics
- API Access

### Enterprise Plan - $99.99/month
- Unlimited Everything
- All Features

## PayPal Integration

For paid subscriptions, users are directed to: https://paypal.me/yagzud

To test payments in development:
1. Use PayPal sandbox credentials
2. Update `PAYPAL_CLIENT_ID` and `PAYPAL_CLIENT_SECRET` in backend/.env
3. Set `PAYPAL_MODE=sandbox`

## AWS SES Email Setup

1. Create AWS SES account
2. Verify your sender email
3. Get SMTP credentials
4. Update in backend/.env:
   ```
   AWS_SES_ACCESS_KEY_ID=your_access_key
   AWS_SES_SECRET_ACCESS_KEY=your_secret_key
   DEFAULT_FROM_EMAIL=noreply@yourdomain.com
   ```

## Common Issues

### Database Connection Error
- Make sure PostgreSQL is running: `sudo systemctl status postgresql`
- Check database credentials in .env file
- Ensure database exists: `sudo -u postgres psql -l`

### Frontend Can't Connect to Backend
- Check if backend is running on port 8000
- Verify NEXT_PUBLIC_API_URL in frontend/.env.local
- Check CORS settings in backend/config/settings.py

### Module Not Found Errors
- Backend: Make sure virtual environment is activated
- Frontend: Run `npm install` again

## Development Tips

### Backend Hot Reload
The Django development server automatically reloads when you change Python files.

### Frontend Hot Reload
Next.js automatically reloads when you change React/TypeScript files.

### Database Migrations
After changing models:
```bash
python manage.py makemigrations
python manage.py migrate
```

### View Database
```bash
sudo -u postgres psql paidsignups
```

### Reset Database
```bash
python manage.py flush  # Clears all data
# OR
python manage.py reset_db  # Drops and recreates database (requires django-extensions)
```

## Next Steps

1. Customize the theme in frontend/tailwind.config.ts
2. Add your logo and branding
3. Configure email templates
4. Set up analytics tracking
5. Configure your PayPal account
6. Deploy to production (see README.md)

## Support

For issues or questions:
- Check the README.md for detailed documentation
- Review the API documentation
- Check Django logs: backend terminal
- Check Next.js logs: frontend terminal

## Production Deployment

For production deployment on AWS Lightsail:

```bash
./deploy.sh
```

See README.md for detailed deployment instructions.
