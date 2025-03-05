from django.urls import path

from .views import AddItemToCartView

urlpatterns = [
    path('carts/add/', AddItemToCartView.as_view(), name='add-item-to-cart'),
]
