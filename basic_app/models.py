from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfileInfo(models.Model):
    # To add standard parameters like name, email, etc...
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Additional
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self) -> str:
        return self.user.username