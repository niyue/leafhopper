from leafhopper.descriptors.vcpkg import VcpkgDescriptor, has_github_homepage
from leafhopper.descriptors.github_info_loader import GithubInfoLoader
from leafhopper.main import process_descriptors
import json
import io

GITHUB_REPO_HOMEPAGE = "https://github.com/twbs/bootstrap"


def test_load_vcpkg_package():
    vcpkg_desp = VcpkgDescriptor()
    vcpkg_json = open("tests/data/vcpkg.json").read()
    pkg_infos = vcpkg_desp.parse(vcpkg_json)
    assert len(pkg_infos) == 4
    names = {pkg_info["name"] for pkg_info in pkg_infos}
    for pkg in ["librdkafka", "arrow", "ip2region", "zstd"]:
        assert pkg in names
    assert "homepage" in pkg_infos[1]


def test_github_homepage():
    assert has_github_homepage({"homepage": GITHUB_REPO_HOMEPAGE})
    assert not has_github_homepage({})
    assert not has_github_homepage({"homepage": "https://example.com"})


def test_github_info_loader():
    loader = GithubInfoLoader(GITHUB_REPO_HOMEPAGE)
    repo = loader.load()
    assert repo["name"] == "bootstrap"
    assert "license" in repo
    assert "description" in repo
    assert repo["license"]["name"] == "MIT License"

def test_parse_and_write_table():
    output = io.StringIO()
    process_descriptors(["tests/data/vcpkg.json"], "json", output)
    table = output.getvalue()
    assert "librdkafka" in table
