from django.contrib.sitemaps import Sitemap

from .models import Test
from testing.settings import SITEMAP_URLS


class TestsSitemap(Sitemap):
	changefreq = 'daily'

	def items(self):
		return Test.objects.filter(is_private=False)

	def location(self, item):
		return SITEMAP_URLS['TESTS'].replace(':id', str(item.id))