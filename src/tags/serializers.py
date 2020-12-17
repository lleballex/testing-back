from rest_framework.serializers import ModelSerializer

from .models import Tag


class TagSerializer(ModelSerializer):
	"""Serializer of tag model"""

	class Meta:
		model = Tag
		fields = ['tag']