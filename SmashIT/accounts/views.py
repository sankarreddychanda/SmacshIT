from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, Wallet
from .forms import CustomUserCreationForm

# User Registration View
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create wallet for new user
            Wallet.objects.create(user=user)
            login(request, user)
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})

# User Login View
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})

# User Logout View
def logout_view(request):
    logout(request)
    return redirect("home")

# Wallet View
def wallet_view(request):
    if not hasattr(request.user, 'wallet'):
        Wallet.objects.create(user=request.user)  # Create wallet if not exist
    wallet = Wallet.objects.get(user=request.user)
    return render(request, "accounts/wallet.html", {"wallet": wallet})
from decimal import Decimal
# Add Money to Wallet
def add_money(request):
    if not hasattr(request.user, 'wallet'):
        Wallet.objects.create(user=request.user)  # Create wallet if not exist

    if request.method == "POST":
        # Convert the amount to Decimal
        amount = Decimal(request.POST.get("amount"))

        # Get the user's wallet
        wallet = Wallet.objects.get(user=request.user)

        # Add money to wallet
        wallet.balance += amount  # Ensure both are Decimal type

        # Save the wallet
        wallet.save()

        return redirect("wallet")

    return render(request, "accounts/add_money.html")
# Orders View
def orders_view(request):
    orders = request.user.orders.all()  # Assuming a related name for user's orders
    return render(request, "accounts/orders.html", {"orders": orders})

# Profile View (Optional)
def profile_view(request):
    return render(request, "accounts/profile.html")
