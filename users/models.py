"""
User models for MegaGoals platform.
"""

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user."""
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model for MegaGoals platform."""

    SUBSCRIPTION_TIERS = (
        ('free', _('Free')),
        ('pro', _('Pro')),
        ('unlimited', _('Unlimited')),
    )

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    # Profile fields
    bio = models.TextField(_('bio'), blank=True)
    avatar = models.ImageField(_('avatar'), upload_to='avatars/', blank=True, null=True)
    location = models.CharField(_('location'), max_length=100, blank=True)
    website = models.URLField(_('website'), blank=True)

    # Gamification fields
    xp = models.BigIntegerField(_('experience points'), default=0)
    level = models.PositiveIntegerField(_('level'), default=1)
    current_streak = models.PositiveIntegerField(_('current streak'), default=0)
    longest_streak = models.PositiveIntegerField(_('longest streak'), default=0)
    last_activity_date = models.DateField(_('last activity date'), null=True, blank=True)

    # Credit system
    credits = models.IntegerField(_('credits'), default=10)
    credits_expiry = models.DateTimeField(_('credits expiry'), default=timezone.now)
    total_credits_earned = models.BigIntegerField(_('total credits earned'), default=10)
    total_credits_spent = models.BigIntegerField(_('total credits spent'), default=0)

    # Subscription
    subscription_tier = models.CharField(
        _('subscription tier'),
        max_length=20,
        choices=SUBSCRIPTION_TIERS,
        default='free'
    )
    subscription_start_date = models.DateTimeField(_('subscription start date'), null=True, blank=True)
    subscription_end_date = models.DateTimeField(_('subscription end date'), null=True, blank=True)
    stripe_customer_id = models.CharField(_('Stripe customer ID'), max_length=255, blank=True)
    stripe_subscription_id = models.CharField(_('Stripe subscription ID'), max_length=255, blank=True)

    # Coaching
    is_coach = models.BooleanField(_('is coach'), default=False)
    verified_coach = models.BooleanField(_('verified coach'), default=False)
    coach_bio = models.TextField(_('coach bio'), blank=True)
    coach_expertise = models.JSONField(_('coach expertise'), default=list)
    coach_hourly_rate_credits = models.PositiveIntegerField(_('coach hourly rate (credits)'), default=50)
    coach_rating = models.DecimalField(_('coach rating'), max_digits=3, decimal_places=2, default=0.00)
    coach_total_sessions = models.PositiveIntegerField(_('total coaching sessions'), default=0)

    # Account status
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    email_verified = models.BooleanField(_('email verified'), default=False)

    # Preferences
    language = models.CharField(_('language'), max_length=10, default='en')
    timezone_name = models.CharField(_('timezone'), max_length=50, default='UTC')
    email_notifications = models.BooleanField(_('email notifications'), default=True)
    push_notifications = models.BooleanField(_('push notifications'), default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-date_joined']

    def __str__(self):
        return self.email

    def get_full_name(self):
        """Return the user's full name."""
        return f'{self.first_name} {self.last_name}'.strip() or self.email

    def get_short_name(self):
        """Return the user's short name."""
        return self.first_name or self.email.split('@')[0]

    def add_xp(self, amount):
        """Add XP and check for level up."""
        from django.conf import settings

        self.xp += amount

        # Check for level up
        for level_data in reversed(settings.LEVELS):
            if self.xp >= level_data['xp_required']:
                if level_data['level'] > self.level:
                    self.level = level_data['level']
                break

        self.save(update_fields=['xp', 'level'])
        return self.level

    def add_credits(self, amount, reason=''):
        """Add credits to user account."""
        from payments.models import CreditTransaction

        self.credits += amount
        self.total_credits_earned += amount if amount > 0 else 0
        self.save(update_fields=['credits', 'total_credits_earned'])

        # Log transaction
        CreditTransaction.objects.create(
            user=self,
            credits=amount,
            reason=reason
        )

        return self.credits

    def spend_credits(self, amount, reason=''):
        """Deduct credits from user account."""
        if self.subscription_tier == 'unlimited':
            return True  # Unlimited tier doesn't spend credits

        if self.credits < amount:
            return False

        from payments.models import CreditTransaction

        self.credits -= amount
        self.total_credits_spent += amount
        self.save(update_fields=['credits', 'total_credits_spent'])

        # Log transaction
        CreditTransaction.objects.create(
            user=self,
            credits=-amount,
            reason=reason
        )

        return True

    def update_streak(self):
        """Update user's streak based on activity."""
        today = timezone.now().date()

        if self.last_activity_date is None:
            self.current_streak = 1
            self.longest_streak = max(self.longest_streak, 1)
        elif self.last_activity_date == today:
            # Already logged today
            return self.current_streak
        elif self.last_activity_date == today - timezone.timedelta(days=1):
            # Continuing streak
            self.current_streak += 1
            self.longest_streak = max(self.longest_streak, self.current_streak)
        else:
            # Streak broken
            self.current_streak = 1

        self.last_activity_date = today
        self.save(update_fields=['current_streak', 'longest_streak', 'last_activity_date'])

        return self.current_streak


class Friend(models.Model):
    """Friend relationship between users."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_of')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('friend')
        verbose_name_plural = _('friends')
        unique_together = ('user', 'friend')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} - {self.friend}'


class FriendRequest(models.Model):
    """Friend request model."""

    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('accepted', _('Accepted')),
        ('rejected', _('Rejected')),
    )

    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_friend_requests')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_friend_requests')
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('friend request')
        verbose_name_plural = _('friend requests')
        unique_together = ('from_user', 'to_user')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.from_user} -> {self.to_user} ({self.status})'

    def accept(self):
        """Accept the friend request."""
        self.status = 'accepted'
        self.save()

        # Create bidirectional friendship
        Friend.objects.get_or_create(user=self.from_user, friend=self.to_user)
        Friend.objects.get_or_create(user=self.to_user, friend=self.from_user)

    def reject(self):
        """Reject the friend request."""
        self.status = 'rejected'
        self.save()
