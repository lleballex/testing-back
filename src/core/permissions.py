from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
	"""Allows full access to owner of object or read only"""

	def has_object_permission(self, request, view, obj):
		return obj.user == request.user