from django.contrib.auth.decorators import login_required
from .models import Product
from django.shortcuts import render

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, "products/product_list.html", {"products": products})
