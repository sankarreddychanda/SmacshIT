from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import render

# @login_required
def product_list(request):
    categories = Category.objects.prefetch_related("products").all()  # Load categories with their products
    return render(request, "products/product_list.html", {"categories": categories})