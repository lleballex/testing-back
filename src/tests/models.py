from django.db import models

from account.models import User


class Question(models.Model):
	condition = models.TextField()
	answer = models.CharField(max_length=100)

	def __str__(self):
		return self.condition[:30]


class Test(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tests')
	questions = models.ManyToManyField(Question, related_name='test')
	title = models.CharField(max_length=100)
	description = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.title