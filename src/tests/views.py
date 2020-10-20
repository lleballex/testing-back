from django.http import Http404
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Test
from core.mixins import BaseAPIView
from core.utils import get_image_from_str
from .serializers import TestSerializer, BaseTestInfoSerializer
from .serializers import CreateQuestionSerializer, CreateTestSerializer


class TestsView(mixins.ListModelMixin, GenericAPIView):
	"""Getting a list of tests and creating a new one"""

	queryset = Test.objects.filter(is_private=False)
	serializer_class = BaseTestInfoSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]

	def get(self, request):
		return self.list(request)

	def post(self, request):
		for i in range(len(request.data['questions'])):
			answer_options = ''
			for answer in request.data['questions'][i]['answer_options']:
				answer_options += answer + '$&$;'
			answer_options = answer_options[:len(answer_options) - 4]
			request.data['questions'][i]['answer_options'] = answer_options

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
			request.data['image'] = get_image_from_str(request.data['image'])

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


class TestInfoView(mixins.RetrieveModelMixin, BaseAPIView):
	"""Getting base info about test"""

	queryset = Test.objects.all()
	serializer_class = BaseTestInfoSerializer
	lookup_field = 'id'

	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)


class SearchTestsView(APIView):
	"""Searching tests"""

	def get(self, request):
		text = request.query_params.get('text')
		if not text:
			return Response('Request must have \'text\' parameter', status=400)

		tests = Test.objects.filter(is_private=False, title__icontains=text)
		serializer = TestSerializer(tests, many=True)

		return Response(serializer.data)