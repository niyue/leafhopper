from urllib.request import urlopen
import json
from leafhopper.logger import logger
from leafhopper.descriptors.extra import ExtraInfoLoader
from leafhopper.descriptors.extra import has_no_license, extract_sourceforge_project_id


def fill_license(pkg_dict: dict, project_dict: dict) -> None:
    if not pkg_dict.get("license", None):
        if "categories" in project_dict and "license" in project_dict["categories"]:
            license = project_dict["categories"]["license"]
            if isinstance(license, list):
                pkg_dict["license"] = license[0]["shortname"]

def fill_description(pkg_dict: dict, project_dict: dict) -> None:
    if "description" not in pkg_dict:
        pkg_dict["description"] = project_dict.get(
            "short_description", project_dict.get("summary", None)
        )


class SourceForgeInfoLoader(ExtraInfoLoader):
    def __init__(self, project_id = None) -> None:
        self.project_id = project_id

    def has_extra_info(self, pkg_dict: dict) -> bool:
        self.project_id = extract_sourceforge_project_id(pkg_dict)
        return self.project_id

    def load(self, pkg_dict: dict) -> dict:
        assert self.project_id is not None
        # https://sourceforge.net/p/forge/documentation/Allura%20API/
        project_api_url = f"https://sourceforge.net/rest/p/{self.project_id}"
        try:
            logger.info(
                f"loading info from sourceforge name={pkg_dict['name']} url={project_api_url}"
            )
            sourceforge_json = urlopen(project_api_url).read()
            project_dict = json.loads(sourceforge_json)
            fill_license(pkg_dict, project_dict)
            fill_description(pkg_dict, project_dict)
        except Exception as e:
            logger.debug(f"failed to load info from sourceforge name={pkg_dict['name']} url={project_api_url} error={e}")
        return pkg_dict
