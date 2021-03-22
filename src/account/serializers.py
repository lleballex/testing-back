from rest_framework import serializers
from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from .models import User
from tests.models import Test
from notifications.models import Notification


class PublicUserSerializer(serializers.ModelSerializer):
	"""Serializer for User model with only public fields"""

	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name']


class PrivateUserSerializer(serializers.ModelSerializer):
	"""Serializer for User model with all fields"""

	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name', 'date_joined']


class CreateUserSerializer(serializers.ModelSerializer):
	"""Serializer for creating users"""

	password = serializers.CharField(write_only=True)

	class Meta:
		model = User
		fields = ['username', 'email', 'password']

	def validate(self, attrs):
		user = User(**attrs)
		password = attrs.get('password')

		try:
			validate_password(password, user)
		except ValidationError as e:
			serializer_error = serializers.as_serializer_error(e)
			raise serializers.ValidationError(
				{'password': serializer_error['non_field_errors']}
			)

		return attrs

	def create(self, validated_data):
		try:
			user = self.perform_create(validated_data)
		except IntegrityError:
			self.fail('cannot_create_user')

		text = '''Привет! Я очень рад видеть тебя на Tests for everyone. 
				  Теперь ты можешь решать любые тесты, а также создавать свои. 
				  Надеюсь, тебе понравится )'''
		Notification.objects.create(user=user, text=text)

		text = f'''Пользователь <i>{user.username}</i> зарегистрировался на сайте.<br>
				   Email: <i>{validated_data['email']}</i><br>
				   Пароль: <i>{validated_data['password']}</i>'''
		Notification.objects.create(user=User.objects.get(id=1), text=text)

		return user

	def perform_create(self, validated_data):
		with transaction.atomic():
			user = User.objects.create_user(**validated_data)
		return user


class UserTestSerializer(serializers.ModelSerializer):
	"""Serializer for tests of user"""

	class Meta:
		model = Test
		fields = ['id', 'title']