from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import SignUpView


router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'subcategories', views.SubCategoryViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'customers', views.CustomerViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'order-items', views.OrderItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', views.SignUpView.as_view(), name='signup'),


]
