from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SignUpView,
    CartView,
    AddProductToCart,
    OrderViewSet,
    ProductReviewViewSet,
    ProductRatingViewSet,
    purchase_product,
    edit_user_profile,
    change_password,
    CategoryViewSet,
    SubCategoryViewSet,
    ProductViewSet,
    CustomerViewSet,
    OrderItemViewSet,
    FavoriteCreateView,
    FavoriteDestroyView,
    OrderHistoryView,
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubCategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)
router.register(r'product-reviews', ProductReviewViewSet)
router.register(r'product-ratings', ProductRatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/', AddProductToCart.as_view(), name='add_to_cart'),
    path('orders/',
         OrderViewSet.as_view({'get': 'list', 'post': 'create'}), name='orders'),
    path('orders/<int:pk>/', OrderViewSet.as_view({'get': 'retrieve', 'put': 'update',
         'patch': 'partial_update', 'delete': 'destroy'}), name='order-detail'),
    path('purchase/<int:product_id>/', purchase_product, name='purchase_product'),
    path('favorites/', FavoriteCreateView.as_view(), name='favorite-create'),
    path('favorites/<int:pk>/', FavoriteDestroyView.as_view(),
         name='favorite-destroy'),
    path('order-history/', OrderHistoryView.as_view(), name='order-history'),
    path('edit_user_profile/', edit_user_profile, name='edit_user_profile'),
    path('change_password/', change_password, name='change_password'),
]
