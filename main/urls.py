from django.urls import path
from . import views

# 🔥 IMPORTANTE PARA MEDIA
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('services/', views.services, name='services'),

    path('product/<int:id>/', views.product_detail, name='product_detail'),

    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.create_checkout_session, name='checkout'),
    path('success/', views.success, name='success'),
    path('remove/<str:key>/', views.remove_from_cart, name='remove_from_cart'),
]

# 🔥 ESTO HACE QUE LAS IMÁGENES DEL ADMIN FUNCIONEN
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)