from rest_framework.permissions import SAFE_METHODS
from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
	"""Allows access to owner of object or safe method"""

	def has_object_permission(self, request, view, obj):
		return request.method in SAFE_METHODS or obj.user == request.user