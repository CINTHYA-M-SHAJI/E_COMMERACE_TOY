from django.urls import path, include
from . import views
from django.contrib.auth import authenticate
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static





urlpatterns=[
    path('master/',views.Master,name='master'),
    path('',views.index,name='index'),
    path('signup',views.signup,name='signup'),
    path('login',views.login,name='login'),
    
    path('accounts/',include('django.contrib.auth.urls')),

    #add to cart

    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),

    path('cart/checkout/',views.checkout,name='checkout'),
    path('cart/placeorder/',views.placeorder,name='place_order'),

    path('success', views.success,name='success'),
    path('my_order/',views.my_order,name='my_order'),
    path('product/', views.Product_page,name='product'),
    
    path('product/<str:id>', views.product_detail,name='product_detail'),
    path('search/', views.Search, name='search'),




   

]
