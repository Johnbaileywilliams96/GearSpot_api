from django.db import models


class Post(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)
    image_path = models.ImageField(
        upload_to="products",
        height_field=None,
        width_field=None,
        max_length=None,
        null=True,
    )

    