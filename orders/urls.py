from django.urls import path
from .views import OrderCreateView, OrderReceiptView

urlpatterns = [
    path('', OrderCreateView.as_view(), name='orders-create'),
    path('<int:pk>/receipt/', OrderReceiptView.as_view(), name='order-receipt'),
]
