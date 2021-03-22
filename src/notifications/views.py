from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import NotificationSerializer


class NotificationsView(mixins.ListModelMixin, GenericAPIView):
	"""Getting user notifications"""

	serializer_class = NotificationSerializer
	permission_classes = [IsAuthenticated]

	def get(self, request):
		return self.list(request)

	def get_queryset(self):
		for notif in self.request.user.notifications.all():
			yield notif
			notif.read()