from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/account/', include('account.urls')),
    path('api/tests/', include('tests.urls')),
    path('api/tags/', include('tags.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
