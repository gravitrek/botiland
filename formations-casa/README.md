# Formations.casa - Professional Training Marketplace

A comprehensive platform for training courses in Casablanca, Morocco, where coaches create formations, training centers offer spaces, and students can enroll and learn.

## Features

### Core Functionality

- **Multi-Role System**: Users, Coaches, Training Centers, and Admins
- **Formation Management**: Create, manage, and browse training courses
- **Training Centers**: Manage venues, rooms, availability, and amenities
- **Booking System**: Enroll in formations with automated payment instructions
- **Payment Management**: Bank transfer instructions, reconciliation, and proof upload
- **Approval Workflow**: Admin approval for coaches, centers, and formations

### Advanced Features

- **100% Gamification**: Badges, achievements, points, leaderboards, and rewards
- **Credit System**: Feature-based credits with subscription plans
- **Blog & CMS**: WYSIWYG content management for admins
- **Reviews & Ratings**: Rate formations and training centers
- **Directory Views**: Browse coaches, centers, and formations
- **Multi-Delivery Modes**: In-person, remote, or hybrid trainings
- **Room Management**: Capacity, amenities, pricing, and availability tracking

## Tech Stack

### Backend
- **Django 5.0+** - Web framework
- **Django REST Framework** - API
- **JWT Authentication** - Simple JWT
- **PostgreSQL/SQLite** - Database
- **CKEditor** - Rich text editing
- **drf-yasg** - API documentation

### Frontend
- **Next.js 15** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Axios** - API client

## Project Structure

```
formations-casa/
├── backend/
│   ├── config/              # Django settings
│   ├── accounts/            # User management, roles, profiles
│   ├── formations/          # Training courses, categories, curriculum
│   ├── centers/             # Training centers, rooms, availability
│   ├── bookings/            # Enrollments, attendance
│   ├── payments/            # Payment processing, reconciliation
│   ├── gamification/        # Badges, achievements, points, rewards
│   ├── blog/                # Blog posts, comments
│   ├── features/            # Feature routing, credits, subscriptions
│   └── requirements.txt
└── frontend/
    ├── app/                 # Next.js pages
    ├── components/          # React components
    ├── lib/                 # Utilities, API client
    └── package.json
```

## Setup Instructions

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd formations-casa/backend
   ```

2. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**:
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000`
- Admin panel: `http://localhost:8000/admin/`
- API documentation: `http://localhost:8000/api/docs/`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd formations-casa/frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.local.example .env.local
   ```
   Edit `.env.local` and set:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000/api
   ```

4. **Run development server**:
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:3000`

## Database Models

### Accounts App
- **User** - Extended user model with roles (user, coach, center, admin)
- **CoachProfile** - Coach-specific information (specializations, bank details)
- **TrainingCenterProfile** - Training center details

### Formations App
- **Category** - Formation categories (hierarchical)
- **FormationType** - Type of formation
- **Formation** - Main training course model
- **Curriculum** - Course syllabus/modules
- **FormationReview** - User reviews and ratings

### Centers App
- **TrainingCenter** - Physical training venues
- **Room** - Individual rooms with capacity and amenities
- **RoomImage** - Room photos
- **RoomAvailability** - Availability calendar
- **CenterReview** - Center reviews

### Bookings App
- **Booking** - Formation enrollments
- **BookingNotification** - Notification history
- **Attendance** - Attendance tracking

### Payments App
- **Payment** - Payment records with proof
- **PaymentInstruction** - Coach bank details
- **Reconciliation** - Payment reconciliation tracking

### Gamification App
- **Badge** - Earned badges (100s of different types)
- **UserBadge** - User-earned badges
- **Achievement** - Unlockable achievements
- **UserAchievement** - User achievements
- **PointsTransaction** - Points history
- **Leaderboard** - Rankings
- **Reward** - Redeemable rewards
- **RewardRedemption** - Reward purchases

### Features App
- **Feature** - Platform features with credit costs
- **FeatureUsage** - Usage tracking
- **CreditPurchase** - Credit purchases
- **Subscription** - Subscription plans

### Blog App
- **BlogCategory** - Blog categories
- **BlogPost** - Blog posts with WYSIWYG
- **BlogComment** - Comments with threading

## API Endpoints

### Authentication
- `POST /api/token/` - Get JWT token
- `POST /api/token/refresh/` - Refresh JWT token
- `POST /api/accounts/users/register/` - Register new user
- `GET /api/accounts/users/me/` - Get current user

### Formations
- `GET /api/formations/formations/` - List formations
- `POST /api/formations/formations/` - Create formation (coaches only)
- `GET /api/formations/formations/{slug}/` - Formation detail
- `GET /api/formations/categories/` - List categories

### Training Centers
- `GET /api/centers/centers/` - List centers
- `GET /api/centers/centers/{slug}/` - Center detail
- `GET /api/centers/rooms/` - List rooms

Full API documentation available at `/api/docs/`

## User Roles

### Regular User
- Browse and enroll in formations
- View training centers and coaches
- Earn badges and points
- Leave reviews

### Coach
- Create and manage formations
- Set up payment instructions
- View enrollments and reconcile payments
- Manage curriculum

### Training Center
- Add and manage rooms
- Set availability and pricing
- View bookings

### Admin
- Approve/reject users, coaches, centers
- Manage all content (WYSIWYG)
- Set feature costs and credits
- Manage gamification (badges, rewards)
- View all statistics

## Gamification System

- **100+ Badges**: Various categories (beginner, participation, achievement, social, expert, special)
- **Achievements**: Trigger-based unlocks (first formation, completion streaks, etc.)
- **Points System**: Earn points through activities
- **Leaderboards**: Weekly, monthly, yearly, all-time rankings
- **Rewards**: Redeem points for rewards

## Payment Flow

1. User enrolls in a formation
2. System sends booking confirmation with payment instructions
3. User transfers payment to coach's bank account
4. User uploads proof of payment
5. Coach/Admin verifies payment
6. Booking status updated to "payment received"
7. User gets access to formation materials

## Features & Credits System

All platform features can be gated behind a credit system:
- Admins can set credit costs for any feature (default: 0)
- Users can purchase credits
- Subscription plans provide monthly credits
- Feature usage is tracked

## Development

### Adding New Badges

1. Go to Django admin
2. Navigate to Gamification > Badges
3. Create new badge with criteria
4. Badge will be automatically awarded when criteria are met

### Customizing Features

1. Go to Django admin
2. Navigate to Features > Features
3. Add/edit features and set credit costs

## Production Deployment

### Backend
1. Set `DEBUG=False` in settings
2. Configure PostgreSQL database
3. Set up static file serving
4. Use gunicorn/uwsgi
5. Configure CORS for frontend domain
6. Set up SSL certificate

### Frontend
1. Build production bundle: `npm run build`
2. Deploy to Vercel/Netlify or serve with `npm start`
3. Set production API URL in environment variables

## Contributing

This is a comprehensive training marketplace platform. Key areas for contribution:
- Additional payment methods
- Email notifications
- SMS notifications (Morocco)
- Advanced search and filtering
- Mobile app
- Video conferencing integration
- Certificate generation

## License

Proprietary - All rights reserved

## Support

For support and questions:
- Email: support@formations.casa
- Website: https://formations.casa

---

**Built with ❤️ for the Casablanca training community**
