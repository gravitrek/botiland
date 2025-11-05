"""
Models for the Users app - JoliTableau
Handles user profiles, artists, galleries, collectors, and roles
"""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import URLValidator


class UserProfileManager(BaseUserManager):
    """Custom user manager for email-based authentication"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('L\'adresse email est obligatoire'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class UserProfile(AbstractUser):
    """
    Custom User Model for JoliTableau
    Supports artists, galleries, collectors, and regular users
    """

    class UserType(models.TextChoices):
        ARTIST = 'ARTIST', _('Artiste')
        GALLERY = 'GALLERY', _('Galerie')
        COLLECTOR = 'COLLECTOR', _('Collectionneur')
        USER = 'USER', _('Utilisateur')
        ADMIN = 'ADMIN', _('Administrateur')

    username = None  # Remove username field
    email = models.EmailField(_('adresse email'), unique=True)
    user_type = models.CharField(
        _('type d\'utilisateur'),
        max_length=20,
        choices=UserType.choices,
        default=UserType.USER
    )

    # Profile Information
    full_name = models.CharField(_('nom complet'), max_length=200, blank=True)
    bio = models.TextField(_('biographie'), blank=True)
    profile_picture = models.ImageField(
        _('photo de profil'),
        upload_to='profiles/',
        blank=True,
        null=True
    )
    cover_image = models.ImageField(
        _('image de couverture'),
        upload_to='covers/',
        blank=True,
        null=True
    )

    # Contact Information
    phone = models.CharField(_('téléphone'), max_length=20, blank=True)
    website = models.URLField(_('site web'), blank=True, validators=[URLValidator()])
    address = models.CharField(_('adresse'), max_length=300, blank=True)
    city = models.CharField(_('ville'), max_length=100, blank=True)
    country = models.CharField(_('pays'), max_length=100, default='France')
    postal_code = models.CharField(_('code postal'), max_length=20, blank=True)

    # Social Media
    instagram_url = models.URLField(_('Instagram'), blank=True)
    facebook_url = models.URLField(_('Facebook'), blank=True)
    twitter_url = models.URLField(_('Twitter/X'), blank=True)
    linkedin_url = models.URLField(_('LinkedIn'), blank=True)

    # Language Preference
    preferred_language = models.CharField(
        _('langue préférée'),
        max_length=5,
        choices=[('fr', 'Français'), ('en', 'English'), ('es', 'Español')],
        default='fr'
    )

    # Verification Status
    is_verified = models.BooleanField(_('vérifié'), default=False)
    verification_date = models.DateTimeField(_('date de vérification'), null=True, blank=True)
    verification_method = models.CharField(
        _('méthode de vérification'),
        max_length=100,
        blank=True
    )

    # Conseil des Sages
    is_sage = models.BooleanField(_('membre du Conseil des Sages'), default=False)
    sage_since = models.DateTimeField(_('sage depuis'), null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(_('créé le'), auto_now_add=True)
    updated_at = models.DateTimeField(_('mis à jour le'), auto_now=True)
    last_login_ip = models.GenericIPAddressField(_('dernière IP de connexion'), null=True, blank=True)

    # Newsletter & Communication
    newsletter_subscribed = models.BooleanField(_('abonné à la newsletter'), default=True)
    whatsapp_optin = models.BooleanField(_('opt-in WhatsApp'), default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('profil utilisateur')
        verbose_name_plural = _('profils utilisateurs')
        ordering = ['-created_at']

    def __str__(self):
        return self.email

    @property
    def display_name(self):
        """Return the best available name for display"""
        return self.full_name or self.email.split('@')[0]

    def promote_to_sage(self):
        """Promote user to Conseil des Sages"""
        self.is_sage = True
        self.sage_since = timezone.now()
        self.save(update_fields=['is_sage', 'sage_since'])

    def verify_account(self, method='manual'):
        """Mark account as verified"""
        self.is_verified = True
        self.verification_date = timezone.now()
        self.verification_method = method
        self.save(update_fields=['is_verified', 'verification_date', 'verification_method'])


class ArtistProfile(models.Model):
    """
    Extended profile for artists
    Contains artist-specific information
    """

    user = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='artist_profile',
        verbose_name=_('utilisateur')
    )

    # Artist Information
    artist_name = models.CharField(_('nom d\'artiste'), max_length=200)
    artist_statement = models.TextField(_('déclaration artistique'), blank=True)
    artistic_style = models.CharField(_('style artistique'), max_length=100, blank=True)
    medium = models.CharField(_('médium'), max_length=200, blank=True, help_text=_('Peinture, Sculpture, Photo, etc.'))

    # Professional Info
    birth_year = models.IntegerField(_('année de naissance'), null=True, blank=True)
    education = models.TextField(_('formation'), blank=True)
    awards = models.TextField(_('prix et distinctions'), blank=True)
    exhibitions = models.TextField(_('expositions'), blank=True)

    # Maison des Artistes / Professional Registration
    maison_artistes_number = models.CharField(
        _('numéro Maison des Artistes'),
        max_length=50,
        blank=True
    )
    siret = models.CharField(_('numéro SIRET'), max_length=14, blank=True)

    # Art Market Presence
    represented_by_gallery = models.BooleanField(_('représenté par une galerie'), default=False)
    gallery_representation = models.TextField(_('représentation par galeries'), blank=True)

    # Featured Status
    is_featured = models.BooleanField(_('artiste mis en avant'), default=False)
    featured_since = models.DateTimeField(_('mis en avant depuis'), null=True, blank=True)

    created_at = models.DateTimeField(_('créé le'), auto_now_add=True)
    updated_at = models.DateTimeField(_('mis à jour le'), auto_now=True)

    class Meta:
        verbose_name = _('profil artiste')
        verbose_name_plural = _('profils artistes')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.artist_name} ({self.user.email})"


class GalleryProfile(models.Model):
    """
    Extended profile for galleries
    Contains gallery-specific information
    """

    user = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='gallery_profile',
        verbose_name=_('utilisateur')
    )

    # Gallery Information
    gallery_name = models.CharField(_('nom de la galerie'), max_length=200)
    description = models.TextField(_('description'), blank=True)
    founding_year = models.IntegerField(_('année de fondation'), null=True, blank=True)

    # Professional Registration
    siret = models.CharField(_('numéro SIRET'), max_length=14, blank=True)
    vat_number = models.CharField(_('numéro TVA'), max_length=20, blank=True)

    # CCI Partnership
    cci_member = models.BooleanField(_('membre CCI'), default=False)
    cci_number = models.CharField(_('numéro CCI'), max_length=50, blank=True)

    # Physical Location
    has_physical_location = models.BooleanField(_('emplacement physique'), default=True)
    opening_hours = models.TextField(_('horaires d\'ouverture'), blank=True)

    # Specialization
    specialization = models.CharField(_('spécialisation'), max_length=200, blank=True)
    represented_artists_count = models.IntegerField(_('nombre d\'artistes représentés'), default=0)

    # Featured Status
    is_featured = models.BooleanField(_('galerie mise en avant'), default=False)
    featured_since = models.DateTimeField(_('mise en avant depuis'), null=True, blank=True)

    created_at = models.DateTimeField(_('créé le'), auto_now_add=True)
    updated_at = models.DateTimeField(_('mis à jour le'), auto_now=True)

    class Meta:
        verbose_name = _('profil galerie')
        verbose_name_plural = _('profils galeries')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.gallery_name} ({self.user.email})"


class CollectorProfile(models.Model):
    """
    Extended profile for art collectors
    """

    user = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='collector_profile',
        verbose_name=_('utilisateur')
    )

    # Collector Information
    collector_name = models.CharField(_('nom du collectionneur'), max_length=200, blank=True)
    collection_focus = models.TextField(_('focus de la collection'), blank=True)
    collecting_since = models.IntegerField(_('collectionne depuis'), null=True, blank=True)

    # Preferences
    preferred_styles = models.CharField(_('styles préférés'), max_length=300, blank=True)
    budget_range = models.CharField(_('gamme de budget'), max_length=100, blank=True)

    # Privacy
    public_collection = models.BooleanField(_('collection publique'), default=False)
    show_purchases = models.BooleanField(_('afficher les achats'), default=False)

    created_at = models.DateTimeField(_('créé le'), auto_now_add=True)
    updated_at = models.DateTimeField(_('mis à jour le'), auto_now=True)

    class Meta:
        verbose_name = _('profil collectionneur')
        verbose_name_plural = _('profils collectionneurs')
        ordering = ['-created_at']

    def __str__(self):
        return f"Collector: {self.user.email}"


class Follow(models.Model):
    """
    Follow relationship between users
    Allows users to follow artists, galleries, collectors
    """

    follower = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name=_('abonné')
    )
    following = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name=_('suivi')
    )
    created_at = models.DateTimeField(_('créé le'), auto_now_add=True)

    class Meta:
        verbose_name = _('abonnement')
        verbose_name_plural = _('abonnements')
        unique_together = ['follower', 'following']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.follower.display_name} suit {self.following.display_name}"
