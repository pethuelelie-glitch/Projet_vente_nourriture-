from rest_framework import generics
from rest_framework.permissions import AllowAny
from products.models import Product
from products.serializers import ProductSerializer

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
