from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField


class RatingSerializer(ModelSerializer):
	"""Serializer of rating fields"""

	is_liked_user = SerializerMethodField()
	is_disliked_user = SerializerMethodField()

	def get_is_liked_user(self, obj):
		return bool(obj.liked_users.filter(id=self.context['request'].user.id))
	
	def get_is_disliked_user(self, obj):
		return bool(obj.disliked_users.filter(id=self.context['request'].user.id))