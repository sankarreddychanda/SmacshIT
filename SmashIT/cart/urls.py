from django.urls import path
from .views import add_to_cart, view_cart

urlpatterns = [
    path("cart/", view_cart, name="cart"),
    path("cart/add/<int:product_id>/", add_to_cart, name="add_to_cart"),
]
