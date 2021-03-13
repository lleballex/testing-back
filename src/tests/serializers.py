from rest_framework.serializers import ModelSerializer, SerializerMethodField

from tags.models import Tag
from tags.serializers import TagSerializer
from rating.serializers import RatingSerializer
from account.serializers import PublicUserSerializer
from .models import Test, Question, SolvedTest, SolvedQuestion


class QuestionSerializer(ModelSerializer):
	"""Serializer of question"""

	answer_options = SerializerMethodField()

	class Meta:
		model = Question
		fields = ['condition', 'answer_options', 'answer_type']

	def get_answer_options(self, obj):
		return obj.answer_options.split('$&$;')


class CreateQuestionSerializer(ModelSerializer):
	"""Serializer for creating question"""

	class Meta:
		model = Question
		fields = ['id', 'condition', 'answer', 'answer_type', 'answer_options']


class TestSerializer(RatingSerializer, ModelSerializer):
	"""Serializer of test"""

	user = PublicUserSerializer()
	questions = QuestionSerializer(many=True)
	is_protected = SerializerMethodField()

	class Meta:
		model = Test
		fields = ['id', 'user', 'title', 'description', 'image',
				  'date_created', 'questions', 'is_private', 'need_auth',
				  'rating', 'is_liked_user', 'is_disliked_user', 'is_protected']

	def get_is_protected(self, obj):
		for tag in obj.tags.all():
			if tag.tag == 'домашка':
				return True
		return False


class CreateTestSerializer(ModelSerializer):
	"""Serializer for creating test"""

	class Meta:
		model = Test
		fields = ['title', 'description', 'image',
				  'questions', 'is_private', 'need_auth', 'tags']


class UpdateQuestionSerializer(ModelSerializer):
	"""Serializer for updating question"""

	answer_options = SerializerMethodField()

	class Meta:
		model = Question
		fields = ['condition', 'answer', 'answer_type', 'answer_options']

	def get_answer_options(self, obj):
		return obj.answer_options.split('$&$;')


class UpdateTestSerializer(ModelSerializer):
	"""Serializer for updating test"""

	questions = UpdateQuestionSerializer(many=True, read_only=True)
	tags = TagSerializer(many=True)

	class Meta:
		model = Test
		fields = ['title', 'description', 'image', 'questions',
				  'is_private', 'need_auth', 'tags']
		read_only_fields = ['tags']

	def update(self, instanse, validated_data):
		tags = validated_data.get('tags')

		if tags or tags == []:
			instanse.tags.clear()
			for tag in tags:
				instanse.tags.add(Tag.objects.get(tag=tag['tag']))
			del validated_data['tags']

		return super().update(instanse, validated_data)


class OwnTestSerializer(ModelSerializer):
	"""Serializer of own test"""

	tags = SerializerMethodField()
	date_created = SerializerMethodField()

	class Meta:
		model = Test
		fields = ['id', 'title', 'solutions', 'date_created',
				  'tags', 'image', 'rating']

	def get_tags(self, obj):
		return [tag.tag for tag in obj.tags.all()]

	def get_date_created(self, obj):
		return obj.date_created.strftime('%d.%m.%y %H:%M')


class BaseTestInfoSerializer(RatingSerializer, ModelSerializer):
	"""Serializer of base info about test"""

	user = PublicUserSerializer()
	tags = SerializerMethodField()
	questions = SerializerMethodField()
	date_created = SerializerMethodField()

	class Meta:
		model = Test
		fields = ['id', 'user', 'title', 'questions', 'tags',
				  'is_private', 'need_auth', 'image', 'date_created',
				  'rating', 'is_liked_user', 'is_disliked_user']

	def get_tags(self, obj):
		return [tag.tag for tag in obj.tags.all()]

	def get_questions(self, obj):
		return obj.questions.count()

	def get_date_created(self, obj):
		return obj.date_created.strftime('%#d %B')


class SolvedQuestionSerializer(ModelSerializer):
	"""Serializer of solved question"""

	class Meta:
		model = SolvedQuestion
		fields = ['user_answer', 'right_answer']


class SolvedTestSerializer(ModelSerializer):
	"""Serializer of own test solution"""

	answers = SolvedQuestionSerializer(many=True)

	class Meta:
		model = SolvedTest
		fields = ['title', 'answers', 'right_answers']


class SolvedTestsSerializer(ModelSerializer):
	"""Serializer of solved test"""

	answers = SerializerMethodField()

	class Meta:
		model = SolvedTest
		fields = ['id', 'test_id', 'title', 'answers', 'right_answers']

	def get_answers(self, obj):
		return obj.answers.count();


class TestSolutionSerializer(ModelSerializer):
	"""Serializer of test solution"""

	user = SerializerMethodField()
	start_date = SerializerMethodField()
	end_date = SerializerMethodField()
	answers = SolvedQuestionSerializer(many=True)

	class Meta:
		model = SolvedTest
		fields = ['user', 'answers', 'right_answers', 'start_date', 'end_date']

	def get_user(self, obj):
		return obj.user.username

	def get_start_date(self, obj):
		return obj.start_date.strftime('%d.%m.%y %H:%M')

	def get_end_date(self, obj):
		return obj.end_date.strftime('%d.%m.%y %H:%M')