from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from .models import Cart, CartItem, Category, SubCategory, Product, Customer, Order, OrderItem
from .serializers import CartSerializer, CategorySerializer, SubCategorySerializer, ProductSerializer, CustomerSerializer, OrderSerializer, OrderItemSerializer
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
