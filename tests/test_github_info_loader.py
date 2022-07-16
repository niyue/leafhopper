from leafhopper.descriptors.github_info_loader import (
    GithubInfoLoader,
    has_github_homepage,
)

GITHUB_REPO_HOMEPAGE = "https://github.com/twbs/bootstrap"


def test_github_info_loader():
    loader = GithubInfoLoader(GITHUB_REPO_HOMEPAGE)
    repo = loader.load()
    assert repo["name"] == "bootstrap"
    assert "license" in repo
    assert "description" in repo
    assert repo["license"]["name"] == "MIT License"


def test_github_homepage():
    assert has_github_homepage({"homepage": GITHUB_REPO_HOMEPAGE})
    assert not has_github_homepage({})
    assert not has_github_homepage({"homepage": "https://example.com"})
