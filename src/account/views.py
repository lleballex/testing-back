from django.http import Http404
from rest_framework import mixins
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import SAFE_METHODS
from rest_framework.exceptions import PermissionDenied

from .models import User
from core.mixins import BaseAPIView
from .permissions import IsOwnerOrReadOnly
from .authentication import encode_auth_token, decode_auth_token
from .serializers import UserTestSerializer, PrivateUserSerializer
from .serializers import PublicUserSerializer, CreateUserSerializer


class UsersView(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
	"""Getting a list of all users"""

	queryset = User.objects.all()

	def get(self, request):
		query = request.query_params.get('query')
		sorting = request.query_params.get('sorting')

		if sorting == 'solutions': sorting = 'solved_tests'
		elif sorting != 'tests': sorting = '' 

		if query:
			self.queryset = self.queryset.filter(username__icontains=query)

		if sorting:
			self.queryset = self.queryset.annotate(count=Count(sorting)).order_by('-count')

		return self.list(request)

	def post(self, request):
		return self.create(request)

	def get_serializer_class(self):
		if self.request.method in SAFE_METHODS:
			return PublicUserSerializer
		return CreateUserSerializer


class UserView(mixins.UpdateModelMixin, BaseAPIView):
	"""Getting user data"""

	queryset = User.objects.all()
	serializer_class = PrivateUserSerializer
	lookup_field = 'username'
	permission_classes = [IsOwnerOrReadOnly]

	def get(self, request, username):
		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			raise Http404

		area = request.query_params.get('area')
		extra_data = {}

		if area and area == 'main':
			serializer = UserTestSerializer(user.tests.all()[:5], many='true')
			extra_data['tests'] = serializer.data
		elif area and area == 'tests':
			serializer = UserTestSerializer(user.tests.all(), many='true')
			extra_data['tests'] = serializer.data
		elif area and area == 'personal':
			if request.user != user:
				raise PermissionDenied
			else:
				extra_data = {
					'email': user.email,
					'first_name': user.first_name,
					'last_name': user.last_name
				}

		return Response({
			'image': '',
			**extra_data
		})

	def put(self, request, username):
		return self.update(request, username)


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

		return Response({
			'token': encode_auth_token(user.id),
			'has_notifications': bool(user.notifications.filter(is_readed=False)),
			'username': user.username,
		})


class CheckTokenView(APIView):
	"""Checking auth token"""

	def post(self, request):
		token = request.data.get('token')
		if not token:
			return Response({'detail': 'Request must have token'}, status=400)

		user_id = decode_auth_token(token)
		if not user_id:
			return Response({'detail': 'Token is invalid'}, status=400)

		try:
			user = User.objects.get(id=user_id)
		except User.DoesNotExist:
			return Response({'detail': 'Token is invalid'}, status=400)

		return Response({
			'username': user.username,
			'has_notifications': bool(user.notifications.filter(is_readed=False)),
		})