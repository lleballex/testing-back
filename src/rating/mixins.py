from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.mixins import BaseAPIView


class LikeMixin(BaseAPIView):
	permission_classes = [IsAuthenticated]

	def post(self, request, **kwargs):
		obj = self.get_object()

		if obj.liked_users.filter(id=request.user.id):
			obj.liked_users.remove(request.user)
			obj.rating -= 1
		else:
			if obj.disliked_users.filter(id=request.user.id):
				obj.disliked_users.remove(request.user)
				obj.rating += 1
			obj.liked_users.add(request.user)
			obj.rating += 1

		obj.save()
		return Response({
			'rating': obj.rating,
			'user_exists': bool(obj.liked_users.filter(id=request.user.id)),
		})


class DislikeMixin(BaseAPIView):
	permission_classes = [IsAuthenticated]

	def post(self, request, **kwargs):
		obj = self.get_object()

		if obj.disliked_users.filter(id=request.user.id):
			obj.disliked_users.remove(request.user)
			obj.rating += 1
		else:
			if obj.liked_users.filter(id=request.user.id):
				obj.liked_users.remove(request.user)
				obj.rating -= 1
			obj.disliked_users.add(request.user)
			obj.rating -= 1

		obj.save()
		return Response({
			'rating': obj.rating,
			'user_exists': bool(obj.disliked_users.filter(id=request.user.id)),
		})
