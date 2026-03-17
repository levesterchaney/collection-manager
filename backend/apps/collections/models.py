from django.db import models
from django.conf import settings


class CollectionType(models.TextChoices):
    FIGURES = 'figures', 'Action Figures'
    CARDS = 'cards', 'Trading Cards'
    COMICS = 'comics', 'Comics'
    GAMES = 'games', 'Games'
    TOYS = 'toys', 'Toys'
    COINS = 'coins', 'Coins'
    STAMPS = 'stamps', 'Stamps'
    VINYL = 'vinyl', 'Vinyl Records'
    BOOKS = 'books', 'Books'
    OTHER = 'other', 'Other'


class ItemStatus(models.TextChoices):
    MINT = 'mint', 'Mint'
    NEAR_MINT = 'near_mint', 'Near Mint'
    EXCELLENT = 'excellent', 'Excellent'
    GOOD = 'good', 'Good'
    FAIR = 'fair', 'Fair'
    POOR = 'poor', 'Poor'
    DAMAGED = 'damaged', 'Damaged'


class Collection(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='collections'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    collection_type = models.CharField(
        max_length=20,
        choices=CollectionType.choices,
        default=CollectionType.OTHER
    )
    cover_image = models.ImageField(
        upload_to='collections/covers/',
        blank=True,
        null=True
    )
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'collections'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner.email} — {self.name}"

    @property
    def item_count(self):
        return self.items.count()

    @property
    def total_paid(self):
        return self.items.aggregate(
            total=models.Sum('price_paid')
        )['total'] or 0

    @property
    def total_value(self):
        return self.items.aggregate(
            total=models.Sum('current_value')
        )['total'] or 0


class CollectionItem(models.Model):
    collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE,
        related_name='items'
    )
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    price_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    current_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    manufacturer = models.CharField(max_length=255, blank=True)
    originating_property = models.CharField(max_length=255, blank=True)
    status = models.CharField(
        max_length=20,
        choices=ItemStatus.choices,
        default=ItemStatus.GOOD
    )
    image = models.ImageField(
        upload_to='collections/items/',
        blank=True,
        null=True
    )
    acquired_at = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'collection_items'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.collection.name})"
