from django.db import models

from account.models import User


class Question(models.Model):
	title = models.CharField(max_length=100)
	answer = models.CharField(max_length=100)

	def __str__(self):
		return self.title[:30]


class Test(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tests')
	questions = models.ManyToManyField(Question, related_name='test')

	def __str__(self):
		return self.user.username