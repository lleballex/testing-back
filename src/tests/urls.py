from django.urls import path

from .views import CheckAnswersView, SolvedTestsView, SolvedTestView
from .views import TestsView, TestView, TestInfoView, SearchTestsView


urlpatterns = [
	path('', TestsView.as_view(), name='tests'),
	path('<int:id>/', TestView.as_view(), name='test'),
	path('<int:id>/info/', TestInfoView.as_view(), name='test_info'),
	path('<int:id>/check_answers/', CheckAnswersView.as_view(), name='check_answers'),
	path('solved/', SolvedTestsView.as_view(), name='solved_tests'),
	path('solved/<int:id>/', SolvedTestView.as_view(), name='solved_test'),
	path('search/', SearchTestsView.as_view(), name='search'),
]