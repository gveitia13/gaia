from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from app_main.views import upload_csv
from gaia import settings

urlpatterns = [
    path('admin/upload_csv/', upload_csv, name='upload_csv'),
    path('admin/', admin.site.urls),
    path('', include('app_main.urls')),
    path('', include('app_cart.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
