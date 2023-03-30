from django.db import models
from django.contrib.auth.models import User


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id}"


class CartItem(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_to_cart_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
