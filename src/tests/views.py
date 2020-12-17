from django.http import Http404
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied, NotAuthenticated

from .models import Test
from core.mixins import BaseAPIView
from core.utils import get_image_from_str
from .serializers import OwnTestSerializer
from .models import SolvedTest, SolvedQuestion
from .serializers import TestSerializer, BaseTestInfoSerializer
from .serializers import SolvedTestSerializer, SolvedTestsSerializer
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


class TestView(BaseAPIView):
	"""Getting a test by id"""

	def get(self, request, id):
		try:
			test = Test.objects.get(id=id)
		except Test.DoesNotExist:
			raise Http404

		if request.user.is_authenticated:
			try:
				request.user.solved_tests.get(test_id=test.id)
				return Response({
					'detail':'You have already solved this test'
				}, status=403)
			except SolvedTest.DoesNotExist:
				pass
		
		serializer = TestSerializer(test)
		return Response(serializer.data)


class TestInfoView(mixins.RetrieveModelMixin, BaseAPIView):
	"""Getting base info about test"""

	queryset = Test.objects.all()
	serializer_class = BaseTestInfoSerializer
	lookup_field = 'id'

	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)


class CheckAnswersView(APIView):
	"""Checking test answers"""

	def post(self, request, id):
		try:
			test = Test.objects.get(id=id)
		except Test.DoesNotExist:
			raise Http404

		if test.need_auth and not request.user.is_authenticated:
			raise PermissionDenied

		right_answers = 0
		solved_test = SolvedTest.objects.create(user=request.user,
												test_id=test.id,
												title=test.title)

		for i in range(len(test.questions.all())):
			if test.questions.all()[i].answer == request.data['answers'][i]:
				right_answers += 1

			solved_test.answers.add(SolvedQuestion.objects.create(
				user_answer = request.data['answers'][i],
				right_answer = test.questions.all()[i].answer
			))

		solved_test.right_answers = right_answers
		solved_test.save()
		test.add_solution()

		return Response(solved_test.id)


class SolvedTestsView(APIView):
	"""Getting a list of solved tests"""

	def get(self, request):
		if not request.user.is_authenticated:
			raise NotAuthenticated

		serializer = SolvedTestsSerializer(request.user.solved_tests, many=True)
		return Response(serializer.data)


class SolvedTestView(APIView):
	"""Getting solved test by id"""

	def get(self, request, id):
		if not request.user.is_authenticated:
			raise NotAuthenticated

		try:
			test = SolvedTest.objects.get(id=id)
		except SolvedTest.DoesNotExist:
			raise Http404

		if not test.user == request.user:
			raise PermissionDenied

		serializer = SolvedTestSerializer(test)
		return Response(serializer.data)


class OwnTestsView(APIView):
	"""Getting a list of own tests"""

	def get(self, request):
		if not request.user.is_authenticated:
			raise NotAuthenticated

		serializer = OwnTestSerializer(request.user.tests, many=True)
		return Response(serializer.data)


class SearchTestsView(APIView):
	"""Searching tests"""

	def get(self, request):
		text = request.query_params.get('text')
		if not text:
			return Response('Request must have \'text\' parameter', status=400)

		tests = Test.objects.filter(is_private=False, title__icontains=text)

		sorting = request.query_params.get('sorting')
		if sorting and sorting == 'old':
			tests = tests.order_by('date_created')

		serializer = BaseTestInfoSerializer(tests, many=True)

		return Response(serializer.data)