from django.urls import path

from .views import LoginView, RegisterView, ProfileView, ManageAddressesView, CustomerOrdersView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/addresses/', ManageAddressesView.as_view(), name='manage-addresses'),
    path('profile/addresses/<int:address_id>/', ManageAddressesView.as_view(), name='update-delete-address'),
    path('orders/', CustomerOrdersView.as_view(), name='manage-orders'),
]
