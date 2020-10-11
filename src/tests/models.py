from django.db import models

from account.models import User


class Question(models.Model):
	condition = models.TextField()
	answer = models.CharField(max_length=100)

	def __str__(self):
		return self.condition[:30]


class Test(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tests')
	title = models.CharField(max_length=100)
	description = models.TextField(null=True, blank=True)
	image = models.ImageField(null=True, blank=True, upload_to='%Y/%m/%d/tests/')
	questions = models.ManyToManyField(Question, related_name='test')
	date_created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-date_created']

	def __str__(self):
		return self.title