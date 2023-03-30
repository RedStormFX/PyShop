from rest_framework import generics, permissions, views, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from store.serializers import UserSerializer, UserPasswordChangeSerializer
from store.models import Customer, Cart
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import update_session_auth_hash
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


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


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer


class RegisterView(views.APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def edit_user_profile(request):
    user_form = UserProfileSerializer(request.user, data=request.data)
    customer_form = CustomerProfileSerializer(
        request.user.customer, data=request.data)

    if user_form.is_valid() and customer_form.is_valid():
        user_form.save()
        customer_form.save()
        return Response({"status": "success"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = UserPasswordChangeSerializer(
        data=request.data, context={'request': request})
    if serializer.is_valid():
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        update_session_auth_hash(request, request.user)
        return Response({"status": "success"})
    else:
        return Response({"status": "error", "errors": serializer.errors})
