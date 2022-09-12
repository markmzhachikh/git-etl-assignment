import logging
from typing import List

from gitlab import Gitlab

from .abstract_git_connector import AbstractGitConnector, AbstractGitRepo, GitPullRequest


class GitLabRepo(AbstractGitRepo):

    def __init__(self, repo, *args, **kwargs):

        super().__init__(source="gitlab", *args, **kwargs)
        self._repo = repo

    def get_pull_requests(self) -> List[GitPullRequest]:

        _pull_requests = [
            GitPullRequest(
                author=pull_request.author['username'],
                state=pull_request.state,
                title=pull_request.title,
                url=pull_request.web_url
            ) for pull_request in self._repo.mergerequests.list(iterator=True, state="all")
        ]
        logging.warning(f'got {len(_pull_requests)} PRs for repo "{self._repo.name}"')

        return _pull_requests


class GitLabConnector(AbstractGitConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.token is None or self.username is None:
            raise TypeError('"token" AND "username" must be specified!')

        self._gitlab = Gitlab(private_token=self.token) if self.token else Gitlab()
        self._git_user = self._gitlab.users.list(username=self.username)[0]

    def get_repos(self) -> List[AbstractGitRepo]:

        _repos = [repo for repo in self._git_user.projects.list(iterator=True, min_access_level=10)]
        logging.warning(f'got {len(_repos)} repositories for user "{self.username}" on gitlab.')

        return [GitLabRepo(
                    owner=repo.owner['username'],
                    external_id=repo.web_url,
                    name=repo.name,
                    private=bool(repo.visibility != 'public'),
                    repo=self._gitlab.projects.get(id=repo.id)
            ) for repo in _repos]
