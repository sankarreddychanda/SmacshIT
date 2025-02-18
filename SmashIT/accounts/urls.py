from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('login/', login_view, name='login'),  # Login page
    path('register/', register, name='register'),  # Registration page
    path('logout/', logout_view, name='logout'),  # Logout page

    # Wallet-related URLs
    path('wallet/', wallet_view, name='wallet'),  # Wallet overview
    path('wallet/add/', add_money, name='add_money'),  # Add money to wallet

    # Orders
    path('orders/', orders_view, name='orders'),  # View orders

    # User Profile (Optional)
    path('profile/', profile_view, name='profile'),  # User profile page
]
