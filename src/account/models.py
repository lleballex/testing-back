from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
	"""Model of user"""

	email = models.EmailField(unique=True)
	first_name = models.CharField(max_length=30, null=True, blank=True)
	last_name = models.CharField(max_length=30, null=True, blank=True)

	class Meta:
		ordering = ['-date_joined']
