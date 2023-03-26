from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return self.name


CURRENCY_CHOICES = [
    ('USD', 'US Dollars'),
    ('EUR', 'Euros'),
    ('UAH', 'Hryvnia'),
]


class Product(models.Model):
    image = models.ImageField(
        upload_to='products/mainImage', blank=True, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(
        max_length=3, choices=CURRENCY_CHOICES, default='USD')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/images')

    def __str__(self):
        return f'{self.product.name} - Изображение {self.pk}'


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


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[(
        'pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')])

    def __str__(self):
        return f"Order {self.id} - {self.customer.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
