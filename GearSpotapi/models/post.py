from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    image_path = models.ImageField(
        upload_to="products",
        height_field=None,
        width_field=None,
        max_length=None,
        null=True,
    )

    def is_Owner(self, request):
        # Check if the request has an authenticated user
        if not hasattr(request, 'auth') or not request.auth:
            return False
            
        # If request.auth exists, compare the authenticated user with the post's user
        return self.user.id == request.auth.user.id