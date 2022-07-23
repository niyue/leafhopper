from turtle import home
from urllib.request import urlopen
from leafhopper.logger import logger
from leafhopper.descriptors.extra import ExtraInfoLoader, has_github_homepage 
from leafhopper.http.github_http_api import GithubHttpApi

def fill_license(pkg_dict: dict, repo_dict: dict) -> None:
    if not pkg_dict.get("license", None) and "license" in repo_dict:
        license = repo_dict["license"]["name"]
        pkg_dict["license"] = license


def fill_description(pkg_dict: dict, repo_dict: dict) -> None:
    if "description" not in pkg_dict and "description" in repo_dict:
        pkg_dict["description"] = repo_dict["description"]

class GithubInfoLoader(ExtraInfoLoader):
    def __init__(self) -> None:
        self.api = GithubHttpApi() 

    def has_extra_info(self, pkg_dict: dict) -> bool:
        return has_github_homepage(pkg_dict)

    def load(self, pkg_dict: dict, load_license_text: bool) -> dict:
        homepage = pkg_dict["homepage"]
        try:
            repo_dict = self.api.get_repo(homepage)
            fill_license(pkg_dict, repo_dict)
            fill_description(pkg_dict, repo_dict)
            if load_license_text:
                self.fill_license_text(pkg_dict, repo_dict)
            return repo_dict
        except Exception as e:
            logger.debug(f"failed to load info from github name={pkg_dict['name']} homepage={homepage} error={e}")
            return {}

    def fill_license_text(self, pkg_dict: dict, repo_dict: dict) -> None:
        default_branch = repo_dict.get("default_branch", "main")
        full_name = repo_dict["full_name"]
        license_text, license_url = self.api.get_license(full_name, default_branch)
        if license_text:
            pkg_dict["license_text"] = license_text
            pkg_dict["license_url"] = license_url