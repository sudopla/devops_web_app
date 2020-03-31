from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from web_app.lib.GitRepo import *
from web_app.lib.DataDog import *


class IndexView(LoginRequiredMixin, TemplateView):

    def get(self, request, **kwargs):
        user_name = request.user.username
        context = {'user_name': user_name}
        return render(request, 'index.html', context)


class GithubRepoView(LoginRequiredMixin, TemplateView):

    def get(self, request, **kwargs):
        return render(request, 'github_repo.html')


class DatalogCheckView(LoginRequiredMixin, TemplateView):

    def get(self, request, **kwargs):
        return render(request, 'datalog_check.html')


# Create Github repository with Django project
@login_required
def create_django_repo(request):
    repo_name = request.POST['repo_name']
    repo_description = request.POST['repo_description']
    # Create GitRepo object and methods to create new repository
    gitRepo = GitRepo()
    new_repo = gitRepo.create_repo(repo_name, repo_description)
    # If repository was created, then push django code to it
    if new_repo['result'] == 'ok':
        gitRepo.push_django_project(repo_name, new_repo['repo_url'])
    return JsonResponse(new_repo)


# Create DataDog event
@login_required
def create_datadog_event(request):
    project_name = request.POST['repo_name']
    datadog = DataDog()
    response = datadog.create_event(project_name)
    return JsonResponse(response)


# Create DataDog synthetic test
@login_required
def create_datadog_test(request):
    test_name = request.POST['test_name']
    test_description = request.POST['test_description']
    location = request.POST['location']
    frequency = request.POST['frequency']
    url = request.POST['url']
    method = request.POST['method']
    datadog = DataDog()
    response = datadog.create_test(test_name, test_description, location, int(frequency), url, method)
    return JsonResponse(response)


