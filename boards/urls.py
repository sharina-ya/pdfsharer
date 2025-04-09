from django.urls import path
from . import views

app_name = 'boards'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('boards.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
