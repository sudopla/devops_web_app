from django.urls import path, re_path
from web_app import views

urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    path('github_repo', views.GithubRepoView.as_view(), name='github_repo'),
    path('datalog_check', views.DatalogCheckView.as_view(), name='datalog_check'),
    path('django_repo/new', views.create_django_repo, name='create_github_django_repo'),
    path('datadog/new_event', views.create_datadog_event, name='create_github_django_repo'),
    path('datadog/new_test', views.create_datadog_test, name='create_github_django_repo'),
]