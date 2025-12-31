from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    img_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

