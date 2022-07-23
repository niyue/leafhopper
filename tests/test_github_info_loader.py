from leafhopper.descriptors.extra.github_info_loader import (
    GithubInfoLoader,
    has_github_homepage,
)

GITHUB_REPO_HOMEPAGE = "https://github.com/twbs/bootstrap"


def test_github_info_loader():
    loader = GithubInfoLoader()
    pkg_info = {"name": "bootstrap", "homepage": GITHUB_REPO_HOMEPAGE}
    repo = loader.load(pkg_info, False)
    assert repo["name"] == "bootstrap"
    assert "license" in repo
    assert "license" in pkg_info
    assert "description" in repo
    assert repo["license"]["name"] == "MIT License"

def test_github_info_loader_loading_license_text():
    loader = GithubInfoLoader()
    pkg_info = {"name": "bootstrap", "homepage": GITHUB_REPO_HOMEPAGE}
    repo = loader.load(pkg_info, True)
    assert repo["name"] == "bootstrap"
    assert "license_text" in pkg_info
    assert "license_url" in pkg_info


def test_github_homepage():
    assert has_github_homepage({"homepage": GITHUB_REPO_HOMEPAGE})
    assert not has_github_homepage({})
    assert not has_github_homepage({"homepage": "https://example.com"})
