import json

from pyspark.sql import SparkSession

from dependencies.git_connectors.abstract_git_connector import AbstractGitConnector
from dependencies.git_connectors.github_connector import GitHubConnector
from dependencies.git_connectors.gitlab_connector import GitLabConnector


def connect_to_git(
        source: str,
        username: str,
        token: str
) -> AbstractGitConnector:
    """
    Connect to a given git source with credentials
    """

    if source == "github":
        return GitHubConnector(username=username, token=token)
    elif source == "gitlab":
        return GitLabConnector(username=username, token=token)
    else:
        raise ValueError(f'Invalid "source": {source}. Valid values are "github" or "gitlab".')


def main():

    spark = SparkSession.builder.appName("Git ETL assignment").getOrCreate()

    # read configs
    with open("configs/job_config.json", "r") as f:
        configs = json.loads(f.read())

    # fetch repositories for each config concurrently
    configs_rdd = spark.sparkContext.parallelize(configs)
    repos_by_config = configs_rdd.map(lambda config: connect_to_git(**config).get_repos()).collect()

    # flatten repositories list
    repos = [repo for config in repos_by_config for repo in config]

    # fetch PRs for each repository concurrently
    repos_rdd = spark.sparkContext.parallelize(repos)
    normalized_data = repos_rdd.map(lambda repo: repo.as_dict()).collect()

    # save to file
    with open("normalized_output.json", "w+") as f:
        f.write(json.dumps(normalized_data, indent=4))

    spark.stop()


if __name__ == '__main__':
    main()
