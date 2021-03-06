from rest_framework import serializers
from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from .models import User
from tests.models import Test
from notifications.models import Notification


class PublicUserSerializer(serializers.ModelSerializer):
	"""Serializer for User model with only public fields"""

	tests = serializers.SerializerMethodField()
	solutions = serializers.SerializerMethodField()

	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'tests', 'solutions']

	def get_tests(self, obj):
		return obj.tests.count()

	def get_solutions(self, obj):
		return obj.solved_tests.count()


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

		Notification().greeting(user)
		Notification().new_user(user, validated_data['password'])

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