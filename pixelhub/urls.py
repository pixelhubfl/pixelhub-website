from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # 🔥 idioma automático
    path('', include('main.urls')),
]

# MEDIA
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)