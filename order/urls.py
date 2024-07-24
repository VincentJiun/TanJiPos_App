from django.urls import path

from . import  views

urlpatterns = [
    
    #path('cart/', views.cart_view, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('change_quantity/<str:product_id>/', views.change_quantity, name='change_quantity'),
    path('remove_from_cart/<str:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/checkout/', views.checkout, name='checkout'),
    path('<slug:slug>/', views.order_home, name='order_home'),
]