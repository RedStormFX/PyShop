from rest_framework import serializers
from store.models import Cart, CartItem


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    product_title = serializers.ReadOnlyField(source='product.title')
    product_price = serializers.ReadOnlyField(source='product.price')
    product_image = serializers.ImageField(source='product.image')

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'product_title',
                  'product_price', 'product_image', 'quantity',)
