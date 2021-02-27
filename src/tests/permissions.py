from rest_framework.permissions import SAFE_METHODS
from rest_framework.permissions import BasePermission

class UnsolvedTestsPermission(BasePermission):
	"""Allows access to unsolved tests or not safe methods"""

	message = 'You have already solved this test'

	def has_object_permission(self, request, view, obj):
		if request.method in SAFE_METHODS and request.user.is_authenticated:
			if request.user.solved_tests.filter(test_id=obj.id):
				return False
		return True