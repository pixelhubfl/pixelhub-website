from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),

    path('product/<int:id>/', views.product_detail, name='product_detail'),

    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('remove/<str:key>/', views.remove_from_cart, name='remove_from_cart'),

    path('checkout/', views.create_checkout_session, name='checkout'),
    path('success/', views.success, name='success'),
]