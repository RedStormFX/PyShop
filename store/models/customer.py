from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, default='Unknown')
    country = models.CharField(max_length=100, default='Unknown')
    city = models.CharField(max_length=100, default='Unknown')
    region = models.CharField(max_length=100, default='Unknown')
    street = models.CharField(max_length=255, default='Unknown')
    postal_office = models.CharField(max_length=100, default='Unknown')

    def __str__(self):
        return self.user.username
