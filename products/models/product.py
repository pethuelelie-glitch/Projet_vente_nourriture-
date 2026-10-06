from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('attieke', 'Attiéké'),
        ('riz', 'Riz'),
        ('tradition', 'Tradition'),
        ('formule', 'Formule'),
        ('supplement', 'Supplément'),
    ]

    external_id = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=150)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    image = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f'{self.name} ({self.external_id})'
