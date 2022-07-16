from urllib.request import urlopen
import json
from leafhopper.descriptors import has_github_homepage, has_no_license
from leafhopper.logger import logger


class GithubInfoLoader(object):
    def __init__(self, github_repo_url: str) -> None:
        # https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api#repositories
        github_repo_url = github_repo_url.replace("github.com", "api.github.com/repos")
        self.github_repo_url = github_repo_url

    def load(self) -> dict:
        try:
            github_json = urlopen(self.github_repo_url).read()
            repo_dict = json.loads(github_json)
            return repo_dict
        except:
            return {}


def fill_github_info(pkg_dict):
    if has_no_license(pkg_dict) and has_github_homepage(pkg_dict):
        loader = GithubInfoLoader(pkg_dict["homepage"])
        try:
            repo_info = loader.load()
            license = repo_info["license"]["name"]
            pkg_dict["license"] = license
            logger.info(
                f"loading info from github name={pkg_dict['name']} license={license}"
            )
            if "description" not in pkg_dict:
                pkg_dict["description"] = repo_info["description"]
        except:
            pass
