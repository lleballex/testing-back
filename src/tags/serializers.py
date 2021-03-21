from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField

from .models import Tag
from core.fields import WriteSerializerMethodField


class TagsSerializer(ModelSerializer):
	"""Serializer for tag fields"""

	tags = WriteSerializerMethodField()

	def get_tags(self, obj):
		return [tag.tag for tag in obj.tags.all()]


class TagSerializer(ModelSerializer):
	"""Serializer of tag"""

	lookup_field = 'tag'

	class Meta:
		model = Tag
		fields = ['tag']