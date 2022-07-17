from leafhopper.descriptors.mvn import (
    MvnDescriptor,
    _get_pom_path,
    _load_pkg_version,
    _load_pkg_info_with_version,
)


def test_get_pom_path():
    pom_path = _get_pom_path(
        {
            "name": "com.google.guava.failureaccess",
            "group_id": "com.google.guava",
            "artifact_id": "failureaccess",
            "version": "1.0.1",
        }
    )
    assert pom_path == "com/google/guava/failureaccess/1.0.1/failureaccess-1.0.1.pom"


def test_load_pkg_version():
    pkg_info = _load_pkg_version(
        {
            "group_id": "com.google.code.findbugs",
            "artifact_id": "jsr305",
        }
    )
    # it will find the latest version of jsr305, this assertion is not stable and may need to be weaken since the latest version is not stable
    assert pkg_info["version"] == "3.0.2"

def test_load_pkg_info_with_version():
    pkg_info = _load_pkg_info_with_version(
        {
            "group_id": "com.google.code.findbugs",
            "artifact_id": "jsr305",
            "version": "3.0.2",
        }
    )
    assert pkg_info["artifact_id"] == "jsr305"
    assert pkg_info["homepage"] == "http://findbugs.sourceforge.net/"
    assert pkg_info["license"] == "The Apache Software License, Version 2.0"
    assert pkg_info["description"] == "JSR305 Annotations for Findbugs"


def test_load_mvn_package():
    mvn_desp = MvnDescriptor()
    pom_xml = open("tests/data/pom.xml").read()
    pkg_infos = mvn_desp.parse(pom_xml)
    assert len(pkg_infos) == 4
    names = {pkg_info["name"] for pkg_info in pkg_infos}
    for pkg in ["com.google.guava.failureaccess", "com.google.code.findbugs.jsr305"]:
        assert pkg in names


def test_load_pkg_info_with_version_with_scm_url_multi_licenses():
    # this pom 1) has no maven namespace 2) has multiple licenses 3) has github scm url
    pkg_info = _load_pkg_info_with_version(
        {
            "group_id": "com.h2database",
            "artifact_id": "h2",
            "version": "2.1.214",
        }
    )
    assert pkg_info["artifact_id"] == "h2"
    assert pkg_info["homepage"] == "https://h2database.com"
    # multiple licenses will be shown as a comma separated string
    assert pkg_info["license"] == "MPL 2.0, EPL 1.0"
    assert pkg_info["description"] == "H2 Database Engine"

