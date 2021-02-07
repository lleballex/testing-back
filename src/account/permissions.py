from rest_framework.permissions import SAFE_METHODS
from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
	message = 'This action is available only to this user'

	def has_object_permission(self, request, view, obj):
		return request.method in SAFE_METHODS or obj == request.user