from django.db import models

from account.models import User


class Notification(models.Model):
	"""Model of notification"""

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
	text = models.TextField()
	is_readed = models.BooleanField(default=False)
	date_created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-date_created']

	def __str__(self):
		return self.text[:30]

	def read(self):
		if not self.is_readed:
			self.is_readed = True
			self.save()