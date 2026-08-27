from django.db import models


class Catalogue(models.Model):
    class CategoryGroup(models.TextChoices):
        RESIDENTIAL = 'residential', 'Residential'
        COMMERCIAL = 'commercial', 'Commercial'

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    category_group = models.CharField(
        max_length=20,
        choices=CategoryGroup.choices,
        blank=True,
        default='',
    )
    description = models.TextField(blank=True)
    designs = models.ImageField(upload_to='avatars/', blank=True, null=True)
    price = models.DecimalField(max_digits=19, decimal_places=4)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    seller = models.ForeignKey(
        'users.SellerProfile',
        on_delete=models.CASCADE,
        related_name='catalogues',
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.category})"
