"""
This module contains base classes for git connection.
All concrete connectors are inherited from them.
"""

from typing import Optional, List, Dict
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod


@dataclass
class GitPullRequest:
    """
    This class represents a PR
    """

    author: str
    state: str
    title: str
    url: str


class AbstractGitRepo(ABC):
    """
    This class represents an abstract git repository.
    All concrete repository classes should be inherited from this.
    """

    def __init__(
            self,
            owner: str,
            source: str,
            external_id: str,
            name: str,
            private: bool
    ):
        self.owner = owner
        self.source = source
        self.external_id = external_id
        self.name = name
        self.private = private

    @abstractmethod
    def get_pull_requests(self) -> List[GitPullRequest]:
        """
        Fetch all PRs for this repository.
        """

        raise NotImplementedError()

    def as_dict(self) -> Dict:
        """
        Return normalized representation of repository, with all PRs attached.
        """

        pull_requests = self.get_pull_requests()

        return {
            "owner": self.owner,
            "source": self.source,
            "external_id": self.external_id,
            "name": self.name,
            "private": self.private,
            "pull_requests": [asdict(pr) for pr in pull_requests]
        }


class AbstractGitConnector(ABC):
    """
    This class represents an abstract git connector.
    All concrete connectors should be inherited from this.
    """

    def __init__(
            self,
            username: Optional[str] = None,
            token: Optional[str] = None
    ):
        self.username = username
        self.token = token

    @abstractmethod
    def get_repos(self) -> List[AbstractGitRepo]:
        """
        Fetch all repositories for this git connection.
        """

        raise NotImplementedError()
