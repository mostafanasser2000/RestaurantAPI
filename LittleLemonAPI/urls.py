from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.api_root, name='root'),
    path('users/', include('djoser.urls')),
    path('groups/manager/users/', views.ManagerGroupListView.as_view(), name='manager-list'),
    path('groups/manager/users/<int:pk>/', views.ManagerGroupDetailView.as_view(), name='manager-detail'),
    path('groups/delivery-crew/users/', views.DeliveryCrewListView.as_view(), name='delivery-crew-list'),
    path('groups/delivery-crew/users/<int:pk>/', views.DeliveryCrewDetailView.as_view(), name='delivery-crew-detail'),
    path('category-list/', views.CategoryiesView.as_view(), name='category-list'),
    path('menu-items/', views.MenuItemListView.as_view(), name='item-list'),
    path('menu-items/<int:pk>/',views.MenuItemDetailView.as_view(), name='item-detail'),
    path('cart/menu-items/', views.cart_view, name='user-cart'),
    path('orders/', views.order_list, name='order-list'),
    path('orders/<int:pk>/', views.order_deatil, name='order-detail'),

]