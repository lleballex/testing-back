from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Tag


class TagsView(APIView):
	def get(self, request):
		return Response([tag.tag for tag in Tag.objects.all()])