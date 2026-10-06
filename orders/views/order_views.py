from datetime import date
from django.db import IntegrityError
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from orders.models import Order, OrderItem
from products.models import Product
from orders.serializers import OrderSerializer

class OrderCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        payload = request.data
        customer = payload.get('customer') or {}

        ref = payload.get('ref') or f"GN-{date.today().strftime('%Y%m%d')}-{len(Order.objects.filter(created_at__date=date.today())) + 1:03d}"
        customer_name = (customer.get('name') or '').strip()
        customer_phone = (customer.get('phone') or '').strip()
        mode = customer.get('mode') or payload.get('mode') or 'Livraison'
        address = (customer.get('address') or '').strip()
        note = (customer.get('note') or '').strip()
        payment_method = customer.get('payment') or payload.get('payment_method') or 'Mobile Money'
        total = payload.get('total') or 0

        if not customer_name or not customer_phone:
            return Response({'error': 'Le nom et le téléphone du client sont obligatoires.'}, status=status.HTTP_400_BAD_REQUEST)

        delivery_raw = customer.get('date') or payload.get('createdAt')
        if delivery_raw:
            delivery_value = delivery_raw.split('T', 1)[0]
            try:
                delivery_date = date.fromisoformat(delivery_value)
            except ValueError:
                return Response({'error': 'La date de commande est invalide.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            delivery_date = date.today()

        items_payload = payload.get('items') or []
        if not isinstance(items_payload, list) or not items_payload:
            return Response({'error': 'Une commande doit contenir au moins un article.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.objects.create(
                ref=ref,
                customer_name=customer_name,
                customer_phone=customer_phone,
                mode=mode,
                address=address,
                delivery_date=delivery_date,
                payment_method=payment_method,
                note=note,
                total=total,
            )
        except IntegrityError:
            return Response({'error': 'La référence de commande existe déjà.'}, status=status.HTTP_400_BAD_REQUEST)

        for item in items_payload:
            product_id = item.get('id')
            product = Product.objects.filter(external_id=product_id).first() if product_id else None
            item_name = item.get('name') or (product.name if product else 'Produit')
            qty = int(item.get('qty') or item.get('quantity') or 1)
            unit_price = item.get('unitPrice') or item.get('unit_price') or (product.price if product else 0)
            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=item_name,
                quantity=qty,
                unit_price=unit_price,
            )

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
