from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import Wallet
from .models import Cart, CartItem
from products.models import Product

# View Cart
# def view_cart(request):
#     cart, created = Cart.objects.get_or_create(user=request.user)
#     cart_items = CartItem.objects.filter(cart=cart)
#     return render(request, "cart/cart.html", {"cart_items": cart_items})

from django.contrib.auth.decorators import login_required


from decimal import Decimal

@login_required
def view_cart(request):
    # Get or create the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Fetch all the cart items associated with this cart
    cart_items = CartItem.objects.filter(cart=cart)

    # Calculate the total amount for the cart (convert to Decimal)
    total_amount = Decimal(sum(item.get_total_price() for item in cart_items))

    # Get the user's wallet balance (convert to Decimal)
    wallet_balance = (Wallet.objects.get(user=request.user))
    wallet_balance=Decimal(wallet_balance.balance)
    print("wallet_balance",wallet_balance,total_amount)

    return render(request, "cart/cart.html", {
        "cart_items": cart_items,
        "total_amount": total_amount,
        "wallet_balance": wallet_balance,
    })
# Add item to Cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if item already in cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect("cart")
