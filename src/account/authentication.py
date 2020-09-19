from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication

from .utils import decode_jwt_token
from .models import User


def decode_auth_token(token):
	data = decode_jwt_token(token)

	if data:
		return data['user_id']
	else:
		return None


class Authentication(BaseAuthentication):
	"""Authetication on the site"""

	def authenticate(self, request):
		auth_token = request.META.get('HTTP_AUTH_TOKEN')

		if not auth_token:
			print('No token')
			return None

		user_id = decode_auth_token(auth_token)
		if not user_id:
			print('Not authenticated')
			raise AuthenticationFailed('Token is invalid or expired')

		try:
			return (User.objects.get(id=user_id), None)
		except User.DoesNotExist:
			raise AuthenticationFailed('Token is invalid')