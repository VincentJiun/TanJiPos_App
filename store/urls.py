from django.urls import path

from . import  views

urlpatterns = [
    # path('signup/', views.signup, name='signup'),
    path('signup/', views.store_register, name='store_register'),
    path('signin/', views.store_signin, name='store_signin'),
    path('signout/', views.signout, name='signout'),
    path('manage/', views.store_manage, name='store_manage'),
    path('manage/products/', views.store_products, name='store_products'),
    path('manage/add_product/', views.add_product, name='add_product'),
    path('manage/add_category/', views.add_category, name='add_category'),
    path('manage/edit_product/<int:pk>/', views.edit_product, name='edit_product'),
    path('manage/delete_product/<int:pk>/', views.delete_product, name='delete_product'),
    path('manage/options/', views.store_options, name='store_options')
]