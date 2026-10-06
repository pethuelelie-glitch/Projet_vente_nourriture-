from rest_framework import serializers
from products.models import Product

class ProductSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'external_id', 'name', 'category', 'description', 'price', 'image']

    def get_id(self, obj):
        return obj.external_id
