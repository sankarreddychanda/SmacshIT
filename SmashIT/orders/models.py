from django.db import models

# Create your models here.
from django.db import models
from accounts.models import CustomUser, Wallet
from products.models import Product

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status_choices = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    ]
    status = models.CharField(max_length=15, choices=status_choices, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_total(self):
        total = sum(item.quantity * item.product.price for item in self.items.all())
        self.total_amount = total
        self.save()

    @property
    def items(self):
        return self.order_items.all()

    def __str__(self):
        return f"Order {self.id} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total_price(self):
        return self.quantity * self.price

    def save(self, *args, **kwargs):
        self.price = self.product.price
        super().save(*args, **kwargs)
        # Recalculate total when items are added
        self.order.calculate_total()
