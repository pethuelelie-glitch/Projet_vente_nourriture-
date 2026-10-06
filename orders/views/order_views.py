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

        response_data = OrderSerializer(order).data
        
        # LOGIQUE DE PAIEMENT WAVE (API OFFICIELLE)
        from django.conf import settings
        import requests
        
        api_key = getattr(settings, 'WAVE_API_KEY', None)
        
        # Si la clé API n'est pas "vide" ou "mock"
        if api_key and api_key != "wave_sn_prod_...":
            wave_url = "https://api.wave.com/v1/checkout/sessions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            # L'API Wave nécessite un format précis
            wave_payload = {
                "amount": str(int(order.total)), 
                "currency": "XOF", # Devise (CFA)
                "client_reference": order.ref,
                "error_url": f"http://127.0.0.1:5500/?payment=error&ref={order.ref}",
                "success_url": f"http://127.0.0.1:5500/?payment=success&ref={order.ref}"
            }
            
            try:
                wave_response = requests.post(wave_url, json=wave_payload, headers=headers, timeout=30)
                wave_data = wave_response.json()
                if wave_response.status_code == 201 or wave_response.status_code == 200:
                    response_data['payment_url'] = wave_data.get('checkout_url', wave_data.get('wave_launch_url'))
                    # On enregistre l'ID de session Wave dans la commande pour vérification future
                    order.payment_id = wave_data.get('id')
                    order.save()
                else:
                    return Response({"error": "Erreur avec l'API Wave", "details": wave_data}, status=400)
            except Exception as e:
                return Response({"error": "Impossible de contacter Wave", "details": str(e)}, status=500)
        else:
            # Mode Mock si la clé API n'est pas encore mise
            payment_url = f"https://pay.wave.com/checkout/mock_session_{order.ref}"
            response_data['payment_url'] = payment_url
        
        # Lien pour le reçu PDF
        response_data['receipt_url'] = f"/api/v1/orders/{order.ref}/receipt/"

        return Response(response_data, status=status.HTTP_201_CREATED)
