from django.contrib.sitemaps import Sitemap

from .models import User
from testing.settings import SITEMAP_URLS


class UsersSitemap(Sitemap):
	changefreq = 'weekly'

	def items(self):
		return User.objects.all()

	def location(self, item):
		return SITEMAP_URLS['USERS'].replace(':username', item.username)