from django.http import Http404
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import SAFE_METHODS
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Test
from core.mixins import BaseAPIView
from core.utils import get_image_from_str
from .serializers import UpdateTestSerializer
from notifications.models import Notification
from .models import SolvedTest, SolvedQuestion
from core.permissions import IsOwnerOrReadOnly
from .permissions import UnsolvedTestsPermission
from rating.mixins import LikeMixin, DislikeMixin
from .serializers import TestSerializer, BaseTestSerializer
from .serializers import OwnTestSerializer, TestSolutionSerializer
from .serializers import SolvedTestSerializer, OwnTestSolutionSerializer

from .serializers import FullQuestionSerializer

from datetime import datetime


class TestsView(mixins.ListModelMixin, mixins.CreateModelMixin,
				GenericAPIView):
	"""Getting a list of tests and creating a new one"""

	queryset = Test.objects.filter(is_private=False)
	serializer_class = BaseTestSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]

	def get(self, request):
		query = request.query_params.get('query')
		if query:
			self.queryset = self.queryset.filter(title__icontains=query)

		tags = request.query_params.get('tags')
		if tags:
			for tag in tags.split(','):
				self.queryset = self.queryset.filter(tags__tag=tag)

		sorting = request.query_params.get('sorting')
		if sorting and sorting == 'old':
			self.queryset = self.queryset.order_by('date_created')

		return self.list(request)

	def post(self, request):
		if request.data.get('image'):
			request.data['image'] = get_image_from_str(request.data['image'])
		return self.create(request)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

	def get_serializer_class(self):
		if self.request.method in SAFE_METHODS:
			return BaseTestSerializer
		return UpdateTestSerializer


class TestView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
			   mixins.DestroyModelMixin, BaseAPIView):
	"""Getting, updating and deleting a test"""

	queryset = Test.objects.all()
	lookup_field = 'id'
	permission_classes = [UnsolvedTestsPermission, IsOwnerOrReadOnly]

	def get(self, request, id):
		instance = self.get_object()

		if instance.needs_auth and not request.user.is_authenticated:
			return Response({
				'detail': 'Authorization required',
				'test': {
					'title': instance.title,
					'description': instance.description,
					'image': instance.get_image_url(),
				}
			}, status=403)

		serializer = self.get_serializer(instance)
		return Response(serializer.data)

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
	serializer_class = BaseTestSerializer
	lookup_field = 'id'

	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)


class SolveTestView(GenericAPIView):
	"""Solving a test"""

	def post(self, request, id):
		try:
			test = Test.objects.get(id=id)
		except Test.DoesNotExist:
			raise Http404

		if test.needs_auth and not request.user.is_authenticated:
			raise PermissionDenied

		date_started = datetime.fromtimestamp(request.data['start_date'] / 1000.0)
		date_ended = datetime.fromtimestamp(request.data['end_date'] / 1000.0)
		
		solved_test = SolvedTest.objects.create(test=test,
												date_started=date_started,
								 				date_ended=date_ended)

		if request.user.is_authenticated: solved_test.user = request.user

		for i in range(len(test.questions.all())):
			if test.questions.all()[i].answer == request.data['answers'][i]:
				solved_test.right_answers += 1

			solved_test.answers.add(SolvedQuestion.objects.create(
				user_answer=request.data['answers'][i],
				question=test.questions.all()[i],
			))

		solved_test.save()
		Notification().new_solution(solved_test)

		return Response(solved_test.id, status=201)


class LikeView(LikeMixin):
	queryset = Test.objects.all()
	lookup_field = 'id'


class DislikeView(DislikeMixin):
	queryset = Test.objects.all()
	lookup_field = 'id'


class SolvedTestsView(mixins.ListModelMixin, GenericAPIView):
	"""Getting a list of solved tests"""

	serializer_class = SolvedTestSerializer
	permission_classes = [IsAuthenticated]

	def get(self, request):
		return self.list(request)

	def get_queryset(self):
		return self.request.user.solved_tests


class SolvedTestView(mixins.RetrieveModelMixin, BaseAPIView):
	"""Getting solved test"""

	serializer_class = OwnTestSolutionSerializer
	permission_classes = [IsAuthenticated]
	lookup_field = 'id'

	def get(self, request, id):
		return self.retrieve(id)

	def get_queryset(self):
		return self.request.user.solved_tests


class OwnTestsView(mixins.ListModelMixin, GenericAPIView):
	"""Getting a list of own tests"""

	serializer_class = OwnTestSerializer
	permission_classes = [IsAuthenticated]

	def get(self, request):
		return self.list(request)

	def get_queryset(self):
		return self.request.user.tests


class OwnTestView(GenericAPIView):
	"""Getting solutions of own test"""

	permission_classes = [IsAuthenticated]
	lookup_field = 'id'

	def get(self, request, id):
		test = self.get_object()
		serializer = TestSolutionSerializer(test.solutions, many=True)
		
		return Response({
			'title': test.title,
			'rating': test.rating,
			'date_created': test.date_created.strftime('%d.%m.%y %H:%M'),
			'solutions': serializer.data,
			'questions': FullQuestionSerializer(test.questions, many=True).data,
		})

	def get_queryset(self):
		return self.request.user.tests