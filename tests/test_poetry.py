from leafhopper.descriptors.poetry import (
    PoetryDescriptor,
    _load_pkg_info,
)


def test_load_poetry_package():
    desp = PoetryDescriptor()
    pyproject_toml = open("tests/data/pyproject.toml").read()
    pkg_infos = desp.parse(pyproject_toml)
    assert len(pkg_infos) == 2
    names = {pkg_info["name"] for pkg_info in pkg_infos}
    for pkg in ["pytablewriter", "pyarrow"]:
        assert pkg in names
    pyarrow_pkg = pkg_infos[1]
    assert "homepage" in pyarrow_pkg
    assert "description" in pyarrow_pkg
    assert pyarrow_pkg["description"] == "Python library for Apache Arrow"


def test_load_pkg_info_with_project_urls_home_page_and_license_missing():
    pkg_info = _load_pkg_info({"name": "tomli", "version": "0.2.0"})
    assert pkg_info["name"] == "tomli"
    assert pkg_info["version"] == "0.2.0"
    assert pkg_info["homepage"] == "https://github.com/hukkin/tomli"
    assert pkg_info["license"] == "MIT License"


def test_load_pkg_info_with_license_at_github():
    pkg_info = _load_pkg_info({"name": "fastapi", "version": "0.70.0"})
    assert pkg_info["name"] == "fastapi"
    assert pkg_info["version"] == "0.70.0"
    assert pkg_info["homepage"] == "https://github.com/tiangolo/fastapi"
    assert pkg_info["license"] == "MIT License"


def test_load_pkg_info_with_source_code_link_as_homepage():
    pkg_info = _load_pkg_info({"name": "structlog", "version": "21.5.0"})
    assert pkg_info["name"] == "structlog"
    assert pkg_info["version"] == "21.5.0"
    assert pkg_info["homepage"] == "https://github.com/hynek/structlog"
    assert pkg_info["license"] == "Other"
