from django.shortcuts import render, redirect
from accounts.models import Wallet
from cart.models import CartItem
from .models import Order, OrderItem
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.models import *
from orders.models import *
from decimal import Decimal
# Checkout Process
def checkout(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items)

    wallet = Wallet.objects.get(user=request.user)
    if wallet.deduct_money(total_price):  # Check if user has enough balance
        order = Order.objects.create(user=request.user, total_amount=total_price)

        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
            item.delete()  # Clear Cart

        return render(request, "orders/checkout_success.html", {"message": "Order placed successfully!"})
    else:
        return render(request, "orders/checkout_fail.html", {"message": "Insufficient balance!"})

# View Orders
def view_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "orders/orders.html", {"orders": orders})


from decimal import Decimal
from django.shortcuts import redirect, get_object_or_404
@login_required

def place_order(request):
    # Get the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Calculate the total amount in the cart
    total_amount = cart.get_total_amount()  # Ensure this method returns Decimal
    total_amount = Decimal(total_amount)

    # Get the user's wallet
    wallet = get_object_or_404(Wallet, user=request.user)

    # Check if the user has enough wallet balance
    if wallet.balance >= total_amount:
        # Deduct the amount from the wallet
        wallet.balance -= total_amount
        wallet.save()  # Save the updated wallet balance

        # Create a new order
        order = Order.objects.create(user=request.user, total_amount=total_amount, status="Pending")

        # Add items to the order
        for item in cart.items.all():
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)

        # Clear the cart after the order is placed
        cart.items.all().delete()

        return redirect('order_detail', order_id=order.id)
    else:
        # If the user doesn't have enough wallet balance
        return redirect('wallet')  # Redirect to the wallet page to add more money

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_detail.html', {'order': order})
