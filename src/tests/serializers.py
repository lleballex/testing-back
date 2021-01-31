from rest_framework.serializers import ModelSerializer, SerializerMethodField

from account.serializers import PublicUserSerializer
from .models import Test, Question, SolvedTest, SolvedQuestion


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
				  'questions', 'is_private', 'need_auth', 'tags']


class OwnTestSerializer(ModelSerializer):
	"""Serializer for getting own tests"""

	date_created = SerializerMethodField()

	class Meta:
		model = Test
		fields = ['id', 'title', 'solutions', 'date_created']

	def get_date_created(self, obj):
		return obj.date_created.strftime('%d.%m.%y %H:%M')


class BaseTestInfoSerializer(ModelSerializer):
	"""Serializer for base info about a test"""

	user = PublicUserSerializer()
	tags = SerializerMethodField()
	questions = SerializerMethodField()
	date_created = SerializerMethodField()

	class Meta:
		model = Test
		fields = ['id', 'user', 'title', 'questions', 'tags',
				  'is_private', 'need_auth', 'image', 'date_created']

	def get_tags(self, obj):
		return [tag.tag for tag in obj.tags.all()]

	def get_questions(self, obj):
		return obj.questions.count()

	def get_date_created(self, obj):
		return obj.date_created.strftime('%#d %B')


class SolvedQuestionSerializer(ModelSerializer):
	"""Serializer for solved question"""

	class Meta:
		model = SolvedQuestion
		fields = ['user_answer', 'right_answer']


class SolvedTestSerializer(ModelSerializer):
	"""Serializer for only one solved test"""

	answers = SolvedQuestionSerializer(many=True)

	class Meta:
		model = SolvedTest
		fields = ['title', 'answers', 'right_answers']


class SolvedTestsSerializer(ModelSerializer):
	"""Serializer for many solved tests"""

	answers = SerializerMethodField()

	class Meta:
		model = SolvedTest
		fields = ['id', 'test_id', 'title', 'answers', 'right_answers']

	def get_answers(self, obj):
		return obj.answers.count();


class TestSolutionSerializer(ModelSerializer):
	"""Serializer for solutions of test"""

	user = SerializerMethodField()
	start_date = SerializerMethodField()
	end_date = SerializerMethodField()

	class Meta:
		model = SolvedTest
		fields = ['user', 'answers', 'right_answers', 'start_date', 'end_date']

	def get_user(self, obj):
		return obj.user.username

	def get_start_date(self, obj):
		return obj.start_date.strftime('%d.%m.%y %H:%M')

	def get_end_date(self, obj):
		return obj.end_date.strftime('%d.%m.%y %H:%M')