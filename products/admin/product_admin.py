from django.contrib import admin
from products.models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'name', 'category', 'price', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('external_id', 'name')
