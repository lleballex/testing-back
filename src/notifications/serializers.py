from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField

from .models import Notification


class NotificationSerializer(ModelSerializer):
	"""Serializer of notification"""

	date_created = SerializerMethodField()

	class Meta:
		model = Notification
		fields = ['text', 'kind', 'is_readed', 'date_created']

	def get_date_created(self, obj):
		return obj.date_created.strftime('%#d %B %H:%M')