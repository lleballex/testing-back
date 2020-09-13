from rest_framework import mixins
from rest_framework.generics import GenericAPIView

from .models import Test
from .serializers import TestSerializer


class TestView(mixins.RetrieveModelMixin, GenericAPIView):
	"""Getting a test by id"""

	queryset = Test.objects.all()
	lookup_field = 'id'
	serializer_class = TestSerializer

	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)
