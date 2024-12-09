from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from detector.views import upload_and_detect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', upload_and_detect, name='upload_and_detect'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
