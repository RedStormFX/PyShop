

from .category_views import (CategoryViewSet, SubCategoryViewSet)

from .customer_views import CustomerViewSet

from .favorite_views import (
    FavoriteCreateView,
    FavoriteDestroyView,
)

from .order_views import (
    OrderViewSet,
    OrderItemViewSet,
    OrderHistoryView,
)

from .product_views import (
    ProductViewSet,
    ProductReviewViewSet,
    ProductRatingViewSet,

)
from .cart_views import (
    CartView,
    AddProductToCart,
    RemoveProductFromCart,
    ChangeProductQuantity,
)


from .user_views import (
    CustomTokenObtainPairView,
    SignUpView,
    RegisterView,
    edit_user_profile,
    change_password,
)
from .purchase_views import purchase_product
