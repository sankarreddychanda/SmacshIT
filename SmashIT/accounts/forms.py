from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser  # Use our CustomUser instead of auth.User
        fields = ["username", "email", "password1", "password2"]
