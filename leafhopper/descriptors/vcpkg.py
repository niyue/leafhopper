from leafhopper.descriptors.descriptor import Descriptor
from leafhopper.descriptors.github_info_loader import GithubInfoLoader, fill_github_info
import json
from urllib.request import urlopen
from leafhopper.logger import logger


def fill_version_if_needed(pkg_dict):
    if "version" not in pkg_dict:
        # folly/catch2/breakpad
        for version_attr in ["version-string", "version-semver", "version-date"]:
            if version_attr in pkg_dict:
                pkg_dict["version"] = pkg_dict[version_attr]


class VcpkgDescriptor(Descriptor):
    def __init__(self) -> None:
        super().__init__()

    def parse(self, vcpkg_json: str) -> list:
        names = self._parse_dependency_names(vcpkg_json)
        pkg_infos = [self._load_pkg_info(name) for name in names]
        return pkg_infos

    def _parse_dependency_names(self, vcpkg_json: str) -> list:
        # parse vcpkg json string into a dictionary
        vcpkg_dict = json.loads(vcpkg_json)
        # get dependencies
        dependencies = vcpkg_dict["dependencies"]
        dep_names = []
        for dep in dependencies:
            # if dep is a string, process it as a dependency name
            # else get `name` attribute from dep dict, and process it as a dependency name
            if isinstance(dep, str):
                dep_name = dep
            else:
                dep_name = dep["name"]
            dep_names.append(dep_name)
        return dep_names

    def _load_pkg_info(self, pkg_name: str) -> dict:
        vcpkg_json_url = f"https://raw.githubusercontent.com/microsoft/vcpkg/master/ports/{pkg_name}/vcpkg.json"
        logger.info(f"processing vcpkg package name={pkg_name}")
        # retrieve the url content via http request
        try:
            pkg_json = urlopen(vcpkg_json_url).read()
            pkg_dict = json.loads(pkg_json)
            fill_version_if_needed(pkg_dict)
            fill_github_info(pkg_dict)
        except:
            pkg_dict = {"name": pkg_name}
        return pkg_dict
