from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import SAFE_METHODS

from .models import User
from .authentication import encode_auth_token
from .serializers import CreateUserSerializer
from .serializers import PublicUserSerializer, PrivateUserSerializer


class UsersView(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
	"""Getting a list of all users"""

	queryset = User.objects.all()

	def get(self, request):
		return self.list(request)

	def post(self, request):
		return self.create(request)

	def get_serializer_class(self):
		if self.request.method in SAFE_METHODS:
			return PublicUserSerializer
		return CreateUserSerializer


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