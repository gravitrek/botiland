# MegaGoals Platform Architecture

## Overview

MegaGoals is built on a modular Django architecture designed for scalability, maintainability, and global reach. The platform follows a hierarchical goal structure with full gamification, AI coaching, and credit-based monetization.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Users/Clients                         │
│              (Web, Mobile, API Clients)                      │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                    Load Balancer (Nginx)                     │
│                  SSL Termination, Static Files               │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                   Django Application Layer                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Core  │  Users  │  Goals  │  Community  │  Coaching │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │ Gamification │ AI Coach │ Payments │ Analytics        │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────┬───────────────────────────────────────────┘
                  │
        ┌─────────┴──────────┬──────────────┬────────────┐
        ▼                    ▼              ▼            ▼
┌──────────────┐    ┌──────────────┐  ┌─────────┐  ┌─────────┐
│  PostgreSQL  │    │    Redis     │  │ Celery  │  │ Stripe  │
│   Database   │    │    Cache     │  │ Workers │  │   API   │
└──────────────┘    └──────────────┘  └─────────┘  └─────────┘
        │                    │              │
        │                    │              │
        └────────────────────┴──────────────┴────────────┐
                                                          │
                                                          ▼
                                                    ┌──────────┐
                                                    │ Grok AI  │
                                                    │   API    │
                                                    └──────────┘
```

## Core Components

### 1. Django Applications

#### Core App
- **Purpose:** Central utilities, configuration, shared functionality
- **Key Files:**
  - `context_processors.py`: Site-wide template context
  - `utils.py`: Shared utility functions
  - `middleware.py`: Custom middleware

#### Users App
- **Purpose:** Authentication, user profiles, friendships
- **Key Models:**
  - `User`: Custom user model with email auth
  - `Friend`: Bidirectional friendships
  - `FriendRequest`: Friend request management
- **Features:**
  - Email/Google/Apple authentication
  - Gamification fields (XP, level, streaks)
  - Credit system
  - Coach profiles

#### Goals App
- **Purpose:** Core goal management and hierarchy
- **Key Models:**
  - `Goal`: Top-level goals with templates
  - `Milestone`: Major checkpoints
  - `Action`: Repeatable tasks
  - `Step`: One-off tasks
  - `GoalLike`: Social engagement
- **Features:**
  - Hierarchical structure
  - Privacy controls
  - Template marketplace
  - Progress tracking
  - Replication system

#### Community App
- **Purpose:** Social features and community engagement
- **Key Models:**
  - `Community`: Groups and communities
  - `Post`: Community posts
  - `Comment`: Comments on posts/goals
  - `Cheer`: Emoji reactions
  - `Notification`: Real-time notifications
- **Features:**
  - Auto-created communities by category
  - Paid communities
  - Moderation tools
  - Social feed

#### Gamification App
- **Purpose:** XP, levels, badges, quests, leaderboards
- **Key Models:**
  - `Badge`: Achievement badges
  - `UserBadge`: User badge awards
  - `Quest`: Daily/weekly quests
  - `Leaderboard`: Ranking systems
- **Features:**
  - 8-level progression system
  - Dynamic badge awards
  - Multiple leaderboard types
  - Quest tracking

#### AI Coach App
- **Purpose:** AI-powered guidance and insights
- **Key Models:**
  - `AICoachConversation`: Chat sessions
  - `AICoachMessage`: Individual messages
  - `AIInsight`: AI-generated insights
  - `AIReport`: Weekly/monthly reports
- **Features:**
  - Grok API integration
  - Personalized suggestions
  - Pattern recognition
  - Progress analysis

#### Payments App
- **Purpose:** Credit system and subscription management
- **Key Models:**
  - `CreditTransaction`: Credit history
  - `Payment`: Stripe payments
  - `CreditPack`: Purchasable packages
  - `Subscription`: Subscription management
- **Features:**
  - Stripe integration
  - Credit expiry tracking
  - Subscription tiers
  - Revenue sharing (70/30)

#### Coaching App
- **Purpose:** Coaching marketplace and sessions
- **Key Models:**
  - `CoachingSession`: Booking management
  - `CoachAvailability`: Coach schedules
- **Features:**
  - Coach verification
  - Session booking
  - Credit-based payment
  - Rating system

#### Analytics App
- **Purpose:** User and goal analytics
- **Key Models:**
  - `UserAnalytics`: User statistics
  - `GoalAnalytics`: Goal metrics
  - `ActivityLog`: Event tracking
- **Features:**
  - Progress tracking
  - Pattern analysis
  - Consistency scoring
  - Exportable reports

## Data Flow

### 1. Goal Creation Flow
```
User → Create Goal Form → Goal Model →
  → Save to Database →
  → Create Analytics Record →
  → Auto-create Community (if new category) →
  → Activity Log
```

### 2. Action Completion Flow
```
User → Complete Action → Action.mark_complete_today() →
  → Award XP →
  → Update Streak →
  → Update User Level (if threshold reached) →
  → Award Badge (if requirement met) →
  → Update Goal Progress →
  → Trigger AI Insight (Celery task) →
  → Create Notification (if milestone reached) →
  → Activity Log
```

### 3. Template Replication Flow
```
User → Browse Templates → Select Template →
  → Check Credits (if premium) →
  → Deduct Credits →
  → Deep Copy Goal (with all children) →
  → Set original_goal reference →
  → Increment template_downloads →
  → Award Creator Revenue (if premium) →
  → Notify Creator →
  → Activity Log
```

### 4. Payment Flow
```
User → Select Credit Pack → Stripe Checkout →
  → Webhook → Payment Model →
  → Add Credits to User →
  → Create CreditTransaction →
  → Send Confirmation Email →
  → Activity Log
```

## Database Design

### Key Relationships

```
User (1) ──── (M) Goal
Goal (1) ──── (M) Milestone
Milestone (1) ──── (M) Action
Action (1) ──── (M) Step
Goal (1) ──── (M) GoalLike
Action (1) ──── (M) Cheer
User (M) ──── (M) Community (through CommunityMembership)
User (1) ──── (M) Badge (through UserBadge)
Goal (1) ──── (1) GoalAnalytics
User (1) ──── (1) UserAnalytics
```

### Indexes
- `goals.Goal`: (user, completed), (is_template, privacy), (category)
- `analytics.ActivityLog`: (user, -timestamp), (activity_type, -timestamp)
- Custom indexes on frequently queried fields

## Caching Strategy

### Redis Caching
1. **User Sessions:** Django session storage
2. **Leaderboards:** Cached for 5 minutes
3. **Template Marketplace:** Cached for 15 minutes
4. **User Profile:** Cached for 10 minutes
5. **Community Feeds:** Cached for 2 minutes

### Cache Invalidation
- On user action completion → Invalidate leaderboards
- On goal update → Invalidate user profile
- On post creation → Invalidate community feed

## Background Tasks (Celery)

### Periodic Tasks (Celery Beat)
1. **Daily:**
   - Reset daily quests
   - Check streak continuity
   - Generate daily AI insights
   - Expire old credits

2. **Weekly:**
   - Generate weekly reports
   - Award weekly badges
   - Clean up old notifications
   - Update leaderboards

3. **Monthly:**
   - Grant subscription credits
   - Generate monthly analytics
   - Archive old data

### Async Tasks
1. **On Action Completion:**
   - Generate AI insights
   - Check badge requirements
   - Update analytics

2. **On Payment:**
   - Process Stripe webhooks
   - Send confirmation emails
   - Update subscription status

## Security Architecture

### Authentication
- Email-based authentication (Django Allauth)
- Social OAuth (Google, Apple)
- Email verification required
- Password hashing (PBKDF2)

### Authorization
- Django's built-in permission system
- django-guardian for object-level permissions
- Custom permission checks in views

### API Security
- CSRF protection for forms
- Rate limiting (coming soon)
- Stripe webhook signature verification
- Environment-based secrets

### Data Protection
- User data privacy controls
- GDPR-compliant data export
- Secure payment processing (Stripe)
- No credit card storage

## Scalability Considerations

### Horizontal Scaling
- Stateless Django application servers
- Redis for shared session storage
- Celery workers can be scaled independently
- PostgreSQL read replicas for analytics

### Performance Optimization
- Database query optimization (select_related, prefetch_related)
- Lazy loading of related objects
- Pagination for large lists
- CDN for static assets (production)

### Monitoring
- Django logging framework
- Error tracking (Sentry integration ready)
- Performance monitoring (New Relic ready)
- Database query analysis

## Internationalization (i18n)

### Language Support
- 8 languages configured (EN, ES, FR, DE, PT, AR, ZH, JA)
- Django's i18n framework
- LocaleMiddleware for language detection
- Translation files in `locale/` directory

### Implementation
- All user-facing strings wrapped in `gettext_lazy()`
- URL patterns use `i18n_patterns`
- Language switcher in UI
- User language preference stored

## API Architecture (Coming Soon)

### REST API
- Django REST Framework
- Token authentication
- Versioned endpoints (/api/v1/)
- Rate limiting per user tier

### GraphQL API
- Graphene-Django
- Single endpoint with flexible queries
- Real-time subscriptions (for pro users)

### WebSockets
- Django Channels
- Real-time notifications
- Live leaderboard updates
- Chat functionality

## Deployment Architecture

### Development
- SQLite database
- Django dev server
- Console email backend
- Debug toolbar enabled

### Staging
- PostgreSQL database
- Gunicorn WSGI server
- Redis cache
- Celery workers
- Email via SendGrid

### Production
- Multi-server setup
- Load balancer (Nginx)
- PostgreSQL with replication
- Redis cluster
- Celery workers with autoscaling
- CDN for static files
- SSL/TLS encryption
- Monitoring and alerts

## Future Enhancements

1. **Microservices:** Split AI Coach into separate service
2. **GraphQL:** Full GraphQL API for mobile apps
3. **Real-time:** WebSocket support for live updates
4. **CDN:** CloudFront for global static asset delivery
5. **Elasticsearch:** Full-text search for goals and templates
6. **Machine Learning:** On-premise ML models for insights
7. **Mobile Apps:** React Native iOS/Android apps
8. **White-label:** Multi-tenant architecture for partners

## Technology Decisions

### Why Django?
- Mature ORM with excellent PostgreSQL support
- Built-in admin panel for content management
- Strong security defaults
- Excellent i18n support
- Large ecosystem of packages

### Why PostgreSQL?
- ACID compliance
- JSON field support
- Full-text search
- Scalability and performance
- Industry standard

### Why Celery?
- Distributed task queue
- Periodic task scheduling
- Robust error handling
- Scalable worker pool

### Why Redis?
- Fast in-memory caching
- Pub/sub for real-time features
- Celery broker support
- Session storage

### Why Stripe?
- Industry-leading payment processing
- Excellent documentation
- Subscription management
- Global currency support

---

This architecture is designed for global scale while maintaining code quality, security, and developer productivity.
