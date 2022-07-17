from leafhopper.descriptors.extra.github_info_loader import (
    GithubInfoLoader,
    has_github_homepage,
)

GITHUB_REPO_HOMEPAGE = "https://github.com/twbs/bootstrap"


def test_github_info_loader():
    loader = GithubInfoLoader()
    repo = loader.load({"name": "bootstrap", "homepage": GITHUB_REPO_HOMEPAGE})
    assert repo["name"] == "bootstrap"
    assert "license" in repo
    assert "description" in repo
    assert repo["license"]["name"] == "MIT License"


def test_github_homepage():
    assert has_github_homepage({"homepage": GITHUB_REPO_HOMEPAGE})
    assert not has_github_homepage({})
    assert not has_github_homepage({"homepage": "https://example.com"})
