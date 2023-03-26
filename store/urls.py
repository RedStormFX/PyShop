from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, views_cart
from .views import SignUpView, CartView, OrderViewSet, ProductReviewViewSet, ProductRatingViewSet

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'subcategories', views.SubCategoryViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'customers', views.CustomerViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'order-items', views.OrderItemViewSet)
router.register(r'product-reviews', ProductReviewViewSet)
router.register(r'product-ratings', ProductRatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('add-to-cart/<int:product_id>/',
         views_cart.add_to_cart, name='add_to_cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('orders/', OrderViewSet.as_view(), name='orders'),
    path('purchase/<int:product_id>/',
         views.purchase_product, name='purchase_product'),


]
