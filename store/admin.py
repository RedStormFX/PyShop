from django.contrib import admin
from django.db import models
from .models import Category, SubCategory, Product, ProductImage, Customer, Order, OrderItem
from .widgets import ImagePreviewWidget


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
    extra = 0
    max_num = 8
    formfield_overrides = {
        models.ImageField: {'widget': ImagePreviewWidget},
    }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]
    formfield_overrides = {
        models.ImageField: {'widget': ImagePreviewWidget},
    }


admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
