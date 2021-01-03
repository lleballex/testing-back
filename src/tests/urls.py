from django.urls import path

from .views import SearchTestsView
from .views import OwnTestsView, OwnTestView
from .views import SolvedTestsView, SolvedTestView
from .views import TestsView, TestView, TestInfoView, CheckAnswersView


urlpatterns = [
	path('', TestsView.as_view(), name='tests'),
	path('<int:id>/', TestView.as_view(), name='test'),
	path('<int:id>/info/', TestInfoView.as_view(), name='test_info'),
	path('<int:id>/check_answers/', CheckAnswersView.as_view(), name='check_answers'),
	path('solved/', SolvedTestsView.as_view(), name='solved_tests'),
	path('solved/<int:id>/', SolvedTestView.as_view(), name='solved_test'),
	path('own/', OwnTestsView.as_view(), name='own_tests'),
	path('own/<int:id>/', OwnTestView.as_view(), name='own_test'),
	path('search/', SearchTestsView.as_view(), name='search'),
]