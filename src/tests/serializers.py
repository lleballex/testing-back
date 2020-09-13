from rest_framework.serializers import ModelSerializer

from account.serializers import PublicUserSerializer
from .models import Test, Question


class QuestionSerializer(ModelSerializer):
	"""Serializer for Question model"""

	class Meta:
		model = Question
		fields = ['title']


class TestSerializer(ModelSerializer):
	"""Serializer for Test model"""

	user = PublicUserSerializer()
	questions = QuestionSerializer(many=True)

	class Meta:
		model = Test
		fields = ['user', 'questions']