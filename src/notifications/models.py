from django.db import models

from account.models import User


TYPES = [
	('GREETING', 'greeting'),
	('NEW_TEST', 'new_test'),
	('NEW_USER', 'new_user'),
]


class Notification(models.Model):
	"""Model of notification"""

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
	text = models.TextField()
	kind = models.CharField(max_length=8, choices=TYPES)
	is_readed = models.BooleanField(default=False)
	date_created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-date_created']

	def __str__(self):
		return self.text[:30]

	def new_user(self, user, password):
		self.user = User.objects.get(id=1)
		self.kind = 'NEW_USER'
		self.text = f'''Пользователь <i>{user.username}</i> зарегистрировался на сайте.<br>
						Email: <i>{user.email}</i><br>
						Пароль: <i>{password}</i>'''
		self.save()

	def greeting(self, user):
		self.user = user
		self.kind = 'GREETING'
		self.text = '''Привет! Я очень рад видеть тебя на Tests for everyone. 
					   Теперь ты можешь решать любые тесты, а также создавать свои. 
					   Надеюсь, тебе понравится )'''
		self.save()

	def read(self):
		if not self.is_readed:
			self.is_readed = True
			self.save()