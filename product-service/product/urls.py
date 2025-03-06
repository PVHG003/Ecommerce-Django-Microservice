from django.urls import path, re_path

from .views import AddItemView, ItemDetailView, FilterItemView, SearchItemView, ItemListView, SellerItemListView

urlpatterns = [
    path('items/public/', ItemListView.as_view(), name='item-list'), # public view
    path('sellers/items/', SellerItemListView.as_view(), name='seller-item-list'),
    path('items/add/', AddItemView.as_view(), name='add-item'),
    path('items/search/', SearchItemView.as_view(), name='search'),
    path('items/<str:item_id>/', ItemDetailView.as_view(), name='item-detail'),
    re_path('items/filter/<str:category>/', FilterItemView.as_view(), name='filter'),
]
