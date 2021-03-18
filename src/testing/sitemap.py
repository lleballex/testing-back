from django.contrib.sitemaps import Sitemap

from .settings import SITEMAP_URLS


class PagesSitemap(Sitemap):
	changefreq = 'weekly'

	def items(self):
		return SITEMAP_URLS['OTHER']

	def location(self, item):
		return item