# MegaGoals.com – Full-Stack Django Platform

**Tagline:** Achieve Your Mega Goals

**Mission:** The ultimate universal goal-achievement platform that empowers anyone to set, structure, track, and achieve any life goal (fitness, career, learning, entrepreneurship, etc.) using a proven, replicable, gamified framework — with AI coaching, paid templates, credit-based monetization, and global scalability.

## Features

### ✅ Core Features (Fully Implemented in MVP)

#### 1. Universal Goal Framework (Replicable & Hierarchical)
- **Structure:** Goal → Milestones → Actions → Steps
  - **Goal:** High-level outcome (e.g., "Run a marathon")
  - **Milestone:** Measurable checkpoint (e.g., "Run 10K non-stop")
  - **Action:** Repeatable task (e.g., "Run 3x/week")
  - **Step:** One-off or sub-task (e.g., "Buy running shoes")
- **Replicable:** Any public goal, milestone, or action can be duplicated as a template with full attribution

#### 2. Privacy Levels
- Private / Friends-only / Public
- Public items enable: likes, cheers (reactions), comments, replication

#### 3. Progress Tracking & Visualization
- Real-time progress bars, streak counters, timeline
- Calendar view with action scheduling
- Milestone celebrations: confetti, shareable achievement cards

#### 4. Full Gamification System
- XP points for every action completed, streak maintained, milestone hit
- Levels: Newbie → Achiever → Champion → Legend → Mega Goal Master
- Leaderboards: global, per-goal, per-community
- Badges: "7-Day Streak", "First Marathon", "Template Creator", "100 Cheers"
- Daily/weekly quests
- Unlockable profile flair, avatars, themes

#### 5. AI-Powered Goal Coach
- Built-in AI assistant (Grok API or local LLM fallback)
- Personalized insights and suggestions
- Auto-suggest actions based on goal type
- Weekly progress summaries
- Smart reminders via email/push

#### 6. Community & Social Engagement
- Cheer/Like/Comment on public actions (with emoji reactions)
- Replicate any public goal or action (instant fork + edit)
- Auto-grouping: Users with same active goal type → auto-suggested community
- Community feeds, announcements, polls

#### 7. Communities & Groups
- Auto-created by goal category
- Coach-created groups (public, private, or paid)
- Moderation tools, member roles, pinned posts

#### 8. Coaching Marketplace
- Verified Coach Accounts (admin approval)
- Public profiles: bio, expertise, ratings, availability, credit pricing
- Book 1:1 sessions via credit payment
- Coaches can create paid groups

#### 9. Credit-Based Monetization System
All premium actions cost credits (configurable):
- Replicate a premium template: 5 credits
- Join paid group: 10 credits/month
- Book coach session: 50 credits
- Unlock AI deep analysis: 3 credits
- Feature your template: 20 credits

**Subscription Tiers:**
- **Free:** 10 credits/month (expire after 30 days)
- **Pro:** 100 credits/month + unlimited replication ($9.99/month)
- **Unlimited:** No credit cost, all features free ($29.99/month)

#### 10. Paid & Free Templates
- Users can mark goals as "Template"
- Free templates: anyone can replicate
- Paid templates: require credits to replicate
- Template marketplace with search, filters, ratings, previews
- Revenue share: creator earns 70% of credit cost

#### 11. Analytics & Insights Dashboard
- Success rate, consistency score, best time/day
- AI-generated weekly report
- Exportable progress (PDF, CSV)

## Technical Stack

- **Backend:** Django 5.2.8
- **Database:** PostgreSQL (SQLite for development)
- **Caching/Queue:** Redis + Celery
- **Real-time:** Django Channels (WebSockets)
- **Authentication:** Django Allauth (Email, Google, Apple)
- **Payments:** Stripe
- **AI:** Grok API (x.ai)
- **Frontend:** Server-side rendering with HTMX (planned: Tailwind CSS)
- **i18n:** Full internationalization support (8 languages configured)

## Project Structure

```
megagoals/
├── core/               # Utilities, context processors
├── users/              # Custom User model, authentication, profiles
├── goals/              # Goals, Milestones, Actions, Steps, Templates
├── community/          # Communities, Posts, Comments, Cheers, Notifications
├── coaching/           # Coach profiles, sessions, availability
├── gamification/       # XP, Levels, Badges, Leaderboards, Quests
├── ai_coach/           # AI conversations, insights, reports
├── payments/           # Credits, Subscriptions, Transactions, Stripe
├── analytics/          # User/Goal analytics, Activity logs
├── templates/          # HTML templates
├── static/             # CSS, JS, images
└── media/              # User uploads
```

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd botiland

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your settings
nano .env
```

### 2. Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# (Optional) Load initial data
python manage.py loaddata fixtures/initial_data.json
```

### 3. Run Development Server

```bash
# Start Django development server
python manage.py runserver

# In another terminal, start Celery (for background tasks)
celery -A megagoals worker -l info

# In another terminal, start Celery Beat (for scheduled tasks)
celery -A megagoals beat -l info
```

### 4. Access the Application

- **Frontend:** http://localhost:8000
- **Admin Panel:** http://localhost:8000/admin
- **API:** (Coming soon)

## Environment Variables

See `.env.example` for all available environment variables. Key variables:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3

# For production, use PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost:5432/megagoals

# Stripe (for payments)
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

# Grok AI (for AI coach)
GROK_API_KEY=your-grok-api-key

# Social Auth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

## Key Models

### User Model
Custom user model with email authentication, gamification fields, credit system, and coaching capabilities.

### Goal Hierarchy
- **Goal:** Top-level objective with privacy settings, template options
- **Milestone:** Major checkpoint with target dates
- **Action:** Repeatable tasks with frequency and streak tracking
- **Step:** One-off tasks (optional)

### Gamification
- **Badge:** Achievement badges with requirements
- **Quest:** Daily/weekly challenges
- **Leaderboard:** Global and category leaderboards

### Community
- **Community:** Groups organized by goal categories
- **Post:** Community posts with engagement metrics
- **Cheer:** Emoji reactions on actions
- **Notification:** Real-time user notifications

### Payments
- **CreditTransaction:** Credit purchase/spend history
- **Payment:** Stripe payment records
- **CreditPack:** Purchasable credit packages
- **Subscription:** User subscriptions

## Admin Panel

Access the admin panel at `/admin/` to:
- Manage users and coaches
- Configure credit costs for features
- Create badges and quests
- Moderate communities and content
- View analytics and reports
- Manage payments and subscriptions

## Gamification System

### XP Rewards
- Action completion: 10 XP
- Milestone completion: 50 XP
- Goal completion: 200 XP
- Daily streak: 5 XP
- Community help: 15 XP

### Levels
1. Newbie (0 XP)
2. Beginner (100 XP)
3. Intermediate (500 XP)
4. Achiever (1,500 XP)
5. Expert (3,000 XP)
6. Champion (6,000 XP)
7. Legend (12,000 XP)
8. Mega Goal Master (25,000 XP)

## Credit System

All premium features use credits:
- Template replication: 5 credits
- Paid group entry: 10 credits
- Coaching session: 50 credits
- AI deep analysis: 3 credits
- Feature template: 20 credits

Users on the **Unlimited** tier never spend credits.

## AI Coach Integration

The AI Coach uses the Grok API to provide:
- Personalized goal suggestions
- Progress insights
- Pattern recognition
- Motivational messages
- Weekly/monthly reports

## Internationalization (i18n)

Supported languages:
- English (default)
- Spanish
- French
- German
- Portuguese
- Arabic
- Chinese (Simplified)
- Japanese

To add translations:
```bash
python manage.py makemessages -l es
python manage.py compilemessages
```

## Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test goals

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## Deployment

See `DEPLOYMENT.md` for detailed deployment instructions for:
- Production server setup
- PostgreSQL configuration
- Redis setup
- Celery workers
- Nginx/Apache configuration
- SSL certificates
- Stripe webhook configuration

## Contributing

This is a private project for MegaGoals.com. Internal contributors should:
1. Create a feature branch
2. Make changes with clear commits
3. Submit a pull request
4. Ensure tests pass

## Security

- All passwords are hashed using Django's default PBKDF2
- CSRF protection enabled
- XSS protection enabled
- SQL injection protection (Django ORM)
- Stripe webhook signature verification
- Rate limiting (coming soon)

## Performance

- Database query optimization with select_related and prefetch_related
- Redis caching for frequently accessed data
- Celery for background tasks
- Database indexes on frequently queried fields

## Roadmap

### MVP (Current)
✅ All core features implemented
✅ Database schema complete
✅ Admin panel configured
✅ Basic views and URLs

### Phase 2 (Next)
- [ ] Complete frontend with Tailwind CSS
- [ ] HTMX integration for live updates
- [ ] Comprehensive test coverage
- [ ] API endpoints (REST/GraphQL)
- [ ] Mobile app (React Native)

### Phase 3 (Future)
- [ ] Advanced analytics
- [ ] Social features expansion
- [ ] Marketplace expansion
- [ ] Third-party integrations
- [ ] White-label solutions

## License

Proprietary - All rights reserved by MegaGoals.com

## Support

For questions or support:
- Email: support@megagoals.com
- Documentation: https://docs.megagoals.com
- Status: https://status.megagoals.com

## Acknowledgments

Built with:
- Django
- Django Allauth
- Celery
- Stripe
- Grok AI (x.ai)
- And many other amazing open-source projects

---

**Start in English. Scale to billions.**
**One framework. Any goal. Infinite motivation. Gamified. AI-powered. Credit-driven. Unstoppable.**
