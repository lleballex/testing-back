from django.db import models
from django.contrib.postgres.fields import ArrayField

from tags.models import Tag
from account.models import User
from rating.models import RatingModel


ANSWER_TYPES = [
	('TEXT', 'text'),
	('NUMBER', 'number'),
	('RADIOS', 'radios'),
]


class Question(models.Model):
	"""Model of question"""

	condition = models.TextField()
	answer = models.CharField(max_length=100)
	answer_options = ArrayField(models.CharField(max_length=500), blank=True)
	answer_type = models.CharField(max_length=10, choices=ANSWER_TYPES, default='TEXT')

	def __str__(self):
		return self.condition[:30]


class SolvedQuestion(models.Model):
	"""Model of solved question"""

	user_answer = models.CharField(max_length=100)
	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='solutions')

	def __str__(self):
		return self.user_answer


class Test(RatingModel, models.Model):
	"""Model of test"""

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tests')
	title = models.CharField(max_length=100)
	description = models.TextField(null=True, blank=True)
	image = models.ImageField(null=True, blank=True, upload_to='%Y/%m/%d/tests/')
	questions = models.ManyToManyField(Question, related_name='test')
	date_created = models.DateTimeField(auto_now_add=True)
	is_private = models.BooleanField(default=False)
	needs_auth = models.BooleanField(default=True)
	tags = models.ManyToManyField(Tag, blank=True, related_name='tests')

	class Meta:
		ordering = ['-date_created']

	def __str__(self):
		return self.title


class SolvedTest(models.Model):
	"""Model of solved test"""

	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='solved_tests')
	test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='solutions')
	answers = models.ManyToManyField(SolvedQuestion)
	right_answers = models.IntegerField(default=0)
	date_started = models.DateTimeField()
	date_ended = models.DateTimeField()

	class Meta:
		ordering = ['-date_ended']

	def __str__(self):
		return self.test.title

	def get_absolute_url(self):
		return f'/tests/my/{self.test.id}/'