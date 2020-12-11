from django.db import models

from account.models import User


ANSWER_TYPE = [
	('TEXT', 'text'),
	('NUMBER', 'number'),
	('CHECKBOXES', 'checkboxes'),
	('RADIOS', 'radios'),
]


class Tag(models.Model):
	"""Model of teg"""

	title = models.CharField(max_length=100)

	def __str__(self):
		return self.title


class Question(models.Model):
	"""Model of question"""

	condition = models.TextField()
	answer = models.CharField(max_length=100)
	answer_options = models.CharField(max_length=1000, null=True, blank=True)
	answer_type = models.CharField(max_length=10, choices=ANSWER_TYPE,
								   default='TEXT')

	def __str__(self):
		return self.condition[:30]


class Test(models.Model):
	"""Model of test"""

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tests')
	title = models.CharField(max_length=100)
	description = models.TextField(null=True, blank=True)
	image = models.ImageField(null=True, blank=True, upload_to='%Y/%m/%d/tests/')
	questions = models.ManyToManyField(Question, related_name='test')
	date_created = models.DateTimeField(auto_now_add=True)
	is_private = models.BooleanField(default=False)
	need_auth = models.BooleanField(default=True)
	tags = models.ManyToManyField(Tag, related_name='tests')

	class Meta:
		ordering = ['-date_created']

	def __str__(self):
		return self.title


class SolvedQuestion(models.Model):
	"""Model for solved question"""

	user_answer = models.CharField(max_length=100)
	right_answer = models.CharField(max_length=100)

	def __str__(self):
		return self.user_answer


class SolvedTest(models.Model):
	"""Model for solved test"""

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solved_tests')
	test_id = models.IntegerField()
	title = models.CharField(max_length=100)
	answers = models.ManyToManyField(SolvedQuestion)
	right_answers = models.IntegerField(default=0)

	def __str__(self):
		return self.title