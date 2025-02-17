from django.urls import path
from .views import *

urlpatterns = [
    path("checkout/", checkout, name="checkout"),
    path("orders/", view_orders, name="orders"),
path('place-order/', place_order, name='place_order'),
    path('order/<int:order_id>/', order_detail, name='order_detail'),
]
