from rest_framework.serializers import ModelSerializer

from account.serializers import PublicUserSerializer
from .models import Test, Question


class QuestionSerializer(ModelSerializer):
	"""Serializer for Question model"""

	class Meta:
		model = Question
		fields = ['condition']


class CreateQuestionSerializer(ModelSerializer):
	"""Serializer for creating questions"""

	class Meta:
		model = Question
		fields = ['id', 'condition', 'answer']


class TestSerializer(ModelSerializer):
	"""Serializer for Test model"""

	user = PublicUserSerializer()
	questions = QuestionSerializer(many=True)

	class Meta:
		model = Test
		fields = ['id', 'user', 'title', 'description', 'questions']


class CreateTestSerializer(ModelSerializer):
	"""Serializer for creating tests"""

	class Meta:
		model = Test
		fields = ['title', 'description', 'questions']