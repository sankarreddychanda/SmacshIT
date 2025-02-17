from django.contrib import admin

# Register your models here.
from django.contrib import admin
from cart.models import *
from products.models import *
from orders.models import *
admin.site.register(CustomUser)
admin.site.register(Wallet)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
