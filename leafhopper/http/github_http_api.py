import os
import urllib3
from leafhopper.logger import logger
import json


class GithubHttpApi(object):
    # get username and password from environment variables
    def __init__(self):
        self.username = os.environ.get("LEAFHOPPER_GITHUB_USERNAME")
        self.password = os.environ.get("LEAFHOPPER_GITHUB_PASSWORD")
        self.http = urllib3.PoolManager()

    def _get(self, url):
        headers = {}
        if self.username:
            headers = urllib3.util.make_headers(
                basic_auth=f"{self.username}:{self.password}"
            )
        res = self.http.request("GET", url, headers=headers)
        if res.status == 200:
            return res.data.decode("utf-8")
        else:
            raise Exception(f"failed to call github api status={res.status} response={res.data}")

    def get_repo(self, homepage: str):
        # https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api#repositories
        github_repo_api_url = homepage.replace("github.com", "api.github.com/repos")
        logger.info(f"loading repo info from github url={github_repo_api_url}")
        repo_json = self._get(github_repo_api_url)
        repo_dict = json.loads(repo_json)
        return repo_dict

    def get_license(self, repo_full_name: str, default_branch: str):
        for license_file in ["LICENSE", "LICENSE.txt", "LICENSE.md", "LICENSE.rst"]:
            license_url = f"https://raw.githubusercontent.com/{repo_full_name}/{default_branch}/{license_file}"
            logger.debug(
                f"loading github license text name={repo_full_name} url={license_url}"
            )
            try:
                license_text = self._get(license_url)
                return (license_text, license_url)
            except Exception as e:
                logger.debug(
                    f"failed to load github license text repo={repo_full_name} url={license_url} error={e}"
                )
        return (None, None)
