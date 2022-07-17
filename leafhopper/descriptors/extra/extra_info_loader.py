from leafhopper.descriptors.extra.github_info_loader import GithubInfoLoader
from leafhopper.descriptors.extra.sourceforge_info_loader import SourceForgeInfoLoader
from leafhopper.descriptors.extra import has_info_missing


def load_extra_info(pkg_dict: dict) -> dict:
    if has_info_missing(pkg_dict):
        loaders = [GithubInfoLoader(), SourceForgeInfoLoader()]
        for loader in loaders:
            if loader.has_extra_info(pkg_dict):
                return loader.load(pkg_dict)
    return pkg_dict
