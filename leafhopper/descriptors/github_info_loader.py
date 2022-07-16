from urllib.request import urlopen
import json

class GithubInfoLoader(object):
    def __init__(self, github_repo_url: str) -> None:
        # https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api#repositories
        if "api" not in github_repo_url:
            github_repo_url = github_repo_url.replace("github.com", "api.github.com/repos")
        self.github_repo_url = github_repo_url

    def load(self) -> dict:
        try:
            github_json = urlopen(self.github_repo_url).read()
            repo_dict = json.loads(github_json)
            return repo_dict
        except:
            return {}