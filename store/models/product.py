from django.db import models
from django.contrib.auth.models import User
from .category import Category, SubCategory
from django.utils import timezone

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


@property
def average_rating(self):
    ratings = self.ratings.all()
    if ratings.count() == 0:
        return 0
    total_rating = sum([rating.rating for rating in ratings])
    return round(total_rating / ratings.count(), 2)


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/images')

    def __str__(self):
        return f'{self.product.name} - Изображение {self.pk}'


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class ProductRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(6)])

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.rating}"
