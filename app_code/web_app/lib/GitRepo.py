import shutil
from django.core import management
from github import Github
from git import Repo

class GitRepo:

    def __init__(self):
        # Connect to Github account with token
        self.token = ""
        self.g = Github(self.token)
        self.u = self.g.get_user()

    # Create new Github repository
    def create_repo(self, repo_name, description):
        list_repo_names = self.get_repo_names()
        if repo_name not in list_repo_names:
            repo_new = self.u.create_repo(repo_name, description)
            # Getting repo URL removing .api at the end of it
            repo_url = repo_new.clone_url[:-4]
            results = {'result': 'ok', 'repo_url': repo_url}
        else:
            results = {'result': 'failed', 'message': 'There is a repository already with this name. Please choose another name.'}

        return results

    # Create django project and push code to Github repository
    def push_django_project(self, repo_name, repo_url):
        # create temp django project
        management.call_command('startproject', repo_name)
        # Init Git and push code to Github repository
        local_repo = Repo.init(repo_name)
        git = local_repo.git
        git.add('.')
        git.commit('-m', 'initial commit')
        # Insert token in repo URL for push
        final_url = repo_url[:8] + self.token + '@' + repo_url[8:]
        git.push(final_url, 'master')
        # remove temp django project
        shutil.rmtree(repo_name)
        return None

    # Get a list with the name of existing Github repositories
    def get_repo_names(self):
        github_repos = self.u.get_repos()
        list_repo_names = []
        for repo in github_repos:
            list_repo_names.append(repo.name)
        return list_repo_names
