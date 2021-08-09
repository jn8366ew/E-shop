from django.urls import path
from .views import GetItemView, AddItemView, GetTotalView, \
    GetTotalItemView, UpdateItemView, RemoveItemView, EmptyCartView, \
    SyncCartView


urlpatterns = [
    path('cart-items', GetItemView.as_view()),
    path('add-item', AddItemView.as_view()),
    path('get-total', GetTotalView.as_view()),
    path('get-item-total', GetTotalItemView.as_view()),
    path('update-item', UpdateItemView.as_view()),
    path('remove-item', RemoveItemView.as_view()),
    path('empty-cart', EmptyCartView.as_view()),
    path('synch', SyncCartView.as_view()),

]