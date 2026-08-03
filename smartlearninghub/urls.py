from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Tambahkan import ini
from learning import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('learning.urls')),

    # URL AI Chat
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)