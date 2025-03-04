from django.urls import path

from .views import AddItemView, ItemDetailView, FilterItemView, SearchItemView, ItemListView

urlpatterns = [
    path('items/', ItemListView.as_view(), name='item-list'),
    path('items/add/', AddItemView.as_view(), name='add-item'),
    path('items/search/', SearchItemView.as_view(), name='search'),
    path('items/<str:item_id>/', ItemDetailView.as_view(), name='item-detail'),
    path('items/filter/<str:category>/', FilterItemView.as_view(), name='filter'),
]
