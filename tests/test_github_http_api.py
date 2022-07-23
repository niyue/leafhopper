from leafhopper.http.github_http_api import GithubHttpApi


def test_github_http_api():
    api = GithubHttpApi()
    repo_dict = api.get_repo("https://github.com/twbs/bootstrap")
    assert repo_dict["name"] == "bootstrap"


def test_github_api_get_license():
    api = GithubHttpApi()
    license_text, license_url = api.get_license("twbs/bootstrap", "main")
    assert "The MIT License" in license_text
    assert license_url is not None

def test_github_api_get_license_txt():
    api = GithubHttpApi()
    license_text, license_url = api.get_license("antlr/antlr4", "master")
    assert "BSD 3-clause" in license_text
    assert license_url is not None
