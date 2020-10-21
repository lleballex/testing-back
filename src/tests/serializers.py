from rest_framework.serializers import ModelSerializer, SerializerMethodField

from account.serializers import PublicUserSerializer
from .models import Test, Question


class QuestionSerializer(ModelSerializer):
	"""Serializer for getting questions"""

	answer_options = SerializerMethodField()

	class Meta:
		model = Question
		fields = ['condition', 'answer_options', 'answer_type']

	def get_answer_options(self, obj):
		return obj.answer_options.split('$&$;')


class CreateQuestionSerializer(ModelSerializer):
	"""Serializer for creating questions"""

	class Meta:
		model = Question
		fields = ['id', 'condition', 'answer', 'answer_type', 'answer_options']


class TestSerializer(ModelSerializer):
	"""Serializer for tests"""

	user = PublicUserSerializer()
	questions = QuestionSerializer(many=True)

	class Meta:
		model = Test
		fields = ['id', 'user', 'title', 'description', 'image',
				  'date_created', 'questions', 'is_private', 'need_auth']


class CreateTestSerializer(ModelSerializer):
	"""Serializer for creating tests"""

	class Meta:
		model = Test
		fields = ['title', 'description', 'image',
				  'questions', 'is_private', 'need_auth']


class BaseTestInfoSerializer(ModelSerializer):
	"""Serializer for base info about a test"""

	user = PublicUserSerializer()
	questions = SerializerMethodField()

	class Meta:
		model = Test
		fields = ['id', 'user', 'title', 'questions',
				  'is_private', 'need_auth', 'image']

	def get_questions(self, obj):
		return obj.questions.count()