from django.shortcuts import get_object_or_404, HttpResponseRedirect, reverse
from .models import Cart, CartItem, Product


def add_to_cart(request, product_id):
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
