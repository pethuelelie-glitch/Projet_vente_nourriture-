from rest_framework import serializers
from orders.models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'quantity', 'unit_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'ref',
            'customer_name',
            'customer_phone',
            'mode',
            'address',
            'delivery_date',
            'payment_method',
            'note',
            'total',
            'created_at',
            'items',
        ]
