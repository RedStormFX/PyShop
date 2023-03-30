from django.db import models
from django.contrib.auth.models import User
from .product import Product


class Favorite(models.Model):
    user = models.ForeignKey(User(), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']
