from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from .models import Cart, CartItem, Category, SubCategory, Product, Customer, Order, OrderItem, ProductReview, ProductRating, Favorite
from .serializers import CartSerializer, CategorySerializer, SubCategorySerializer, ProductSerializer, CustomerSerializer, OrderSerializer, OrderItemSerializer, ProductReviewSerializer, ProductRatingSerializer, FavoriteSerializer
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rest_framework import filters
from .views_cart import *
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            cart_id = request.session.get('cart_id')
            if cart_id:
                user = self.get_queryset().get(email=request.data['email'])
                session_cart = Cart.objects.get(pk=cart_id)

                if user.customer.cart:
                    user_cart = user.customer.cart

                    # Merge session cart with user cart
                    for item in session_cart.items.all():
                        user_item, created = CartItem.objects.get_or_create(
                            cart=user_cart, product=item.product)
                        if not created:
                            user_item.quantity += item.quantity
                        user_item.save()

                    # Delete session cart
                    session_cart.delete()

                else:
                    user.customer.cart = session_cart
                    user.customer.save()

                del request.session['cart_id']

        return response


class CartView(APIView):

    @swagger_auto_schema(
        operation_description="Получить содержимое корзины пользователя",
        responses={
            200: CartSerializer(many=True),
            404: "Корзина не найдена"
        },
        tags=['cart'],
    )
    def get(self, request):
        if request.user.is_authenticated:
            cart = request.user.customer.cart
        else:
            cart_id = request.session.get('cart_id')
            if cart_id:
                cart = Cart.objects.get(pk=cart_id)
            else:
                cart = None

        if cart:
            serializer = CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No cart found."}, status=status.HTTP_404_NOT_FOUND)


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_class = ProductFilter
    search_fields = ['name']
    ordering_fields = ['name', 'price']
    filterset_fields = {
        'price': ['lt', 'gt'],
    }


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class OrderViewSet(APIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @classmethod
    def get_extra_actions(cls):
        return []

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "You must be logged in to create an order."},
                            status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        data['customer'] = request.user.customer.id
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class ProductReviewViewSet(viewsets.ModelViewSet):
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProductRatingViewSet(viewsets.ModelViewSet):
    queryset = ProductRating.objects.all()
    serializer_class = ProductRatingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['POST'])
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


class FavoriteCreateView(generics.CreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class FavoriteDestroyView(generics.DestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
