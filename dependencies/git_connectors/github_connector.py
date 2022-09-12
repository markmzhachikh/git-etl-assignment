import logging
from typing import List

from github import Github

from .abstract_git_connector import AbstractGitConnector, AbstractGitRepo, GitPullRequest


class GitHubRepo(AbstractGitRepo):

    def __init__(self, repo, *args, **kwargs):

        super().__init__(source="github", *args, **kwargs)
        self._repo = repo

    def get_pull_requests(self) -> List[GitPullRequest]:

        _pull_requests = [
            GitPullRequest(
                author=pull_request.user.login,
                state=pull_request.state,
                title=pull_request.title,
                url=pull_request.html_url
            ) for pull_request in self._repo.get_pulls(state="all")
        ]
        logging.warning(f'got {len(_pull_requests)} PRs for repo "{self._repo.name}"')

        return _pull_requests


class GitHubConnector(AbstractGitConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.token is None or self.username is None:
            raise TypeError('"token" AND "username" must be specified!')
        elif self.username is not None and self.token is not None:
            logging.warning(
                'provided "username" will be ignored (will fetch all repositories associated with this token).')
            self.username = None

        self._github = Github(login_or_token=self.token) if self.token else Github()
        self._git_user = self._github.get_user(login=self.username) if self.username else self._github.get_user()

    def get_repos(self) -> List[AbstractGitRepo]:

        _repos = [repo for repo in self._git_user.get_repos()]
        logging.warning(f'got {len(_repos)} repositories for user "{self.username}" on github.')

        return [GitHubRepo(
                    owner=repo.owner.login,
                    external_id=repo.html_url,
                    name=repo.name,
                    private=repo.private,
                    repo=repo
            ) for repo in _repos]
