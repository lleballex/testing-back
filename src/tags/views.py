from rest_framework import mixins
from rest_framework.generics import GenericAPIView

from .models import Tag
from .serializers import TagSerializer


class TagsView(mixins.ListModelMixin, GenericAPIView):
	queryset = Tag.objects.all()
	serializer_class = TagSerializer

	def get(self, request):
		return self.list(request)
