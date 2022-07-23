from leafhopper.extra_pkgs import ExtraPkgs

def _load_extra_file():
    extra_pkgs_file = "tests/data/extra.json"
    extra_pkgs = ExtraPkgs(extra_pkgs_file)
    return extra_pkgs


def test_load_extra_pkg_file():
    extra_pkgs = _load_extra_file()
    assert extra_pkgs.overrides == {
        "com.google.code.findbugs.jsr305": {"name": "com.google.code.findbugs.jsr305", "license": "LGPL"},
        "guava": {"name": "guava", "homepage": "https://github.com/google/guava"},
    }

def test_overrides_pkgs():
    extra_pkgs = _load_extra_file()
    pkg_infos = [
        {"name": "com.google.code.findbugs.jsr305", "license": "Apache v2", "description": "this is findbugs"},
        {"name": "log4j", "license": "Apache v2"},
    ]
    pkg_infos = extra_pkgs.override_pkg_infos(pkg_infos)
    assert pkg_infos == [
        {"name": "com.google.code.findbugs.jsr305", "license": "LGPL", "description": "this is findbugs"},
        {"name": "log4j", "license": "Apache v2"},
    ]
    overrides = extra_pkgs.overrides
    assert len(overrides) == 2
    assert overrides["com.google.code.findbugs.jsr305"]["_overridden"]
    # guava is not overridden
    assert "_overridden" not in overrides["guava"]