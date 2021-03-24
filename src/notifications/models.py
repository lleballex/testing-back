from django.db import models

from account.models import User


TYPES = [
	('GREETING', 'greeting'),
	('NEW_USER', 'new user'),
	('NEW_TEST', 'new test'),
	('NEW_SOLUTION', 'new solution')
]


class Notification(models.Model):
	"""Model of notification"""

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
	text = models.TextField()
	kind = models.CharField(max_length=12, choices=TYPES)
	is_readed = models.BooleanField(default=False)
	date_created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-date_created']

	def __str__(self):
		return self.text[:30]

	def read(self):
		if not self.is_readed:
			self.is_readed = True
			self.save()

	def new_user(self, user, password):
		self.user = User.objects.get(id=1)
		self.kind = 'NEW_USER'
		self.text = f'Пользователь <i>{user.username}</i> зарегистрировался на сайте.<br>' \
					f'Email: <i>{user.email}</i><br>'									   \
					f'Пароль: <i>{password}</i>'
		self.save()

	def greeting(self, user):
		self.user = user
		self.kind = 'GREETING'
		self.text = 'Привет! Я очень рад видеть тебя на Tests for everyone. '		\
					'Теперь ты можешь решать любые тесты, а также создавать свои. ' \
					'Надеюсь, тебе понравится )'
		self.save()

	def new_solution(self, solution):
		if not solution.user.is_authenticated: username = 'АНОНИМ'
		else: username = solution.user.username

		self.user = solution.test.user
		self.kind = 'NEW_SOLUTION'
		self.text = f'Пользователь <i>{username}</i> решил твой тест "{solution.test.title}". ' 					\
					f'Не хочешь посмотреть <a href="{solution.get_absolute_url()}">результаты</a>?'
		self.save()