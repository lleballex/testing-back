from django.http import Http404
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import SAFE_METHODS
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied, NotAuthenticated

from .models import Test
from core.mixins import BaseAPIView
from core.utils import get_image_from_str
from .serializers import UpdateTestSerializer
from .models import SolvedTest, SolvedQuestion
from core.permissions import IsOwnerOrReadOnly
from .permissions import UnsolvedTestsPermission
from rating.mixins import LikeMixin, DislikeMixin
from .serializers import TestSerializer, BaseTestInfoSerializer
from .serializers import OwnTestSerializer, TestSolutionSerializer
from .serializers import SolvedTestSerializer, SolvedTestsSerializer
from .serializers import CreateQuestionSerializer, CreateTestSerializer

from datetime import datetime


class TestsView(mixins.ListModelMixin, GenericAPIView):
	"""Getting a list of tests and creating a new one"""

	queryset = Test.objects.filter(is_private=False)
	serializer_class = BaseTestInfoSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]

	def get(self, request):
		query = request.query_params.get('query')
		if query:
			self.queryset = self.queryset.filter(title__icontains=query)

		tags = request.query_params.get('tags')
		if tags:
			for tag in tags.split(','):
				self.queryset = self.queryset.filter(tags__id=int(tag))

		sorting = request.query_params.get('sorting')
		if sorting and sorting == 'old':
			self.queryset = self.queryset.order_by('date_created')

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


class TestView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
			   mixins.DestroyModelMixin, BaseAPIView):
	"""Getting and deleting a test"""

	queryset = Test.objects.all()
	lookup_field = 'id'
	permission_classes = [UnsolvedTestsPermission, IsOwnerOrReadOnly]

	def get(self, request, id):
		return self.retrieve(request, id)

	def post(self, request, id):
		return self.retrieve(request, id)

	def put(self, request, id):
		if request.data.get('image'):
			request.data['image'] = get_image_from_str(request.data['image'])
		return self.partial_update(request, id)

	def delete(self, request, id):
		return self.destroy(request, id)

	def get_serializer_class(self):
		if self.request.method in SAFE_METHODS:
			return TestSerializer
		return UpdateTestSerializer


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
		start_date = datetime.fromtimestamp(request.data['start_date'] / 1000.0)
		end_date = datetime.fromtimestamp(request.data['end_date'] / 1000.0)
		solved_test = SolvedTest.objects.create(user=request.user,
												test_id=test.id,
												title=test.title,
												start_date=start_date,
												end_date=end_date)

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


class LikeView(LikeMixin):
	queryset = Test.objects.all()
	lookup_field = 'id'


class DislikeView(DislikeMixin):
	queryset = Test.objects.all()
	lookup_field = 'id'


class SolvedTestsView(APIView):
	"""Getting a list of solved tests"""

	def get(self, request):
		if not request.user.is_authenticated:
			raise NotAuthenticated

		serializer = SolvedTestsSerializer(request.user.solved_tests, many=True)
		return Response(serializer.data)


class SolvedTestView(BaseAPIView):
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


class OwnTestView(APIView):
	"""Getting solutions of own test"""

	def get(self, request, id):
		if not request.user.is_authenticated:
			raise NotAuthenticated

		try:
			test = Test.objects.get(id=id)
		except Test.DoesNotExist:
			raise Http404

		if not test.user == request.user:
			raise PermissionDenied

		serializer = TestSolutionSerializer(SolvedTest.objects.filter(test_id=test.id),
											many=True)
		return Response({
			'title': test.title,
			'rating': test.rating,
			'date_created': test.date_created.strftime('%d.%m.%y %H:%M'),
			'solutions': serializer.data,
		})