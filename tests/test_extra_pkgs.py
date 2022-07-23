from leafhopper.extra_pkgs import ExtraPkgs


def _load_extra_file():
    extra_pkgs_file = "tests/data/extra.json"
    extra_pkgs = ExtraPkgs(extra_pkgs_file)
    return extra_pkgs


def test_load_extra_pkg_file():
    extra_pkgs = _load_extra_file()
    assert extra_pkgs.overrides == {
        "com.google.code.findbugs.jsr305": {
            "name": "com.google.code.findbugs.jsr305",
            "license": "LGPL",
            "disclosed_source": "https://example.com/my/copy/of/findbugs",
        },
        "guava": {
            "name": "guava",
            "homepage": "https://github.com/google/guava",
            "overridden_name": "com.google.guava",
        },
    }


def test_overrides_pkgs_should_be_marked_as_overridden():
    extra_pkgs = _load_extra_file()
    pkg_infos = [
        {
            "name": "com.google.code.findbugs.jsr305",
            "license": "Apache v2",
            "description": "this is findbugs",
        },
        {"name": "log4j", "license": "Apache v2"},
    ]
    pkg_infos = extra_pkgs.override_pkg_infos(pkg_infos)
    assert len(pkg_infos) == 2
    assert pkg_infos[0]["name"] == "com.google.code.findbugs.jsr305"
    assert pkg_infos[0]["_overridden"]
    assert "description" in pkg_infos[0]
    # guava is not overridden
    assert "_overridden" not in pkg_infos[1]


def test_hidden_packages():
    extra_pkgs = _load_extra_file()
    pkg_infos = [
        {
            "name": "com.google.code.findbugs.jsr305",
            "license": "Apache v2",
            "description": "this is findbugs",
        },
        {"name": "junit", "license": "Apache v2"},
    ]
    pkg_infos = extra_pkgs.override_pkg_infos(pkg_infos)
    assert len(pkg_infos) == 1
    assert pkg_infos[0]["name"] == "com.google.code.findbugs.jsr305"


def test_overridden_name():
    extra_pkgs = _load_extra_file()
    pkg_infos = [
        {"name": "guava", "license": "Apache v2"},
        {"name": "log4j"},
    ]
    pkg_infos = extra_pkgs.override_pkg_infos(pkg_infos)
    assert len(pkg_infos) == 2
    assert pkg_infos[0]["name"] == "com.google.guava"
