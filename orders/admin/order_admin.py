from django.contrib import admin
from orders.models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('ref', 'customer_name', 'customer_phone', 'mode', 'total', 'created_at')
    list_filter = ('mode', 'payment_method', 'created_at')
    search_fields = ('ref', 'customer_name', 'customer_phone')
    inlines = [OrderItemInline]
