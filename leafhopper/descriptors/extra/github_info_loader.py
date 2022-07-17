from urllib.request import urlopen
import json
from leafhopper.logger import logger
from leafhopper.descriptors.extra import ExtraInfoLoader, has_github_homepage 


def fill_license(pkg_dict: dict, repo_dict: dict) -> None:
    if not pkg_dict.get("license", None) and "license" in repo_dict:
        license = repo_dict["license"]["name"]
        pkg_dict["license"] = license


def fill_description(pkg_dict: dict, repo_dict: dict) -> None:
    if "description" not in pkg_dict and "description" in repo_dict:
        pkg_dict["description"] = repo_dict["description"]


class GithubInfoLoader(ExtraInfoLoader):
    def __init__(self) -> None:
        pass

    def has_extra_info(self, pkg_dict: dict) -> bool:
        return has_github_homepage(pkg_dict)

    def load(self, pkg_dict: dict) -> dict:
        homepage = pkg_dict["homepage"]
        # https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api#repositories
        github_repo_api_url = homepage.replace("github.com", "api.github.com/repos")
        try:
            logger.info(
                f"loading info from github name={pkg_dict['name']} url={github_repo_api_url}"
            )
            github_json = urlopen(github_repo_api_url).read()
            repo_dict = json.loads(github_json)
            fill_license(pkg_dict, repo_dict)
            fill_description(pkg_dict, repo_dict)
        except Exception as e:
            logger.debug(f"failed to load info from github name={pkg_dict['name']} url={github_repo_api_url} error={e}")
        return repo_dict
