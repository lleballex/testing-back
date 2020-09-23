from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate

from .models import User
from .authentication import encode_auth_token
from .serializers import PrivateUserSerializer


class UsersView(APIView):
	"""Getting a list of all users"""

	def get(self, request):
		users = User.objects.all()
		serializer = PrivateUserSerializer(users, many=True)
		return Response(serializer.data)


class GetTokenView(APIView):
	"""Getting authentication token"""

	def post(self, request):
		username = request.data.get('username')
		password = request.data.get('password')

		if not username or not password:
			return Response({'detail': 'Request must have \'username\' and \'password\''},
							status=400)

		user = authenticate(username=username, password=password)
		if not user:
			return Response({'detail': 'Username or password is invalid'},
							status=400)

		serializer = PrivateUserSerializer(user)

		return Response({
			'token': encode_auth_token(user.id),
			'user': serializer.data,
		})


class CheckTokenView(APIView):
	pass