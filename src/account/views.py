from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User
from .serializers import PrivateUserSerializer


class UsersView(APIView):
	"""Getting a list of all users"""

	def get(self, request):
		users = User.objects.all()
		serializer = PrivateUserSerializer(users, many=True)
		return Response(serializer.data)