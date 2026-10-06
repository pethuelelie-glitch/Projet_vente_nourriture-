from datetime import date
from django.db import models

class Order(models.Model):
    MODE_CHOICES = [
        ('Livraison', 'Livraison'),
        ('Retrait', 'Retrait'),
    ]
    PAYMENT_CHOICES = [
        ('Espèces', 'Espèces'),
        ('Mobile Money', 'Mobile Money'),
        ('Carte bancaire', 'Carte bancaire'),
        ('Wave', 'Wave'),
    ]

    ref = models.CharField(max_length=40, unique=True)
    customer_name = models.CharField(max_length=150)
    customer_phone = models.CharField(max_length=30)
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='Livraison')
    address = models.CharField(max_length=255, blank=True)
    delivery_date = models.DateField(default=date.today)
    payment_method = models.CharField(max_length=25, choices=PAYMENT_CHOICES, default='Mobile Money')
    note = models.TextField(blank=True)
    total = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.ref} - {self.customer_name}'
