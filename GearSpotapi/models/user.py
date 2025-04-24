from django.db import models
from django.utils import timezone



class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password_hash = models.CharField(max_length=255)
    profile_image = models.ImageField(
        upload_to="products",
        height_field=None,
        width_field=None,
        max_length=None,
        null=True,
    )
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

