from leafhopper.descriptors.extra.github_info_loader import GithubInfoLoader
from leafhopper.descriptors.extra.sourceforge_info_loader import SourceForgeInfoLoader
from leafhopper.descriptors.extra import has_info_missing


def load_extra_info(pkg_dict: dict, load_license_text=False) -> dict:
    if has_info_missing(pkg_dict, load_license_text):
        loaders = [GithubInfoLoader(), SourceForgeInfoLoader()]
        for loader in loaders:
            if loader.has_extra_info(pkg_dict):
                return loader.load(pkg_dict, load_license_text)
    return pkg_dict

def load_extra_info_for_pkgs(pkg_list: list, load_license_text=False) -> list:
    return [load_extra_info(pkg, load_license_text) for pkg in pkg_list]