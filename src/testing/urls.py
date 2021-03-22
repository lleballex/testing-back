from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from .sitemap import PagesSitemap
from tests.sitemap import TestsSitemap
from account.sitemap import UsersSitemap


sitemaps = {
	'pages': PagesSitemap,
	'tests': TestsSitemap,
	'users': UsersSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/account/', include('account.urls')),
    path('api/tests/', include('tests.urls')),
    path('api/tags/', include('tags.urls')),
    path('api/notifications/', include('notifications.urls')),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
