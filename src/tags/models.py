from django.db import models


class Tag(models.Model):
	"""Model of tag"""

	tag = models.CharField(max_length=30)

	def __str__(self):
		return self.tag
