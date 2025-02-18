
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, unique=True, blank=True, null=True)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    profile_image = models.ImageField(upload_to='profile_pics/', default='default.jpg')


    def __str__(self):
        return self.username
class Wallet(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def add_money(self, amount):
        self.balance += amount
        self.save()

    def deduct_money(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            return True
        return False
