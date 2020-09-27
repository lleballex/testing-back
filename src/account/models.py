from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager


'''class User(AbstractUser):
	"""Model of user"""

	email = models.EmailField(unique=True)
	#first_name = models.CharField(max_length=30, null=True, blank=True)
	#last_name = models.CharField(max_length=30, null=True, blank=True)

	class Meta:
		ordering = ['-date_joined']'''


class UserManager(BaseUserManager):
	"""Custom user manager"""

	def create_user(self, username, email, password):
		print('create user')

		if not username:
			raise ValueError('User must have username')
		if not email:
			raise ValueError('User must have email')

		email = self.normalize_email(email)
		user = self.model(username=username, email=email)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username, email, password):
		user = self.create_user(username=username, email=email, password=password)
		user.is_staff = True
		return user.save()


class User(AbstractBaseUser):
	username = models.CharField(max_length=30, unique=True)
	email = models.EmailField(unique=True)
	first_name = models.CharField(max_length=30, null=True, blank=True)
	last_name = models.CharField(max_length=30, null=True, blank=True)
	date_joined = models.DateTimeField(auto_now=True)
	is_staff = models.BooleanField(default=False)

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	objects = UserManager()

	def __str__(self):
		return self.username

	def has_perm(self, perm, obj=None):
		return self.is_staff

	def has_module_perms(self, package_name):
		return self.is_staff
