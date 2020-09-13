from django.urls import path

from .views import TestView


urlpatterns = [
	path('<int:id>/', TestView.as_view(), name='test'),
]