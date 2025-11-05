from django.db import models
from django.conf import settings


class Badge(models.Model):
    """Badges that users can earn"""

    CATEGORY_CHOICES = [
        ("beginner", "Beginner"),
        ("participation", "Participation"),
        ("achievement", "Achievement"),
        ("social", "Social"),
        ("expert", "Expert"),
        ("special", "Special Event"),
    ]

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    icon = models.CharField(max_length=50, help_text="Icon class or emoji")
    image = models.ImageField(upload_to="badges/", null=True, blank=True)

    # Criteria
    points_required = models.IntegerField(default=0)
    formations_completed_required = models.IntegerField(default=0)
    formations_created_required = models.IntegerField(default=0)
    reviews_given_required = models.IntegerField(default=0)

    # Badge properties
    points_reward = models.IntegerField(default=0)
    is_rare = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["category", "name"]

    def __str__(self):
        return self.name


class UserBadge(models.Model):
    """Badges earned by users"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="earned_badges"
    )
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name="earned_by")
    earned_at = models.DateTimeField(auto_now_add=True)
    is_displayed = models.BooleanField(default=True)

    class Meta:
        unique_together = ["user", "badge"]
        ordering = ["-earned_at"]

    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"


class Achievement(models.Model):
    """Specific achievements users can unlock"""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Icon class or emoji")
    points = models.IntegerField(default=10)
    is_active = models.BooleanField(default=True)

    # Trigger conditions
    trigger_type = models.CharField(
        max_length=50,
        choices=[
            ("first_formation", "First Formation Enrollment"),
            ("first_completion", "First Formation Completion"),
            ("first_review", "First Review Given"),
            ("create_formation", "Create First Formation"),
            ("complete_profile", "Complete Profile"),
            ("social_share", "Share on Social Media"),
            ("streak", "Learning Streak"),
            ("referral", "Refer a Friend"),
        ],
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    """Achievements unlocked by users"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="achievements"
    )
    achievement = models.ForeignKey(
        Achievement, on_delete=models.CASCADE, related_name="unlocked_by"
    )
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "achievement"]
        ordering = ["-unlocked_at"]

    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"


class PointsTransaction(models.Model):
    """Track points earned/spent by users"""

    TRANSACTION_TYPES = [
        ("earned", "Points Earned"),
        ("spent", "Points Spent"),
        ("purchased", "Points Purchased"),
        ("bonus", "Bonus Points"),
        ("penalty", "Points Penalty"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="points_transactions",
    )
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    points = models.IntegerField()
    description = models.TextField()

    # Optional references
    formation = models.ForeignKey(
        "formations.Formation",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="points_transactions",
    )
    badge = models.ForeignKey(Badge, on_delete=models.SET_NULL, null=True, blank=True)
    achievement = models.ForeignKey(
        Achievement, on_delete=models.SET_NULL, null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.points} pts"


class Leaderboard(models.Model):
    """Leaderboard rankings"""

    PERIOD_TYPES = [
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
        ("yearly", "Yearly"),
        ("all_time", "All Time"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="leaderboard_entries",
    )
    period_type = models.CharField(max_length=20, choices=PERIOD_TYPES)
    rank = models.IntegerField()
    total_points = models.IntegerField()

    period_start = models.DateField()
    period_end = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["period_type", "rank"]
        unique_together = ["user", "period_type", "period_start"]

    def __str__(self):
        return f"{self.user.username} - Rank #{self.rank} ({self.period_type})"


class Reward(models.Model):
    """Rewards that can be redeemed with points"""

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to="rewards/", null=True, blank=True)

    # Cost
    points_cost = models.IntegerField()

    # Availability
    is_active = models.BooleanField(default=True)
    quantity_available = models.IntegerField(
        null=True, blank=True, help_text="Null means unlimited"
    )
    quantity_redeemed = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["points_cost", "name"]

    def __str__(self):
        return f"{self.name} ({self.points_cost} pts)"


class RewardRedemption(models.Model):
    """Track reward redemptions"""

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("fulfilled", "Fulfilled"),
        ("rejected", "Rejected"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reward_redemptions",
    )
    reward = models.ForeignKey(
        Reward, on_delete=models.CASCADE, related_name="redemptions"
    )
    points_spent = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    # Fulfillment
    fulfilled_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.reward.name}"
