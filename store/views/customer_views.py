from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from store.models import Customer
from store.serializers import CustomerSerializer, UserProfileSerializer, CustomerProfileSerializer
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from rest_framework.permissions import IsAuthenticated


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


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
    form = PasswordChangeForm(request.user, request.data)

    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        return Response({"status": "success"})
    else:
        return Response({"status": "error", "errors": form.errors})
