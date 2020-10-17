from django.http import Http404
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Test
from core.mixins import BaseAPIView
from .serializers import TestSerializer
from account.serializers import PublicUserSerializer
from .serializers import CreateQuestionSerializer, CreateTestSerializer

from base64 import b64decode


class TestsView(mixins.ListModelMixin, GenericAPIView):
	"""Creating a test"""

	queryset = Test.objects.all()
	serializer_class = TestSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]

	def get(self, request):
		return self.list(request)

	def post(self, request):
		question_serializer = CreateQuestionSerializer(data=request.data['questions'],
													   many=True)
		if not question_serializer.is_valid():
			return Response(question_serializer.errors, status=400)
		question_serializer.save()

		questions = []
		for question in question_serializer.data:
			questions.append(question['id'])
		request.data['questions'] = questions

		if request.data.get('image'):
			_, img_str = request.data['image'].split('base64,')
			image_extension = _.split('/')[-1].split(';')[0]
			img_base64 = b64decode(img_str)
			image_b = ContentFile(img_base64)
			image_b.name = get_random_string(length=6) + '.' + image_extension
			request.data['image'] = image_b

		test_serializer = CreateTestSerializer(data=request.data)

		if not test_serializer.is_valid():
			return Response(test_serializer.errors, status=400)
		test_serializer.save(user=request.user)

		return Response(test_serializer.data, status=201)


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


class SearchTestsView(APIView):
	"""Searching tests"""

	def get(self, request):
		text = request.query_params.get('text')
		if not text:
			return Response('Request must have \'text\' parameter', status=400)

		tests = Test.objects.filter(title__icontains=text)
		serializer = TestSerializer(tests, many=True)

		return Response(serializer.data)