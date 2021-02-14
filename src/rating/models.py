from django.db import models

from account.models import User


class RatingModel(models.Model):
	liked_users = models.ManyToManyField(User, related_name='liked_%(class)ss')
	disliked_users = models.ManyToManyField(User, related_name='disliked_%(class)ss')
	rating = models.IntegerField(default=0)

	class Meta:
		abstract = True