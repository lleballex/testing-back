from django.http import Http404
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Test
from core.mixins import BaseAPIView
from .serializers import TestSerializer
from account.serializers import PublicUserSerializer
from .serializers import CreateQuestionSerializer, CreateTestSerializer


class TestsView(APIView):
	"""Creating a test"""

	permission_classes = [IsAuthenticatedOrReadOnly]

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