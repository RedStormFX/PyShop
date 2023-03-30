from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from store.models import Product


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def purchase_product(request, product_id):
    if not request.user.is_authenticated:
        return Response({"detail": "You must be logged in to make a purchase."},
                        status=status.HTTP_401_UNAUTHORIZED)

    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return Response({"detail": "Product not found."},
                        status=status.HTTP_404_NOT_FOUND)

    # Можно добавить интеграцию с платежной системой.
    # Но пока что мы просто вернем сообщение о том, что товар куплен успешно.
    return Response({"detail": f"Successfully purchased {product.name}. The payment system will contact you when the product is shipped."},
                    status=status.HTTP_200_OK)
