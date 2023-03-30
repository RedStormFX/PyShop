from rest_framework import viewsets, permissions
from store.models import Product, ProductReview, ProductRating
from store.serializers import ProductSerializer, ProductReviewSerializer, ProductRatingSerializer
from django_filters.rest_framework import DjangoFilterBackend
from store.filters import ProductFilter
from rest_framework import filters


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_class = ProductFilter
    search_fields = ['name']
    ordering_fields = ['name', 'price']
    filterset_fields = {
        'price': ['lt', 'gt'],
    }
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


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
