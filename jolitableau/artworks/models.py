"""
Models for Artworks - JoliTableau
Handles artworks, provenance, categories, and AR features
"""

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class Category(models.Model):
    """Art categories/styles"""
    name_fr = models.CharField(_('nom (français)'), max_length=100)
    name_en = models.CharField(_('nom (anglais)'), max_length=100)
    name_es = models.CharField(_('nom (espagnol)'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    description = models.TextField(_('description'), blank=True)
    icon = models.CharField(_('icône'), max_length=50, blank=True)

    created_at = models.DateTimeField(_('créé le'), auto_now_add=True)

    class Meta:
        verbose_name = _('catégorie')
        verbose_name_plural = _('catégories')
        ordering = ['name_fr']

    def __str__(self):
        return self.name_fr

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en)
        super().save(*args, **kwargs)


class Artwork(models.Model):
    """
    Main artwork model - paintings, sculptures, photos, digital art, etc.
    """

    class Status(models.TextChoices):
        DRAFT = 'DRAFT', _('Brouillon')
        PUBLISHED = 'PUBLISHED', _('Publié')
        SOLD = 'SOLD', _('Vendu')
        ARCHIVED = 'ARCHIVED', _('Archivé')

    # Owner/Artist
    artist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='artworks',
        verbose_name=_('artiste')
    )

    # Basic Information
    title = models.CharField(_('titre'), max_length=300)
    slug = models.SlugField(_('slug'), max_length=350, unique=True)
    description_fr = models.TextField(_('description (français)'), blank=True)
    description_en = models.TextField(_('description (anglais)'), blank=True)
    description_es = models.TextField(_('description (espagnol)'), blank=True)

    # Classification
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='artworks',
        verbose_name=_('catégorie')
    )
    medium = models.CharField(_('médium'), max_length=200, help_text=_('Peinture à l\'huile, Sculpture bronze, etc.'))
    style = models.CharField(_('style'), max_length=100, blank=True)

    # Physical Properties
    width = models.DecimalField(_('largeur (cm)'), max_digits=8, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(_('hauteur (cm)'), max_digits=8, decimal_places=2, null=True, blank=True)
    depth = models.DecimalField(_('profondeur (cm)'), max_digits=8, decimal_places=2, null=True, blank=True)
    weight = models.DecimalField(_('poids (kg)'), max_digits=8, decimal_places=2, null=True, blank=True)

    # Date
    year_created = models.IntegerField(_('année de création'), null=True, blank=True)
    date_created = models.DateField(_('date de création'), null=True, blank=True)

    # Media Files
    main_image = models.ImageField(_('image principale'), upload_to='artworks/')
    image_2 = models.ImageField(_('image 2'), upload_to='artworks/', blank=True, null=True)
    image_3 = models.ImageField(_('image 3'), upload_to='artworks/', blank=True, null=True)
    image_4 = models.ImageField(_('image 4'), upload_to='artworks/', blank=True, null=True)
    video_360 = models.FileField(_('vidéo 360°'), upload_to='artworks/360/', blank=True, null=True)
    ar_model = models.FileField(_('modèle AR'), upload_to='artworks/ar/', blank=True, null=True)

    # Pricing
    is_for_sale = models.BooleanField(_('à vendre'), default=True)
    price = models.DecimalField(_('prix'), max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(_('devise'), max_length=3, default='EUR')
    price_on_request = models.BooleanField(_('prix sur demande'), default=False)

    # Auction
    is_auction = models.BooleanField(_('aux enchères'), default=False)
    starting_bid = models.DecimalField(_('enchère de départ'), max_digits=10, decimal_places=2, null=True, blank=True)

    # Edition (for prints, sculptures, etc.)
    is_unique = models.BooleanField(_('pièce unique'), default=True)
    edition_number = models.IntegerField(_('numéro d\'édition'), null=True, blank=True)
    edition_total = models.IntegerField(_('total édition'), null=True, blank=True)

    # Certificate & Authenticity
    has_certificate = models.BooleanField(_('certificat d\'authenticité'), default=False)
    certificate_number = models.CharField(_('numéro de certificat'), max_length=100, blank=True)
    is_signed = models.BooleanField(_('signé'), default=False)
    signature_location = models.CharField(_('emplacement signature'), max_length=100, blank=True)

    # Status & Visibility
    status = models.CharField(
        _('statut'),
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )
    is_featured = models.BooleanField(_('mis en avant'), default=False)
    featured_until = models.DateTimeField(_('mis en avant jusqu\'au'), null=True, blank=True)

    # SEO & Tags
    tags = models.CharField(_('tags'), max_length=500, blank=True, help_text=_('Séparés par des virgules'))
    meta_keywords = models.CharField(_('mots-clés meta'), max_length=300, blank=True)

    # Statistics
    view_count = models.IntegerField(_('nombre de vues'), default=0)
    favorite_count = models.IntegerField(_('favoris'), default=0)
    share_count = models.IntegerField(_('partages'), default=0)

    # Timestamps
    created_at = models.DateTimeField(_('créé le'), auto_now_add=True)
    updated_at = models.DateTimeField(_('mis à jour le'), auto_now=True)
    published_at = models.DateTimeField(_('publié le'), null=True, blank=True)
    sold_at = models.DateTimeField(_('vendu le'), null=True, blank=True)

    class Meta:
        verbose_name = _('œuvre')
        verbose_name_plural = _('œuvres')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['is_for_sale', 'price']),
        ]

    def __str__(self):
        return f"{self.title} - {self.artist.display_name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.artist.id}")
        super().save(*args, **kwargs)

    @property
    def dimensions_display(self):
        """Display dimensions in a readable format"""
        if self.width and self.height:
            if self.depth:
                return f"{self.width} x {self.height} x {self.depth} cm"
            return f"{self.width} x {self.height} cm"
        return ""

    @property
    def is_available(self):
        """Check if artwork is available for purchase"""
        return self.status == self.Status.PUBLISHED and self.is_for_sale


class ArtworkImage(models.Model):
    """Additional images for artworks"""
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(_('image'), upload_to='artworks/gallery/')
    caption = models.CharField(_('légende'), max_length=200, blank=True)
    order = models.IntegerField(_('ordre'), default=0)

    created_at = models.DateTimeField(_('créé le'), auto_now_add=True)

    class Meta:
        verbose_name = _('image d\'œuvre')
        verbose_name_plural = _('images d\'œuvre')
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.artwork.title}"


class Provenance(models.Model):
    """
    Artwork provenance/history - blockchain integration for authenticity
    """
    artwork = models.ForeignKey(
        Artwork,
        on_delete=models.CASCADE,
        related_name='provenance_records',
        verbose_name=_('œuvre')
    )

    # Event details
    event_date = models.DateField(_('date de l\'événement'))
    event_type = models.CharField(
        _('type d\'événement'),
        max_length=50,
        choices=[
            ('CREATION', _('Création')),
            ('ACQUISITION', _('Acquisition')),
            ('SALE', _('Vente')),
            ('EXHIBITION', _('Exposition')),
            ('RESTORATION', _('Restauration')),
            ('TRANSFER', _('Transfert')),
        ]
    )

    # Parties involved
    from_party = models.CharField(_('de'), max_length=200, blank=True)
    to_party = models.CharField(_('à'), max_length=200, blank=True)
    location = models.CharField(_('lieu'), max_length=200, blank=True)

    # Documentation
    description = models.TextField(_('description'), blank=True)
    documentation = models.FileField(_('documentation'), upload_to='provenance/docs/', blank=True, null=True)

    # Blockchain (NFT)
    blockchain_verified = models.BooleanField(_('vérifié blockchain'), default=False)
    transaction_hash = models.CharField(_('hash de transaction'), max_length=200, blank=True)
    nft_token_id = models.CharField(_('ID token NFT'), max_length=200, blank=True)

    # Timestamps
    created_at = models.DateTimeField(_('créé le'), auto_now_add=True)
    updated_at = models.DateTimeField(_('mis à jour le'), auto_now=True)

    class Meta:
        verbose_name = _('provenance')
        verbose_name_plural = _('provenances')
        ordering = ['-event_date']

    def __str__(self):
        return f"{self.artwork.title} - {self.event_type} ({self.event_date})"


class Favorite(models.Model):
    """User favorites for artworks"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name=_('utilisateur')
    )
    artwork = models.ForeignKey(
        Artwork,
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name=_('œuvre')
    )
    created_at = models.DateTimeField(_('créé le'), auto_now_add=True)

    class Meta:
        verbose_name = _('favori')
        verbose_name_plural = _('favoris')
        unique_together = ['user', 'artwork']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} ♥ {self.artwork.title}"
