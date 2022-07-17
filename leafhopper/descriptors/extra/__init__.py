import re

class ExtraInfoLoader(object):
    def has_extra_info(self, pkg_dict: dict) -> bool:
        return False 

    def load(self, pkg_dict: dict) -> dict:
        return pkg_dict

def has_info_missing(pkg_dict):
    return has_no_license(pkg_dict) or has_no_description(pkg_dict)

def has_no_license(pkg_dict):
    return "license" not in pkg_dict or not pkg_dict["license"]

def has_no_description(pkg_dict):
    return "description" not in pkg_dict or not pkg_dict["description"]


def has_github_homepage(pkg_dict):
    return "homepage" in pkg_dict and pkg_dict["homepage"].startswith(
        "https://github.com"
    )

def _extract_sourceforge_project_id(homepage):
    patterns = ["sourceforge.net/projects/([^/]+)", "http[s]?://(.*).sourceforge.net.*"]
    for pattern in patterns:
        match = re.search(pattern, homepage)
        if match:
            return match.group(1)
    return None

def extract_sourceforge_project_id(pkg_dict):
    if "homepage" in pkg_dict:
        return _extract_sourceforge_project_id(pkg_dict["homepage"])
    return None