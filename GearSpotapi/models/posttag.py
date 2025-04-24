from django.db import models
from django.utils import timezone
from .post import Post
from .user import User
from .tag import Tag

class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='post_tags')

    class Meta:
        unique_together = ('post', 'tag')