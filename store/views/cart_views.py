from django.shortcuts import get_object_or_404, HttpResponseRedirect, reverse
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from store.models import Cart, CartItem, Product
from store.serializers import CartItemSerializer


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        cart_items = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        user = request.user
        product_id = request.data.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        cart, created = Cart.objects.get_or_create(user=user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)


def add_product_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart_id = request.session.get('cart_id')
    if cart_id:
        cart = Cart.objects.get(pk=cart_id)
    else:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return HttpResponseRedirect(reverse('cart_view'))


def remove_product_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    cart_item.delete()
    return HttpResponseRedirect(reverse('cart_view'))


def change_product_quantity(request, cart_item_id, quantity):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    cart_item.quantity = quantity
    cart_item.save()
    return HttpResponseRedirect(reverse('cart_view'))


class AddProductToCart(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        product_id = request.data.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        cart, created = Cart.objects.get_or_create(user=user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)


class RemoveProductFromCart(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        product_id = request.data.get('product_id')
        cart = get_object_or_404(Cart, user=user)
        cart_item = get_object_or_404(
            CartItem, cart=cart, product_id=product_id)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangeProductQuantity(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        cart = get_object_or_404(Cart, user=user)
        cart_item = get_object_or_404(
            CartItem, cart=cart, product_id=product_id)
        cart_item.quantity = quantity
        cart_item.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)
