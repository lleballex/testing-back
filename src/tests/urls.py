from django.urls import path

from .views import TestsView, TestView, TestInfoView, SearchTestsView


urlpatterns = [
	path('', TestsView.as_view(), name='tests'),
	path('<int:id>/', TestView.as_view(), name='test'),
	path('<int:id>/info/', TestInfoView.as_view(), name='test_info'),
	path('search/', SearchTestsView.as_view(), name='search'),
]