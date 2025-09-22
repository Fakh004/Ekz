from django.urls import path
from .views import *

urlpatterns = [
    path('home/', home, name='home'),
    path('register/',register,name='register'),
    path('login/', login, name='login'),
    path('logout/',logout_profile,name='logout'),

    path('profile_edit/<int:pk>',ProfileUpdateView.as_view(), name='profile-update'),
    path('profile_list/',ProfileListView.as_view(),name='profile-list'),
    path('profile_detail<int:pk>',ProfileDetailView.as_view(),name='profile-detail'),

    path('product_list/',ProductListView.as_view(),name='product-list'),
    path('product_create/',ProductCreateView.as_view(),name='product-create'),
    path('product_detail/<int:pk>', ProductDetailView.as_view(),name='product-detail'),
    path('product_update/<int:pk>',ProductUpdateView.as_view(),name='product-update'),
    path('product_delete/<int:pk>',ProductDeleteView.as_view(),name='product-delete'),

    path('cart_list/',CartListView.as_view(),name='cart-list'),
    path('cart_create/',CartCreateView.as_view(),name='cart-create'),
    path('cart_detail/<int:pk>',CartDetailView.as_view(),name='cart-detail'),
    path('cart_update/<int:pk>',CartUpdateView.as_view(),name='cart-update'),
    path('cart_delete/<int:pk>',CartDeleteView.as_view(),name='cart-delete'),

    path('order_list/',OrderListView.as_view(),name='order-list'),
    path('order_create/',OrderCreateView.as_view(),name='order-create'),
    path('order_detail/<int:pk>',OrderDetailView.as_view(),name='order-detail'),
    path('order_delete/<int:pk>',OrderDeleteView.as_view(),name='order-delete')
]