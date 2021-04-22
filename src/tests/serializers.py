from rest_framework.fields import empty
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField

from tags.models import Tag
from rating.serializers import RatingSerializer
from core.fields import WriteSerializerMethodField
from account.serializers import PublicUserSerializer
from tags.serializers import TagsSerializer, TagSerializer
from .models import Question, SolvedQuestion, Test, SolvedTest


class QuestionSerializer(ModelSerializer):
	"""Serializer of question"""

	answer_options = SerializerMethodField()

	class Meta:
		model = Question
		fields = ['condition', 'answer_options', 'answer_type']

	def get_answer_options(self, obj):
		return obj.answer_options.split('$&$;')


class FullQuestionSerializer(ModelSerializer):
	"""Serializer with all question fields"""

	answer_options = WriteSerializerMethodField()

	class Meta:
		model = Question
		fields = ['id', 'condition', 'answer', 'answer_options', 'answer_type']

	def get_answer_options(self, obj):
		return obj.answer_options.split('$&$;')

	def get_data_answer_options(self, data):
		if type(data) == str: return data
		return '$&$;'.join(data)


class SolvedQuestionSerializer(ModelSerializer):
	"""Serializer of solved question"""

	right_answer = SerializerMethodField()
	condition = SerializerMethodField()

	class Meta:
		model = SolvedQuestion
		fields = ['user_answer', 'right_answer', 'condition']

	def get_right_answer(self, obj):
		return obj.question.answer

	def get_condition(self, obj):
		return obj.question.condition


class TestSerializer(RatingSerializer, ModelSerializer):
	"""Serializer of test"""

	user = PublicUserSerializer()
	questions = QuestionSerializer(many=True)

	class Meta:
		model = Test
		fields = ['user', 'title', 'description', 'image',
				  'questions', 'is_private', 'needs_auth',
				  'rating', 'is_liked_user', 'is_disliked_user']


class BaseTestSerializer(TagsSerializer, RatingSerializer, ModelSerializer):
	"""Serializer of base info about test"""

	user = PublicUserSerializer()
	questions = SerializerMethodField()
	date_created = SerializerMethodField()

	class Meta:
		model = Test
		fields = ['id', 'user', 'title', 'questions', 'tags',
				  'is_private', 'needs_auth', 'image', 'date_created',
				  'rating', 'is_liked_user', 'is_disliked_user']
				  
	def get_questions(self, obj):
		return obj.questions.count()

	def get_date_created(self, obj):
		return obj.date_created.strftime('%#d %B')


class UpdateTestSerializer(TagsSerializer, ModelSerializer):
	"""Serializer for updating and creating a test"""

	questions = FullQuestionSerializer(many=True)

	class Meta:
		model = Test
		fields = ['title', 'description', 'image', 'questions',
				  'is_private', 'needs_auth', 'tags']

	def update(self, instanse, validated_data):
		if validated_data.get('questions', None) != None:
			del validated_data['questions']

		tags = validated_data['tags']
		del validated_data['tags']

		instanse.tags.clear()
		for tag in tags:
			instanse.tags.add(Tag.objects.get(tag=tag))

		return super().update(instanse, validated_data)

	def create(self, validated_data):
		questions_data = validated_data['questions']
		tags_data = validated_data.get('tags', [])
		del validated_data['questions']
		if tags_data: del validated_data['tags']

		instanse = super().create(validated_data)

		questions_serializer = FullQuestionSerializer(data=questions_data,
													  many=True)
		questions_serializer.is_valid(raise_exception=True)
		questions_serializer.save()

		for question in questions_serializer.data:
			instanse.questions.add(Question.objects.get(id=question['id']))

		for tag in tags_data:
			instanse.tags.add(Tag.objects.get(tag=tag))

		instanse.save()
		return instanse


class OwnTestSerializer(TagsSerializer, ModelSerializer):
	"""Serializer of own test"""

	solutions = SerializerMethodField()
	date_created = SerializerMethodField()

	class Meta:
		model = Test
		fields = ['id', 'title', 'solutions', 'tags',
				  'date_created', 'image', 'rating']

	def get_solutions(self, obj):
		return obj.solutions.count()

	def get_date_created(self, obj):
		return obj.date_created.strftime('%d.%m.%y %H:%M')


class SolvedTestSerializer(TagsSerializer, ModelSerializer):
	"""Serializer of solved test (base info about solved test)"""

	answers = SerializerMethodField()
	title = SerializerMethodField()
	test_id = SerializerMethodField()
	image = SerializerMethodField()

	class Meta:
		model = SolvedTest
		fields = ['id', 'test_id', 'title', 'answers', 'right_answers',
				  'image', 'tags']
		# remove test_id (used in old version)

	def get_answers(self, obj):
		return obj.answers.count();

	def get_title(self, obj):
		return obj.test.title

	def get_test_id(self, obj):
		return obj.test.id

	def get_image(self, obj):
		if obj.test.image:
			return obj.test.image.url
		return None

	def get_tags(self, obj):
		return super().get_tags(obj.test)


class OwnTestSolutionSerializer(TagsSerializer, ModelSerializer):
	"""Serializer of own test solution"""

	answers = SolvedQuestionSerializer(many=True)
	title = SerializerMethodField()

	class Meta:
		model = SolvedTest
		fields = ['title', 'answers', 'right_answers']

	def get_title(self, obj):
		return obj.test.title


class TestSolutionSerializer(ModelSerializer):
	"""Serializer of test solution"""

	user = SerializerMethodField()
	date_started = SerializerMethodField()
	date_ended = SerializerMethodField()
	answers = SolvedQuestionSerializer(many=True)

	class Meta:
		model = SolvedTest
		fields = ['user', 'answers', 'right_answers',
				  'date_started', 'date_ended']

	def get_user(self, obj):
		if obj.user: return obj.user.username
		return 'АНОНИМ'

	def get_date_started(self, obj):
		return obj.date_started.strftime('%d.%m.%y %H:%M')

	def get_date_ended(self, obj):
		return obj.date_ended.strftime('%d.%m.%y %H:%M')