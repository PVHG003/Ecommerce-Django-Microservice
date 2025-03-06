from django.urls import path

from .views import CartItemView

urlpatterns = [
    path('carts/', CartItemView.as_view(), name='add-get-cart-item'),
    path('carts/<str:item_id>/', CartItemView.as_view(), name='update-delete-cart-item'),
]
