from leafhopper.descriptors.descriptor import Descriptor
from leafhopper.descriptors.github_info_loader import GithubInfoLoader, fill_github_info
import json
from urllib.request import urlopen
from leafhopper.logger import logger
import tomli


def _get_home_page(pypi_info: dict) -> None:
    if "home_page" in pypi_info and pypi_info["home_page"]:
        return pypi_info["home_page"]
    elif "project_urls" in pypi_info and "Homepage" in pypi_info["project_urls"]:
        return pypi_info["project_urls"]["Homepage"]
    elif "project_urls" in pypi_info and "Source Code" in pypi_info["project_urls"]:
        return pypi_info["project_urls"]["Source Code"]
    else:
        return None


def _load_pkg_info(pkg_info: dict) -> dict:
    pkg_name = pkg_info["name"]
    pypi_project_url = f"https://pypi.org/pypi/{pkg_name}/json"
    logger.info(f"processing pypi package name={pkg_name}")
    # retrieve the url content via http request
    try:
        pkg_json = urlopen(pypi_project_url).read()
        pkg_dict = json.loads(pkg_json)
        pypi_info = pkg_dict["info"]
        pkg_info["homepage"] = _get_home_page(pypi_info)
        pkg_info["description"] = pypi_info.get(
            "summary", pypi_info.get("description", None)
        )
        pkg_info["license"] = pypi_info.get("license", None)
        fill_github_info(pkg_info)
    except:
        return pkg_info
    return pkg_info


class PoetryDescriptor(Descriptor):
    def __init__(self) -> None:
        super().__init__()

    def parse(self, poetry_toml: str) -> list:
        pkg_infos = self._parse_dependencies(poetry_toml)
        pkg_infos = [_load_pkg_info(pkg_info) for pkg_info in pkg_infos]
        return pkg_infos

    def _parse_dependencies(self, poetry_toml: str) -> list:
        poetry_dict = tomli.loads(poetry_toml)
        pkg_infos = []
        if (
            "tool" in poetry_dict
            and "poetry" in poetry_dict["tool"]
            and "dependencies" in poetry_dict["tool"]["poetry"]
        ):
            dependencies = poetry_dict["tool"]["poetry"]["dependencies"]
            for dep_name, dep_info in dependencies.items():
                if dep_name != "python":
                    pkg_info = {"name": dep_name}
                    if isinstance(dep_info, str):
                        pkg_info["version"] = dep_info
                    elif isinstance(dep_info, dict):
                        if "version" in dep_info:
                            pkg_info["version"] = dep_info["version"]
                    pkg_infos.append(pkg_info)
        return pkg_infos
