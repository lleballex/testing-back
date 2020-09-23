from django.urls import path

from .views import UsersView
from .views import GetTokenView, CheckTokenView


urlpatterns = [
	path('users/', UsersView.as_view(), name='users'),
	path('token/get_token/', GetTokenView.as_view(), name='get_token'),
	path('token/check_token/', CheckTokenView.as_view(), name='check_token'),
]