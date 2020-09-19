from rest_framework import serializers

from .models import User


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