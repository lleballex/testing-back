from django.http import Http404
from rest_framework import mixins
from rest_framework.response import Response

from .models import Test
from .serializers import TestSerializer
from core.mixins import BaseAPIView
from account.serializers import PublicUserSerializer


class TestView(mixins.RetrieveModelMixin, BaseAPIView):
	"""Getting a test by id"""

	queryset = Test.objects.all()
	lookup_field = 'id'
	serializer_class = TestSerializer

	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)


class TestInfoView(BaseAPIView):
	"""Getting base info about test"""

	def get(self, request, id):
		try:
			test = Test.objects.get(id=id)
		except Test.DoesNotExist:
			raise Http404()

		user_serializer = PublicUserSerializer(test.user)

		return Response({
			'user': user_serializer.data,
			'title': test.title,
			'questions': test.questions.count()
		})