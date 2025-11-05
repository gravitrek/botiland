# Quick Setup Guide

## Prerequisites
- Python 3.10+
- Node.js 18+
- pip and npm

## Quick Start (Development)

### 1. Backend Setup (Terminal 1)
```bash
cd formations-casa/backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser
# Username: admin
# Email: admin@formations.casa
# Password: (your password)

# Run server
python manage.py runserver
```

Backend will be at: http://localhost:8000
- Admin: http://localhost:8000/admin/
- API Docs: http://localhost:8000/api/docs/

### 2. Frontend Setup (Terminal 2)
```bash
cd formations-casa/frontend

# Install dependencies
npm install

# Copy environment file
cp .env.local.example .env.local

# Run development server
npm run dev
```

Frontend will be at: http://localhost:3000

## Initial Setup Tasks

### 1. Create Some Initial Data (Django Admin)

Login to http://localhost:8000/admin/ with your superuser credentials

#### Formation Categories
1. Go to Formations > Categories
2. Add categories like:
   - Technology (slug: technology)
   - Business (slug: business)
   - Design (slug: design)
   - Marketing (slug: marketing)
   - Languages (slug: languages)

#### Formation Types
1. Go to Formations > Formation Types
2. Add types:
   - Workshop
   - Course
   - Bootcamp
   - Seminar

#### Gamification Badges (100+ examples)

Go to Gamification > Badges and create badges like:

**Beginner Badges:**
- First Step: Complete registration
- Explorer: View 10 formations
- Curious Mind: Browse 5 categories

**Participation Badges:**
- Student: Enroll in first formation
- Dedicated Learner: Complete 5 formations
- Master: Complete 20 formations

**Achievement Badges:**
- Early Bird: Enroll within 24hrs of formation creation
- Perfect Attendance: 100% attendance in a formation
- Quick Learner: Complete formation in minimum time

**Social Badges:**
- Reviewer: Leave first review
- Influencer: 10 helpful reviews
- Community Leader: 50 helpful reviews

**Expert Badges:**
- Specialist: Complete all formations in one category
- Polymath: Complete formations in 5 different categories
- Guru: 100 formations completed

**Special Badges:**
- Launch Member: Early platform adopter
- Beta Tester: Participated in beta
- VIP: Special invitation

#### Features & Credits

Go to Features > Features and add:
- Featured Formation Listing (0 credits)
- Premium Placement (0 credits)
- Analytics Dashboard (0 credits)
- Advanced Reporting (0 credits)
- Priority Support (0 credits)

*Note: All features set to 0 credits initially. Admin can adjust later.*

### 2. Test User Registration

1. Go to http://localhost:3000
2. Click "Sign Up"
3. Register as:
   - Regular user
   - Coach (to create formations)
   - Training center (to add venues)

### 3. Approve Users (Admin)

1. Login to Django Admin
2. Go to Accounts > Users
3. Find newly registered users
4. Check "Is approved" checkbox
5. Save

### 4. Create a Formation (As Coach)

1. Login as approved coach
2. Go to http://localhost:8000/admin/formations/formation/add/
3. Fill in:
   - Title
   - Slug (auto-generated)
   - Description (rich text)
   - Category
   - Price (in MAD)
   - Start/End dates
   - Delivery mode (in-person/remote/hybrid)
   - Max participants
4. Add curriculum items
5. Set status to "published"
6. Save

### 5. Create Training Center (As Center Owner)

1. Login as approved training center
2. Go to http://localhost:8000/admin/centers/trainingcenter/add/
3. Fill in details
4. Add rooms
5. Set availability
6. Admin approves

## Common Development Tasks

### Create superuser
```bash
python manage.py createsuperuser
```

### Make migrations after model changes
```bash
python manage.py makemigrations
python manage.py migrate
```

### Create initial badges (management command - to be created)
```bash
python manage.py create_initial_badges
```

### Reset database
```bash
rm db.sqlite3
rm */migrations/00*.py  # Keep __init__.py
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## Testing the Platform

### User Flow
1. Register as user
2. Browse formations
3. Enroll in formation
4. Receive payment instructions
5. Upload payment proof
6. Admin verifies payment
7. Access formation materials
8. Complete formation
9. Earn badges and points
10. Leave review

### Coach Flow
1. Register as coach
2. Wait for approval
3. Create formation with curriculum
4. Set payment instructions (bank details)
5. Wait for enrollments
6. Send payment instructions automatically
7. Verify payments
8. Reconcile payments
9. Track student progress

### Training Center Flow
1. Register as training center
2. Wait for approval
3. Add rooms with details
4. Set availability calendar
5. Set pricing
6. Coaches book rooms
7. Track bookings

### Admin Flow
1. Approve/reject users
2. Manage categories
3. Approve formations
4. Set feature costs
5. Create/manage badges
6. Create blog posts
7. View analytics
8. Handle disputes

## Production Checklist

- [ ] Set DEBUG=False
- [ ] Configure PostgreSQL
- [ ] Set SECRET_KEY
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up static files (whitenoise/nginx)
- [ ] Set up media files
- [ ] Configure CORS for frontend domain
- [ ] Set up SSL (Let's Encrypt)
- [ ] Configure email backend
- [ ] Set up backups
- [ ] Configure logging
- [ ] Set up monitoring
- [ ] Load testing
- [ ] Security audit

## Environment Variables

### Backend (.env)
```
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/formations
ALLOWED_HOSTS=formations.casa,www.formations.casa
CORS_ALLOWED_ORIGINS=https://formations.casa
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=https://api.formations.casa/api
```

## Troubleshooting

### Backend won't start
- Check if virtual environment is activated
- Verify all dependencies installed: `pip list`
- Check for migration errors: `python manage.py showmigrations`

### Frontend won't start
- Delete node_modules and package-lock.json
- Run `npm install` again
- Check Node.js version: `node --version` (should be 18+)

### CORS errors
- Check CORS_ALLOWED_ORIGINS in settings.py
- Verify frontend URL in backend settings

### Database errors
- Delete db.sqlite3 and re-run migrations
- Check PostgreSQL connection if using Postgres

## Support

For issues, check:
1. Django logs: backend console
2. Next.js logs: frontend console
3. Browser console for API errors
4. Django admin logs

---

Happy coding! 🚀
