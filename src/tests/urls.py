from django.urls import path

from .views import TestView, TestInfoView


urlpatterns = [
	path('<int:id>/', TestView.as_view(), name='test'),
	path('<int:id>/info/', TestInfoView.as_view(), name='test_info'),
]