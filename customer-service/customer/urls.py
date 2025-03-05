from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import LoginView, RegisterView, ProfileView, ManageAddressesView, CustomerOrdersView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/addresses/', ManageAddressesView.as_view(), name='manage-addresses'),
    path('profile/addresses/<int:address_id>/', ManageAddressesView.as_view(), name='update-delete-address'),
    path('orders/', CustomerOrdersView.as_view(), name='manage-orders'),
]
